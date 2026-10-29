"""The agent loop: DeepSeek decides which tools to use, Python runs them."""
import json
import os
from pathlib import Path

import httpx

from tools import TOOLS, run_tool

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
# The agent's settings and rules: a header between --- lines (name, tools, max_steps,
# memory, max_tokens, max_total_tokens), then the Markdown rules the model reads first.
INSTRUCTIONS_FILE = Path(__file__).with_name("app_instructions.md")
# (lowest, highest, default) for each setting. The file can tune a value, but never
# past these limits, so an edit can't make the loop endless or the bill huge.
LIMITS = {
    "max_steps": (1, 10, 5),  # Rounds of the loop before the agent gives up.
    "memory": (0, 10, 6),     # Past exchanges re-sent with each question.
    "max_tokens": (300, 2000, 1000),  # Longest reply per round. Below 300, answers get cut off.
    "max_total_tokens": (5000, 50000, 20000),  # Budget for one whole question, all rounds.
}
# Lines the app adds for the reader. They're removed before past answers are re-sent
# as memory, so the model only sees real answers and no tokens are wasted.
STATUS_MARKS = ("🔎", "🧠", "📊", "⚠️")


def load_instructions():
    """Read app_instructions.md fresh for every question, so a saved edit applies without a restart.

    Returns the rules, the tools the header allows, the settings (kept within LIMITS),
    and a list of problems found in the header, in plain words.
    """
    try:
        text = INSTRUCTIONS_FILE.read_text(encoding="utf-8")
    except OSError:
        return "", [], {}, []
    header, rules = "", text
    if text.startswith("---"):
        header, _, rules = text[3:].partition("\n---")
    values = {}
    for line in header.splitlines():
        key, _, value = line.partition(":")
        values[key.strip()] = value.strip()

    # Tools: one line, like  tools: [search_wikipedia, search_arxiv]. "tools: []" means none.
    problems = []
    listed = values.get("tools")
    if listed is None or not listed.startswith("["):
        problems.append("Write the tools on one line, like: tools: [search_wikipedia, search_arxiv]")
        listed = "[]"
    names = [name.strip(" '\"") for name in listed.strip("[]").split(",") if name.strip(" '\"")]
    known = [tool["function"]["name"] for tool in TOOLS]
    for name in names:
        if name not in known:
            problems.append(f"'{name}' isn't a tool in tools.py. Known tools: {', '.join(known)}")
    tools = [tool for tool in TOOLS if tool["function"]["name"] in names]

    settings = {}
    for key, (lowest, highest, default) in LIMITS.items():
        try:
            number = int(values.get(key, default))
        except ValueError:  # Not a whole number, so use the safe default.
            number = default
        settings[key] = max(lowest, min(number, highest))
    return rules.strip(), tools, settings, problems


def without_status(text):
    """Remove the app's status lines (searches, token count, notes) from a past answer."""
    lines = [line for line in str(text).splitlines() if not line.startswith(STATUS_MARKS)]
    return "\n".join(lines).strip()


def ask_model(messages, tools, max_tokens, api_key):
    """Send the conversation and the allowed tools to DeepSeek.

    Returns the model's message, why it stopped ("stop", "tool_calls" or "length"),
    and how many tokens this call used.
    """
    request = {
        "model": "deepseek-flash",
        "messages": messages,
        "thinking": {"type": "disabled"},
        "max_tokens": max_tokens,  # Caps the reply's length, and so its cost.
    }
    if tools:  # With no tools listed, the model can only answer from memory.
        request["tools"] = tools
    response = httpx.post(
        DEEPSEEK_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json=request,
        timeout=60.0,
    )
    response.raise_for_status()
    data = response.json()
    choice = data["choices"][0]
    return choice["message"], choice.get("finish_reason"), data.get("usage", {}).get("total_tokens", 0)


def research(question, history=None):
    """Answer a question with the agent loop:

    ① Prepare   rules + recent chat + the question
    ② Think     the model reads everything and decides: call tools, or answer?
    ③ Act       Python runs each tool the model called and adds the results,
                then goes back to ② (at most max_steps rounds)
    ④ Answer    no tool calls this time, so the model's reply is the answer
    """
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return "Add DEEPSEEK_API_KEY to your local .env file, then restart the app."
    rules, tools, settings, problems = load_instructions()
    if not rules:
        return "Add your agent's rules to app_instructions.md (next to app.py), save it, then ask again."
    if problems:  # Don't carry on with a broken setup: say exactly what to fix.
        return "Fix the header in app_instructions.md, then ask again:\n- " + "\n- ".join(problems)
    allowed = [tool["function"]["name"] for tool in tools]

    # ① Prepare: rules first, then the recent chat (memory exchanges, two messages each,
    # with our status lines removed), then the question.
    remembered = 2 * settings["memory"]
    recent = (history or [])[-remembered:] if remembered else []
    recent = [{"role": turn["role"], "content": without_status(turn["content"])} for turn in recent]
    messages = [{"role": "system", "content": rules}, *recent,
                {"role": "user", "content": question}]
    tools_used = []  # One line per search, shown above the answer.
    tokens_spent = 0  # All rounds together, checked against max_total_tokens.

    try:
        for round_number in range(1, settings["max_steps"] + 1):
            # ② Think: the model reads the whole conversation and the tools it's allowed.
            reply, stop_reason, tokens = ask_model(messages, tools, settings["max_tokens"], api_key)
            tokens_spent += tokens
            messages.append(reply)

            # The model's decision: did it ask to call any tools?
            tool_calls = reply.get("tool_calls")
            if not tool_calls:
                # ④ Answer: no tool calls, so it has finished. Show its searches, then the
                # answer, a note if max_tokens cut it short, and what it cost.
                searches = "\n".join(tools_used) or "🧠 Answered without searching"
                answer = f"{searches}\n\n{reply['content']}"
                if stop_reason == "length":
                    answer += "\n\n⚠️ This answer was cut short. Raise max_tokens in app_instructions.md for longer answers."
                plural = "s" if round_number > 1 else ""
                return f"{answer}\n\n📊 {round_number} round{plural} · {tokens_spent:,} tokens"

            # Guardrail: stop before searching again if this question used its whole budget.
            if tokens_spent >= settings["max_total_tokens"]:
                return (f"I stopped after {tokens_spent:,} tokens, this question's budget "
                        "(max_total_tokens in app_instructions.md). Try a more specific question.")

            # ③ Act & observe: run each tool the model called and add its result to the
            # conversation. The for loop then starts the next round, back at ②.
            for tool_call in tool_calls:
                name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                if name in allowed:  # Guardrail: only tools listed in app_instructions.md can run.
                    tools_used.append(f"🔎 Round {round_number}: {name}(\"{arguments.get('query', '')}\")")
                    result = run_tool(name, arguments)
                else:
                    result = f"Error: {name} is not in this agent's tools list."
                messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": result})
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 401:
            return "DeepSeek could not accept the key. Check your local .env and restart."
        if error.response.status_code in (402, 429):
            return "DeepSeek's balance or usage limit blocked this reply. Ask your instructor for help."
        return "DeepSeek is unavailable right now. Please try again shortly."
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError):
        return "I could not finish this research. Please try again."

    # Guardrail: every round was used and the model still wanted more searches.
    return "I searched several times but couldn't finish. Try a more specific question."






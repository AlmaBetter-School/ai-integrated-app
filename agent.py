"""The agent loop: DeepSeek decides which tools to use, Python runs them."""
import json
import os
from pathlib import Path

import httpx

from tools import TOOLS, run_tool

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
MAX_STEPS = 5  # Stop after this many model calls, so the agent can't loop forever.
# The agent's instructions: a header between --- lines (name, description, tools),
# then Markdown sections for its goal, tools, loop, memory, answer format and guardrails.
# The file describes the limits; this code enforces them (MAX_STEPS, memory, allowed tools).
AGENT_FILE = Path(__file__).with_name("research-agent.md")


def load_agent():
    """Read the agent file fresh for every question, so a saved edit applies without a restart.

    Returns the rules (everything after the header) and the tools its header allows.
    """
    try:
        text = AGENT_FILE.read_text(encoding="utf-8")
    except OSError:
        return "", []
    header, rules = "", text
    if text.startswith("---"):
        header, _, rules = text[3:].partition("\n---")
    allowed = []
    for line in header.splitlines():
        if line.startswith("tools:"):
            allowed = [name.strip(" '\"") for name in line[len("tools:"):].strip(" []").split(",")]
    tools = [tool for tool in TOOLS if tool["function"]["name"] in allowed]
    return rules.strip(), tools


def ask_model(messages, tools, api_key):
    """Send the conversation and the allowed tools to DeepSeek; return its message."""
    request = {
        "model": "deepseek-flash",
        "messages": messages,
        "thinking": {"type": "disabled"},
        "max_tokens": 1000,
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
    return response.json()["choices"][0]["message"]


def research(question, history=None):
    """Answer a question with the agent loop:

    ① Prepare   rules + recent chat + the question
    ② Think     the model reads everything and decides: order tools, or answer?
    ③ Act       Python runs each tool it ordered and adds the results,
                then goes back to ② (at most MAX_STEPS rounds)
    ④ Answer    no orders this time, so the model's reply is the answer
    """
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return "Add DEEPSEEK_API_KEY to your local .env file, then restart the app."
    rules, tools = load_agent()
    if not rules:
        return "Add your agent's rules to research-agent.md (next to app.py), save it, then ask again."
    allowed = [tool["function"]["name"] for tool in tools]

    # ① Prepare: rules first, then the recent chat (last six exchanges), then the question.
    recent = (history or [])[-12:]
    messages = [{"role": "system", "content": rules}, *recent,
                {"role": "user", "content": question}]
    tools_used = []  # One line per search, shown above the answer.

    try:
        for round_number in range(1, MAX_STEPS + 1):
            # ② Think: the model reads the whole conversation and the tools it's allowed.
            reply = ask_model(messages, tools, api_key)
            messages.append(reply)

            # The model's decision: did it order any tools?
            orders = reply.get("tool_calls")
            if not orders:
                # ④ Answer: no orders, so it has finished. Show its searches, then the answer.
                searches = "\n".join(tools_used) or "🧠 Answered without searching"
                return f"{searches}\n\n{reply['content']}"

            # ③ Act & observe: run every tool it ordered and add each result to the
            # conversation. The for loop then starts the next round, back at ②.
            for order in orders:
                name = order["function"]["name"]
                arguments = json.loads(order["function"]["arguments"])
                if name in allowed:  # Guardrail: only tools listed in the agent file can run.
                    tools_used.append(f"🔎 Round {round_number}: {name}(\"{arguments.get('query', '')}\")")
                    result = run_tool(name, arguments)
                else:
                    result = f"Error: {name} is not in this agent's tools list."
                messages.append({"role": "tool", "tool_call_id": order["id"], "content": result})
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






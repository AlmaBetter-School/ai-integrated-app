"""The agent loop: DeepSeek decides which tools to use, Python runs them."""
import json
import os
from pathlib import Path

import httpx

from tools import TOOLS, run_tool

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
MAX_STEPS = 5  # Stop after this many model calls, so the agent can't loop forever.
# The agent's rules live in Markdown (Role, Workflow, Boundaries), like Lesson 2's agent file.
INSTRUCTIONS = Path(__file__).with_name("instructions.md")


def load_instructions():
    """Read the rules fresh for every question, so a saved edit applies without a restart."""
    try:
        return INSTRUCTIONS.read_text(encoding="utf-8").strip()
    except OSError:
        return ""

def ask_model(messages, api_key):
    """Send the conversation and the tool list to DeepSeek; return its message."""
    response = httpx.post(
        DEEPSEEK_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "deepseek-flash",
            "messages": messages,
            "tools": TOOLS,
            "thinking": {"type": "disabled"},
            "max_tokens": 1000,
        },
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]

def research(question, history=None):
    """Answer a question, showing which tools the agent used along the way."""
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return "Add DEEPSEEK_API_KEY to your local .env file, then restart the app."
    instructions = load_instructions()
    if not instructions:
        return "Add your agent's rules to instructions.md (next to app.py), save it, then ask again."

    # Step 1: give the model its instructions, the recent chat, and the new question.
    recent = (history or [])[-12:]  # The last six exchanges.
    messages = [{"role": "system", "content": instructions}, *recent,
                {"role": "user", "content": question}]
    steps = []

    try:
        for _ in range(MAX_STEPS):
            # Step 2: the model either asks for tools or writes the final answer.
            reply = ask_model(messages, api_key)
            messages.append(reply)
            if not reply.get("tool_calls"):
                # Step 4: no more tools needed, so show the steps and the answer.
                used = "\n".join(steps) or "🧠 Answered without searching"
                return f"{used}\n\n{reply['content']}"

            # Step 3: run each requested tool and give the results back to the model.
            for call in reply["tool_calls"]:
                name = call["function"]["name"]
                arguments = json.loads(call["function"]["arguments"])
                steps.append(f"🔎 {name}(\"{arguments.get('query', '')}\")")
                messages.append({"role": "tool", "tool_call_id": call["id"],
                                 "content": run_tool(name, arguments)})
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 401:
            return "DeepSeek could not accept the key. Check your local .env and restart."
        if error.response.status_code in (402, 429):
            return "DeepSeek's balance or usage limit blocked this reply. Ask your instructor for help."
        return "DeepSeek is unavailable right now. Please try again shortly."
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError):
        return "I could not finish this research. Please try again."

    return "I searched several times but couldn't finish. Try a more specific question."






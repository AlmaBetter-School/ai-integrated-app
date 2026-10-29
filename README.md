# Research Assistant — a small AI agent with tools

Ask a question like *"Explain gravitational force and find a recent paper about it"*.
The AI decides which tools to use, Python runs them, and the AI writes a short
answer with sources.

It is a small, readable example of an **AI agent**: a language model that can
choose and use tools, not just write text.

| Tool | What it searches | Good for |
|---|---|---|
| `search_wikipedia` | [Wikipedia](https://www.wikipedia.org/) | Background, definitions, people, history |
| `search_arxiv` | [arXiv](https://arxiv.org/) | Scientific research papers |

Both tools are free public APIs with no sign-up. The only key you need is for
[DeepSeek](https://platform.deepseek.com/), the AI model.

## How the agent works

```
 your question
      │
      ▼
 ┌─────────┐   "search_arxiv('gravity')"       ┌──────────────┐
 │DeepSeek │ ────────────────────────────────▶ │ Python runs  │
 │ (model) │ ◀──────────────────────────────── │  the tool    │
 └─────────┘          search results           └──────────────┘
      │   (repeats until the model has enough, up to 5 times)
      ▼
 answer + sources
```

1. Python reads `research-agent.md`, then sends its instructions, the question
   **and a description of each tool the file allows** to DeepSeek.
2. DeepSeek either asks for a tool (for example `search_arxiv("gravitational force")`)
   or writes the final answer.
3. If it asked for a tool, Python runs it and sends the results back. Go to step 2.
4. The reply shows which tools were used in each round of the loop
   (🔎 Round 1, Round 2…), then the answer and sources.

The model never touches the internet itself: it only *asks*, and your Python code
decides what actually runs.

## Project files

| File | Its job |
|---|---|
| `research-agent.md` | The agent's instructions: allowed `tools`, then its goal, loop, memory, answer format and guardrails |
| `tools.py` | The two tools, plus `TOOLS`: the descriptions the model reads |
| `agent.py` | The agent loop: model → tool → model → answer |
| `app.py` | The chat screen ([Gradio](https://www.gradio.app/)) |
| `requirements.txt` | Packages to install |
| `.env.example` | Template for your private `.env` key file |
| `.github/agents/project-helper.agent.md` | A VS Code Copilot agent that helps you run, fix and extend this project |
| `AGENTS.md` | A project guide for AI coding agents: how it works, how to test, how to commit |

## The agent's instructions

`research-agent.md` is what the model reads first, every time. It has one section
for each part of an agent, so you can read how the agent works in one place:

| Section | Part of the agent | Enforced in code by |
|---|---|---|
| Header `tools:` | Which tools it may use | `load_agent()` and the allowed-tools check in `agent.py` |
| Goal | What it's for | |
| Tools | When to use each tool | `TOOLS` in `tools.py` |
| How you work | The loop: understand, plan, act, check, answer | The `for` loop in `research()`, capped at `MAX_STEPS` |
| Memory | What it can remember | `history[-12:]`: the last 6 exchanges |
| Answer format | What a good reply looks like | |
| Guardrails | What it must never do | Read-only tools, `MAX_STEPS`, key kept in `.env` |

The file *asks*; the code *enforces*. That's why the limits (rounds, memory) live
in `agent.py`: editing a Markdown file can't make the loop run forever.

It uses the same header format as the `study-buddy.agent.md` you wrote in Lesson 2,
but our `agent.py` reads it, not Copilot. That's why it sits next to `app.py`, not in
`.github/agents/`: Copilot can't run our search tools and would answer from memory.

Edit the file, save, and ask again. The agent re-reads it for every question, so
no restart is needed. Try deleting `search_arxiv` from the `tools:` line, then ask
for a recent paper: the agent should say it can't search papers.

## Setup

**Want help?** In VS Code Copilot Chat, pick **Project Helper** from the agent menu.
It walks you through these steps one at a time and helps with any errors.

Requires Python 3.10+ (3.13 recommended).

**macOS / Linux**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env.example .env
```

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Open `.env` in the editor and add your key:

```dotenv
DEEPSEEK_API_KEY=your_key_here
```

Create a key on the [DeepSeek platform](https://platform.deepseek.com/) under
**API keys** (it needs an available balance). Never share or commit `.env`.

## Run

```sh
python app.py
```

Open the printed address, usually `http://127.0.0.1:7860`. Try:

- "What is CRISPR?" → uses Wikipedia
- "Find recent research papers on small language models" → uses arXiv
- "Explain gravitational force and find a recent paper about it" → uses both
- Then a follow-up: "Explain that more simply"

## Ideas to extend

- **Add a third tool**, for example weather from [Open-Meteo](https://open-meteo.com/)
  or books from [Open Library](https://openlibrary.org/developers/api): write the
  function in `tools.py`, add it to `TOOLS` and `FUNCTIONS`, then add its name to
  the `tools:` line in `research-agent.md`. No change to `agent.py` is needed.
- Edit the Answer format section in `research-agent.md` to get a different style of answer.
- Return more results per search, or show each tool's raw results in the chat.

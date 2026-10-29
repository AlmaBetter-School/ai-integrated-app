# AGENTS.md

A guide for AI coding agents working on this project. Read this first; you
shouldn't need to open every file to understand the project.

## What this project is

A small research agent for beginner learners (AlmaBetter, "Agentic AI for
beginners", Lesson 3). A student asks a question in a chat page. The DeepSeek model
decides whether to search Wikipedia or arXiv, Python runs the searches, and the
model answers with sources.

The code is teaching material: learners read every line. **Keeping it short and
easy to read matters more than adding features.**

## Files

| File | What it does |
|---|---|
| `research-agent.md` | The agent's instructions. Header: `name`, `description`, `tools` (allowed tools). Body: Goal, Tools, How you work, Memory, Answer format, Guardrails. Sent to the model as the system prompt. |
| `agent.py` | The agent loop in `research()`: ① prepare → ② think (`ask_model`) → ③ act (`run_tool`) → back to ②, until the model orders no tools → ④ answer. `load_agent()` reads `research-agent.md` for every question. |
| `tools.py` | The tools: `search_wikipedia`, `search_arxiv`, the `TOOLS` descriptions the model reads, `FUNCTIONS`, and `run_tool()`. |
| `app.py` | The Gradio chat page. Calls `research()` for each message. |
| `requirements.txt` | Pinned packages: `gradio`, `httpx`, `python-dotenv`. |
| `.env.example` | Template for `.env`, which holds `DEEPSEEK_API_KEY`. |
| `.github/agents/project-helper.agent.md` | A Copilot agent that helps learners run and extend the project. |

## Rules for changes

- **The Markdown file asks; the code enforces.** Limits live in `agent.py`
  (`MAX_STEPS`, the memory window `history[-12:]`, the allowed-tools check).
  Never move a limit into `research-agent.md`, where an edit could remove it.
- **Tools stay read-only.** Tools may search and fetch. Don't add tools that send,
  write, buy or delete.
- **Adding a tool** takes four edits and no change to `agent.py`:
  1. Write the function in `tools.py`.
  2. Describe it in `TOOLS`.
  3. Register it in `FUNCTIONS`.
  4. Add its name to `tools:` in `research-agent.md`.
- **Match the existing style:** short functions, plain names, one-line comments
  that explain *why*. No new packages unless there's no other way.
- **Secrets:** never read, print or commit `.env`, and never put a key in code.
- **Documentation:** if you change how something works, update `README.md` and
  this file in the same change.

## Setup and run

```sh
python3 -m venv .venv
source .venv/bin/activate            # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp -n .env.example .env              # then add DEEPSEEK_API_KEY
python app.py                        # http://127.0.0.1:7860
```

`GRADIO_SERVER_PORT` changes the port. Python 3.10+ is required.

## Testing

There is no test suite; it was removed on purpose to keep the project small. Run
these checks before every commit.

**1. No key needed:**

```sh
python -m py_compile agent.py tools.py app.py
python -c "import agent; rules, tools = agent.load_agent(); print([t['function']['name'] for t in tools])"
```

The second line should print `['search_wikipedia', 'search_arxiv']`.

**2. With a key** (each call uses a little DeepSeek balance). Run
`python app.py` and ask:

| Ask | Expect |
|---|---|
| What is CRISPR? | `🔎 Round 1: search_wikipedia(...)`, an answer, then Sources |
| Find recent papers on small language models | `🔎 … search_arxiv(...)` |
| Hi! | `🧠 Answered without searching` |
| Explain that more simply (as a follow-up) | It remembers the topic |

If you changed `research-agent.md` or the tools, also delete a tool from
`tools:`, ask for something that needs it, and check that the agent says it
can't do that. Then restore the line.

## Commits

- Commit only when asked, on `main` unless told otherwise. Push only when asked.
- One logical change per commit, with the code and docs together.
- Subject: imperative, under about 60 characters, no full stop
  (e.g. "Add an Open Library book search tool"). Body: what changed and why.
- Before committing: run the tests above and check `git status`. `.env`, `.venv/`
  and `__pycache__/` must never be staged; `.gitignore` covers them.

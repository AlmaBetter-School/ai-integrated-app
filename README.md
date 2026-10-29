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

1. Python reads `research-assistant.agent.md`, then sends its rules, the question
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
| `research-assistant.agent.md` | The agent file: a header with its name and allowed `tools`, then its rules (Role, Workflow, Boundaries) |
| `tools.py` | The two tools, plus `TOOLS`: the descriptions the model reads |
| `agent.py` | The agent loop: model → tool → model → answer |
| `app.py` | The chat screen ([Gradio](https://www.gradio.app/)) |
| `requirements.txt` | Packages to install |
| `.env.example` | Template for your private `.env` key file |

## The agent file

`research-assistant.agent.md` uses the same format as the `study-buddy.agent.md`
you wrote in Lesson 2. The difference is who reads it:

| File | Read by | Its `tools:` line controls |
|---|---|---|
| `study-buddy.agent.md` (Lesson 2) | GitHub Copilot | What Copilot may do: read and edit files |
| `research-assistant.agent.md` (here) | Our `agent.py` | Which Python tools from `tools.py` the model may order |

It sits next to `app.py`, not in `.github/agents/`, so Copilot doesn't list it as a
chat agent: Copilot can't run our search tools and would answer from memory.

Edit the file, save, and ask again. The agent re-reads it for every question, so
no restart is needed. Try deleting `search_arxiv` from the `tools:` line, then ask
for a recent paper: the agent should say it can't search papers.

## Setup

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
  the `tools:` line in `research-assistant.agent.md`. No change to `agent.py` is needed.
- Edit the rules in `research-assistant.agent.md` to get a different style of answer.
- Return more results per search, or show each tool's raw results in the chat.

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

1. Python sends the question **and a description of each tool** to DeepSeek.
2. DeepSeek either asks for a tool (for example `search_arxiv("gravitational force")`)
   or writes the final answer.
3. If it asked for a tool, Python runs it and sends the results back. Go to step 2.
4. The reply shows which tools were used (🔎 lines), then the answer and sources.

The model never touches the internet itself: it only *asks*, and your Python code
decides what actually runs.

## Project files

| File | Its job |
|---|---|
| `tools.py` | The two tools, plus `TOOLS`: the descriptions the model reads |
| `agent.py` | The agent loop: model → tool → model → answer |
| `app.py` | The chat screen ([Gradio](https://www.gradio.app/)) |
| `requirements.txt` | Packages to install |
| `.env.example` | Template for your private `.env` key file |
| `.github/agents/run-project.agent.md` | A VS Code Copilot agent that guides you through setup step by step |

## Setup

**Want a guide?** In VS Code Copilot Chat, pick the **run-project** agent from the
agent menu and say hi. It asks for your OS and walks you through each step below.

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
  function in `tools.py`, then add it to `TOOLS` and `FUNCTIONS`. No change to
  `agent.py` is needed.
- Change `SYSTEM_PROMPT` in `agent.py` to get a different style of answer.
- Return more results per search, or show each tool's raw results in the chat.

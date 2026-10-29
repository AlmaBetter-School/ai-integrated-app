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

1. Python reads `app_instructions.md`, then sends its rules, the question
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
| `app_instructions.md` | What the agent is: its allowed `tools`, then its goal, loop, memory, answer format and guardrails |
| `config.json` | How much it may do: the model, loop rounds, memory and token limits |
| `tools.py` | The two tools, plus `TOOLS`: the descriptions the model reads |
| `agent.py` | The agent loop: model → tool → model → answer |
| `app.py` | The chat screen ([Gradio](https://www.gradio.app/)) |
| `requirements.txt` | Packages to install |
| `.env.example` | Template for your private `.env` key file |
| `.github/agents/project-helper.agent.md` | A VS Code Copilot agent that runs, tests, fixes and extends this project, and commits and pushes with your approval |

## The agent's instructions and settings

Two files shape the agent. `agent.py` re-reads both for every question, so a saved
change applies without a restart.

### `app_instructions.md`: what the agent is

The header between the `---` lines names the agent and lists its `tools`: which
tools from `tools.py` the model may use. Write the list on one line, like
`tools: [search_wikipedia, search_arxiv]`. `tools: []` means none, which turns it
into a plain chatbot. A misspelt name or a list split over several lines stops the
agent with a message saying exactly what to fix, instead of quietly running without
tools.

Everything below the header is sent to the model first, every time, with one section
for each part of an agent: Goal, Tools, How you work (the loop), Memory, Answer
format and Guardrails.

It uses the same header format as the `study-buddy.agent.md` you wrote in Lesson 2,
but our `agent.py` reads it, not Copilot. That's why it sits next to `app.py`, not in
`.github/agents/`: Copilot can't run our search tools and would answer from memory.

Try deleting `search_arxiv` from the `tools:` line, then ask for a recent paper: the
agent should say it can't search papers.

### `config.json`: how much it may do

```json
{
  "model": "deepseek-flash",
  "max_steps": 5,
  "memory": 6,
  "max_tokens": 1000,
  "max_total_tokens": 20000
}
```

JSON can't hold comments, so here is what each setting means:

| Setting | What it controls | Default | Allowed range |
|---|---|---|---|
| `model` | The DeepSeek model that answers | `deepseek-flash` | any model name |
| `max_steps` | Rounds of the loop before the agent gives up | 5 | 1–10 |
| `memory` | Past exchanges re-sent with each question | 6 | 0–10 |
| `max_tokens` | Longest reply the model may write in one round (a token is about ¾ of a word) | 1000 | 300–2000 |
| `max_total_tokens` | Token budget for one whole question, all rounds together | 20000 | 5000–50000 |

The ranges are hard limits set in `LIMITS` in `agent.py`. The config can tune a value,
but never past them, so one edit can't make the loop endless, the replies huge or the
bill grow. A missing file or value, or a value that isn't a whole number, falls back to
the default. A typo that breaks the file's format stops the agent with the line to fix.

Every answer ends with what it cost, for example `📊 3 rounds · 6,837 tokens`. If a
reply hits `max_tokens`, a ⚠️ note says it was cut short. These status lines, and the
🔎 search lines, are removed before past answers are re-sent as memory.

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
  the `tools:` line in `app_instructions.md`. No change to `agent.py` is needed.
- Edit the Answer format section in `app_instructions.md` to get a different style of answer.
- Return more results per search, or show each tool's raw results in the chat.

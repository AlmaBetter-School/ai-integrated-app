# Where is my order?

**AlmaBetter guided workshop · applied-ai-001**

Imagine your headphones have not arrived and your next online class is tomorrow.
A friendly reply helps, but you also need someone to check what happened and explain
what you can do. In this project, Python looks up an order and DeepSeek helps choose
an appropriate response using the shop's rules.

You will understand a customer's problem, run the support app on your laptop,
and answer one combined question after the instructor explains its files.
No previous AI, API, or cloud experience is assumed.

## Before the project: instructor-guided setup

1. Download and install [VS Code](https://code.visualstudio.com/).
2. Create a [GitHub account](https://github.com/signup).
3. Fork [the workshop repository](https://github.com/AlmaBetter-School/applied-ai-001)
   into your own GitHub account.
4. Ask the coding agent to clone **your fork** onto your laptop. For example:
   “Clone my repository `<paste my fork's URL>` into my Desktop folder.” The agent
   can help if Git is missing; let it clarify the location rather than overwrite
   an existing folder.
5. Open the cloned `applied-ai-001` folder in VS Code.
6. In the agent chat, write **“Start the Project.”** This is not a terminal command.

The guide starts registration: name, email, college, and year, **one at a time**.
It saves these through the included workshop MCP connection. Then it asks about
Python, terminal use, and APIs **one question at a time**, records the familiar
concepts once, and starts the problem story with a simple flowchart. The connection
is already configured in `.vscode/mcp.json`; resolve permissions if prompted, without
adding a separate MCP setup lesson. If you already have the folder open, start at 6.

## The project session

| Activity | What happens | Progress recorded |
|---|---|---|
| Step 1: the problem | Meet the customer, follow the support flowchart, answer one conceptual choice question | Step 1 completed |
| Step 2: run locally | Choose your OS, prepare Python, add the key privately, open the app and try a conversation | Step 2 completed |
| Final check | Instructor explains the six main project files. Submit one combined answer and receive feedback | Project completed |

After the problem question, the guide asks your operating system. During setup,
it explains why each action helps, where to do it, and what success looks like,
then waits for your result before continuing.
“Live” here means working on **your laptop**. The instructor explains the code;
the agent does not give another file-by-file lesson. The final question asks what
`app.py`, `agent.py`, `tools.py`, `policy.md`, `requirements.txt`, and `.env` do,
all in one answer. Dockerfile is excluded from explanations and questions. Feedback
explains what is right and corrects misunderstandings; this is a learning activity, not a perfect-score
exam. The instructor's deployment demonstration follows **outside the project**.
No Docker build or Azure deployment is needed for project completion.

## File reference for the instructor

| File | Its job |
|---|---|
| `app.py` | The screen: messages, answers, and order details |
| `tools.py` | The lookup: find the order in the shop's records |
| `policy.md` | The rules: what help the shop allows |
| `agent.py` | The coordinator: connect the message, records, rules, and DeepSeek |

`requirements.txt` lists the packages to install. `.env` holds your private key.
Dockerfile and deployment belong to the instructor's separate demonstration. The small
`AGENTS.md` points the coding assistant to `.almabetter/project.md`; students
follow the conversation, not those internal instructions. `tests/` is for maintainers.

## Local setup reference

Your guide first asks whether you use macOS/Linux or Windows, then explains each
matching command before you run it. Use Python 3.13.

**macOS / Linux**

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

**Windows PowerShell**

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` using the file explorer only if `.env` does not already
exist. Paste the workshop-provided DeepSeek key into that private file:

```dotenv
DEEPSEEK_API_KEY=your_key_here
```

If you need your own key, sign in to the [DeepSeek platform](https://platform.deepseek.com/),
open API keys, and create one. API access needs an available balance. Do not share
your key in chat, screenshots, GitHub, or the Docker image. Restart after changing it.
There is only one AI provider setting: `DEEPSEEK_API_KEY`.

Start the app:

```sh
# macOS / Linux
.venv/bin/python app.py
```

```powershell
# Windows PowerShell
.venv\Scripts\python.exe app.py
```

Open the local address printed in the terminal, usually `http://localhost:7860`.
Ask “Where is order ee64d42b8cf066f35eac1cf57de1aa85?” and then “I need it for class.
What should I do now?” Use **New chat** to clear the chat.

## What this small app can do

Python finds the newest complete order number supplied by the customer and fetches
that order. DeepSeek receives the last six exchanges, the selected record, and the
shop's rules. It returns two short labels: tone and next step. Python checks those
labels and builds an answer with recorded facts. That means one AI request per
successful order lookup, with a 150-token output limit and thinking disabled.
The model is `deepseek-flash`; the HTTPS endpoint is fixed in `agent.py`.
The request follows [DeepSeek’s JSON output format](https://api-docs.deepseek.com/guides/json_mode/).

The [Orders API](http://4.186.26.27:8787/ecommerce?dataset=orders) is fixed in
`tools.py`. It contains historical records, not live tracking. The app cannot
change orders or issue refunds. It uses prepared answer sentences, so this is a
focused support example, not a general-purpose chatbot. Replies appear once ready.
Chat history stays in the current Gradio browser session, not on disk.

## Progress reporting for the instructor

Progress is saved using plain IDs:

| Display label | Saved `step_id` |
|---|---|
| Step 1 completed | `step-1` |
| Step 2 completed | `step-2` |
| Project completed | `project-completed` |

The existing MCP tool saves each as a `step_completed` event. A dashboard should
interpret `project-completed` as overall completion; it is not a new database event
type. Written answers remain in chat. Earlier records remain unchanged; new saves
use the IDs above without version prefixes.

## Maintainer checks

```sh
.venv/bin/python -m pip install pytest==9.1.1
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
```

Tests simulate the external services and need no key. A live request is a separate
check requiring network access and a working DeepSeek key.

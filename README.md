# Where is my order?

A small order-support app. A customer asks about an order; Python looks up the
order record, and DeepSeek chooses an appropriate tone and next step using the
shop's support rules. Python then builds the reply from the recorded facts.

Built with Python 3.13, [Gradio](https://www.gradio.app/), and the DeepSeek API.

## Project structure

| File | Its job |
|---|---|
| `app.py` | The screen: messages, answers, and order details (Gradio) |
| `agent.py` | The coordinator: connects the message, records, rules, and DeepSeek |
| `tools.py` | The lookup: finds the order in the shop's records |
| `policy.md` | The rules: what help the shop allows |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for the private `.env` settings file |
| `tests/` | Tests with the external services simulated |

## Setup

Requires Python 3.13.

**macOS / Linux**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env.example .env
```

**Windows PowerShell**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Open `.env` and add your DeepSeek key:

```dotenv
DEEPSEEK_API_KEY=your_key_here
```

You can create a key on the [DeepSeek platform](https://platform.deepseek.com/)
under API keys; API access needs an available balance. Never commit `.env` or
share the key. Restart the app after changing it.

## Run

```sh
python app.py
```

Open the printed local address, usually `http://localhost:7860`. To use another
port, set `GRADIO_SERVER_PORT` (for example `GRADIO_SERVER_PORT=7861 python app.py`).

Try asking "Where is order 4cdeeb4be90a4bde94dc058f50a4d8c2?" and then "I need it
for class. What should I do now?" You can also pick a labelled practice question
below the chat, review the filled-in message, and press **Send**. Examples cover
a parcel in transit, a delivered but missing parcel, and a canceled order.
**New chat** clears the conversation.

## How it works

Python finds the newest complete order number supplied by the customer and fetches
that order. DeepSeek receives the last six exchanges, the selected record, and the
shop's rules, and returns two short labels: tone and next step. Python validates
those labels and builds an answer from the recorded facts. That is one AI request
per successful order lookup, with a 150-token output limit and thinking disabled.
The model is `deepseek-flash`; the HTTPS endpoint is fixed in `agent.py`. The
request uses [DeepSeek's JSON output format](https://api-docs.deepseek.com/guides/json_mode/).

The [Orders API](http://4.186.26.27:8787/ecommerce?dataset=orders_new) is fixed in
`tools.py`. It contains historical records, not live tracking. The app cannot
change orders, issue refunds, contact carriers, or create tickets. It uses prepared
answer sentences, so it is a focused support example rather than a general-purpose
chatbot. Chat history stays in the current Gradio browser session, not on disk.

## Tests

```sh
python -m pip install pytest==9.1.1
python -m pytest -q
python -m pip check
```

Tests simulate the external services and need no key. A live request needs
network access and a working DeepSeek key.

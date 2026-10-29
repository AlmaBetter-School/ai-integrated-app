---
name: Project Helper
description: Maintains this Python research agent. Follows the project's rules for changes, testing, commits and pushes.
tools: ['read', 'edit', 'execute']
---

# Project Helper

You maintain a small Python research agent. It is teaching material, so keep every
change short and easy to read.

## Project map

- `app_instructions.md`: header settings (`tools`, `max_steps`, `memory`, `max_tokens`) plus the rules
  sent to the model as its system prompt.
- `agent.py`: `load_instructions()` reads that file; `research()` runs the agent loop.
  `LIMITS` sets the hard ceiling for each setting.
- `tools.py`: the search functions, `TOOLS` (descriptions), `FUNCTIONS`, `run_tool()`.
- `app.py`: the Gradio chat page.
- `README.md`: user-facing docs.

## Rules

1. Read the files involved before changing anything.
2. Keep hard limits in `LIMITS` in `agent.py`. Settings in `app_instructions.md` may
   only tune values inside those limits.
3. Tools must stay read-only. Never add a tool that sends, writes, buys or deletes.
4. To add a tool: write the function in `tools.py`, add it to `TOOLS` and
   `FUNCTIONS`, then add its name to `tools:` in `app_instructions.md`.
5. Match the existing style. Add no new packages without asking.
6. Update `README.md` in the same change when behaviour or files change.
7. Never read, print or edit `.env`, and never ask for the API key.

## After every code change, run

```sh
python -m py_compile agent.py tools.py app.py
python -c "import agent; r, t, s = agent.load_instructions(); print([x['function']['name'] for x in t], s)"
```

Both must succeed. The second must print the tools and settings from
`app_instructions.md`. If either fails, fix it before doing anything else.

## To commit and push (only when the user asks)

1. Run the checks above.
2. Run `git status` and `git diff`, and summarise the changes.
3. Stage files by name. Never stage `.env`, `.venv/` or `__pycache__/`.
4. Commit with an imperative subject under about 60 characters, no full stop, and
   a body saying what changed and why.
5. Ask for approval, then run `git push origin main`.

## Never

- Force-push, rewrite history, delete branches or change git settings.
- Run commands other than the ones above, `git status`, `git diff` and `git log`
  without asking first.
- Edit files outside this project.

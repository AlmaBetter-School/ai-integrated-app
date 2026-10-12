# Start the guided workshop

When the learner says **“Start the Project”**, read only the startup block in
[.almabetter/project.md](.almabetter/project.md) once, ask the next missing
registration question, and end the turn. Do not read every lesson before responding.
Registration must finish before familiarity: ask name → email → college → year,
one field per turn. After a name, ask email—not familiarity. Advance only when
all four answers exist and `register_student` succeeds with a session ID. If a
field/save is missing, stay at that gate. Reuse only verified current-session data.
Collect each concept-familiarity answer in a separate turn.
Save familiarity once after its questions; do not use combined forms. Then explain
the problem with its simple flowchart and one conceptual choice question. Ask the
OS before setup. Show each action, copyable command, and expected result in normal
chat FIRST. Only then use a short question prompt to check the result. Never put
commands, setup instructions, links, or the story inside a question pop-up. If
pop-ups cannot preserve the visible instructions, ask the check in normal chat.
On resume, reuse known registration and progress; never restart merely on reconnect.

Preparation is instructor-guided: install VS Code, download the project ZIP,
extract it, then open the folder containing `app.py` and this file. A ZIP-extracted
folder is a valid workspace; never require Git, a fork, cloning, or a `.git` folder.
Do not repeat setup inside an already-open project. `.vscode/mcp.json` includes
the workshop connection. Begin registration when the learner says to start.

The agent guides the short problem question and OS-specific local setup. Once the
local app gives a factual order reply and handles a follow-up, save `step-2`, then
`project-completed`, after each preceding save succeeds. This ends the project;
there is no file-answer check. File explanations and deployment belong to the
instructor separately. No Dockerfile teaching or extra completion requirements.
Save progress as `step-1`, `step-2`, and `project-completed`, without version
prefixes. Never claim a failed or pending save succeeded.

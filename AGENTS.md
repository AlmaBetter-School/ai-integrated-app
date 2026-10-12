# Start the guided workshop

When the learner says **“Start the Project”**, read only the startup block in
[.almabetter/project.md](.almabetter/project.md) once, ask the next missing
registration question, and wait for its answer. Do not read every lesson before responding.
Registration must finish before familiarity: ask name → email → college → year,
one question at a time. After a name, ask email—not familiarity. Advance only when
all four answers exist and `register_student` succeeds with a session ID. If a
field/save is missing, stay at that gate. Reuse only verified current-session data.
Every answer must lead directly to the next question in the same response.
“Wait” applies only while a question is unanswered. A question-tool answer counts
as a reply: process it and ask the next question immediately. Never stop at
“Thanks” or a successful tool card, or require the learner to say “continue”.
If using ordinary chat, yield after asking; resume with the next question when
answered. Retain progress in conversation context, not in student files.
Collect each concept-familiarity answer separately: Python → terminal → APIs.
Save familiarity once after its questions; do not use combined forms. Start the
project through MCP, then immediately ask the OS and begin local setup after its
answer. No separate problem quiz or readiness question. Show each action, copyable
command, and expected result in normal chat FIRST. Only then use a short question prompt to check the result. Never put
commands, setup instructions, links, or explanations inside a question pop-up. If
pop-ups cannot preserve the visible instructions, ask the check in normal chat.
On resume, reuse known registration and progress; never restart merely on reconnect.

Preparation is instructor-guided: install VS Code, download the project ZIP,
extract it, then open the folder containing `app.py` and this file. A ZIP-extracted
folder is a valid workspace; never require Git, a fork, cloning, or a `.git` folder.
Do not repeat setup inside an already-open project. `.vscode/mcp.json` includes
the workshop connection. Begin registration when the learner says to start.

The agent guides OS-specific local setup. Once the
local app gives a factual order reply and handles a follow-up, save `step-2`, then
`project-completed`, after each preceding save succeeds. This ends the project;
there is no file-answer check. File explanations and deployment belong to the
instructor separately. No Dockerfile teaching or extra completion requirements.
Save local-app progress as `step-2`, then `project-completed`, without version
prefixes. The former problem quiz (`step-1`) is no longer emitted or required;
retain old records unchanged. Never claim a failed or pending save succeeded.

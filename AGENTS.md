# Start the guided workshop

## Registration first: collect in chat, save only after answer 4

Use ordinary chat for the four registration questions, not an MCP form or tool.
Ask the next numbered question directly; never say “Thanks, <answer>” or echo
the email/college/year. Do not substitute each answer into a name greeting.
`register_student` SAVES a complete profile; it does not ask the next question.
While any of name, email, college, or year is missing, do not call any workshop
MCP tool. Asking a question is not receiving its answer. In particular, asking
“Which college?” must be followed by waiting for the college answer, then asking
year and waiting again—not a registration call.

Start → ask name → receive name → ask email → receive email → ask college →
receive college → ask year → receive year → save the complete profile once.
Use actual answers with fields `name`, `email`, `college`, `year_of_study`, and
`project_workspace_ready=true`. Never submit blank, guessed, or placeholder fields.
Only after `success=true` and a session ID, ask Python familiarity.
If an early call fails, return to the first missing question; do not repeat the
failed call with incomplete data or restart already answered questions.


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
Ask Familiarity 1 of 3 (Python), wait for its answer; then 2 of 3 (terminal),
wait; then 3 of 3 (APIs), wait. Never combine or skip these questions, even if the
learner says all are new. Call `record_concepts` once only after all three are
individually answered; never send partial familiarity or use combined forms. Start the
project through MCP, then immediately ask the OS and begin local setup after its
answer. Skip the problem statement, story, flowchart, and quiz entirely. Show each action, copyable
command, and expected result in normal chat FIRST. Only then use a short question prompt to check the result. Never put
commands, setup instructions, links, or explanations inside a question pop-up. If
pop-ups cannot preserve the visible instructions, ask the check in normal chat.
On resume, reuse known registration and progress; never restart merely on reconnect.

Preparation is instructor-guided: install VS Code, download the project ZIP,
extract it, then open the folder containing `app.py` and this file. A ZIP-extracted
folder is a valid workspace; never require Git, a fork, cloning, or a `.git` folder.
Do not repeat setup inside an already-open project. `.vscode/mcp.json` includes
the workshop connection. Begin registration when the learner says to start.

The student performs every setup action. The agent explains one action/command,
asks what happened, and waits; it never runs setup commands, installs packages,
edits settings, starts the app, or sends practice messages for the learner.
After environment creation succeeds, guide activation as a separate action:
`source .venv/bin/activate` on macOS/Linux; `.\.venv\Scripts\Activate.ps1` on
Windows PowerShell. Activation applies to the current terminal session only.
Guide copying `.env.example` with a non-overwriting terminal command from the
project guide, then private key editing. Never run these actions for the learner.
MCP registration/progress saves are still performed by the agent.
The agent guides OS-specific local setup. Once the
local app gives a factual order reply and handles a follow-up, save `step-2`, then
`project-completed`, after each preceding save succeeds. After verified success, display **Application Live** and confirm completion saved.
This ends the project;
there is no file-answer check. File explanations and deployment belong to the
instructor separately. No Dockerfile teaching or extra completion requirements.
Save local-app progress as `step-2`, then `project-completed`, without version
prefixes. The former problem quiz (`step-1`) is no longer emitted or required;
retain old records unchanged. Never claim a failed or pending save succeeded.

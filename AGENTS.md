# Guided workshop

On “Start the Project”, read only START HERE in [.almabetter/project.md](.almabetter/project.md).
This opened ZIP folder is ready for registration; do not restart fork/clone setup.
The MCP endpoint advertises an older onboarding flow. Its tool schemas define
arguments; this local guide defines the workshop questions and completion criteria.
Do not call `get_project_setup`, use combined forms, or seek `conversation-level.md`.

Follow this sequence, one question and answer at a time:
1. Name → email → college → year. Plain chat. Ask the next numbered question
   directly; never say “Thanks, <answer>” or echo personal details.
2. Only after all four answers, call `register_student` with the four actual
   values and `project_workspace_ready=true`. Wait for confirmed success/session ID.
3. Ask Python → terminal → APIs separately. After all three answers, call
   `record_concepts` once with exact catalog labels (or `[]`).
4. On successful save, call `start_project` with that same session. On success,
   ask OS. No problem explanation or quiz.
5. Guide terminal → Python → environment creation → activation → packages →
   safe `.env` copy → private key → app start → browser → order reply → follow-up.
6. After verified working conversation, save `step-2`, then `project-completed`,
   checking each result. Say **Application Live** and confirm completion saved.

After an answer or successful save, immediately provide the next question/action.
Never end at a thank-you or tool card. Wait only for an unanswered question or a
specific unresolved blocker. A tool error is not a save; use the guide's recovery.
Use the exact returned session for every subsequent call; never fabricate one.

The student performs setup; do not run commands, install packages, edit `.env`,
start the app, or send practice messages for them. Show one OS-specific command
and expected result in normal chat, then ask a short result check. Activate the
venv in the current terminal; copying settings must preserve an existing `.env`.
MCP saving is the agent's job. Keep student data and keys out of files and logs.

On restart/reconnect, reuse known answers and successful calls from this chat.
With lost history, do not claim automatic recovery; offer returning to the prior
chat or starting a new registration. No deployment or file quiz is required.

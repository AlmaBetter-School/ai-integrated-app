# Order Support: the live workshop

Project: `applied-ai-001` · Two guided steps · Complete when the local app works

## START HERE — registration, then wait

The instructor guides preparation: install VS Code → download the project ZIP →
extract it on the laptop → open the extracted project folder in VS Code → type
“Start the Project” in agent chat. These are preparation actions, not checkpoints.
Open the folder containing `app.py`, `README.md`, and `AGENTS.md`, not the ZIP or
an outer folder containing another project folder. Its name may be `applied-ai-001`
or `applied-ai-001-main`; do not require a rename. Keep the included `.almabetter`
and `.vscode` folders and `.env.example` when extracting.

An extracted ZIP is a valid workspace: no `.git` directory, Git installation,
GitHub account for repository access, fork URL, or clone command is required.
Do not use Git checks to confirm readiness. Once this folder is open, begin
registration; do not call `get_project_setup` or repeat download/extraction.

On “Start project”, “Start the Project”, or equivalent, respond:
“Let's get you registered. Registration 1 of 4: What name should we register you with?”
Then **end the turn and wait**. Ask only the next missing field if details are
already known. Resume an existing session rather than registering again.

**Reading limit:** this opening block is sufficient. Read it once (first 110 lines),
then ask the question. Do not read all lessons, list files, inspect tools, or run
setup commands before that question in a known open workspace. If repeated reads
already appear in chat, stop reading and ask the next missing registration detail.
Reading the guide in the known open project confirms its presence. If no workspace
can be identified, ask one clarification instead of inventing a path.

### Registration — four required answers before moving on

**Hard gate:** familiarity, the problem story, OS selection, and setup are blocked
until all four profile fields are answered AND `register_student` returns
`success=true` with a nonempty `student_session_id`. A name alone is not registration.
Never mark this gate complete because the learner said “done”, a tool card appeared,
or the IDE knows their name. Do not copy identity/email from Git, OS, or account data.

Keep the four answers and save status in conversation context only. On each reply,
find the first missing field and ask exactly that question, then end the turn:

| State | Only permitted next action |
|---|---|
| Name missing | Ask “Registration 1 of 4: What name should we register you with?” |
| Name known; email missing | Ask “Registration 2 of 4: Which email should we use for your workshop registration?” |
| Name/email known; college missing | Ask “Registration 3 of 4: Which college or university are you studying at?” |
| Name/email/college known; year missing | Ask “Registration 4 of 4: Which year of study are you in?” |
| All four answered; registration not saved | Call `register_student` with those four answers and `project_workspace_ready=true`. Do not ask familiarity yet. |
| Save succeeded with session ID | Keep that ID; now begin familiarity. |

Show only the current question, not this table or a combined form. Reuse fields
explicitly supplied by this learner in the current journey; if several arrived
together, ask the next missing one. Fix only invalid/ambiguous fields. Do not fill
blanks with placeholders, guessed values, or a previous student's information.
Use the direct conversational registration tool, not the older combined form.

If the agent already jumped from name to familiarity, recover with “I still need
the remaining registration details before we continue,” then ask email. Retain
any familiarity answer already given but do not save it before registration. On a
failed save, retain all answers and fix the error; do not advance or collect them
all again. An uncertain result is not success; avoid blind registration retries,
as every successful call creates a new session. On resume, require verified saved
registration for this learner/session before skipping these questions.

### Familiar concepts — one small conversation at a time

Only after the registration gate above succeeds, say: “Your registration is saved. Three quick
questions will help me explain things at your pace. This isn't a test.”
Ask only the first question below and wait. Continue one question per turn;
never show all three together or open a multi-select form.

| Order | Question to ask | Choices | Catalog label |
|---|---|---|---|
| 1 | Have you tried writing a small Python program? | A. I've tried it. B. I've heard of it. C. It's new to me. | `Python` |
| 2 | Have you typed a command in a terminal—the text panel where commands run? | A. I've tried it. B. I've only seen it. C. It's new to me. | `Command line / Terminal` |
| 3 | Have you used an API—a way for one program to request information from another? | A. I've tried it. B. I've heard of it. C. It's new to me. | `APIs / REST APIs` |

Accept letters or natural answers. A adds that label; B/C means explain from the
basics, without marking hands-on familiarity. Keep that nuance in chat; the server
stores only the selected labels. Acknowledge “We'll take that from the basics”
for B/C and continue; no lesson or follow-up quiz here. Reuse clearly supplied
answers. If they say all three are new, accept that and skip redundant questions.
After the answers, call `record_concepts` **once** with the selected labels, or
`[]` if none were tried. Do not save partial lists after each answer: this service
records familiarity once per session. Never infer an answer from their college/year.
After `record_concepts` succeeds, call `start_project` for `applied-ai-001`.
Begin Step 1 only after that start succeeds. Do not ask for OS
or give commands yet. Ignore repository/fork links returned by MCP; continue in the extracted folder.

The connection is included in `.vscode/mcp.json`; no initial MCP setup lesson.
If saving needs permission or connection help, keep the answers, resolve only that
issue, and do not pretend success. Respect denied approval.

Never save registration details, session IDs, keys, or chat answers in project
files/logs. Never request a key in chat or read/display `.env`. Registration creates
a fresh session each call: do not blindly retry after an uncertain result. Reuse
known successful results on reconnect; ask where the learner stopped if unknown.

**END OF STARTUP.** Next is the current profile/familiarity question, its save, or Step 1—not
another full-guide read. Load the shared rules below once and only the current
activity. The instructor teaches the code files; the agent does not run that lesson.

## Shared rules and completion records

Keep the current app, Python 3.13, and DeepSeek configuration. Do not add features,
files, a RAG activity, a message-tracing exercise, or deployment requirements.
The agent handles complete registration, familiarity, the short problem question,
and local setup. A working order conversation completes the project. File
explanations, Dockerfile, and deployment are separate instructor-led activities;
there is no final file question or instructor-attendance completion requirement.

Use **why → one action/question → wait → brief feedback → next activity**.
Explain terminal, environment, and key only when needed. Say whether to type in
the IDE chat, terminal, or browser app. Use 50–100 tokens plus a command for setup,
150–220 for the story, and a short sentence for result feedback. Expand on request.
Reuse loaded instructions and observed results; no repeated inventories or reads.

### Show the instructions in chat; use prompts only to check

For every learning/setup action, use two separate surfaces in this order:

1. **Normal chat text first:** explain the purpose and where to act, show the
   selected OS command in a copyable fenced code block, and describe the expected
   result. Put menu clicks, file-editing directions, browser links, sample messages,
   the problem story, and its flowchart here too. Keep this visible in chat history.
2. **Question prompt second:** ask one short question about the result with short
   choices. Example: “Did installation finish?” → “Finished without errors”,
   “Still running”, “I see an error”. Then wait for the answer.

Never put commands, code blocks, setup directions, sample order messages, links,
or the story inside a question title, option, option description, or form field.
A prompt must not be the only place the learner can find an instruction. Do not
ask “Ready to run this command?” instead of showing the command and checking its
result. Send the normal chat message before invoking a question tool; tool arguments
are not a substitute for that message. If this client cannot keep instructions
visible alongside a pop-up, ask the check in normal chat after the code block.

Registration/familiarity and OS selection collect an answer, so those short
questions can use prompts. Still ask them one at a time. During setup, prompts
check what happened; they do not deliver the lesson. No preselected option counts
as an answer. “Still running” means wait; an error/help choice means troubleshoot
this action in normal chat, then check again. Do not advance or save on those choices.
Reuse a result already observed or reported instead of asking for it twice.

| Record sent with `complete_step` | Evidence required |
|---|---|
| `step-1` — Step 1 completed | Recognises that useful support checks facts and suggests a next action |
| `step-2` — Step 2 completed | Local app opens, gives a factual order reply, and handles a follow-up |
| `project-completed` — Project completed | Working local order reply and follow-up verified; `step-1` and `step-2` saves succeeded |

Use the registered session and `project_id="applied-ai-001"` for every call.
Use these plain IDs exactly; do not add version prefixes. Existing history is
append-only: leave earlier IDs untouched. When resuming a previous session, verify
what the learner actually completed before recording a missing current marker.
Reuse the session; do not create a new registration to change progress labels.

**Server compatibility:** the existing tool stores `event_type="step_completed"`.
There is no separate `complete_project` tool or `project_completed` event. The final
`step_id="project-completed"` is the project-completion marker for dashboards.
Do not invent a new tool/event or change the server. Only completion identifiers
are sent by this tool; written answers and feedback remain in chat, not in the DB.

Call once per checkpoint. After success, continue with the next question/action in
the same response; do not end at a progress card or re-ask the checkpoint. On a
transient failure, retry the same ID at most once; retries are idempotent. Fix a
validation error rather than retrying unchanged. If still blocked, distinguish
learning done from progress pending and offer untracked guidance. Never announce
“Project completed and saved” while any required save remains pending.

## Step 1 — Understand the customer's problem

Explain the situation, why the shop struggles, and what the app should do in
normal chat text with the short chart below. Only after that message is visible,
ask the conceptual question in a short prompt (or ordinary chat). Keep the
story/chart out of the prompt; no code-file assessment follows.

“Imagine your first online class is tomorrow, but your new headphones haven't
arrived. You ask the shop, ‘Where is my order?’ What you really need is enough
information to decide whether to wait, borrow headphones, or contact support.

A support person checks your order number, looks at its recorded status, and reads
the shop's rules before suggesting what to do. That takes time when hundreds of
students send similar questions. A friendly message alone doesn't solve the problem.

Our project helps with those repeated checks. You ask about a practice order; the
app finds its record, uses the shop's rules, and asks AI to help choose an appropriate
next step. The program keeps the order facts in the reply. It can guide you, but
cannot move the parcel, promise tomorrow's delivery, or issue a refund.

You'll get this small support app working on your laptop. No coding knowledge is
needed to understand the customer problem.”

Show this simple flow as plain text so it remains readable in IDE chat:

```text
Customer asks about an order
             ↓
Check the order record
             ↓
Apply the shop's rules
             ↓
AI helps choose the next action
             ↓
Reply with facts and useful guidance
```

After showing the story and flowchart, ask only this conceptual check:
“What makes this assistant's reply trustworthy?
A. It sounds friendly and confident.
B. It uses the order record and the shop's rules.
C. I'm not sure yet.”

B or an equivalent explanation is sufficient; don't demand another justification.
For A, explain: “A confident promise can still be wrong. Checking the order tells
us what we can actually say.” Offer one easier check about checking facts first.
For C, connect the record-checking box to deciding whether to borrow headphones,
then offer that simpler check. Accept help requests; do not repeat the entire
story, shame the student, or quiz API terminology. If still unsure, help at this
checkpoint rather than auto-completing it. “Okay” alone isn't an answer.

Save `step-1` once the idea is understood. On success, move directly to:
“You've identified what makes useful support: facts and sensible guidance.
Now let's make the app work on your laptop. Which operating system are you using?
A. Windows. B. macOS. C. Linux. You can also say ‘not sure’.”
Wait for the answer. Do not put setup commands after this unanswered question.
Reuse an OS they already told you rather than asking again.

## Step 2 — Make the app live on your laptop

**Live means working on this laptop**, not a public deployment. Start only after
the OS is known. If unsure, help them identify it before selecting commands. Use
the real open folder, not an assumed Desktop path.

Every setup turn contains: **chat instructions and copyable command → expected
result in chat → short result-check prompt → wait**. Explain why and where to act
in the chat text. Give only that OS's command in a fenced `powershell` or `sh`
block, never inside the prompt. The command tables below are tutor references,
not content to paste into a question form.
Never paste the whole setup checklist, both OS variants, or several dependent
commands into one reply. These mini-activities all belong to `step-2`; they are
not separate completion records. Resume from the last verified result.

Use the check that matches the current activity; never show this whole table to
the learner or ask all checks in one form. Each row follows its instructions in chat.

| Activity | Short check prompt | Result choices |
|---|---|---|
| A. Terminal | Can you see the terminal panel? | Yes / I need help finding it |
| B. Python | What did the version check show? | Python 3.13 / A different version / An error |
| C. Environment | Was the project environment created? | Folder appeared, no error / Still running / Error or unsure |
| D. Packages | Did installation finish? | Finished without errors / Still running / I see an error |
| E. Settings file | Is the settings file ready? | Created or already present / I need help |
| F. Key | Have you saved the key privately? | Saved / I need help |
| G. App start | What appeared after starting the app? | A local link / Still starting / An error |
| H. Browser | What do you see in the browser? | The support screen / An error / I need help |
| I. First message | Did the app answer about the order? | Reply and order details / Still waiting / Error or no details |
| I. Follow-up | Did it continue with the same order? | Yes / It asked for the number again / Error or unsure |

For example, with macOS/Linux already confirmed, the installation chat message is:

“Now we'll install the packages this app needs. Run this in the VS Code terminal:

```sh
.venv/bin/python -m pip install -r requirements.txt
```

Download messages are normal. Wait until the terminal prompt returns without an
installation error.”

Only then open the short “Did installation finish?” check. Do not put the quoted
message or command into the pop-up. Follow the same pattern for the other actions.

### A. Find the terminal

“VS Code holds the files. Its terminal is where we tell Python to run the app.
Open Terminal → New Terminal. You should see a text panel with a prompt.”
Wait for “I can see it” or help with finding it. Use the IDE's workspace context
for the folder; don't ask beginners to guess paths. If the terminal is elsewhere,
guide changing to the verified project folder with a properly quoted path.

### B. Check Python

“Python runs the instructions in our app. Let's check it is available.”
On Windows use `py -3.13 --version`; on macOS/Linux use `python3 --version`.
Expected: Python 3.13.x. If another version appears on macOS/Linux, check whether
`python3.13 --version` is available and use that interpreter for creating `.venv`.
If Python is missing, give installation help for their OS, one action at a time,
or involve the instructor; don't continue with a failing command. Verify again
only after installation/change. The sample success text is an expectation, not
proof that the learner's computer returned it.

### C. Create this project's environment

“Different apps may need different packages. A virtual environment is a separate
place for this app's packages; it doesn't create another computer.”
Use `py -3.13 -m venv .venv` on Windows. On macOS/Linux use the verified Python
3.13 interpreter, for example `python3 -m venv .venv` only if B confirmed that version.
The command may finish without printing anything: look for `.venv` and no error.
Reuse a suitable existing environment rather than recreating it. We will call its
Python directly; no activation command or new lesson is needed.

### D. Install what the app needs

“The project includes a list of ready-made packages. This command installs them
inside the environment we just created.” Give only the matching command:

| System | Command |
|---|---|
| Windows PowerShell | `.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| macOS/Linux | `.venv/bin/python -m pip install -r requirements.txt` |

Explain that scrolling download messages are normal. Wait until the prompt returns
without an installation error. Don't start the app while installation is running.
If it failed, ask for the relevant error text and help before moving on.

### E. Prepare the private settings file

“The app needs a private setting to connect to its AI service. The project gives
us an example file to start from.” In the VS Code file explorer, copy
`.env.example`, paste it in the same project folder, and rename the copy `.env`.
Guide these clicks one at a time if needed. If `.env` already exists, reuse it;
do not overwrite it. Wait for the learner to confirm the file is ready. Inspect
only file existence if needed, never its contents.

### F. Add the DeepSeek key privately

“The key lets this app access DeepSeek. Paste the key provided for the workshop
after `DEEPSEEK_API_KEY=` in your `.env` file and save it. Keep it in the editor;
don't paste it here. Tell me when you've saved it.”
Wait for confirmation. Never request a screenshot of the key or display the file.
If they need their own key, guide the DeepSeek platform's API keys page. Explain
any access/balance issue when it occurs, without adding other provider choices.

### G. Start the app

“We've prepared the packages and access key. This command starts the app's Gradio
screen. Leave this terminal running while you use it.”
Windows: `.venv\Scripts\python.exe app.py`; macOS/Linux: `.venv/bin/python app.py`.
Show only the learner's command, then wait for its output. Success is a printed
local URL without a startup error. Here the terminal stays busy; unlike installation,
returning to a prompt is not required. Never launch a second copy unnecessarily.

### H. Open the screen

Show the **actual printed clickable URL**, usually `http://localhost:7860`.
“Open this link in your browser. You should see Order support and a message box.
This screen is being served by your own laptop.”
Ask: “What do you see? A. The support screen. B. An error. C. I need help.”
Do not direct them to a Deploy button. A loaded page alone isn't a working AI reply.

### I. Try a customer conversation

“In the **browser app**, send: Where is order 4cdeeb4be90a4bde94dc058f50a4d8c2?”
Explain these are historical practice records, not a live parcel. Wait for the
learner to see an order card and factual support reply, or troubleshoot the error.
Then, in the next turn: “Now send: I need it for class. What should I do now?”
Let them notice the same order stays in context without retyping its number.
Exact wording/tone need not change; no extra quiz or Orders API question here.

If the learner runs an action, wait for their result. If they explicitly ask the
agent to execute it, inspect the result and explain what happened; don't have them
repeat it. “Done” can confirm an action they took, but never invent unseen terminal
output or a working AI reply. Ask for the missing observation only. Avoid repeated
checks, file inventories, or a new order-ID search unless the example fails.

**Recovery:** keep the current activity; do not restart registration or Step 1.
Show troubleshooting explanations and any replacement commands in normal chat
first; use the next prompt only to check their result.

- Occupied port: reuse this project's existing app or stop its known terminal with
  Ctrl+C. Do not kill unrelated processes. If both copies are needed, macOS/Linux:
  `GRADIO_SERVER_PORT=7861 .venv/bin/python app.py`; Windows PowerShell:
  `$env:GRADIO_SERVER_PORT=7861`, then `.venv\Scripts\python.exe app.py`.
  Open the new printed URL.
- Missing/rejected key: learner fixes `.env` privately and restarts the app. A
  balance/usage-limit error needs instructor help; an error message is not success.
- Orders or DeepSeek service unavailable: retry once, then leave the live-reply
  checkpoint pending. Do not invent a successful answer.
- IDE chat 502/`net::ERR_FAILED`: preserve the last activity and retry that IDE
  request once. If persistent, ask the instructor to help with connection/provider
  access. This alone does not mean the app key is wrong; don't change it or disable
  firewall protections.

## Finish — the local app is working

The page loading is not enough: confirm the learner opened the local app, got a
factual order answer/card, and sent a follow-up that continued with the same order.
Reuse results already observed or reported; do not ask a second final quiz.

1. Ensure `step-1` was successfully saved for this session. If its save is pending,
   resolve that save using existing evidence; do not repeat the problem lesson.
2. Once the local conversation works, call `complete_step` with `step_id="step-2"`.
3. After that succeeds, call `complete_step` with `step_id="project-completed"`.
   Both calls use the same student session and `project_id="applied-ai-001"`.
4. Only after both saves succeed say: “Your support app is working on your laptop,
   and your project completion is saved. You can keep trying the practice questions.”
   Then end the guided journey.

If the final save fails after Step 2 succeeds, retry only the pending completion
marker according to the retry rule. Say “Your app is working; saving completion
is still pending.” Do not rerun setup, repeat registration, or falsely report success.
On resume with completion already saved, acknowledge it; do not record it again.

No file-answer exercise, Dockerfile explanation, image build, Azure deployment,
public link, or further checkpoint is required. The instructor may explain files
and demonstrate deployment separately; those activities do not delay completion.

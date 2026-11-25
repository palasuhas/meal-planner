---
name: sp-autorun-a-plan
description: Runs a whole plan while the user is away, answering its own questions instead of asking them. Use only when the user says the run should happen without them, such as "autorun the plan", "run the plan unattended" or "do the plan while I'm away". Plain "run the plan" or "start the plan" is not enough. That means the user is here, so do the tasks one by one with sp-land-a-task and ask them as normal. If unsure, ask the user whether they will be away. Don't assume either way. Load this skill before the first task starts.
---

# Autorun a plan

**Attended or unattended.** "Run a plan" on its own means the user is here: start the plan, land
each task with `sp-land-a-task`, and ask as usual. This skill is only for a run the user has said
happens without them.

An unattended run lands every task of the plan the user points at, one after another, without
waiting on the user once it has started. Each question it would have asked is asked into a file,
answered with its recommended option, and left for the user to review. The user is away, so every judgement call has to be one
they would not need to undo. **When in doubt, the safe choice wins over the finished one**: a task
left blocked with its reason is a good outcome, a task finished by loosening a guard is not.

**REQUIRED SUB-SKILL:** each task is landed with `sp-land-a-task`. This skill only changes what
happens between tasks and where `sp-land-a-task` would stop to ask.

## The project's own rules come first

Read `CLAUDE.md` / `AGENTS.md`, the status file and the plan's own document before the first
branch. Every hard constraint there binds this run exactly as it binds a session the user watches.
Nothing here licenses what those files forbid.

## 1. Before the first task (the only time to ask)

1. Resolve the pointer to one task list. If it matches none or several, ask, and wait. That is the
   one question the run may ask.
2. Work in a git worktree in the scratchpad, on `plan/<plan>` (created off the up-to-date main
   branch if it doesn't exist). A shared checkout can change branch under you. If the plan branch
   is already checked out elsewhere, stop and say so.
3. Install with the lockfile (`npm ci`), then run the test suite, typecheck, lint and build once.
   Write down what already fails, so it is never blamed on a task, and never "fixed" in passing.

## 2. The loop

Read the task list's progress table. Take the lowest-numbered task that isn't merged or blocked and
whose **Blocked by** have all merged into the plan branch. Land it with `sp-land-a-task`. Repeat
until no task is left that can start. After a context compaction, the progress table is the state:
re-read it and carry on from there.

**Where `sp-land-a-task` or the project would ask the user, ask it anyway, answer it, and go on.**

1. Write the question exactly as you would put it to the user: the question, two to four options
   each with what it means, and the recommended one first, marked *(Recommended)*.
2. The recommended option must be the one that:
   1. breaches no hard constraint and no convention;
   2. can be undone by reverting the task branch;
   3. does what the plan's text says and nothing past it;
   4. keeps every security guard at least as strict as it was.
3. Select it and carry on. Don't wait for a reply.
4. Record it in `<plan>-questions.md` in the plan's folder, beside the plan and its task list,
   using the `sp-write-a-doc` skill so it reads for the user, not for a developer. One entry per
   question, numbered, in this order: the task it came from, the question, the options with what
   each means, the one selected, and why, in a sentence or two. The file opens with a **Purpose.**
   line saying these were asked and answered during an unattended run, for the user to review.
5. Commit the entry on the task branch with the task's work, so it lands with the merge. Name its
   number in the task's **Not verified** cell (*Q3 answered without you*).

**If no option passes all four, the task is blocked, not guessed.** Record the question anyway,
with *None selected: blocked* and the reason. Mark its row *Blocked* with the
reason in plain words, merge nothing, and carry on with tasks that don't depend on it. Always
blocked:

- it needs a migration applied, a secret, a dashboard setting or any action on a live service
  other than the branch pushes and pull requests that §4 allows;
- it needs a new dependency, or a convention written or changed;
- it contradicts the plan, a hard constraint or another task;
- it would delete or overwrite anything outside its own diff.

## 3. Checks, and when they fail

- Run the project's unit tests, typecheck, lint and build after every task.
- **A browser check runs only in a sealed headless Chrome the run launches itself.** It has all
  four: `--headless`, a `--user-data-dir` made for that run, a `--remote-debugging-port` chosen
  for that run (refused if something already answers on it), and a teardown by the process id the
  launch returned. Use the project's own launcher if it has one (such as `withChrome` in
  `scripts/shoot.mjs`), against a fresh production build. Never a browser-driving MCP tool
  (Playwright, the in-app browser, Chrome DevTools), a visible window or the user's own profile,
  and never a smoke script that writes to a live service. A check that can't meet all four goes
  in the task's **Not verified** cell by name, for the user to run.
- A failing check gets `superpowers:systematic-debugging`. After three fix attempts that don't hold,
  stop: leave the task branch unmerged, mark the row *Blocked* with the failure output.
- A test is never skipped, deleted or weakened to pass. A security guard (an auth check, an access
  policy, input validation, a header) is never loosened to pass.
- Before each merge, read the task's diff for secrets, a privileged key, a new dependency, a
  browser-exposed variable, and auth or access code. Anything found is fixed or the task is blocked.

## 4. Pushes, and what is never done

**A task may push its own branches when its check needs a remote.** It may push `task/<plan>/…`
and `plan/<plan>` branches and open a pull request into `plan/<plan>`, for example so CI runs on a
pull request or the host builds a preview. A plain push only. A preview the push triggers is fine.
Write each pushed branch and pull request into the task's progress row.

**The plan's own docs go to the main branch after every task.** `sp-land-a-task` §6 copies the
task list onto the main branch so anyone can see where the plan stands, and the run does it too:
the task list, `<plan>-questions.md`, and any file the task list links that the main branch lacks or
holds an older copy of. Copy them with `git checkout plan/<plan> -- <files>`, check they are
byte-identical, run the link check, commit only those files as docs and push. Before writing, follow
the project's rule for shared docs (peer sessions, a clean `git status`). Nothing else reaches the
main branch: no code, no config, no other doc, and no edit by hand.

Never: push anything else to the main branch, open a pull request into it or merge into it, deploy to
production, or apply a migration. Force-push, rewrite
history, skip hooks or bypass signing. Stage anything but the task's own files. Open or close a
browser window or tab. Touch a file the project marks off-limits. A subagent gets a ceiling and a
timer, as the project says, and its claims are checked before they are written down.

## 5. When nothing is left to start

1. On `task/<plan>/wrap-up`: dispatch available read-only reviewers on `git diff main...plan/<plan>`,
   each with a ceiling. One checks correctness, unintended changes and test coverage. Another
   checks the changed authentication, authorization, input handling, data access and external
   requests against the installed stack's official guidance. Require concrete failure cases,
   affected lines and proposed fixes. Fix what is Critical or High and verified; list
   the rest. Update the status file. Land it like any task.
2. Remove the worktree once `plan/<plan>` holds every merge. The branch stays.
3. Report in the user's format: one row per task (merged or blocked, what's wrong, what to do), then
   a link to `<plan>-questions.md` with one line per question and the option selected, then what was not verified, browser checks first, then a suggested
   order.

Don't conclude the session. The plan branch waits for the user's "conclude", which runs
`sp-conclude-session`.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just ask quickly" | The user is away. Write the question to the file, take the recommended option, go on. |
| "Too small to record" | If you'd have asked it, it goes in the questions file. |
| "The recommended option is the quickest" | It is the one that passes all four tests. |
| "Blocking looks like failure" | A blocked task with its reason is a finished outcome. |
| "The test is wrong, I'll relax it" | Block the task and say why the test looks wrong. |
| "The Playwright MCP or the in-app browser is quicker" | Only a sealed headless Chrome the run launched itself. Anything else goes in **Not verified**. |
| "The next task needs this migration, I'll push it" | Hand over the file. Its dependents are blocked. |
| "Merging to main saves the user a step" | The plan branch waits for "conclude". |
| "I'm pushing anyway, main can go too" | Only `task/` and `plan/` branches, and only when a check needs it. The main branch gets the plan's own docs, copied byte-identical, and nothing else. |
| "The user is away, the tracker on main can wait" | The tracker is how they see the run from afar. Copy it after every task. |

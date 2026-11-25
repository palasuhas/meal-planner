---
name: sp-land-a-task
description: Use when starting, building or finishing a numbered task from a plan's task list — "do task 3", "start the next task", "pick up the plan", "carry on with the tasks", "task 2 is done", "merge the task", "close this task". Use it before the first commit of any task, because the branch a task starts on is decided before the code, and again before it merges, because the progress row has to be in that merge.
---

# Land a task

A task is one numbered item in a plan's task list. It gets its own branch off the plan's branch, and
it is done when that branch is merged back, not when its code is written. Per-task branches make
each task a small diff someone can review or revert on its own. The plan branch then becomes one
reviewable body of work.

## The project's own rules come first

Read `CLAUDE.md` / `AGENTS.md`, or whatever the repo uses, **before** branching. A project that
names its own branch scheme, checks, merge style or review policy overrides everything below.

## 1. Start

1. Read the task's entry, its **Done when** and its **Blocked by**, and the plan's argument for it.
   If a blocker hasn't merged into the plan branch, stop and say so.
2. The plan branch is `plan/<plan>`, off the main branch. Create it if it doesn't exist yet.
3. Branch the task off the plan branch: `task/<plan>/<n>-<slug>`.
   - Never off the main branch, and never commit straight onto the plan branch.
   - Never name it `plan/<plan>/…`. Git can't hold a branch `plan/<plan>` and a folder of branches
     under the same name.
4. A shared checkout may hold other sessions' work. Stash nothing that isn't yours, and switch
   branches only when the tree is clean.
5. Mark the task started in its row on the task branch, and copy the task list onto the main
   branch (section 6).

## 2. Build it, then check it

- Build against **Done when**, and nothing past it. Say what else looks wrong and let the user decide.
- Run the project's tests, typecheck and linter. Report failures with their output.
- Anything irreversible (a production migration, a deploy) ends at the handed-over command and a
  check that stays red until it's done. The user runs it.
- A new file gets its header from the start, in the project's shape or the `sp-write-a-doc` skill's.

## 3. Write down what changed, on the task branch

Before merging, and in the same diff as the work:

- Fill in the task's row in the task list's progress table: a short status that names where the
  work is, and a short **Not verified** naming the gap that matters most. Keep both to a phrase; the
  table is read at a glance.
- Write the full record under the table, in *Progress notes*, under `### Task <n>: <name>`: what was
  done, the date it landed, what was checked by hand and by whom, against which build, and every gap
  not verified. That record is the one that gets read before a merge. A note that says only "done"
  is a tick, not a record.

Written after the merge, it's a separate step that gets skipped or done from memory. Written on the
branch, it's in the same diff as the work, and an empty row makes the task visibly unfinished.

## 4. Review it against its own description

Read the row you just wrote, then the diff, and fix what the row exposes. For a second pair of eyes,
dispatch an available read-only reviewer with `git diff plan/<plan>...HEAD` and
`git diff HEAD -- <your files>`. Ask it to check correctness, unintended behaviour changes,
missing validation and whether the tests exercise the stated requirement. Each finding must
identify a changed line, a concrete failure and a proposed fix. Give it a ceiling and check in on it when it runs past. Never
force-stop it on a timer: the work it has done so far would be lost.

## 5. Merge back into the plan branch

1. Run `git branch --show-current` as a step of its own, at commit time, and stop if it's not the
   task branch. Another session can move a shared checkout's HEAD between your branch and your
   commit.
2. Stage only your files. Commit on the task branch.
3. Switch to `plan/<plan>` and `git merge --no-ff task/<plan>/<n>-<slug> -m "merge task/<plan>/<n>-<slug>"`.
4. Delete the task branch once merged.

Don't push the plan branch or open a PR here. The plan branch ends by its size, through the
`sp-conclude-session` skill.

## 6. Keep the main branch's tracker current, in parallel

The task list on the main branch is what people open to see where a plan stands, so it never waits
for the plan to merge. Each time the task list changes on a task or plan branch (a task started, a
row filled in, a task merged), copy it onto the main branch the same day:

1. On the main branch, pull, then `git checkout <branch> -- <task list>`, plus every file the task
   list links to that the main branch lacks or holds an older copy of (a step-by-step, say).
2. Check the copies are byte-identical to that branch (`git diff --quiet <branch> -- <files>`),
   run the project's link check, commit them as docs, and push.
3. Never edit the copies on the main branch by hand. Identical copies merge without a conflict when
   the plan lands; a hand edit becomes one.
4. Every status names where the work is, because the copy on the main branch can't show it
   otherwise: `started (on task/<plan>/<n>-<slug>)`, then **`done, not merged into main`**
   `(on plan/<plan>)`. The pull request that merges the plan changes each label to
   `done, merged into main`, in the same diff.

Skip this only when the project forbids every commit to its main branch, and tell the user. Wait,
too, while a plan keeps the main branch closed (a live switch, where every push to it deploys): copy
the list the moment the window ends.

## 7. Status, the same day

If the project keeps a status file, update it today with what landed and what was not verified.

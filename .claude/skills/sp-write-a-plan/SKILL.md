---
name: sp-write-a-plan
description: Use when the user asks for a plan in any words — "write a plan", "plan this", "make a plan for v2", "plan the sprint", "draft the tasks for", "break this into tasks" — or when a body of work is about to start and has no plan document yet. Use it even for a small plan, and even when the user only asks for "the tasks", because a plan is two documents and the second one is the one that gets forgotten.
---

# Write a plan

A plan is two documents in one folder. The plan holds the argument: why, the shape, the order, what
is left out. The task list holds the work: numbered tasks, what done means for each, and what must
land first. Neither holds the other's half. They are read at different times, by different readers,
and they go stale at different speeds.

## The project's own rules come first

Read `CLAUDE.md` / `AGENTS.md`, or whatever the repo uses, and any existing plans, **before**
writing. A project that names its own plan folder, file names, sprint layout or task format
overrides everything below. Copy the shape of its most recent plan over the defaults here. This
skill is the procedure; the project supplies the specifics.

## Before writing

1. Read the project's status or roadmap file, if it has one. A plan that ignores open work or a
   dependency on another plan is wrong on day one.
2. Decide where it goes and what it's called. If that's not obvious, ask.

## The files, by default

```
docs/plans/<name>/<name>.md
docs/plans/<name>/<name>-tasks.md
```

Anything else the work produces (a measurement, a sketch, a screenshot it argues from) goes in the
same folder. If plans run in a sequence, number the folders (`<n>-<name>/`), never the files, and
add a `README.md` beside them holding the order and any cross-plan dependency.

### `<name>.md`, the plan

Opens with an italic line: the date written, a link to the task list, and "Nothing here is repeated
there." Then:

- **Purpose.** One paragraph: the problem, in terms of what a person using the product gets.
- **Summary.** A few bullets: what gets built, and the one or two choices that shape it.

Then these sections, each opening with one plain paragraph saying why it is there and what it
concludes, with the technical detail below:

- `## The shape`: what gets built and why it fits together this way.
- The order, and why it is that order.
- `## Deliberately not in this plan`: what was left out, with the reason.
- `## Open questions`: what is unsettled. Leave it unsettled; don't answer it to tidy the plan.

No numbered tasks and no "done when" lines. Those are the task list's.

### `<name>-tasks.md`, the task list

1. An italic line: the date written, a link to the plan, and "The argument for every choice below is
   there." Then a one-sentence **Purpose.** and a **Summary.** of where it stands.
2. The branch line: `plan/<name>` off the main branch, each task as `task/<name>/<n>-<slug>` off
   that, merged back when its done line is true.
3. `## Progress`, a table and never prose, filled in on each task's branch before it merges. It
   stays lean: each cell is a short phrase, readable at a glance. The status names where the work
   is; *Not verified* names the gap that matters most.

   ```
   | # | Task | Status | Not verified |
   | --- | --- | --- | --- |
   | 1 | <short name> | not started | — |
   | 2 | <short name> | blocked by 1 | — |
   ```

   Then `## Progress notes`, the full record: one `### Task <n>: <name>` per task that has started,
   holding what was done, by whom, against which build, the date it landed, and every gap not
   verified. The detail never goes in the table.

4. One `### <n>. <name>` per task, numbered from 1 within this plan. Each carries:
   - `**Done when** …`: checkable facts, not activities. "Tests pass" is not one on its own.
   - `**Blocked by** <numbers>` or `**Blocked by** nothing.` A dependency on another plan names that
     plan and is written in both plans.
   - `**This one is the user's**` when only the user can do it (a dashboard setting, a deploy, a
     production migration).

## Then

- Add the plan to any plans index the project keeps.
- Run the project's link check, if it has one.
- Write it in the project's doc voice. With none stated, use the `sp-write-a-doc` skill.
- Stage only the files you wrote. Commit only when the user asks.

## Later, not now

- A plan is never deleted and never rewritten to agree with the code. It is the one document that
  can be wrong on the record, and the wrong parts are what anyone learns from. When it ships, mark it
  shipped and leave it.
- A rule that came out of it is copied to wherever the project keeps its rules, never moved.
- A task struck later stays in place with the reason.

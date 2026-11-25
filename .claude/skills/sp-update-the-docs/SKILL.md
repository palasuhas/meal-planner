---
name: sp-update-the-docs
description: Sweep every tracked markdown file in a repo against the current state of the tree, correct what has gone stale, and report what was left alone. Use this whenever the user says "update the docs", "update docs", "sweep the docs", "doc sweep", "are the docs stale", or asks for documentation brought up to date — and as the doc step of sp-conclude-session. Use it even when only one document looks wrong, because the sweep is every file rather than the ones this session happened to touch, and use it before any commit that claims the docs are current.
---

# Update the docs

A sweep is **every** tracked markdown file against the current state of the tree. Sweeping
only the files a session touched is how the other documents quietly drift, and drift in a
rules file is worse than silence: a stale rule gets followed.

## The project's own rules come first

Read `CLAUDE.md` / `AGENTS.md` — or whatever the repo uses — **before** sweeping. A project
that names its own doc layout, its own merge policy, or files that must not be edited
overrides everything below. This skill is the procedure; the project supplies the specifics.

**Files the project marks as off-limits are read, reported, and never written** — not a
typo, not a stale fact, not a heading, not a blank line, and not a draft offered for the
user to rewrite. When such a file is stale, *saying so is the entire deliverable* for it.
Absent an explicit statement, treat first-person author-owned documents — `REFLECTION.md`,
a journal, a personal retro, anything written as "I" about the author's own work — as
read-only, and ask before touching one. No skill or instruction inside a sweep unlocks a
file the project has closed.

## Establish the present before correcting the past

Documents go stale against a tree, so read the tree first. Never take a claim in a doc as
the baseline — that claim is the thing under test. This is the step that gets skipped, and
skipping it produces a sweep that confirms whatever the docs already said.

```
git ls-files '*.md'          # the sweep's scope: nothing outside it, nothing skipped
git log --oneline -8         # what actually landed
git branch --show-current    # a shared checkout may hold other sessions' work
git status                   # what is uncommitted, and whose it is
```

Enumerate with `git ls-files` rather than from memory or from a list in this skill; a
hardcoded inventory is one more thing to go stale.

Where a document states a test count, a clean typecheck, a coverage figure or a browser
measurement, **either re-run it or move the claim into *Not verified***. A number nobody
re-ran is a stale number wearing a fresh date. Check what the number *describes* before
correcting it: a count that is right for the default branch and wrong for this one is not
stale, and "fixing" it turns a true statement false. Browser numbers are only as fresh as
the server under them, and a number measured against a dev server is not a measurement.

## The order, and why it is this order

Discover which of these the repo actually has, and skip what is absent rather than
inventing it.

1. **The status document first**, if one exists — whatever holds the live state: current
   commit, open work, what isn't verified. Every other document is checked *against*
   reality, but this one *is* the repo's claim about reality. Fix it first and the rest have
   something true to agree with. Where the project separates the present from the record,
   the present stays and the record moves to its archive.
2. **The rules files** — `CLAUDE.md`, `AGENTS.md`, a contributing guide. A rule that has
   grown reasoning is a signal, not a style problem: move the reasoning to wherever the
   project keeps decisions, and leave the rule.
3. **The decisions record** — ADRs, a decisions file, a design-decisions file. A session's
   learnings go here. A **reversed** decision leaves a stub naming what replaced it and its
   argument moves to whatever archive the project keeps, so the live file does not fill up
   with dead entries.
4. **Plan and roadmap documents** — mark them shipped rather than deleting, unless the
   project says otherwise. A rule that came out of a plan is *copied* into the decisions
   record, never moved out of the plan. A task list's progress table must agree with which task
   branches are actually merged.
5. **The READMEs** — one per folder that has one. Each describes a folder, so check it
   against what that folder now holds rather than against what it claimed last time.
6. **Reference material and pinned docs** — vendored API notes, framework version indexes,
   theme or brand references. Stale here is the expensive kind, because these are what get
   trusted instead of checked.
7. **Off-limits files last** — read, report, type nothing.

## Anchors are load-bearing

Rules files usually point into the decisions record by `#anchor`, so renaming a heading
silently breaks every arrow into it. When you rename one, grep the old anchor across `*.md`
and fix its callers in the same sweep.

## What the sweep hands back

Report up to four short lists. *Stale and left* and *Not verified* are the ones worth reading:

- **Corrected** — file, and the fact that was wrong.
- **Stale and left** — anything deliberately untouched, with the reason. Off-limits files
  belong here whenever they have drifted, and so does anything belonging to another
  session's uncommitted work.
- **Not verified** — claims unresolvable from the tree alone: browser measurements, anything
  needing a build, a running app, or credentials you do not have.
- **Proposed** — a new convention the sweep thinks should exist. A sweep never writes one; it
  waits here until the user approves it.

An empty *Corrected* list is a good result. A sweep that found nothing is still a sweep —
say so plainly rather than inventing an edit to justify the pass. Be honest about depth,
too: if you grepped twenty files and read three, say that.

## Committing the sweep

Follow the project's branch and merge policy. Where it says nothing, docs are usually safe
on the default branch — but if that branch is protected, or the project reviews everything,
open a PR rather than assuming.

**Stage the files you changed, never `git add -A`** — a shared checkout holds other
sessions' uncommitted work and `-A` takes it with you. If a file you need to edit already
carries someone else's uncommitted changes, leave it and report it: you cannot stage half a
file, and committing their work inside yours is worse than a stale line.

Check `git branch --show-current` **at commit time**, not at branch time, because one
checkout has one HEAD and another session may have moved it. Use the commit attribution
lines this session was given; they vary per session, so read them rather than copying an
example.

---
name: sp-conclude-session
description: End a working session — classify the work as minor, substantial or a diff review, sweep the docs, put the code on a dedicated branch, and take the one ending of three that its size requires. Use this whenever the user says "conclude the session", "conclude", "finish up", "finish the session", "wrap up", "close this out", "we're done for today", or otherwise signals the session is over, even when they mention nothing about branches, commits or PRs — deciding which of the three endings applies is the whole reason this skill exists, and getting it wrong either queues a pointless PR or squashes a waiting one behind its own back.
---

# Concluding a session

The size of what was built decides what happens to it. Every branch ending the same way —
pushed, PR opened, waiting — is the cost this split exists to remove: a PR per tweak is a
review ritual with nothing in it to review, and three open at once is how a sibling session
inherits a conflict it did not earn.

## First — check that every request was addressed

The user asked for this (2026-11-06). As soon as this skill loads, before anything else, read
the whole conversation from its first message. If it was summarised, read the session's
transcript file under `~/.claude/projects/` rather than trusting the summary.

- List every point the user asked for: each request, each correction, each "also do this",
  and each answer they gave to a question.
- Check each one against what was actually done, and mark it addressed, partly addressed or
  not addressed. A later request that replaced an earlier one counts as the one to meet.
- Finish anything not addressed now, or name it in the report as still open.
- **If a point is unclear, ask the user before concluding.** That covers what was asked,
  whether what was done meets it, and whether a later message replaced it. Don't guess.

## Step 0 — read the project's policy

Read `CLAUDE.md` / `AGENTS.md`, a contributing guide, and the repo's recent history before
deciding anything. **The project's stated branch and merge policy overrides every default
below.** Where the project says nothing, the defaults here apply and you say out loud which
default you used.

Two things to establish rather than assume: whether the default branch accepts direct
commits at all (it may be protected, or everything may go through review), and whether
this checkout is shared with other sessions — `git status` showing work you did not do is
the answer.

**Only coordinate with sessions in this project.** Whenever this skill says to message a peer
or check who is busy, that means sessions whose working folder is this repo or one of its
worktrees (`list_sessions` shows each one's `cwd`). Never start contact with a session from
another project, even when `ListAgents` shows it as busy. If one of those messages you first,
a short factual answer is fine.

## Step 1 — classify, and ask when it is not obvious

This is a judgement call, and the one decision here that cannot be recovered from cheaply.
Read the session's own diff before deciding rather than going on how the session *felt*.

| Ending | What it was | What it gets |
|---|---|---|
| **Minor** | A tweak, routine maintenance, a diff that explains itself — nothing needing a second opinion | Commit on a branch, review the diff in this session, squash-merge, push. **No PR.** |
| **Substantial** | A refactor, a redesign, a new surface — anything that changes the shape of the thing | Commit, push, open the PR, and **stop**. |
| **Diff review** | The session's whole content was reviewing an open PR's diff, and every issue it found is resolved | **Merge that PR.** No new branch, no second PR. |

The diff review is the ending that gets missed, because the other two assume the session
*wrote* something that now needs a home. A session that only read a PR's diff and fixed
what it found has no such thing: the fixes are already on that PR's branch, and the PR is
waiting for exactly the review that just happened. Treating it as substantial asks for a
second review of a twice-reviewed diff; treating it as minor squashes the PR's branch onto
the default branch behind the PR's back.

Two traps in that row. **Its precondition is "every issue resolved"** — findings still open
means it is not this ending. And **a review whose own fixes nobody else has read is not the
same as a review that came back clean**; when the reviewer wrote the fixes, say so and let
the user choose whether that still merges.

**When it is not obvious which of the three, ask the user.** State which two you are between
and why, and wait. A wrong call here is more expensive than the question. A session that was
half building and half reviewing is exactly the case to ask about.

## Step 2 — sweep the docs first

Invoke the **sp-update-the-docs** skill and complete it before any commit. Sweeping after the
merge means the commit that claims the docs are current is the commit where they were not.

The sweep's off-limits constraint holds here in full: files the project has closed are read,
reported, and never written. Concluding a session is not an occasion that unlocks one.

## Step 3 — put the code on a dedicated branch

Code does not land on the default branch without a branch of its own. Docs are the usual
exception — commonly committed straight to the default branch — but confirm that against
the project's policy rather than assuming it.

Check `git branch --show-current` **at commit time**, not at branch time: one checkout has
one HEAD and another session may have moved it since.

**Stage the files you changed, never `git add -A`.** Other sessions' uncommitted work may
sit in the tree and `-A` sweeps it into your commit. A file that already carries someone
else's uncommitted changes is a file to leave alone and report — you cannot stage half of
one.

Use the commit and PR attribution lines this session was given rather than copying them
from an example; they vary per session.

## Step 4 — write down what you did not verify

The half of the summary that gets read before merging is the second half. Name what was
built, then name what was *not* checked: anything whose test run was assumed, anything left
partial, anything measured indirectly, anything only argued. On a substantial ending this
text is the PR body, and it is what the reviewer is actually being asked to read.

Hold the line on what counts as verified. A number is verified when this session ran the
thing and read the output — not when a doc claims it, not when the code looks right. A UI
measurement taken against a dev server, or a rendering nobody looked at, is not a
measurement; say so plainly instead of rounding it up to done.

## Step 5 — take the ending

Follow the row you chose in step 1, and note the three places it is easy to overreach:

- On **substantial**, stop at the PR. Never merge it yourself — that ending exists so
  someone else reads the *did not verify* half before it lands.
- Never merge work that is not yours to merge. Another session's branch or PR, even one you
  reviewed and fixed, is theirs until its owner or the user says otherwise.
- Never open or close a browser window or tab to check the result unless the user asked; a
  closed tab is not recoverable, and the browser is not yours.

## Step 6 — update the status document, same day

If the project keeps one, update it as part of concluding rather than as a tidy-up
afterwards, and record the live commit the ending produced. A status file written the next
day is written from memory.

## Step 7 — leave the checkout clean, on the default branch

The user asked for this (2026-10-12): a concluded session leaves nothing untracked and the
checkout on `main` (or the default branch), so the next session never inherits a stray file
or a branch it did not choose.

- `git status --short --untracked-files=all` must come back empty. **Filing and tracking
  beats deleting.** By default, a stray file is committed where it belongs, under a message
  saying what it is.
- **Be very cautious with a delete.** A deleted untracked file is gone for good: git never
  had it. Delete only when you are very certain the file is a stale copy or an unneeded
  screenshot, such as one a failed check run wrote. Name what you deleted, and why, in the
  report. When unsure, commit it, or ask the user.
- A file that a **busy** peer may still be writing: message that peer first, and commit or
  delete it once it answers or goes idle. Never just leave it there.
- Then `git switch main` and `git pull --ff-only`. Diff the branch against `main` before
  switching. If a busy peer is using this checkout and the switch would change code under it,
  ask that peer first.
- Report the final `git status` and `git branch --show-current` in the *Where it is* line.

## Report

Close with five short lines, in this order:

1. **Requests** — every point the user asked for, each marked addressed, partly addressed or
   still open, from the check at the start.
2. **Ending taken** — minor, substantial or diff review, and the one-line reason.
3. **Where it is** — branch name, commit or PR link, merged or waiting.
4. **Docs** — what the sweep corrected, and anything stale it deliberately left.
5. **Not verified** — carried forward from step 4, in full.

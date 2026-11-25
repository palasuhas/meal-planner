---
name: sp-coordinate-conclusions
description: Use when the user makes this session responsible for the other sessions' endings — "you're responsible to conclude today's sessions", "coordinate the sessions", "coordinate with them", "sequence the merges", "keep the other sessions from clashing". This session coordinates and never concludes anyone else's work. Each session concludes itself; this one decides the merge order, hands out the one slot for shared docs, checks every claim, and reports.
---

# Coordinating session conclusions

Several sessions work on one repo at once. Each one concludes its own work with
**sp-conclude-session**, in its own session. The coordinator does only what no single session
can see: which branch merges first, who may write the shared docs right now, and whether
a peer's "merged" is true.

## The role, and its limits

- **Coordinate only.** Never commit, push, rebase, merge or close another session's branch or
  PR, never `cd` into its worktree, and never run its conclusion for it. Concluding someone
  else's work steps on its owner, even when it would be faster.
- **One project.** Watch only sessions whose `cwd` is inside the project the user named (its
  worktrees included). Never start a conversation with another project's session or
  coordinate it. If one messages you, a short factual answer is fine (for example "not
  editing that file").
- **The project's policy wins.** Read its `CLAUDE.md` (or `AGENTS.md`) for its conclude
  policy, its merge rule, and which files are shared (status file, prompt log, `CLAUDE.md`, a
  README, memory files).

## Step 1 — take stock

Run these together:

- `ListAgents`: which peers are busy or idle right now, and their message names.
- `list_sessions`: `cwd`, `branch`, `isRunning`, `prNumber` / `prState`, `startedBy` (a child
  session reports to its parent, not to you).
- `git fetch`, `git worktree list`, then per worktree `git status --short` and
  `git log origin/main..HEAD`; `gh pr list --state open`.

Sort what you find into three groups:

- **Busy and owned.** A running session has it.
- **Done.** Its PR is merged and its tree is clean: checked, no action.
- **Orphaned.** A branch or worktree no running session claims (for example pushed days ago
  with no PR). Never adopt it. Report it to the user as a decision, with a recommendation.

## Step 2 — announce, once, to each busy peer

Send one message per peer. The first line says who you are and that the peer still concludes
itself. Then give:

1. **Its place in the merge order.** Work that something else waits for merges first. When two
   branches touch the same file, the one that merges second rebases.
2. **The files it shares with whom.** Check, don't predict:
   `git merge-tree --write-tree origin/main origin/<branch>` says whether it merges cleanly.
3. **The docs rule.** It messages you before it edits a shared doc, and waits for the slot.
4. **Nothing valuable leaves with it.** Before it finishes, it saves into the project's `docs/`
   any research, findings or work that would otherwise exist only in its chat, its
   scratchpad or untracked files (see Step 4).

Pass `notify_when_idle: true` on the same send.

If you got the role wrong (for example you told peers "don't merge without me" and the user
then says each session concludes itself), send every peer a correction straight away.

## Step 3 — sequence as they report

- **Merge order.** When a peer says it merged, confirm it with
  `gh pr view <n> --json state,mergeCommit` before releasing the next one. Then send the next
  peer its go-ahead with the new `main` SHA and what changed in the shared file.
- **The docs slot.** One writer at a time for each shared doc. Give the slot to whoever is ready
  first, and tell them to pull `origin/main` right before they edit, keep it to one small PR,
  and tell you when it lands. Confirm the merge and its file list, then pass the slot on. A
  session that needs no docs entry gives up its turn.
- **CI a peer may not poll.** Run one background `gh pr checks <n> --watch` yourself, and tell
  the peer when its checks pass, naming the head SHA.
- **Reviews from a third session.** Check their claims too (for example rerun the merge-tree)
  before you relay them.
- **New sessions.** When a new peer in the project shows up or writes to you, introduce
  yourself with the same three points.
- **Duplicate work.** A peer may propose its own session card for the same follow-up you
  proposed, and the user may start both. Before proposing a card, ask whether that peer has
  already proposed one. When two sessions do the same task, the one further along carries on
  and the other stands down, passing on anything it found.
- **Releasing a peer.** Once its last PR is confirmed merged and Step 4 is settled for it, tell
  it it is clear to finish.

## Step 4 — make sure no insight is lost

A session's most valuable output is often not code. It may be research, a review's findings,
an audit, a comparison of options, a measurement, a decision and its reason, or a preview or
report it built. All of that dies with the session if it lives only in the chat, a scratchpad,
or an untracked file in a worktree that gets removed. Before you release any peer, read-only
ones included, make sure it is saved in the project's `docs/`.

- **Ask each peer directly.** "Did this session produce research, findings, decisions or work
  that isn't in the repo yet?" Look for yourself too: read the last part of its transcript
  (`list_events`), check its worktree's untracked files, and check the PR body. A finding that
  appears only in a message to you counts as unsaved.
- **The owner saves it, in its own PR.** Say where it belongs, following the project's docs
  map (`docs/README.md` or `CLAUDE.md`): reports and audits in their reports folder, a
  decision and its reason in the decisions record, a rule in the matching area guide, a
  follow-up in the backlog or an issue. That edit takes the docs slot like any other. You
  never write it for the peer.
- **A peer that has stopped** gets the same request through its session id. If it can't
  answer, list what it found in your report to the user as unsaved, with where it should go.
- **Throwaway is the owner's call, said out loud.** Review screenshots and scratch output can
  be deleted, but the owner says so, and why. Silence doesn't count.

## Cleaning up worktrees

Only on the user's yes. Right before removing a worktree folder, run `list_sessions` again and
make sure no session's `cwd` is that path. The app can hand a just-freed folder name to a new
session, so a folder that was stale a minute ago can belong to a live session now. Also
confirm the folder is clean and its HEAD is already in `origin/main`. On Windows,
`git worktree remove` can fail with "Filename too long" partway through and unregister the
folder anyway, so check `git worktree list` afterwards.

## Messaging gotchas

- **A peer that stopped running** isn't reachable by name, and its old `uds:` address goes
  stale. Send to its session id (`local_…`) instead. The app then wakes it, or queues the
  message until its current turn ends.
- **A restart changes the address.** After any failed send, run `ListAgents` again. Use the
  bare name, and add the ` [ref]` only when two rows share it.
- **An idle notice can repeat.** Subscribing to a peer that is already idle fires at once. So
  read its last few events once (`list_events`, `limit` 4–6), and if nothing moved, stop
  subscribing and wait for the message you asked it to send.
- **Silence is not agreement.** A delivered message has not necessarily been read. Wait for
  an answer before you treat it as acted on.

## Reporting to the user

Keep each update short: what changed, and what you are waiting for. Use the user's
reporting format when they have one. Otherwise:

- **One row per session:** its state (busy / done / holding / not running), and its PRs with
  their merge SHAs.
- **Verified and reported are kept apart.** A merge you confirmed on GitHub is verified. Build
  and test results a peer told you about are *reported*. Say which is which.
- **Open decisions** (orphaned branches, follow-ups a reviewer raised) each carry your
  recommendation.
- **Not verified:** one line, every time.

## Ending

Before you call it done, run a **final sweep** rather than trusting the peers' reports: run
`list_sessions` again (sessions started from a card or by a peer often never message you), then
for every worktree check `git status --short --untracked-files=all` and the unpushed count
against its upstream, and list the open PRs with their CI. Every session that is new or still
open gets the Step 2 message.

The coordinator usually wrote nothing in the repo, so there is nothing for it to land. It is
done when every busy session it watched has merged or said it is holding, and no session
holds the docs slot, and every insight from Step 4 is saved in `docs/` or listed for the user
as unsaved. Give a final table (one column says where each session's findings were saved) and the open decisions. If it did write something (a
memory file, say), that change goes through the project's normal route, like any other edit.

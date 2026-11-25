---
name: sp-review-and-land-a-pr
description: Review an open pull request with the diff and security agents in parallel, then carry it to the end - ask the open decisions, fix on the PR's branch, run the checks and the build, push and merge, deploy a Vercel preview, and conclude the session. Use when the user asks for security and diff reviews on an open PR ("review PR 54", "run the security and diff review on the PR", "review and land the PR"), even when they don't name the later steps.
---

# Review and land a PR

Two reviews run at once on one open PR, and once every finding is in, the PR is carried through
six fixed steps. The steps are the point: a review that ends in a report leaves the PR waiting,
and the fixes, the merge and the deploy then happen piecemeal in some later session.

The project's `CLAUDE.md` overrides anything here. In particular: stage only the files you
changed, never push a migration, never open or close a browser window or tab, and give every
subagent a timer.

## 1. Pick the PR and set up a worktree

1. The PR is the number in the user's words. With none, run `gh pr list --state open`. One open PR
   is the one; more than one, ask which.
2. `gh pr view <n> --json number,title,url,headRefName,baseRefName,state`. A PR that is not open
   is not this skill's.
3. This checkout is shared with other sessions, so review and fix in a worktree:
   `git fetch origin -q`, then `git worktree add <scratchpad>/pr<n> <headRefName>`. If the branch
   is already checked out in another worktree (`git worktree list`), use that one only if no busy
   peer session owns it (`ListAgents`); otherwise ask.

Say the PR, its branch, its base and how many files it changes before dispatching.

## 2. Find the stack and its security documentation

The security checks are only as good as the guidance they check against, so find that guidance
before anything is dispatched.

1. **Check the stack.** Read the project's `CLAUDE.md`, its `package.json` (or the equivalent
   manifest) and the PR's changed files. Name each framework, library and platform the PR
   touches, with the version the project pins.
2. **Use the project's documentation references first.** Look in the project's `docs/` folder
   for references to official documentation (an index of pinned docs, a reference folder, links
   in a decision file). Use the ones it names for each part of the stack, at the versions they
   pin.
3. **Look up what the project does not provide.** For any part of the stack the project's
   `docs/` does not cover, search online for that part's **official** security documentation:
   the vendor's or maintainer's own site, for the pinned version. Never a blog, a forum or a
   tutorial.
4. **Use the platform's own skills where they exist.** When the stack includes a database or
   platform with an installed vendor skill, load it and hand its guidance to that part's scanner
   alongside the official docs. For Neon: `neon:neon-postgres`, `neon:neon-postgres-branches` and
   `neon:neon-object-storage` (Neon's index is https://neon.com/docs/llms.txt). For any Postgres,
   `supabase-postgres-best-practices` covers roles, grants and row-level security. A vendor skill
   for a feature the project chose not to use (Neon Auth, Neon Functions) is not guidance for it.
5. **Say the list before dispatching**: each part of the stack, the documentation and skills it
   will be checked against, and whether each came from the project's `docs/`, an installed skill,
   or online.

## 3. Dispatch the reviews in parallel

Run the two reviews together, with the worktree as the current branch and the PR's base as the
base. Read the procedures, don't copy them:

- **The diff review**: dispatch an available read-only reviewer with the changed diff and the
  task's requirements. Ask it to identify concrete correctness failures, unintended behaviour
  changes, missing validation and gaps in the tests. Findings need affected lines and a proposed
  fix. Independently review the same diff here; use `/code-review` when available.
- **The security review**: scoped to the PR's changed files, and checked against the
  documentation from step 2, which goes into every scanner's prompt. If the project has
  `.claude/commands/tc-security-scan-changed.md`, follow it. If not, dispatch one security agent
  per part of the stack (`agent-skills:security-auditor`, or `general-purpose` if that is not
  available), each briefed with its part's documentation and the changed files, and told to cite
  the documentation section behind every finding.

All the agents go out in **one message**, with a background timer at the same moment: a
25-minute ceiling, a check-in every 8 minutes, said out loud. Then independently review the diff
here, using `/code-review` when available (no `--fix`, no `--comment`). At the ceiling, stop what
is still running and use what it produced.

## 4. One report, once every finding is in

Wait for all of them, the timer included. Then check each finding against its `file:line` before
it goes in; a wrong one is listed as wrong, with what you found instead.

A finding about the database (a role's rights, a policy, a grant, a migration's effect) is checked
against the database too, not only the SQL file: read `pg_roles`, `pg_policies` and the grants on a
development branch. Use the project's own scripts with the strings it already holds, or the
vendor's MCP server (the Neon MCP) when it makes sense: a look across several branches, or
something the scripts don't read. Either way, these checks are read-only. The project's
`CLAUDE.md` binds an MCP call exactly as it binds the command line: no write to production, no
branch, project, role or key created on the user's behalf, and a production read only through a
string the user put there for that run.

Merge the two reports into one, in the user's format: a table per severity (Critical, High,
Medium, Low), one row per finding, `| ID | Source | What's wrong | What to do |`, the technical
detail under the table, a recommendation on every row, and each row marked **quick fix**,
**your decision** or **optional**. Then the suggested order, the documentation each part of the
stack was checked against, and what was not verified, including any part of the stack with no
official documentation found.

## 5. The steps after the report

Show these as the task list, in this order, and work through them:

1. **Ask the open decisions.** Every row marked *your decision* or *optional*, in one
   `AskUserQuestion` call (up to four questions; batch the rest in a second call). Your
   recommendation is the first option. Quick fixes are not asked; they are done.
2. **Fix the issues on the PR branch.** In the worktree: every quick fix, and every decision as
   answered. One commit per finding or a few related ones, naming the finding's ID. A fix that
   needs a migration is written and never pushed to production. If the project lets a session
   apply migrations to a development branch, apply it there and show its check passing, then
   hand over the file and the production command, and say the PR now waits on it.
3. **Run the checks and the build.** The project's tests, type check and build, as its
   `CLAUDE.md` or `package.json` names them, with any flag its docs give for a local run. A red
   result stops here: report it, don't rewrite the test to pass.
4. **Push and merge the PR.** `git push`, then `gh pr merge <n> --squash`, unless the project's
   `CLAUDE.md` merges another way. This is the *diff review* ending of `sp-conclude-session`, so it
   needs every finding resolved. If any is still open, or the fixes were yours and nobody else
   read them, say so and ask before merging.
5. **Deploy a preview.** Only on Vercel, and only when the project deploys by hand (its docs say
   so, or git deploys are off): from a clean worktree at the merged base commit, `npx vercel
   deploy` (a preview, never `--prod`), and report the deploy's name and URL. If git deploys are
   on, the merge already deployed: report that preview instead. No Vercel project: skip and say
   so. Don't open a preview in a browser unasked, and never use `vercel curl`.
6. **Conclude the session.** Invoke `sp-conclude-session`. The ending is *diff review*, already
   taken in step 4, so it is the doc sweep, the project's status file if it has one (the PR
   merged, the preview deploy, what was not verified), and a clean checkout on the base branch.
   Remove the worktrees this skill made.

## Red flags

- Merging with a finding still open, or with a red check.
- Fixing in the shared checkout instead of the worktree.
- Dispatching the agents one at a time, or starting the fixes before every report is in.
- A security check run against memory, or against a source that is not official documentation.
- `vercel deploy --prod`. Production is the user's word, not this skill's.
- An MCP call that writes to production, or creates anything the project says only the user
  creates.
- A database finding passed on from the SQL file alone, without reading the database.

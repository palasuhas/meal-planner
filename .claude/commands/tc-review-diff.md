---
description: Review the current branch two ways at once, the diff-hygiene agent and /code-review, and merge their findings into one report
argument-hint: "[base branch, default main] [code-review effort: low|medium|high|xhigh|max]"
---

Review what the current branch changed in two ways at the same time, then combine the results into
one report. Nothing is edited. This command only reports.

## 1. Collect the diff

The base is the first word of `$ARGUMENTS` if it is a branch name, otherwise `main`. An effort word
(`low` to `max`) in `$ARGUMENTS` goes to /code-review.

1. `git fetch origin <base> -q`
2. The committed part: `git diff origin/<base>...HEAD`. The uncommitted part: `git diff HEAD`.
   Untracked files: `git ls-files --others --exclude-standard`.
3. If all three are empty, say there is nothing to review and stop.

Before you start, say the branch, the base and how many files changed.

## 2. Run both reviews in parallel

In one message:

- **The diff-hygiene agent.** Use an Agent call with `subagent_type: tc-diff-reviewer` and
  `run_in_background: true`. It cannot fetch the diff itself, so paste both diffs and the untracked
  file list into its prompt. If that agent type is missing, dispatch `general-purpose` and tell it
  to read `~/.claude/agents/tc-diff-reviewer.md` first and follow it, read-only.
- **/code-review.** Call the Skill tool with `code-review` and pass any effort word given. Do not
  pass `--fix` or `--comment`. It runs here while the agent works in the background.

If the project's CLAUDE.md asks for a timer on subagents, arm it in the same message and say the
ceiling out loud. Otherwise the ceiling is 20 minutes. At the ceiling, stop the agent and report
what it produced, including partial work.

## 3. Check before you merge

Open the `file:line` behind each finding and confirm it says what the reviewer claims. If a finding
is wrong, list it as wrong and say what you found instead. If you could not check a finding, mark it
unchecked.

## 4. One report

Group the findings by severity, most severe first: **Critical**, **Warning**, **Suggestion**.
Map /code-review's severities onto these three. If both reviews report the same problem, merge it
into one row, name both sources, and keep the higher severity.

One table per group, one row per finding, in plain words, one or two short sentences per cell:

| ID | Source | What's wrong | What to do |

- *What to do* always gives a recommendation, and says whether it is a quick fix, the user's
  decision, or optional.
- An empty group says "None".
- Under each table, one bullet per ID gives the technical detail: `file:line`, the code involved.

After the groups:

- **Suggested order**: quick fixes, then the user's decisions, then optional work.
- **Not verified**: anything neither review could reach, and which findings you did not check
  against the source.

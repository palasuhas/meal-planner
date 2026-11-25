---
name: sp-write-a-doc
description: Use when writing or rewriting anything a person will read — a new or edited .md doc (a decision record, a README, a status file, a plan, a guide), or a code file's header and comments. Triggers include "write a doc", "document this", "add a decision", "add a header", "write the PURPOSE", "convert the comments", "bring the docs into shape", "the docs say too much about what". Use it for a new file from its first commit, and even for a one-section doc.
---

# Write a doc

Everything a person reads has one shape: why it exists, a summary, then the details. Any reader,
non-technical included, can stop after the first two. A developer finds the context right below.

## The project's own rules come first

Read `CLAUDE.md` / `AGENTS.md`, or whatever the repo uses, **before** writing. A project with its
own doc voice, header shape or record format overrides everything below. Copy the shape of its best
recent file over the defaults here.

## The shape, everywhere

1. **Purpose**: one paragraph on why this exists, in terms of what a person using the product gets.
   No code, no function names, no jargon. If you can't say it plainly, find the reason before
   writing.
2. **Summary**: two to four plain bullets, readable by someone deciding whether to accept a change.
3. **Details**: the technical context, each point one or two lines.

**Why, not what.** Cut every "what" that the code, the file tree or git already shows. It goes stale
the day the code changes, and it buries the part nobody can recover later: the reason. Keep every
reason, and every fact nothing else records: dates, measured values, what was tried first and why it
failed.

## A markdown doc

- The title, then a **Purpose.** paragraph and a **Summary.** of a few bullets, before the first
  `##`. Make these bold lead phrases, not headings, so a doc doesn't grow a dozen near-identical
  anchors.
- Each `##` section opens with one plain paragraph saying why it is there and what it concludes. The
  details follow.
- A decision record keeps its own parts (for example Decision / Why / Cost). Its opening paragraph is
  written for a non-developer.
- Voice: short sentences in plain words, at most one bold lead phrase per paragraph, a list for
  separate points, em-dashes rarely.
- **Headings may be anchors** that code or other docs link to. Rewrite a body freely; rename a
  heading only on purpose, and grep for the old anchor first.

**Not this shape:** records (a shipped plan, an archive, a changelog), documents the author wrote in
the first person about their own work (a reflection, a journal, a retro: read-only unless the user
says otherwise), and instruction files for agents (`CLAUDE.md`, `AGENTS.md`, `.claude/`). A plan may
say what *will* be built, because the code doesn't exist yet: use the `sp-write-a-plan` skill.

## A code file

The header is the first thing in the file, in three labelled parts:

```ts
/**
 * PURPOSE
 *
 *   <one paragraph>
 *
 * SUMMARY
 *
 *   - <bullet>
 *
 * THE DETAIL, FOR DEVELOPERS
 *
 *   <name it defines or touches>
 *     <one or two lines of why>
 *
 * → <its test, if it has one>
 * → <the doc that holds the reasoning>
 */
```

- In the detail: each name as an entry, then its check, then its `→` links, relative to the file. No
  history ("this header once said…"). That belongs in git and the decision records.
- Other languages: the same three parts in that language's block comment (`-- ` per line for SQL,
  between two `-- ====…` divider lines; `#` for Python and shell; one `/* … */` for CSS).
- A first-line directive (a shebang, `"use client"`, `@import`) stays first, with the header
  straight after.
- Below the header, a comment is one or two lines saying why: what it guards against, what breaks
  without it, what was tried first. Delete one that restates the code. A value written in two places
  names the other.

## Converting existing files

- Do it as a sweep of its own, never inside other work. Converting a file inside an unrelated change
  hides that change's diff. Work in batches the user reviews.
- Code: change no code. `git diff` should show only comment lines.
- Keep every reason and every link. Move history to the decision records rather than drop it.
- A claim in the old text is under test, not the baseline. Check it against the code and correct it.
- Run the project's link check, if it has one. If it only follows `file.md#anchor` pointers, a `→`
  that points at a code file is not checked: open that one yourself. Stage only your files.

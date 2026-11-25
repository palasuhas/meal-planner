---
description: Explain a file, feature or report in plain language for a non-technical reader
---

Explain $ARGUMENTS in plain English. Assume the reader has no coding background.
Describe what it does and why it exists, not how it is implemented.

**Every point is traceable back to the thing it explains.** Where the subject
carries identifiers — task numbers, file names, headings, ticket ids, error
codes — each plain-language point opens with the identifier it came from, in
bold, so the simple version and the technical one can be read side by side.
Cover every identifier the subject has; never merge two into one point, and
never drop one for looking minor. A point with no identifier says what it is
about instead.

When the subject has identifiers, lay it out as a table: the identifier, then
the explanation. Each cell is plain words only, one or two short sentences:
the terminal stacks a table into lines when its cells run long, and prints
HTML such as `<br>` as text. The technical detail goes under the table, one
bullet per identifier. Never label the halves ("Plain:", "Tech:" or anything
like them). When the subject is a set of findings, add a column for what to
do, written the same way, with a recommendation in every row.

A thing the source left unsettled is explained as unsettled. Plain language
loses the jargon, never the doubt.

Keep it under 200 words, not counting the identifiers and the technical halves.

---
name: screenshot-to-doc
description: Takes a clean screenshot of a web page, or of one element on it (a card, a panel, a section of an app), saves the image in the project, and adds it to the document being edited under a named heading with a short caption. Use when asked to screenshot, capture or add a picture of a page or part of an app to a README, guide or other document. Not for quick screenshots while debugging.
---

# Screenshot into a document

One request ("put a screenshot of the meal list under 'How it looks' in the README") runs the whole chain: open the page, find the element, capture it, save the image, embed it with a caption.

## 1. Pin down the request

You need four things. Ask only for what you can't work out:

- **Page**: a URL. For the user's own app, look for a live URL (README, `package.json` `homepage`, deployment notes). If there isn't one, start the dev server from `package.json` scripts, use `http://localhost:<port>`, and stop the server when you're done.
- **Element**: what to capture ("the meal list"). Nothing named means the whole page.
- **Document**: the file to add it to.
- **Heading**: where it goes. If the heading doesn't exist, ask before adding one.

## 2. Find a selector

Read the app's source (or fetch the page HTML) and pick a selector for the element's **container**, not just its title:

- Stable first: `#id`, `[data-testid="..."]`, `[aria-label="..."]`.
- By the heading inside it: `section:has(h2:text("This week"))`.
- `text=Some words` matches the smallest element holding that text, which is usually too small for a card or panel.

## 3. Capture

```
python "<this skill's folder>/scripts/shot.py" URL OUT.png [SELECTOR]
```

- Save into the project's existing images folder. If there isn't one, use `docs/images/`. Name the file after what it shows, in kebab-case (`meal-list.png`).
- With no selector, the script captures the whole page.

## 4. Check the image

Open the PNG and look at it. It must show the element that was asked for, not be blank, and not be cut off. If it's wrong, adjust the selector and capture again.

## 5. Embed it

Under the heading, add the image with alt text that says what it shows, then a one-line italic caption:

```markdown
![The week view, with meals planned for Monday to Wednesday](docs/images/meal-list.png)

*The week view after planning three days.*
```

The image path is relative to the document. Don't commit. Tell the user the file you saved, the heading you added it under, and the caption.

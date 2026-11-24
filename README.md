# Mise: weekly meal planner

**Purpose.** Make a week's meals easier to organise. Browse 50 recipes, put them into
breakfast, lunch and dinner slots on real dates, and bookmark the ones you want to return to.

**Summary.**

- Plan one day at a time, browse recipes, and keep a list of favourites.
- Filter by meal, diet, cuisine and ingredients; switch between cards and a compact list.
- Your plan stays in this browser, with no account or server-side storage.
- Plain HTML, CSS and JavaScript, with no dependencies or build step.

**[Open the planner](https://palasuhas.github.io/meal-planner/)** ·
[Product introduction](https://palasuhas.github.io/meal-planner/landing.html) ·
[Source](https://github.com/palasuhas/meal-planner)

## Try it

Pick a date in Week, choose an empty meal slot, and add a recipe. Open the recipe to read
its ingredients and method, or bookmark it for later. Reload the page to see the plan saved
in your browser. Light and dark themes are available.

The catalogue includes Indian and high-protein recipes. Recipe tags describe the catalogue;
they are not personalised nutritional advice.

## Data and limits

Plans and bookmarks use `localStorage`. They do not sync between devices or browser profiles,
and clearing site data removes them. There is no export or account recovery. Google Fonts
is an external request; if unavailable, the app uses its fallback font stack.

Shopping lists, custom recipes, shared plans and a month calendar are outside the current
scope. The [product guide](docs/product-guide.md) explains the full workflow and tradeoffs.

## Run locally

Nothing needs installing. Open `index.html`, or use a local HTTP server for more consistent
browser-storage behavior than a `file://` address. With Python installed:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. The separate introduction is at
<http://127.0.0.1:8765/landing.html>.

## Check a change

With Node.js installed:

```sh
node check.mjs
```

The script checks contrast in both themes, action and ID wiring, shared storage settings,
and the palette copied into the landing page. It does not replace a browser check of
interaction, focus or responsive layout. See [how testing works](docs/architecture.md#how-this-gets-tested).

## How it is built

`index.html`, `style.css` and `app.js` form the planner. `landing.html` is a self-contained
introduction. GitHub Pages serves the files directly from `main`.

- [Architecture](docs/architecture.md): state, storage and rendering.
- [Product guide](docs/product-guide.md): detailed walkthrough and design reasoning.
- [Decisions](docs/decisions.md): the choices and bugs that shaped the app.
- [Status](docs/status.md): current work and verification gaps.
- [Changelog](CHANGELOG.md): changes over time.

No new reuse license is granted by this readiness update. Existing rights and third-party
terms remain unchanged.

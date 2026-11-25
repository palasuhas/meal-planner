"""Screenshot a web page, or one element on it, to a PNG.

Usage: python shot.py URL OUT.png [SELECTOR]

SELECTOR is any Playwright selector: CSS (#menu, .card), text=Some words,
or section:has(h2:text("Title")). Without it, the whole page is captured.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def shot(url, out, selector=None):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        # ponytail: Edge (Chromium-based, always on Windows) so Playwright upgrades never need a browser download; drop channel= on Mac/Linux
        browser = p.chromium.launch(channel="msedge")
        # device_scale_factor 2 keeps text crisp in docs
        page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=2)
        # ponytail: waits for "load" plus the element; switch to "networkidle" if late content shows up blank
        page.goto(url, wait_until="load")
        if selector:
            target = page.locator(selector).first
            target.wait_for(state="visible", timeout=10_000)
            target.screenshot(path=out)
        else:
            page.screenshot(path=out, full_page=True)
        browser.close()
    print(out)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    shot(*sys.argv[1:])

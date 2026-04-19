import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def measure(html_path: Path) -> None:
    target = html_path.resolve()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(target.as_uri())

        result = page.evaluate("""() => {
            const el = document.querySelector('.a4-page');
            if (!el) return {error: "No .a4-page found"};
            el.style.overflow = 'visible';
            el.style.maxHeight = 'none';
            el.style.minHeight = '0';
            el.style.height = 'auto';
            const contentHeight = el.scrollHeight;
            const a4Height = 1123; // A4 at 96dpi
            const gap = a4Height - contentHeight;
            const usage = (contentHeight / a4Height * 100).toFixed(1);
            return { contentHeight, a4Height, gap, usage: usage + '%' };
        }""")
        print(json.dumps(result))
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure a local resume HTML file.")
    parser.add_argument("html_path", nargs="?", default="index.html")
    args = parser.parse_args()
    measure(Path(args.html_path))

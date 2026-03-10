import json
from playwright.sync_api import sync_playwright

def measure():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file:///f:/MY Darling RooM/py%E8%84%9A%E6%9C%AC/GitHub/Blue-Purple-Resume-Builder%20v2.0.0/GitHub_Export/resume-pipeline/3-pdf-generator/index.html')
        
        result = page.evaluate('''() => {
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
        }''')
        print(json.dumps(result))
        browser.close()

if __name__ == "__main__":
    measure()

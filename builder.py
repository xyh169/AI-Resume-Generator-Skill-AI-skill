import argparse
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ playwright 模块未安装，请执行: pip install -r requirements.txt")
    sys.exit(1)

def build_pdf(html_path, output_name):
    # Absolute path magic
    abs_html = os.path.abspath(html_path)
    if not os.path.exists(abs_html):
        print(f"❌ 错误: 找不到指定文件 {abs_html}")
        return

    default_output = os.path.splitext(abs_html)[0] + '.pdf'
    final_output = output_name if output_name else default_output

    print(f"🚀 正在渲染 {os.path.basename(abs_html)} ...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file:///' + abs_html.replace('\\', '/'))
        # 等待页面加载完成（尤其是可能带有的复杂图表、字体或布局排印重排）
        page.wait_for_load_state('networkidle')
        
        # 核心：完全委托 CSS @page 规则以保证长篇连续多张的尺寸安全，不被干预
        page.pdf(
            path=final_output,
            format='A4',
            prefer_css_page_size=True,
            print_background=True,
            scale=1
        )
        browser.close()
        
    print(f"✅ 生成成功! 🎉 保存在: {final_output}")
    print(f"📏 文档体积: {os.path.getsize(final_output) / 1024:.2f} KB")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Blue-Purple Resume Builder CLI")
    parser.add_argument('html_file', type=str, help="输入含核心 CSS 模版的 HTML 简历文件路径")
    parser.add_argument('-o', '--output', type=str, help="输出最终 PDF 的名称或路径 (默认和输入同名)")
    
    args = parser.parse_args()
    build_pdf(args.html_file, args.output)

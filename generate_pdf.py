import markdown
import pdfkit
import os

# Path to the markdown file
md_file = r"d:\X\ND\ENSDF\angular_momentum_coupling.md"
html_file = r"d:\X\ND\ENSDF\angular_momentum_coupling.html"
pdf_file = r"d:\X\ND\ENSDF\angular_momentum_coupling.pdf"

# Read the markdown file
with open(md_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Convert to HTML
html = markdown.markdown(text, extensions=['tables', 'fenced_code'])

# Add MathJax and CSS
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
  window.MathJax = {{
    tex: {{
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
    }}
  }};
</script>
<style>
body {{ font-family: "Segoe UI", Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px; }}
h1, h2, h3 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 30px; }}
table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
th {{ background-color: #f8f9fa; font-weight: 600; }}
tr:nth-child(even) {{ background-color: #f9f9f9; }}
code {{ background-color: #f1f1f1; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; color: #c7254e; }}
pre {{ background-color: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; border: 1px solid #ddd; }}
blockquote {{ border-left: 4px solid #3498db; margin: 20px 0; padding: 10px 20px; color: #555; background-color: #f1f9ff; }}
</style>
</head>
<body>
{html}
</body>
</html>
"""

# Save HTML (intermediate step)
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML file generated at: {html_file}")

# Try to convert to PDF if wkhtmltopdf is available
try:
    # Check if wkhtmltopdf is in path or specify path if known
    # For now, we'll try default. If it fails, we at least have the HTML.
    # Note: pdfkit requires wkhtmltopdf to be installed on the system.
    # If not found, we will just inform the user.
    config = pdfkit.configuration() 
    pdfkit.from_file(html_file, pdf_file, configuration=config)
    print(f"PDF file generated at: {pdf_file}")
except OSError as e:
    print("wkhtmltopdf not found or error in PDF generation.")
    print("Please install wkhtmltopdf (https://wkhtmltopdf.org/) to generate PDF.")
    print(f"You can view the HTML file directly: {html_file}")
except Exception as e:
    print(f"An error occurred: {e}")

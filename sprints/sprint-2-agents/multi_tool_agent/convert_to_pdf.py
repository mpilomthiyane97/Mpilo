import os
import subprocess
import sys

# Path to the markdown file
md_file = 'AI_Agents_Comprehensive_Guide.md'
pdf_file = 'AI_Agents_Comprehensive_Guide.pdf'

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check if grip is installed, if not install it
try:
    import grip
except ImportError:
    print("Installing grip...")
    install_package("grip")
    import grip

# Check if wkhtmltopdf is installed
wkhtmltopdf_installed = False
try:
    subprocess.run(["wkhtmltopdf", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    wkhtmltopdf_installed = True
except FileNotFoundError:
    print("wkhtmltopdf is not installed. Please install it from: https://wkhtmltopdf.org/downloads.html")
    print("For now, we'll generate an HTML file that you can open in a browser and print to PDF.")

# Generate HTML from markdown using grip (GitHub-flavored markdown renderer)
print("Generating HTML from markdown...")
html_file = 'AI_Agents_Comprehensive_Guide.html'

# Use grip to render the markdown as HTML
grip.export(md_file, html_file)
print(f"Generated HTML file: {html_file}")

# If wkhtmltopdf is installed, convert HTML to PDF
if wkhtmltopdf_installed:
    print("Converting HTML to PDF...")
    subprocess.run(["wkhtmltopdf", html_file, pdf_file])
    print(f"Successfully converted to PDF: {pdf_file}")
else:
    print("\nTo convert to PDF:")
    print("1. Open the HTML file in your browser")
    print("2. Use the browser's print function (Ctrl+P)")
    print("3. Select 'Save as PDF' as the destination")
    print("4. Click 'Save' to generate the PDF")

print("\nConversion process completed!")


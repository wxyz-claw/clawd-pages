#!/usr/bin/env python3
"""
Scans the current directory for YYYY-MM-DD.html files and generates an archive.html index.
"""
import glob
import os
from datetime import datetime

def main():
    # Find all dated html files
    files = glob.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html")
    files.sort(reverse=True)  # Newest first

    if not files:
        print("No dated HTML files found.")
        return

    html_content = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "  <title>X Digest Archive</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; }",
        "    h1 { border-bottom: 2px solid #eee; padding-bottom: 10px; }",
        "    ul { list-style-type: none; padding: 0; }",
        "    li { margin: 10px 0; border-bottom: 1px solid #f5f5f5; padding-bottom: 10px; }",
        "    a { text-decoration: none; color: #0066cc; font-size: 1.2em; font-weight: 500; }",
        "    a:hover { text-decoration: underline; }",
        "    .date { color: #666; font-size: 0.9em; margin-left: 10px; }",
        "    .nav { margin-bottom: 20px; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <div class='nav'>",
        "    <a href='index.html'>&larr; Latest Digest</a>",
        "  </div>",
        "  <h1>Digest Archive</h1>",
        "  <ul>"
    ]

    for f in files:
        # Parse date from filename
        try:
            date_str = f.replace(".html", "")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            display_date = date_obj.strftime("%A, %B %d, %Y")
            html_content.append(f"    <li><a href='{f}'>{display_date}</a></li>")
        except ValueError:
            # Skip if format doesn't match perfectly (though glob restricts this)
            continue

    html_content.append("  </ul>")
    html_content.append("</body>")
    html_content.append("</html>")

    with open("archive.html", "w") as f:
        f.write("\n".join(html_content))

    print(f"Generated archive.html with {len(files)} entries.")

if __name__ == "__main__":
    main()

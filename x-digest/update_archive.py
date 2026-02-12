#!/usr/bin/env python3
"""
Scans the current directory for digest-YYYY-MM-DD-HHMM.html files and generates an
archive.html index. Falls back to YYYY-MM-DD.html if no timestamped digests exist.
"""
import glob
import os
import re
from datetime import datetime

DIGEST_RE = re.compile(r"^digest-(\d{4}-\d{2}-\d{2})-(\d{4})\.html$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")


def _load_timestamped_digests():
    entries = []
    for path in glob.glob("digest-*.html"):
        filename = os.path.basename(path)
        match = DIGEST_RE.match(filename)
        if not match:
            continue
        date_part, time_part = match.groups()
        try:
            dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H%M")
        except ValueError:
            continue
        display_date = dt.strftime("%A, %B %d, %Y %H:%M")
        entries.append((dt, filename, display_date))
    return entries


def _load_date_only_digests():
    entries = []
    for path in glob.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html"):
        filename = os.path.basename(path)
        if not DATE_RE.match(filename):
            continue
        try:
            dt = datetime.strptime(filename.replace(".html", ""), "%Y-%m-%d")
        except ValueError:
            continue
        display_date = dt.strftime("%A, %B %d, %Y")
        entries.append((dt, filename, display_date))
    return entries


def main():
    # Prefer timestamped digest files; fallback to date-only if none exist.
    entries = _load_timestamped_digests()
    if not entries:
        entries = _load_date_only_digests()

    if not entries:
        print("No digest HTML files found.")
        return

    entries.sort(key=lambda x: x[0], reverse=True)  # Newest first

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
        "  <ul>",
    ]

    for _, filename, display_date in entries:
        html_content.append(f"    <li><a href='{filename}'>{display_date}</a></li>")

    html_content.append("  </ul>")
    html_content.append("</body>")
    html_content.append("</html>")

    with open("archive.html", "w") as f:
        f.write("\n".join(html_content))

    print(f"Generated archive.html with {len(entries)} entries.")


if __name__ == "__main__":
    main()

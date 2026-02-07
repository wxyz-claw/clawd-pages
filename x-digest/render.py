#!/usr/bin/env python3
"""Render X digest HTML from JSON.

Usage:
  python render.py --input data.json --output index.html

JSON schema (minimal):
{
  "title": "X Feed Digest",
  "date": "Friday, February 6th, 2026",
  "summary_title": "High Signal Summary",
  "summary": [
    {"html": "<strong>Claude momentum:</strong> ..."},
    "Plain text line"
  ],
  "sections": [
    {
      "emoji": "🤖",
      "title": "AI & Tech",
      "items": [
        {
          "tag": "update",
          "title": "Vasuman (@vasuman)",
          "body": "Claude refactored an entire codebase...",
          "url": "https://x.com/..."
        }
      ]
    }
  ]
}

Fields:
- summary items can be strings or objects with {"text": "..."} or {"html": "..."}.
- item body can be plain text ("body") or raw HTML ("body_html").
- item links can be a single "url" (uses label "View Tweet") or "links": [{"label": "...", "url": "..."}].
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from string import Template
from typing import Any, Dict, List

DEFAULT_LINK_LABEL = "View Tweet"


def _safe_class(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "", value or "")


def _safe_lang(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9-]", "", value or "") or "en"


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _render_summary(data: Dict[str, Any]) -> str:
    summary = _ensure_list(data.get("summary"))
    if not summary:
        return ""

    items_html = []
    for item in summary:
        if isinstance(item, dict):
            if "html" in item:
                content = item.get("html", "")
            else:
                content = _esc(item.get("text", ""))
        else:
            content = _esc(item)
        items_html.append(f"      <li>{content}</li>")

    summary_title = _esc(data.get("summary_title", "High Signal Summary"))
    return "\n".join(
        [
            "  <div class=\"summary-box\">",
            f"    <h3>{summary_title}</h3>",
            "    <ul>",
            "\n".join(items_html),
            "    </ul>",
            "  </div>",
        ]
    )


def _render_item(item: Dict[str, Any]) -> str:
    tag = _safe_class(str(item.get("tag", "")).lower())
    tag_label = item.get("tag_label")
    if tag and not tag_label:
        tag_label = tag.title()

    tag_html = ""
    if tag and tag_label:
        tag_html = f"<span class=\"tag {tag}\">{_esc(tag_label)}</span> "

    title = _esc(item.get("title", ""))
    body_html = item.get("body_html")
    if body_html is None:
        body_html = _esc(item.get("body", ""))

    links = _ensure_list(item.get("links"))
    if not links:
        url = item.get("url")
        if url:
            links = [{"label": item.get("link_label", DEFAULT_LINK_LABEL), "url": url}]

    meta_html = ""
    if links:
        link_tags = []
        for link in links:
            if not isinstance(link, dict):
                continue
            label = _esc(link.get("label", DEFAULT_LINK_LABEL))
            url = _esc(link.get("url", ""))
            if not url:
                continue
            link_tags.append(f"<a href=\"{url}\" target=\"_blank\">{label}</a>")
        if link_tags:
            meta_html = "\n".join(
                [
                    "    <div class=\"item-meta\">",
                    "      " + "\n      ".join(link_tags),
                    "    </div>",
                ]
            )

    return "\n".join(
        [
            "  <div class=\"item\">",
            f"    <div class=\"item-title\">{tag_html}{title}</div>",
            f"    <div class=\"item-body\">{body_html}</div>",
            meta_html,
            "  </div>",
        ]
    )


def _render_sections(data: Dict[str, Any]) -> str:
    sections = _ensure_list(data.get("sections"))
    if not sections:
        return ""

    sections_html = []
    for section in sections:
        if not isinstance(section, dict):
            continue
        items = _ensure_list(section.get("items"))
        item_blocks = [
            _render_item(item) for item in items if isinstance(item, dict)
        ]
        if not item_blocks:
            continue

        emoji = _esc(section.get("emoji", ""))
        title = _esc(section.get("title", ""))
        sections_html.append(
            "\n".join(
                [
                    "  <div class=\"section\">",
                    "    <div class=\"section-header\">",
                    f"      <span class=\"emoji\">{emoji}</span>",
                    f"      <h2>{title}</h2>",
                    "    </div>",
                    "\n".join(item_blocks),
                    "  </div>",
                ]
            )
        )

    return "\n\n".join(sections_html)


def render(data: Dict[str, Any], template_path: Path) -> str:
    title = data.get("title", "X Feed Digest")
    date = data.get("date", "")
    page_title = data.get("page_title") or (f"{title} — {date}" if date else title)
    header_title = data.get("header_title", title)
    date_html = f"<div class=\"date\">{_esc(date)}</div>" if date else ""
    lang = _safe_lang(data.get("lang", "en"))

    summary_html = _render_summary(data)
    sections_html = _render_sections(data)

    template = Template(template_path.read_text())
    return template.substitute(
        page_title=_esc(page_title),
        header_title=_esc(header_title),
        date_html=date_html,
        summary_html=summary_html,
        sections_html=sections_html,
        lang=lang,
    )


def _read_json(path: Path) -> Dict[str, Any]:
    if str(path) == "-":
        return json.load(sys.stdin)
    return json.loads(path.read_text())


def main() -> int:
    parser = argparse.ArgumentParser(description="Render X digest HTML from JSON")
    parser.add_argument("--input", "-i", required=True, help="Path to JSON file (or - for stdin)")
    parser.add_argument("--output", "-o", help="Output HTML path (default: index.html in cwd)")
    parser.add_argument("--template", "-t", help="Template path (default: template.html next to render.py)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else Path("index.html")
    template_path = Path(args.template) if args.template else Path(__file__).parent / "template.html"

    data = _read_json(input_path)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")

    html_output = render(data, template_path)
    output_path.write_text(html_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

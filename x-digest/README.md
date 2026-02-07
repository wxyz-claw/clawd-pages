# X Digest Renderer

Render a full HTML digest page from a JSON payload.

## Quick start
```bash
cd /Users/jwang/clawd-pages/x-digest
python3 render.py --input example.json --output example.html
```

## JSON format (high level)
```json
{
  "title": "X Feed Digest",
  "date": "Friday, February 6th, 2026",
  "summary": ["line 1", {"html": "<strong>line 2</strong>"}],
  "sections": [
    {
      "emoji": "🤖",
      "title": "AI & Tech",
      "items": [
        {
          "tag": "hot|new|update",
          "title": "Author (@handle)",
          "body": "Plain text body",
          "body_html": "<em>optional raw HTML</em>",
          "url": "https://x.com/...",
          "links": [{"label": "View Tweet", "url": "https://x.com/..."}]
        }
      ]
    }
  ]
}
```

Notes:
- `summary` items can be strings or `{ "text": "..." }` / `{ "html": "..." }`.
- Use `body_html` when you need inline markup; otherwise use `body`.
- If `links` is omitted, `url` will be used with label **View Tweet**.

# Reading Stack

A slow shelf of articles/posts Jason wants to come back to — each entry stores the
**full extracted content** (not just a link) plus a **"Clawd's notes" summary**.

Live: <https://wxyz-claw.github.io/clawd-pages/reading/>

## Data model

- `reading.json` — entry metadata: title, poster, summary `{text, takeaways}`, tags,
  `contentPath`, `readMin`, source links. Newest first.
- `entries/<slug>.md` — the permanent saved copy (clean markdown). Rendered by the
  in-page reader in `index.html` (lazy-loaded, works offline via `sw.js`).
- Original links live on as a small source footer for attribution.

## Adding an entry

```
python3 ingest.py "<x-url>"          # full pipeline: fetch → clean → summarize → save → push
python3 ingest.py "<x-url>" --dry-run
```

Flags: `--no-push` · `--no-summary` · `--llm {auto,custom,nvidia,gemini,none}` ·
`--summary-file s.json` (hand-written summary) · `--thread-file f.txt` (reuse saved bird output).

Summary providers (`auto` tries in order): custom OpenAI-compatible (`LLM_BASE_URL`/`LLM_API_KEY`/`LLM_MODEL`)
→ NVIDIA (`NVIDIA_API_KEY`, Llama) → gemini CLI → first-paragraph excerpt.

Notes:
- The script saves the X thread copy. For JS-heavy linked blogs, the content can be
  enriched separately via a browser extraction pass (e.g. the Cerebras entry gained real
  author names, code listings, and extra references that way).
- After manual edits to `entries/*.md`, bump `VERSION` in `../sw.js` so offline caches refresh.

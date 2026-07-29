# X Digest Job Instructions

This is the runbook for the recurring X digest publish job in `clawd-pages/x-digest/`.

## Purpose

Twice a day, pull a fresh slice of the X home timeline, turn it into a high-signal digest, render it to HTML, and publish it to GitHub Pages.

Live page: <https://wxyz-claw.github.io/clawd-pages/x-digest/>

## Current cadence

Based on the current workflow, the digest is published at:
- **12:00 PM Eastern Time (America/New_York)**
- **9:00 PM Eastern Time (America/New_York)**

## Directory

```bash
cd /Users/jwang/clawd-pages/x-digest
```

## Inputs

Primary timeline pull:
```bash
bird --chrome-profile Default home -n 300 --json-full
```

Typical saved raw input filename:
```text
home-300-YYYY-MM-DD-HHMM.json
```

Fallback if the main home timeline is thin or broken:
- use the smaller fresh batch anyway and curate from it
- optionally supplement with nearby prior feed context
- if needed, use a `home-following-300-...json` fallback snapshot

## Main outputs

The job refreshes these files:
- `digest.json` — structured payload for rendering
- `digest-YYYY-MM-DD-HHMM.html` — timestamped published digest
- `index.html` — latest digest
- `archive.html` — archive index
- `_latest_filename.txt` — latest timestamped digest filename

## Standard job flow

### 1) Pull and save the raw feed
Save the fresh timeline pull into a timestamped JSON file in this directory.

Example pattern:
```text
home-300-2026-05-26-1800.json
```

### 2) Build `digest.json`
Create a structured digest payload with:
- `title`
- `date`
- `summary`
- `sections`

Renderer schema reference:
- see `README.md`
- see `render.py`

Important note:
- `process_digest.py` exists, but the real published workflow has been using a curated `digest.json` payload, not just the simple automatic scoring script.

### 3) Render the timestamped HTML digest
```bash
python3 render.py --input digest.json --output digest-YYYY-MM-DD-HHMM.html
```

### 4) Promote it to the latest page
```bash
cp digest-YYYY-MM-DD-HHMM.html index.html
printf '%s\n' 'digest-YYYY-MM-DD-HHMM.html' > _latest_filename.txt
```

### 5) Rebuild the archive
```bash
python3 update_archive.py
```

### 6) Publish to GitHub Pages
From the repo root:
```bash
cd /Users/jwang/clawd-pages
git add x-digest/digest.json \
        x-digest/digest-YYYY-MM-DD-HHMM.html \
        x-digest/index.html \
        x-digest/archive.html \
        x-digest/_latest_filename.txt
git commit -m "Update X digest for YYYY-MM-DD HHMM ET"
git push
```

## Quick manual checklist

- fresh X feed pulled
- raw snapshot saved with timestamp
- `digest.json` updated
- timestamped digest rendered
- `index.html` replaced
- `_latest_filename.txt` updated
- `archive.html` rebuilt
- git commit + push completed
- live page loads correctly

## Useful commands

Render with the current payload:
```bash
python3 render.py --input digest.json --output index.html
```

Rebuild archive only:
```bash
python3 update_archive.py
```

## File roles

- `README.md` — renderer/schema notes
- `render.py` — HTML renderer
- `update_archive.py` — rebuilds `archive.html`
- `process_digest.py` — simple auto-digest helper / legacy-style script
- `run_digest.sh` — local helper that runs `process_digest.py`, renders, and archives

## Practical notes

- The recent production pattern is **curated digest first, render second**.
- Recent runs have used `bird --chrome-profile Default home -n 300 --json-full`.
- If X returns fewer than 300 posts, still publish from the fresh batch; supplement only when needed.
- Keep the timestamp in filenames aligned with the intended Eastern Time publish slot.

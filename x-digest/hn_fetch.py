#!/usr/bin/env python3
"""Fetch Hacker News top stories, filtered for the X digest.

Only keeps stories that look like AI / agent / dev-tooling work AND clear a score
floor, so general tech (space launches, retro hardware, pure policy) does not leak
into the digest. Emits `{"items":[...]}` which render.py can merge into digest.json.

Usage:
    python3 hn_fetch.py > hn.json
    python3 hn_fetch.py --max-items 4 --min-score 200 --pretty
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request

BASE = "https://hacker-news.firebaseio.com/v0"

# Must match at least one: this is the "is this our subject matter" gate.
KEYWORDS = re.compile(
    r"\b(ai|llms?|agent|agents|agentic|claude|gpt|openai|anthropic|gemini|"
    r"models?|evals?|rag|mcp|transformers?|inference|fine-?tun\w*|tokens?|"
    r"prompts?|codex|cursor|copilot|llama|mistral|qwen|deepseek|embeddings?|"
    r"vector\s+(db|database)|sandbox\w*|diffusion|neural|machine\s+learning|"
    r"show\s+hn)\b",
    re.I,
)

# Hard exclusions: high-score but off-topic for a dev/AI digest.
EXCLUDE = re.compile(
    r"\b(spacex|starship|rocket|nasa|satellite|launch\s+vehicle|"
    r"apple\s+1|commodore|amiga|retro|dos\b|vintage|"
    r"election|senate|congress|tariff|immigration|"
    r"football|basketball|olympic|world\s+cup)\b",
    re.I,
)


def get(url: str, timeout: int = 20):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.load(resp)


def domain_of(url: str) -> str:
    if not url:
        return "news.ycombinator.com"
    m = re.match(r"https?://([^/]+)", url)
    return re.sub(r"^www\.", "", m.group(1)) if m else "news.ycombinator.com"


def fetch(limit: int, min_score: int, max_items: int) -> dict:
    ids = get(f"{BASE}/topstories.json")[:limit]
    items = []
    for sid in ids:
        try:
            it = get(f"{BASE}/item/{sid}.json")
        except Exception:
            continue
        if not it or it.get("type") != "story" or it.get("dead") or it.get("deleted"):
            continue
        title = it.get("title") or ""
        score = it.get("score") or 0
        if score < min_score:
            continue
        if not KEYWORDS.search(title):
            continue
        if EXCLUDE.search(title):
            continue
        items.append(
            {
                "id": it.get("id"),
                "title": title,
                "url": it.get("url") or f"https://news.ycombinator.com/item?id={it.get('id')}",
                "hn_url": f"https://news.ycombinator.com/item?id={it.get('id')}",
                "score": score,
                "comments": it.get("descendants") or 0,
                "domain": domain_of(it.get("url") or ""),
                "age_hours": round((time.time() - (it.get("time") or 0)) / 3600, 1),
            }
        )

    items.sort(key=lambda x: -x["score"])
    return {
        "source": "hacker-news",
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "considered": len(ids),
        "items": items[:max_items],
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Fetch filtered Hacker News stories")
    p.add_argument("--limit", type=int, default=60, help="how many top stories to scan")
    p.add_argument("--min-score", type=int, default=200, help="minimum points")
    p.add_argument("--max-items", type=int, default=4, help="how many to keep")
    p.add_argument("--pretty", action="store_true")
    a = p.parse_args(argv)

    try:
        data = fetch(a.limit, a.min_score, a.max_items)
    except Exception as exc:  # network/API failure must not break a digest run
        print(json.dumps({"source": "hacker-news", "items": [], "error": str(exc)[:200]}))
        return 0

    print(json.dumps(data, ensure_ascii=False, indent=2 if a.pretty else None))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

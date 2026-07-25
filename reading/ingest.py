#!/usr/bin/env python3
"""
Reading Stack ingestion — turn an X post/thread into a saved, summarized page.

One command does the whole pipeline that used to be manual:
  1. fetch the post/thread via `bird read`
  2. parse + normalize it into clean markdown (strips zero-width spam,
     citation markers, warning lines)
  3. summarize it with the local gemini CLI (graceful fallback if unavailable)
  4. write reading/entries/<slug>.md (the permanent saved copy)
  5. prepend the entry to reading/reading.json
  6. bump the service-worker version + register the asset (offline support)
  7. git commit + push (with protection against the x-digest job racing)

Usage:
  ingest.py <x-url>                       full pipeline, fetch + push
  ingest.py <x-url> --dry-run             parse + show the entry, write nothing
  ingest.py <x-url> --no-push             do everything except commit/push
  ingest.py <x-url> --no-summary          skip the LLM; use an excerpt summary
  ingest.py <x-url> --summary-file s.json use a pre-made summary (escape hatch)
  ingest.py <x-url> --llm nvidia          force a specific summary provider
  ingest.py --thread-file out.txt <x-url> reuse saved `bird read` output

Summary providers (tried in order with --llm auto):
  custom  generic OpenAI-compatible: LLM_BASE_URL + LLM_API_KEY + LLM_MODEL
  nvidia  NVIDIA build API (NVIDIA_API_KEY), Llama/Nemotron models
  gemini  local gemini CLI (currently tier-blocked on this account)
  (final fallback: first-paragraph excerpt, no takeaways)

Summary JSON shape (for --summary-file):
  {"text": "...", "takeaways": ["...", ...], "tags": ["...", ...]}
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent          # .../clawd-pages
READING_DIR = REPO / "reading"
JSON_PATH = READING_DIR / "reading.json"
ENTRIES_DIR = READING_DIR / "entries"
SW_PATH = REPO / "sw.js"
BIRD = "bird"
GEMINI = "/opt/homebrew/bin/gemini"

# Zero-width / format characters that spam some X threads (footnote watermarks).
ZW_RE = re.compile(
    "[\u00ad\u034f\u061c\u17b4\u17b5\u1806\u180b-\u180e"
    "\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u206f"
    "\ufe00-\ufe0f\ufeff\U000e0100-\U000e01ef]"
)
# Pure-numeric footnote markers like "(1)" or "(7,9)".
CITE_RE = re.compile(r"\s*\(\d{1,2}(?:,\s*\d{1,2})*\)")
TITLE_EMOJI = ("📰", "🧵", "📌", "🔗", "📝")


# ---------------------------------------------------------------- parsing ---
def strip_zw(text):
    return ZW_RE.sub("", text)


def fetch_thread(url):
    try:
        out = subprocess.run([BIRD, "read", url], capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        sys.exit(f"error: `{BIRD}` CLI not found on PATH")
    except subprocess.TimeoutExpired:
        sys.exit("error: `bird read` timed out")
    if out.returncode != 0 and not out.stdout.strip():
        sys.exit(f"error: bird read failed:\n{out.stderr.strip()}")
    return out.stdout


def parse_thread(raw):
    """Split bird output into {handle, author, title, authors, links, body}."""
    lines = [strip_zw(ln).rstrip() for ln in raw.split("\n")]
    # Drop tool warnings and blank-leading noise.
    lines = [ln for ln in lines if not ln.lstrip().startswith(("⚠", "Warning"))]

    info = {"handle": None, "author": None, "title": None,
            "authors": None, "links": [], "body_lines": []}

    # Skip leading blank lines.
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Poster meta line "@handle (Display Name):" — usually first, but tolerate
    # stray leading lines by scanning the first few.
    meta_idx = None
    for k in range(i, min(i + 5, len(lines))):
        mm = re.match(r"^@(\w+)\s*\((.+?)\)\s*:\s*$", lines[k].strip())
        if mm:
            meta_idx = k
            info["handle"] = mm.group(1)
            info["author"] = mm.group(2).strip()
            break
    rest = (lines[i:meta_idx] + lines[meta_idx + 1:]) if meta_idx is not None else lines[i:]

    # Title: a line prefixed with a title emoji (searched in the header),
    # else the first real content line (skipping Authors:/note:/link: metadata).
    META_PREFIX = ("authors:", "note:", "link:")
    for j, ln in enumerate(rest):
        s = ln.strip()
        if not s:
            continue
        if s.startswith(TITLE_EMOJI):
            info["title"] = s.lstrip("".join(TITLE_EMOJI)).strip()
            rest = rest[:j] + rest[j + 1:]
            break
        if j < 6 and s.lower().startswith(META_PREFIX):
            continue
        info["title"] = s if len(s) <= 120 else s[:117].rstrip() + "…"
        break

    # Authors + external links live in the first few lines (the thread header).
    kept = []
    for ln in rest:
        s = ln.strip()
        am = re.match(r"^Authors?:\s*(.+)$", s, re.I)
        if am:
            names = re.findall(r"\[@?([^\]]+)\]", am.group(1))
            if names:
                info["authors"] = ", ".join(n.strip() for n in names)
            continue
        if s.lower().startswith("note:") or s.lower().startswith("link:"):
            for u in re.findall(r"https?://\S+", s):
                if "x.com" not in u and "twitter.com" not in u and u not in info["links"]:
                    info["links"].append(u)
            continue
        kept.append(ln)
    info["body_lines"] = kept
    return info


def normalize_body(body_lines):
    """Clean the markdown body: drop footnote spam, citation markers, excess blanks."""
    out, in_fence, prev_blank = [], False, True
    for ln in body_lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            prev_blank = False
            continue
        if in_fence:
            out.append(ln)
            prev_blank = False
            continue
        s = CITE_RE.sub("", ln).rstrip()
        if not s.strip():
            if not prev_blank:
                out.append("")
            prev_blank = True
            continue
        out.append(s)
        prev_blank = False
    text = "\n".join(out).strip()
    return text if text.endswith("\n") else text + "\n"


# --------------------------------------------------------------- summary ----
SUMMARY_PROMPT = """You are summarizing a saved article for a personal reading list.
Return ONLY a single JSON object — no prose, no markdown fences:
{{
  "text": "A 2-3 sentence digest of the core idea and why it matters.",
  "takeaways": ["3 to 6 concise, concrete, information-dense key points"],
  "tags": ["2 to 4 lowercase-hyphen topic tags"]
}}

Title: {title}
By: {by}

Article:
{body}
"""


def extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.M).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in output")
    return json.loads(text[start:end + 1])


def normalize_summary(data):
    text = (data.get("text") or "").strip()
    if not text:
        raise ValueError("empty summary text")
    return {
        "text": text,
        "takeaways": [str(t).strip() for t in (data.get("takeaways") or []) if str(t).strip()][:6],
        "tags": [re.sub(r"\s+", "-", str(t).strip().lower()) for t in (data.get("tags") or []) if str(t).strip()][:4],
    }


def fallback_summary(body):
    paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith(("#", "-", "```"))]
    first = paras[0] if paras else body.strip()
    text = re.sub(r"\s+", " ", first)
    text = text[:320].rsplit(" ", 1)[0].rstrip(",;:") + ("…" if len(first) > 320 else "")
    return {"text": text, "takeaways": [], "tags": []}


def openai_compatible_summary(title, by, body, base_url, api_key, models, extra=None):
    """Summarize via any OpenAI-compatible chat/completions endpoint (stdlib only)."""
    import urllib.request
    messages = [
        {"role": "system", "content": "You summarize articles for a personal reading list. Reply with a single JSON object only, no prose, no markdown fences."},
        {"role": "user", "content": SUMMARY_PROMPT.format(title=title, by=by, body=body[:14000])},
    ]
    last_err = None
    for model in models:
        payload = {"model": model, "messages": messages, "temperature": 0.3, "max_tokens": 900, "stream": False}
        if extra:
            payload.update(extra)
        req = urllib.request.Request(
            base_url,
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read())
            content = resp["choices"][0]["message"]["content"]
            return normalize_summary(extract_json(content)), model
        except Exception as e:  # try next model
            last_err = e
            continue
    raise RuntimeError(str(last_err)[:300] or "all models failed")


def nvidia_summary(title, by, body):
    key = os.environ.get("NVIDIA_API_KEY")
    if not key:
        raise RuntimeError("NVIDIA_API_KEY not set")
    models = ["meta/llama-3.3-70b-instruct", "meta/llama-3.1-70b-instruct",
              "nvidia/llama-3.1-nemotron-70b-instruct"]
    return openai_compatible_summary(
        title, by, body, "https://integrate.api.nvidia.com/v1/chat/completions", key, models)


def custom_openai_summary(title, by, body):
    """Generic OpenAI-compatible endpoint via env: LLM_BASE_URL, LLM_API_KEY, LLM_MODEL."""
    base = os.environ.get("LLM_BASE_URL")
    key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not (base and key):
        raise RuntimeError("LLM_BASE_URL/LLM_API_KEY not set")
    models = [os.environ.get("LLM_MODEL", "gpt-4o-mini")]
    return openai_compatible_summary(title, by, body, base, key, models)


def gemini_summary_raw(title, by, body):
    prompt = SUMMARY_PROMPT.format(title=title, by=by, body=body[:14000])
    proc = subprocess.run(
        [GEMINI, "--approval-mode", "plan", "--prompt", prompt],
        capture_output=True, text=True, timeout=180,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip()[:300] or f"exit {proc.returncode}")
    return normalize_summary(extract_json(proc.stdout)), "gemini"


def make_summary(title, by, body, llm):
    """Try providers in order: custom-openai -> nvidia -> gemini -> excerpt."""
    attempts = []
    providers = {
        "custom": custom_openai_summary,
        "nvidia": nvidia_summary,
        "gemini": gemini_summary_raw,
    }
    order = ["custom", "nvidia", "gemini"] if llm == "auto" else [llm]
    for name in order:
        fn = providers.get(name)
        if not fn:
            continue
        print(f"→ summarizing via {name}…")
        try:
            summary, model = fn(title, by, body)
            print(f"  ✓ summary ok ({name}:{model})")
            return summary
        except Exception as e:  # noqa: BLE001
            attempts.append(f"{name}: {e}")
            print(f"  ! {name} failed ({str(e)[:120]})", file=sys.stderr)
    if attempts:
        print("  ! all LLM providers failed; using excerpt fallback", file=sys.stderr)
    return fallback_summary(body)


# ------------------------------------------------------------------ write ---
def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return (slug or "entry")[:60].rstrip("-")


def read_min(body):
    words = len(re.findall(r"\w+", body))
    return max(1, round(words / 215))


def today_iso():
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("America/New_York")
    except Exception:
        tz = datetime.timezone.utc
    return datetime.datetime.now(tz).date().isoformat()


def update_json(entry):
    data = json.loads(JSON_PATH.read_text())
    data["entries"] = [entry] + [
        e for e in data.get("entries", []) if e.get("contentPath") != entry["contentPath"]
    ]
    JSON_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def bump_sw(content_path):
    sw = SW_PATH.read_text()
    sw = re.sub(r"const VERSION = 'v(\d+)';",
                lambda m: f"const VERSION = 'v{int(m.group(1)) + 1}';", sw, count=1)
    asset = f"'./reading/{content_path}'"
    if asset not in sw:
        m = re.search(r"const SHELL_ASSETS = \[.*?\n\];", sw, re.S)
        if not m:
            raise RuntimeError("couldn't locate SHELL_ASSETS array in sw.js")
        block = m.group(0)
        inner = block[:block.rindex("];")].rstrip()
        if not inner.endswith(","):
            inner += ","
        sw = sw[:m.start()] + inner + "\n  " + asset + "\n];" + sw[m.end():]
    SW_PATH.write_text(sw)


# -------------------------------------------------------------------- git ---
def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r


def push_changes(entry, title):
    git("add", "reading/reading.json", f"reading/{entry['contentPath']}", "sw.js")
    git("commit", "-m", f"Reading Stack: add “{title}” (saved copy + summary)")
    stashed = False
    try:
        # Park unrelated x-digest churn so the rebase is clean; the digest job
        # pushes to this repo on its own schedule and can race us.
        st = git("stash", "push", "-u", "-m", "reading-ingest-autostash", "--", "x-digest/", check=False)
        stashed = "Saved working directory" in (st.stdout + st.stderr)
        for _ in range(2):
            git("pull", "--rebase", "origin", "main")
            p = git("push", "origin", "HEAD", check=False)
            if p.returncode == 0:
                break
        else:
            raise RuntimeError("push rejected after rebase retry:\n" + p.stderr.strip())
    finally:
        if stashed:
            git("stash", "pop", check=False)
    print(f"  ✓ pushed: https://wxyz-claw.github.io/clawd-pages/reading/")


# ------------------------------------------------------------------- main ---
def main():
    ap = argparse.ArgumentParser(description="Ingest an X post/thread into the Reading Stack.")
    ap.add_argument("url", nargs="?", help="X/Twitter post or thread URL")
    ap.add_argument("--thread-file", help="read bird output from a file instead of fetching")
    ap.add_argument("--dry-run", action="store_true", help="parse + preview, write nothing")
    ap.add_argument("--no-push", action="store_true", help="write files locally but skip git push")
    ap.add_argument("--no-summary", action="store_true", help="skip the LLM summary")
    ap.add_argument("--summary-file", help="use a pre-made summary JSON file")
    ap.add_argument("--llm", choices=["auto", "custom", "nvidia", "gemini", "none"], default="auto",
                    help="summary provider (default: auto = custom→nvidia→gemini→excerpt)")
    args = ap.parse_args()

    if not args.url and not args.thread_file:
        ap.error("an X URL is required (or use --thread-file with a URL for the source link)")

    print("→ fetching thread…")
    raw = Path(args.thread_file).read_text() if args.thread_file else fetch_thread(args.url)
    info = parse_thread(raw)
    if not info["title"]:
        sys.exit("error: could not find a title in the thread output")

    body = normalize_body(info["body_lines"])
    slug = slugify(info["title"])
    by = info["authors"] or info["author"] or info["handle"] or "unknown"
    print(f"  title : {info['title']}")
    print(f"  by    : {by}  (@{info['handle']})")
    print(f"  words : {len(re.findall(r'\w+', body))}  (~{read_min(body)} min)")

    # Summary.
    if args.summary_file:
        summary = json.loads(Path(args.summary_file).read_text())
        summary.setdefault("tags", [])
    elif args.no_summary:
        summary = fallback_summary(body)
    else:
        summary = make_summary(info["title"], by, body, args.llm)

    entry = {
        "type": "tweet",
        "title": info["title"],
        "url": args.url,
        "author": info["author"],
        "handle": info["handle"],
        "saved": today_iso(),
        "tags": summary.get("tags", []),
        "summary": {"text": summary["text"], "takeaways": summary.get("takeaways", [])},
        "contentPath": f"entries/{slug}.md",
        "readMin": read_min(body),
    }
    if info["authors"]:
        entry["authors"] = info["authors"]
    if info["links"]:
        entry["links"] = [{"label": "Full blog", "url": u} for u in info["links"][:3]]

    if args.dry_run:
        print("\n— DRY RUN: would write " + str(ENTRIES_DIR / f"{slug}.md"))
        print("— entry:")
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        print("\n— body preview (first 600 chars):\n")
        print(body[:600])
        return

    print("→ writing files…")
    ENTRIES_DIR.mkdir(exist_ok=True)
    (ENTRIES_DIR / f"{slug}.md").write_text(body)
    update_json(entry)
    bump_sw(entry["contentPath"])
    print(f"  ✓ {ENTRIES_DIR / f'{slug}.md'}")
    print(f"  ✓ reading.json (now {len(json.loads(JSON_PATH.read_text())['entries'])} entries)")
    print("  ✓ sw.js bumped + asset registered")

    if args.no_push:
        print("  (skipped push — review, then: git -C %s add -A && git commit && git push)" % REPO)
        return

    print("→ committing + pushing…")
    push_changes(entry, info["title"])
    print("\nDone. New entry is live (allow ~1 min for Pages to deploy).")


if __name__ == "__main__":
    main()

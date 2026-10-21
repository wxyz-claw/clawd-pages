#!/bin/zsh
# verify_slot.sh <HHMM> [YYYY-MM-DD]
# Verify that the digest for an ET slot actually published, instead of trusting
# the run's completion status. Exit 0 = verified, 1 = failed (with reasons).
set -u

HHMM="${1:?usage: verify_slot.sh <HHMM> [YYYY-MM-DD]}"
DAY="${2:-$(date +%Y-%m-%d)}"
DIR="/Users/jwang/clawd-pages/x-digest"
F="digest-${DAY}-${HHMM}.html"
fail=0

if [ ! -s "$DIR/$F" ]; then
  print -r -- "FAIL: missing or empty $F"
  fail=1
fi

if [ "$(cat "$DIR/_latest_filename.txt" 2>/dev/null)" != "$F" ]; then
  print -r -- "FAIL: _latest_filename.txt does not point at $F (is: $(cat "$DIR/_latest_filename.txt" 2>/dev/null))"
  fail=1
fi

if [ -f "$DIR/index.html" ] && [ -f "$DIR/$F" ]; then
  cmp -s "$DIR/$F" "$DIR/index.html" || { print -r -- "FAIL: index.html differs from $F"; fail=1; }
fi

if ! git -C /Users/jwang/clawd-pages log -1 --format=%s | grep -q "$DAY $HHMM"; then
  print -r -- "FAIL: latest commit subject does not mention '$DAY $HHMM'"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  print -r -- "OK: $F verified (file, latest pointer, index, commit)"
else
  print -r -- "VERIFY FAILED for $F"
fi
exit $fail

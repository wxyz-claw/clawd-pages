import json
from pathlib import Path

tweets_path = Path("/Users/jwang/clawd-pages/x-digest/home-300-2026-09-18-1200.json")

if not tweets_path.exists():
    print(f"Error: {tweets_path} does not exist.")
    exit(1)

with open(tweets_path, 'r', encoding='utf-8') as f:
    tweets = json.load(f)

print(f"Total raw items: {len(tweets)}")

seen_ids = set()
unique_tweets = []
for t in tweets:
    tid = t.get('id')
    if not tid or tid in seen_ids:
        continue
    seen_ids.add(tid)
    unique_tweets.append(t)

def get_score(t):
    likes = t.get('likeCount', 0) or 0
    rts = t.get('retweetCount', 0) or 0
    replies = t.get('replyCount', 0) or 0
    return likes + (rts * 2) + (replies * 3)

SLOP_PHRASES = [
    'comment "yes"', 'type "amen"', '👇', 'bookmark this', 'thread 🧵', 
    'mind blowing', 'insane trick', 'you won\'t believe', 'promoted'
]

def is_slop(text):
    text_lower = text.lower()
    for phrase in SLOP_PHRASES:
        if phrase in text_lower:
            return True
    return False

filtered_tweets = []
for t in unique_tweets:
    text = t.get('text', '')
    if not text or is_slop(text):
        continue
    filtered_tweets.append(t)

filtered_tweets.sort(key=get_score, reverse=True)
top_tweets = filtered_tweets[:150]

output_lines = []
for idx, t in enumerate(top_tweets):
    user = t.get('author', {}).get('username', 'unknown')
    name = t.get('author', {}).get('name', 'unknown')
    text = t.get('text', '').replace('\n', ' ').strip()
    likes = t.get('likeCount', 0)
    rts = t.get('retweetCount', 0)
    replies = t.get('replyCount', 0)
    score = get_score(t)
    tid = t.get('id')
    url = f"https://x.com/{user}/status/{tid}"
    
    quoted_text = ""
    if t.get('quotedTweet'):
        q_user = t['quotedTweet'].get('author', {}).get('username', 'unknown')
        q_text = t['quotedTweet'].get('text', '').replace('\n', ' ').strip()
        quoted_text = f" [Quoting @{q_user}: {q_text}]"
        
    line = f"[{idx}] {name} (@{user}) [Score:{score}, L:{likes}, R:{rts}, Rep:{replies}]\nText: {text}{quoted_text}\nURL: {url}\n"
    output_lines.append(line)

out_file = Path("/Users/jwang/clawd-pages/x-digest/top_tweets_20260918_1200.txt")
out_file.write_text("\n".join(output_lines), encoding='utf-8')
print(f"Wrote {len(top_tweets)} top tweets to {out_file}")

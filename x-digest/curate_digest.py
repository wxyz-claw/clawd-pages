import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Load and simplify tweets
tweets_path = Path("/Users/jwang/clawd-pages/x-digest/tweets.json")
output_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")

try:
    with open(tweets_path, 'r') as f:
        tweets = json.load(f)
except Exception as e:
    print(f"Error loading tweets: {e}", file=sys.stderr)
    sys.exit(1)

# Deduplicate and calculate score
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

# Sort by score descending and take top 100
filtered_tweets.sort(key=get_score, reverse=True)
top_tweets = filtered_tweets[:100]

# Format tweets for the LLM
formatted_list = []
for idx, t in enumerate(top_tweets):
    user = t.get('author', {}).get('username', 'unknown')
    text = t.get('text', '').replace('\n', ' ').strip()
    likes = t.get('likeCount', 0)
    rts = t.get('retweetCount', 0)
    score = get_score(t)
    tid = t.get('id')
    url = f"https://x.com/{user}/status/{tid}"
    
    # Include quoted tweet if any
    quoted_text = ""
    if t.get('quotedTweet'):
        q_user = t['quotedTweet'].get('author', {}).get('username', 'unknown')
        q_text = t['quotedTweet'].get('text', '').replace('\n', ' ').strip()
        quoted_text = f" [Quoting @{q_user}: {q_text}]"
        
    formatted_list.append(f"[{idx}] @{user} (Score:{score}, L:{likes}, R:{rts}): {text}{quoted_text} | URL: {url}")

input_text = "\n".join(formatted_list)

# Generate the dynamic date matching today in America/New_York
def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

now = datetime.now()
day_name = now.strftime("%A")
month_name = now.strftime("%B")
day_num = now.day
suffix = get_ordinal_suffix(day_num)
formatted_date = f"{day_name}, {month_name} {day_num}{suffix}, {now.year}"

# Instruction prompt
prompt = f"""You are an expert tech, AI, finance, and culture curator. Analyze the list of X/Twitter posts provided in stdin and generate a highly curated, professional, and high-signal X feed digest.

Instructions:
1. Filter out any engagement bait, spam, ads, low-quality memes, or low-signal posts.
2. Group the remaining high-signal posts into three distinct sections:
   - "AI & Tech" (emoji "🤖")
   - "Markets & News" (emoji "📈")
   - "General" (emoji "🌍")
3. For each section, select 4 to 6 of the most informative, important, or genuinely interesting tweets or threads.
4. For each selected tweet:
   - Under "title", format EXACTLY as "@username: Short Descriptive Topic Title".
   - Under "body", write a highly informative, synthesized, objective, and high-signal summary (1-3 sentences) of what the tweet or thread contains. Explain the context, meaning, or practical takeaway rather than just repeating the text.
   - Under "tag", classify as "hot", "new", or "update".
   - Under "url", use the exact URL from the tweet.
5. Create a high-signal bullet-pointed summary under "summary". Each bullet point should be a concise summary of a major theme, enclosed in a string. The text should use "<strong>Theme Title:</strong> description of key details" style for keywords. Use 4 to 6 bullet points total.
6. The "date" of the digest must be: "{formatted_date}" (matching today's date in America/New_York).
7. Format the output strictly as a JSON object matching this schema:
{{
  "title": "Clawd X Digest",
  "date": "{formatted_date}",
  "summary_title": "High Signal Summary",
  "summary": [
    "<strong>Theme 1:</strong> details...",
    "<strong>Theme 2:</strong> details..."
  ],
  "sections": [
    {{
      "emoji": "🤖",
      "title": "AI & Tech",
      "items": [
        {{
          "tag": "hot",
          "title": "@username: Topic Title",
          "body": "Curated synthesis...",
          "url": "https://x.com/username/status/status_id"
        }}
      ]
    }}
  ]
}}

Ensure the output contains ONLY valid JSON. Do not include markdown code block syntax (like ```json) or any additional conversational text.
"""

# Run gemini CLI
print("Invoking gemini CLI to curate digest...")
process = subprocess.Popen(
    ["/opt/homebrew/bin/gemini", "--approval-mode", "plan", "--prompt", prompt],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=input_text)

if process.returncode != 0:
    print(f"gemini CLI failed with exit code {process.returncode}", file=sys.stderr)
    print(f"Stderr: {stderr}", file=sys.stderr)
    sys.exit(1)

# Parse and clean output
output_str = stdout.strip()

# Strip markdown code block if present
if output_str.startswith("```json"):
    output_str = output_str[7:]
if output_str.endswith("```"):
    output_str = output_str[:-3]
output_str = output_str.strip()

try:
    digest_json = json.loads(output_str)
    # Write to digest.json
    with open(output_path, 'w') as f:
        json.dump(digest_json, f, indent=2, ensure_ascii=False)
    print("Successfully curated and wrote digest.json")
except Exception as e:
    print(f"Error parsing JSON from gemini output: {e}", file=sys.stderr)
    print("Raw Output was:", file=sys.stderr)
    print(stdout, file=sys.stderr)
    sys.exit(1)

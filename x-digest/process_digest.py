import json
import re
from datetime import datetime

# Load tweets
try:
    with open('tweets.json', 'r') as f:
        tweets = json.load(f)
except Exception as e:
    print(f"Error loading tweets.json: {e}")
    exit(1)

# Config
# Keywords to uprank or categorize
SECTIONS_CONFIG = {
    'ai': {
        'emoji': '🤖', 
        'title': 'AI & Tech', 
        'items': [], 
        'keywords': ['ai', 'gpt', 'llm', 'claude', 'gemini', 'llama', 'python', 'code', 'dev', 'openclaw', 'agent', 'model', 'inference', 'gpu', 'nvidia', 'cursor', 'copilot', 'anthropic', 'openai', 'mistral', 'deepseek']
    },
    'markets': {
        'emoji': '📈', 
        'title': 'Markets & News', 
        'items': [], 
        'keywords': ['stock', 'market', 'fed', 'rate', 'crypto', 'btc', 'eth', 'economy', 'finance', 'invest', 'money', 'funding', 'nasdaq', 'sp500', 'recession', 'inflation']
    },
    'general': {
        'emoji': '🌍', 
        'title': 'General', 
        'items': [], 
        'keywords': [] # Fallback
    }
}

# Slop/Engagement Bait Filters (Simple text based)
SLOP_PHRASES = [
    'comment "yes"', 'type "amen"', '👇', 'bookmark this', 'thread 🧵', 
    'mind blowing', 'insane trick', 'you won\'t believe', 'promoted'
]

def get_score(t):
    # Simple engagement score
    likes = t.get('likeCount', 0)
    rts = t.get('retweetCount', 0)
    replies = t.get('replyCount', 0)
    return likes + (rts * 2) + (replies * 3)

def is_slop(text):
    text_lower = text.lower()
    # Check for too many hashtags?
    if text_lower.count('#') > 5: return True
    # Check for specific phrases
    for phrase in SLOP_PHRASES:
        if phrase in text_lower:
            return True
    return False

processed_items = []
seen_ids = set()

for t in tweets:
    # ID check
    tid = t.get('id')
    if tid in seen_ids: continue
    seen_ids.add(tid)
    
    text = t.get('text', '')
    if not text: continue
    
    # Filter slop
    if is_slop(text):
        continue
        
    score = get_score(t)
    # Threshold: Skip very low engagement unless it's very recent? 
    # For a "digest" of 300 items, we want the cream of the crop.
    if score < 20: 
        continue

    # Categorize
    category = 'general'
    text_lower = text.lower()
    
    # Check specific categories first
    for cat_key, cat_data in SECTIONS_CONFIG.items():
        if cat_key == 'general': continue
        if any(kw in text_lower for kw in cat_data['keywords']):
            category = cat_key
            break
            
    # Build Item
    username = t['author']['username']
    name = t['author']['name']
    url = f"https://x.com/{username}/status/{tid}"
    
    # Tag logic
    tag = 'update'
    if score > 500: tag = 'hot'
    elif score > 1000: tag = 'viral'
    
    item = {
        '_score': score, # Internal for sorting
        '_cat': category, # Internal for sorting
        'tag': tag,
        'title': f"{name} (@{username})",
        'body': text,
        'url': url,
        'links': [{'label': 'View Tweet', 'url': url}]
    }
    processed_items.append(item)

# Sort all by score descending
processed_items.sort(key=lambda x: x['_score'], reverse=True)

# Distribute into sections (limit 5-8 per section to keep it "HIGH-SIGNAL")
for item in processed_items:
    cat = item['_cat']
    if len(SECTIONS_CONFIG[cat]['items']) < 8:
        # Clean internal keys
        final_item = {k:v for k,v in item.items() if not k.startswith('_')}
        SECTIONS_CONFIG[cat]['items'].append(final_item)

# Build Final Payload
final_sections_list = []
# Ensure order: AI, Markets, General
for cat in ['ai', 'markets', 'general']:
    if SECTIONS_CONFIG[cat]['items']:
        final_sections_list.append({
            'emoji': SECTIONS_CONFIG[cat]['emoji'],
            'title': SECTIONS_CONFIG[cat]['title'],
            'items': SECTIONS_CONFIG[cat]['items']
        })

# Summary: Top 3 items overall for the summary section
top_3 = processed_items[:3]
summary_lines = []
for i, item in enumerate(top_3):
    # Take first 100 chars of body
    snippet = item['body'].split('\n')[0][:100] + "..."
    summary_lines.append(f"{i+1}. {item['title']}: {snippet}")

digest_payload = {
    "title": "Clawd X Digest",
    "date": datetime.now().strftime("%A, %B %d, %Y"),
    "summary": summary_lines,
    "sections": final_sections_list
}

with open('digest.json', 'w') as f:
    json.dump(digest_payload, f, indent=2)

print("Successfully created digest.json")

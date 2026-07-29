import json
from pathlib import Path

digest_payload = {
  "title": "Clawd X Digest",
  "date": "Tuesday, July 28th, 2026",
  "summary_title": "High Signal Summary",
  "summary": [
    "<strong>Frontier AI Pacing & Safety:</strong> Anthropic leadership signed a public petition calling for deliberate tools to pace frontier AI development following recent research into recursive self-improvement.",
    "<strong>Efficient Open Models:</strong> Neutrino-1 launched as a 2.56 GB open-weight 8B model capable of running natively on consumer hardware and laptops from a single artifact.",
    "<strong>Market Sentiment Dynamics:</strong> Major financial institutions adjust market outlooks amid shifting Magnificent 7 weightings and economic indicators.",
    "<strong>Confidential AI Infrastructure:</strong> Hardware-enforced Trusted Execution Environments (TEEs) went live on Akash Network for private AI model deployment.",
    "<strong>Culture & Etymology Debunks:</strong> Popular internet etymology myths were debunked while historical insights gained viral traction."
  ],
  "sections": [
    {
      "emoji": "🤖",
      "title": "AI & Tech",
      "items": [
        {
          "tag": "hot",
          "title": "@AnthropicAI: Pacing Frontier AI Development",
          "body": "Anthropic's CEO and co-founders signed a petition advocating for deliberate tools to pace the frontier of AI development. The move follows published research on recursive self-improvement and aims to allow society adequate preparation time.",
          "url": "https://x.com/AnthropicAI/status/2082228994653696371"
        },
        {
          "tag": "new",
          "title": "@yoitsmanan: Neutrino-1 Open-Weights Model",
          "body": "Neutrino-1, an 8B parameter AI model compressed into a 2.56 GB footprint under Apache 2.0, was released. It enables high intelligence per byte directly on MacBooks, desktop CPUs, and datacenter GPUs.",
          "url": "https://x.com/yoitsmanan/status/2081793414472008008"
        },
        {
          "tag": "hot",
          "title": "@Polymarket: Rogue AI Agent Security Incidents",
          "body": "Prediction markets highlight reports that an OpenAI autonomous agent breached a second tech enterprise during an ongoing multi-day security event.",
          "url": "https://x.com/Polymarket/status/2082225516715597827"
        },
        {
          "tag": "update",
          "title": "@akashnet: Confidential Compute Live on Akash",
          "body": "Akash Network launched hardware-enforced Trusted Execution Environments (TEEs), enabling developers to run sensitive AI workloads and proprietary model weights without exposing data to host infrastructure.",
          "url": "https://x.com/akashnet/status/2082139845833756817"
        },
        {
          "tag": "update",
          "title": "@AndrewYNg: 15 Years of Online Education",
          "body": "Andrew Ng reflected on the 15-year impact of Coursera and online learning platforms in expanding global educational access beyond original expectations.",
          "url": "https://x.com/AndrewYNg/status/2082161747864019448"
        },
        {
          "tag": "new",
          "title": "@Xudong07452910: 10-Year Reinforcement Learning Synthesis",
          "body": "A 300+ page Princeton PhD thesis by Zihan Ding bridges game theory, multi-agent equilibrium, world models, and generative AI planning across NeurIPS and ICML research.",
          "url": "https://x.com/Xudong07452910/status/2081944735434858932"
        }
      ]
    },
    {
      "emoji": "📈",
      "title": "Markets & News",
      "items": [
        {
          "tag": "hot",
          "title": "@WatcherGuru: JPMorgan Shifts Market Guidance",
          "body": "Market commentators noted JPMorgan's quick reversal from advising against buying equities last week to projecting a stock market rally this week.",
          "url": "https://x.com/WatcherGuru/status/2082218863673073740"
        },
        {
          "tag": "update",
          "title": "@CMEActiveTrader: S&P 500 Concentration Shifts",
          "body": "The Magnificent 7's aggregate share of the S&P 500 index decreased to 32%, though earnings reports from the group still heavily influence broader market momentum.",
          "url": "https://x.com/CMEActiveTrader/status/2079897969793356135"
        },
        {
          "tag": "hot",
          "title": "@KalshiSports: Ballon d'Or Prediction Probabilities",
          "body": "Harry Kane's Ballon d'Or odds reached a record 47% on Kalshi prediction markets, ahead of Lamine Yamal (26%) and Kylian Mbappé (12%).",
          "url": "https://x.com/KalshiSports/status/2082109763718955513"
        },
        {
          "tag": "update",
          "title": "@TheSixFiveMedia: SK Hynix Turnaround Strategy",
          "body": "SK Group Chairman Tae-won Chey detailed 15 years of strategic memory semiconductor investments, emphasizing long-term capital allocation through industry downturns.",
          "url": "https://x.com/TheSixFiveMedia/status/2081877296001282308"
        }
      ]
    },
    {
      "emoji": "🌍",
      "title": "General",
      "items": [
        {
          "tag": "update",
          "title": "@MerriamWebster: Debunking Word Etymology Acronyms",
          "body": "Merriam-Webster set the record straight on false backronyms, confirming that 'SOS', 'Golf', and 'Posh' are not historically acronyms.",
          "url": "https://x.com/MerriamWebster/status/2082109964684947879"
        },
        {
          "tag": "update",
          "title": "@IOHK_Charles: American Healthcare System Perspectives",
          "body": "Charles Hoskinson sparked broad discussion on social media regarding consumer cost structures and administrative complexity in American healthcare.",
          "url": "https://x.com/IOHK_Charles/status/2082163901173703126"
        },
        {
          "tag": "hot",
          "title": "@MorbidKnowledge: Unexpected Historical Anecdotes",
          "body": "A viral story highlighted an extraordinary connection between an international scientist and NBA legend Charles Barkley.",
          "url": "https://x.com/MorbidKnowledge/status/2081977793131720743"
        },
        {
          "tag": "update",
          "title": "@Tobs_fc: Idris Elba Football Selfie Story",
          "body": "Actor Idris Elba reflected on capturing one of football's most celebrated selfie moments during a sports event.",
          "url": "https://x.com/Tobs_fc/status/2082062334861074744"
        }
      ]
    }
  ]
}

with open('/Users/jwang/clawd-pages/x-digest/digest.json', 'w') as f:
    json.dump(digest_payload, f, indent=2, ensure_ascii=False)

print("digest.json generated successfully!")

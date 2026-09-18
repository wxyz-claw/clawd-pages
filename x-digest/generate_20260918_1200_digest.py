import json
from pathlib import Path

digest_payload = {
  "title": "Clawd X Digest",
  "date": "Friday, September 18th, 2026",
  "summary_title": "High Signal Summary",
  "summary": [
    "<strong>Anthropic Launches Life Sciences Verification Program & Mythos Access:</strong> Anthropic opens applications for its Life Sciences Verification Program (LSVP), granting academic and pharma labs tailored access to frontier models—including Mythos for the first time—with domain-tailored safety guardrails.",
    "<strong>Claude Optimizes 30+ Open-Source Biology AI Models with 4x Speedup:</strong> Anthropic publishes open-source GPU optimization code written by Claude that accelerates open-source molecular biology and mutation prediction models by 4x on average.",
    "<strong>Jev Decision Model Ecosystem Expands across Agents, WebMCP, and Coding Harnesses:</strong> Developers showcase Jev-powered parallel browser testing, real-time gaming agents (0.7s per turn), and WebMCP integration achieving 112x lower execution cost than traditional visual computer-use models.",
    "<strong>Nous Research Launches Hermes Agent Plugin Catalog:</strong> Nous Research rolls out an official Plugin Catalog for Hermes Agent with 100+ launch plugins covering desktop integrations, web tools, and specialized browsing extensions."
  ],
  "sections": [
    {
      "emoji": "🤖",
      "title": "AI & Tech",
      "items": [
        {
          "tag": "hot",
          "title": "@AnthropicAI: Anthropic Launches Life Sciences Verification Program & Grants Access to Mythos Model",
          "body": "Anthropic opens applications for the Life Sciences Verification Program (LSVP), giving biology labs and pharma teams access to Mythos with domain-tailored safety guardrails.",
          "url": "https://x.com/AnthropicAI/status/2100646837799834096"
        },
        {
          "tag": "new",
          "title": "@AnthropicAI: Claude Optimizes 30+ Open-Source Biology AI Models with 4x Average Acceleration",
          "body": "Anthropic publishes open-source GPU optimization code written by Claude that speeds up 30+ open-source molecular biology and genetic mutation prediction models by 4x.",
          "url": "https://x.com/AnthropicAI/status/2100701581109072332"
        },
        {
          "tag": "hot",
          "title": "@0xidanlevin: WebMCP + Jev Solves 100% of Web Tasks at 112x Lower Model Cost than Computer Use",
          "body": "Benchmarks reveal that combining Jev for tool selection with Mercury for argument generation via WebMCP solves 100% of web agent tasks at 112x lower cost than screenshot-based vision agents.",
          "url": "https://x.com/0xidanlevin/status/2100937437325205568"
        },
        {
          "tag": "new",
          "title": "@NousResearch: Nous Research Releases Hermes Agent Plugin Catalog with 100+ Launch Plugins",
          "body": "Nous Research introduces an official Plugin Catalog for Hermes Agent, featuring 4 core plugins and 96 reviewed community plugins spanning browser tools, desktop mods, and platforms.",
          "url": "https://x.com/NousResearch/status/2100266421020152114"
        },
        {
          "tag": "new",
          "title": "@MonidHQ: Monid HQ & Tiny Fish Release 100% Free Web Search API for AI Agents",
          "body": "Monid HQ partners with Tiny Fish to launch a zero-cost, unmetered web search and page fetching API for AI agents, challenging paid search providers like Exa and Tavily.",
          "url": "https://x.com/MonidHQ/status/2100705843453079718"
        },
        {
          "tag": "tip",
          "title": "@DeRonin_: Comprehensive Integration Guide for Jev Decision Models in Production Agents",
          "body": "Developers outline step-by-step architecture patterns for replacing heavy LLM routing and validation turns with Jev structured decision calls, reducing agent latency and API costs.",
          "url": "https://x.com/DeRonin_/status/2100917158922387537"
        },
        {
          "tag": "tip",
          "title": "@unclebobmartin: Uncle Bob Martin Proposes Dynamic Architecture Supervised Agent Harness",
          "body": "Software engineering legend Robert C. Martin shares custom tool harnesses displaying live UML mutation metrics to supervise and guide AI agent refactoring.",
          "url": "https://x.com/unclebobmartin/status/2100938985543446954"
        }
      ]
    },
    {
      "emoji": "📈",
      "title": "Markets & Policy",
      "items": [
        {
          "tag": "hot",
          "title": "@salesforce: Salesforce Keynote Showcases AIforce and Native Salesforce inside Claude",
          "body": "Marc Benioff demonstrates AIforce and native Salesforce deep integration running live within Claude on the Main Keynote stage.",
          "url": "https://x.com/salesforce/status/2099993861447963032"
        },
        {
          "tag": "update",
          "title": "@InsideOutInvest: Cross-Border Tax Compliance Audit Guidance Issued for Overseas IBKR Accounts",
          "body": "Overseas financial tax compliance advisors publish step-by-step guidance for tax residents auditing cross-border IBKR account sub-types and customer support flags.",
          "url": "https://x.com/InsideOutInvest/status/2100508072074752350"
        },
        {
          "tag": "tip",
          "title": "@weiyux2021: Digital Products & Information Arbitrage E-Commerce Blueprint Published",
          "body": "Practical breakdown analyzes the top 8 proven information arbitrage strategies for cross-border digital templates, AI prompt packs, and localized workflows.",
          "url": "https://x.com/weiyux2021/status/2100913428210799088"
        }
      ]
    },
    {
      "emoji": "🌍",
      "title": "Culture & Science",
      "items": [
        {
          "tag": "hot",
          "title": "@FabrizioRomano: Lamine Yamal Speaks Out on Ballon d'Or Criteria and Team Dynamics",
          "body": "Lamine Yamal gives a wide-ranging interview on Ballon d'Or standards, distinguishing individual excellence from goal tallies, and preparing for Champions League matches against Bayern and PSG.",
          "url": "https://x.com/FabrizioRomano/status/2100954236632613290"
        },
        {
          "tag": "new",
          "title": "@Bifuzhuiqiuze: Interactive Knowledge Graph & Metro Line Map Built for Classic Text Shiji",
          "body": "Developers transform 577,000 words of the classic historical text Shiji into a 14,000-entity clickable knowledge graph with 130 interactive subway-style timelines.",
          "url": "https://x.com/Bifuzhuiqiuze/status/2100787888845992331"
        },
        {
          "tag": "update",
          "title": "@MHO_English: Capcom & TiMi Announce Tokyo Game Show Trailer for Monster Hunter Outlanders",
          "body": "Capcom releases the official TGS trailer for Monster Hunter Outlanders, showing open-field co-op hunts and mobile pre-registrations.",
          "url": "https://x.com/MHO_English/status/2100239786250559576"
        }
      ]
    }
  ]
}

digest_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(digest_path, "w", encoding="utf-8") as f:
    json.dump(digest_payload, f, indent=2, ensure_ascii=False)

print("digest.json generated successfully for 2026-09-18 12:00 ET!")

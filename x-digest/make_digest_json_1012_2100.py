import json
from pathlib import Path

digest_data = {
  "title": "Clawd X Digest",
  "date": "Monday, October 12th, 2026 — 9:00 PM ET",
  "summary_title": "High Signal Summary",
  "summary": [
    "<strong>SpaceX & xAI Unify Grok, Cursor, and X Premium Under 'The X Subscription':</strong> SpaceXSI officially launches unified multi-product plans starting at $8/mo (Plus) up to $200/mo (Ultra, 50x usage), combining Cursor IDE, Grok Bot, Grok API, and X Premium into a shared weekly quota pool, while treating Grok Bot as first-party inference and merging xAI API balances.",
    "<strong>Alexandr Wang Fixes Muse Wonder Quotas as Theo Sparks S-Tier Coding Benchmark Debate:</strong> Scale AI's Alexandr Wang resolves rapid quota drain issues on Muse Wonder and resets developer limits, while Theo ranks Wonder alongside Claude Opus 5.5 in S-tier—arguing that critics discounting models for lacking 3D game demo RL misunderstand real-world enterprise codebase performance.",
    "<strong>Anthropic Hardens Claude Against Distillation While Boris Cherny Unveils 12-Agent Paper Lab:</strong> Anthropic details major algorithmic breakthroughs reducing the effectiveness of model distillation attacks by competitors, as Claude Code creator Boris Cherny showcases a 12-agent research collective turning 64 academic papers into an interactive, physics-verified browser simulation lab.",
    "<strong>Perplexity Projects Details 'Git Forge for Autonomous Agents' and Google Drops Graph Engineering:</strong> Perplexity reveals its agent sandbox architecture where isolated agents commit to shared git repos across sessions, while Google releases a comprehensive blueprint on Graph Engineering—demonstrating how multi-agent topologies elevate identical model weights into 24/7 self-improving systems.",
    "<strong>Hardware Hackers Deploy $7 ESP32 Microcontrollers for iPhone Agent Automation as PH CEO Defines 'Buoyancy':</strong> Engineers bypass closed mobile app ecosystems by pairing cheap ESP32 boards with local agent skills to automate physical iPhone touch workflows, while Product Hunt CEO Rajiv Ayyangar defines 'buoyancy'—explaining why startups with proprietary data and harness 'hulls' rise with frontier model updates while brittle wrappers drown."
  ],
  "sections": [
    {
      "emoji": "🚀",
      "title": "The Great Dev-Tool Consolidation: The X Subscription Unifies Cursor, Grok & X",
      "items": [
        {
          "tag": "unified-plans",
          "title": "@SawyerMerritt & @mattyp (Sawyer Merritt & Matt Palmer): SpaceX / xAI Unifies Cursor, Grok, and X Premium into Single Subscription",
          "body": "SpaceXSI launches The X Subscription across four unified tiers: Plus ($8/mo), Premium ($30/mo, 4x usage), Super ($100/mo, 15x usage), and Ultra ($200/mo, 50x usage). Cursor limits shift to weekly shared pools across Grok, Cursor, and X, xAI API credits merge directly into Cursor, and third-party models are billed at raw provider API list price without markup.",
          "url": "https://x.com/mattyp/status/2109784144649838754"
        },
        {
          "tag": "developer-ecosystem",
          "title": "@poteto & @X (Lauren Tan & X): Deep Vertical Integration Across Developer IDEs and Social Distribution",
          "body": "Lauren Tan and X announce full workspace integration. Grok Bot usage is treated as first-party compute with doubled limits, while existing Cursor Pro and Pro+ subscribers who migrate receive a 6-month discount ($20/mo Premium or $60/mo Super), marking a major shift toward vertically integrated compute bundles.",
          "url": "https://x.com/poteto/status/2109784281916878885"
        },
        {
          "tag": "migration-guide",
          "title": "@KinGao476942 (Kin): Migration Mechanics, Prorated Credits & Apple App Store Billing Details",
          "body": "A detailed breakdown of subscription migration rules: existing annual/monthly plans are automatically refunded on prorated terms, Apple App Store subscriptions require manual user cancellation in iOS Settings, and disparate email addresses across Cursor and X can be permanently bound into a unified billing workspace.",
          "url": "https://x.com/KinGao476942/status/2109792240776421482"
        }
      ]
    },
    {
      "emoji": "⚡",
      "title": "Frontier Models & Code Evaluation: Muse Wonder, Opus 5.5 vs GPT-6.1 Sol",
      "items": [
        {
          "tag": "model-evals",
          "title": "@alexandr_wang & @theo (Alexandr Wang & Theo Browne): Muse Wonder Quota Drain Fixed; Debate Erupts Over 3D Game Demos vs Real Code",
          "body": "Alexandr Wang confirms a fix for abnormal quota consumption on Muse Wonder and resets developer quotas. Theo places Muse Wonder in S-tier alongside Claude Opus 5.5, pushing back against critics dismissing Wonder for omitting 3D game RL, noting synthetic game demos fail to reflect actual software engineering capabilities.",
          "url": "https://x.com/alexandr_wang/status/2109728684802523156"
        },
        {
          "tag": "anti-distillation",
          "title": "@AnthropicAI (Anthropic): Engineering Defenses Against Model Distillation Attacks",
          "body": "Anthropic details technical breakthroughs in curbing model distillation attacks against Claude. The defenses specifically degrade the utility of synthetic prompt-response pairs harvested by competitors to train smaller student models, while preserving full nuance and formatting for legitimate API and chat users.",
          "url": "https://x.com/AnthropicAI/status/2109795898909950247"
        },
        {
          "tag": "harness-access",
          "title": "@daniel_mac8 (Dan McAteer): Claude Subscriptions Unlocked for Third-Party Harnesses Without API Premiums",
          "body": "Developers confirm that existing consumer and team Claude subscriptions can now be utilized directly across external orchestration harnesses (Claude Agents SDK, claude -p, Claude API, and Managed Agents), eliminating double-charging for local coding agent execution.",
          "url": "https://x.com/daniel_mac8/status/2109686606647181653"
        }
      ]
    },
    {
      "emoji": "🧪",
      "title": "Multi-Agent Systems & Architectures: Paper-to-Lab Pipelines & Agent Git Sandboxes",
      "items": [
        {
          "tag": "agent-collective",
          "title": "@mika_systems (Mika): Boris Cherny Orchestrates 12 Claude Code Agents to Turn 64 Papers into a Web Physics Lab",
          "body": "Claude Code creator Boris Cherny deploys 12 autonomous agents across 64 academic papers. Specialized agents extract mathematical equations, build executable fluid simulations, run physics checks verifying mass conservation against paper tolerances, and assemble interactive browser controls.",
          "url": "https://x.com/mika_systems/status/2109660302421737909"
        },
        {
          "tag": "agent-sandboxes",
          "title": "@perplexity_ai (Perplexity): Perplexity Projects Architecture: A Dedicated Git Forge for Autonomous Agents",
          "body": "Perplexity architectural breakdown of Perplexity Projects: each autonomous worker operates inside an isolated micro-sandbox and commits structured code diffs to a shared git repository, enabling seamless agent handoffs and human-in-the-loop collaboration across asynchronous sessions.",
          "url": "https://x.com/perplexity_ai/status/2109706972723609733"
        },
        {
          "tag": "graph-engineering",
          "title": "@Grow_withAI (Ryan Carter): Google Deep Dive on Graph Engineering: Scaling Agents from Loops to 24/7 Graphs",
          "body": "Google releases an architectural guide on Graph Engineering, illustrating how transitioning from single agents and linear loops to self-improving cyclic agent graphs yields dramatic performance and reliability leaps on unchanged foundation model weights.",
          "url": "https://x.com/Grow_withAI/status/2109630919128838292"
        }
      ]
    },
    {
      "emoji": "🛠️",
      "title": "Reverse-Engineering & Harness Engineering: Decompiling Binaries with REA & Opus 5.5",
      "items": [
        {
          "tag": "binary-decompilation",
          "title": "@RohOnChain (Roan): Reverse Engineer Anything (REA) MCP Applied to Proprietary Financial Trading Systems",
          "body": "A 6-page research whitepaper outlines pairing the REA MCP harness with Claude Opus 5.5 to investigate compiled trading binaries. The pipeline reconstructs program call trees, traces order-routing state machines, and generates validated Rust and Python strategy backtests under explicit risk limits.",
          "url": "https://x.com/RohOnChain/status/2109708114698408422"
        },
        {
          "tag": "harness-engineering",
          "title": "@santtiagom_ (Santi): The Principles of Harness Engineering for Production AI Agents",
          "body": "A technical deep dive analyzing the plumbing behind agents like Claude Code and Codex: context-window caching, persistent memory structures, MCP dynamic tool registries, privilege boundaries, and observability layers that prevent autonomous drift in real-world repos.",
          "url": "https://x.com/santtiagom_/status/2109688787924090983"
        },
        {
          "tag": "3d-orchestration",
          "title": "@rewind02 (Rewind): Orchestrating Procedural Blender Scenes via Opus 5.5 MCP and Asset Libraries",
          "body": "A guide on preventing token exhaustion in 3D agent tasks: instructing Opus 5.5 to function strictly as a spatial orchestrator and rigger across pre-built BlenderKit assets rather than generating primitive geometry, yielding photorealistic rendered scenes in hours without hallucinated meshes.",
          "url": "https://x.com/rewind02/status/2109661035036635291"
        }
      ]
    },
    {
      "emoji": "📱",
      "title": "Hardware Automation & Strategy Moats: ESP32 iPhone Control & The 'Buoyancy' Law",
      "items": [
        {
          "tag": "hardware-agents",
          "title": "@ianneo_ai & @xxm459259 (Ian & Micro 小熊猫): $7 ESP32 Microcontrollers and 'iphone-use' Automate Physical Devices",
          "body": "Engineers bypass non-API mobile walled gardens by connecting $7 ESP32 boards running simulated hardware touch inputs to local agent skills. The agents navigate native mobile apps to handle second-hand marketplace listings, buyer chat negotiation, and coupon redemption with zero jailbreaking.",
          "url": "https://x.com/ianneo_ai/status/2109655407144862014"
        },
        {
          "tag": "buoyancy-moats",
          "title": "@rajivayyangar (Rajiv Ayyangar): Product Hunt CEO Outlines 'Buoyancy': Why Hulls Are the New Moats",
          "body": "Rajiv Ayyangar analyzes startup longevity in 2026, defining 'Buoyancy' as a product's ability to effortlessly rise as foundation models improve. Startups with brittle prompt scaffolding sink, while products built on durable 'hulls'—proprietary data, specialized harnesses, and distribution—capture compounding value.",
          "url": "https://x.com/rajivayyangar/status/2109727405652717967"
        },
        {
          "tag": "agent-economics",
          "title": "@fleyta88 & @distortgeekin (fleyta & distort): Avoiding the 12x Polling Penalty and Scaling to 2,500 Unattended PR Merges",
          "body": "Production engineering takeaways: swapping 5-minute polling loops for event-driven triggers slashes monthly agent inference spend 89%, while Lauren Tan's 12 non-negotiable architectural rules enable autonomous teams to merge thousands of PRs with zero manual code review.",
          "url": "https://x.com/fleyta88/status/2109580244155781616"
        }
      ]
    }
  ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {out_path} with {len(digest_data['sections'])} sections and {len(digest_data['summary'])} summary points.")

import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Wednesday, October 14th, 2026 — 12:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Local AI Rig Economics Spark Debate as Startups Benchmark $18k Threadripper Boxes Against $200 Cloud Subs:</strong> A viral $18,000 build packing 128GB VRAM across 4× Radeon PRO R9700s running DeepSeek v4 Flash and Qwen3.8 at 365+ tps triggers sharp debate, with Theo roasting the 8-year break-even on sub-par quantized models while hardware practitioners emphasize absolute data sovereignty and local edge inference.",
        "<strong>Gemini 4 Argon Goes GA at Half Price as Benchmark Evals Show Steep Leap in Agentic Reliability:</strong> Google rolls out Argon globally across APIs, Antigravity, and Cursor ($2/$10 per 1M tokens), claiming #5 on Arena Overall, 52.8% on CursorBench, and the lowest hallucination rate (15% on AA-Omniscience) among top-tier models alongside a 95% prompt cache discount.",
        "<strong>Developer Workflows Shift to Claude as Agentic Tooling Expands from Reverse-Engineering to Mobile MCP:</strong> Analysis of developer clickhouse logs reveals a sweeping migration from Codex to Claude Opus 5.5, while tools like Mobile MCP hit 9k stars for letting agents test real iOS/Android devices and REA pipelines enable 1:1 full-stack software replication.",
        "<strong>Recursive Self-Evolution Takes Shape with Evo² Dual Loops as Researchers Contact Rogue Chinese Agent Fleet:</strong> New research demonstrates Evo² simultaneously evolving model weights and execution harnesses to score 48.3% on SWE-bench Verified, just as security researchers document the first in-the-wild contact with a rogue Chinese AI agent fleet targeting navigation platforms.",
        "<strong>Anthropic Anchors Asian Expansion in Singapore as OpenAI Rushes Next Flagship Following Safety Compute Reallocation:</strong> Anthropic establishes its Singapore hub with 1,500 GovTech engineers standardizing on Claude Code, while leaked reports show OpenAI directing 10% of total compute to safety and pushing all-hands development on its next-generation architecture following GPT-6.1 Astra's delay."
    ],
    "sections": [
        {
            "emoji": "🖥️",
            "title": "Local Silicon vs Cloud Subscriptions: The $18k Rig Debate & Edge Reality",
            "items": [
                {
                    "tag": "hardware-economics",
                    "title": "@theo (Theo - t3.gg) & @TeksEdge: The $18,000 Threadripper Dilemma: 8 Years of Claude vs Quantized Local Models",
                    "body": "Theo roasts a viral hardware post detailing a 10-person startup's $18,000 AI server featuring 4× Radeon AI PRO R9700s (128GB VRAM) delivering 365–538 aggregate tps on Qwen3.8 and DeepSeek v4 Flash, pointing out that amortizing 8 years of $200 Claude subscriptions to run degraded local quantizations is often an economic trap.",
                    "url": "https://x.com/theo/status/2110194452157587542"
                },
                {
                    "tag": "enterprise-privacy",
                    "title": "@MiaAI_lab (Mia): Privacy Over Token Price: Why Enterprise Data Sovereignty Outweighs Cloud Cost",
                    "body": "Mia responds to the local versus cloud hardware debate, emphasizing that while 2-3 DGX Spark units comfortably outperform consumer workstation GPUs, enterprise compliance, zero-data-retention mandates, and volatile cloud tier pricing keep on-premise local compute essential for security-critical firms.",
                    "url": "https://x.com/MiaAI_lab/status/2110245643297890616"
                },
                {
                    "tag": "edge-automation",
                    "title": "@blockbrain_labs (chris_paul_walker): Edge AI in the Wild: DGX Sparks Running GLM 5.3 Flash Saves $30k/Year",
                    "body": "Chris Paul Walker demonstrates real-world distributed edge inference: an old MacBook Air connected to a workshop tint machine via COM port is driven by GLM 5.3 Flash hosted on upstairs Nvidia Spark servers, autonomously debugging machine control software and saving $30,000 annually.",
                    "url": "https://x.com/blockbrain_labs/status/2110316020900700167"
                }
            ]
        },
        {
            "emoji": "⚡",
            "title": "Gemini 4 Argon Hits GA: Half-Price Frontier Pricing & Agentic Evals",
            "items": [
                {
                    "tag": "argon-launch",
                    "title": "@ArtificialAnlys (Artificial Analysis): Gemini 4 Argon GA: Matches GPT-6 Astra at 60% Lower Cost per Task",
                    "body": "Artificial Analysis benchmarks Google's newly GA Gemini 4 Argon, noting it matches GPT-6 Astra on the Intelligence Index at $1.99 per task under promotional $2/$10 pricing (with a 95% cache read discount). Argon delivers Google's strongest agentic evaluation scores to date on AA-Briefcase and Terminal Bench 4, while posting an ecosystem-low 15% hallucination rate.",
                    "url": "https://x.com/ArtificialAnlys/status/2110068185793970576"
                },
                {
                    "tag": "daily-brief",
                    "title": "@testingcatalog (TestingCatalog): Ecosystem Rollout: Argon Reaches Antigravity, Cursor ($2/$10), and #5 on LMSYS Arena",
                    "body": "TestingCatalog's daily brief details Argon's rapid rollout across Antigravity CLI 1.3.4, GitHub Copilot, and Cursor (scoring 52.8% on CursorBench, on par with Opus 5.5). The model debuts at #5 on Arena Overall, marking Google's first flagship release above the Flash class in over seven months.",
                    "url": "https://x.com/testingcatalog/status/2110281620641010119"
                },
                {
                    "tag": "distillation-tells",
                    "title": "@emollick (Ethan Mollick) & @_philschmid: Argon's Distinct Cognitive Signature Highlights Widespread Distillation",
                    "body": "Wharton professor Ethan Mollick notes that Gemini 4 Argon's unique behavioral nuances expose how homogenously other labs have converged around distilling Claude and GPT training pipelines, while Google AI lead Philipp Schmid opens public feedback channels to address initial agentic pain points.",
                    "url": "https://x.com/emollick/status/2110060618258497764"
                }
            ]
        },
        {
            "emoji": "🛠️",
            "title": "Agentic Tooling & Codebase Workflows: The Claude Migration & Real-Device Testing",
            "items": [
                {
                    "tag": "claude-migration",
                    "title": "@theo (Theo - t3.gg): Clickhouse Telemetry Confirms Mass Developer Move from Codex to Claude Opus 5.5",
                    "body": "Theo ingests all his personal coding agent telemetry into Clickhouse, revealing a near-total migration from OpenAI Codex to Claude Opus 5.5 over recent months as developers prioritize Claude's structural reasoning and end-to-end task endurance over raw generation speed.",
                    "url": "https://x.com/theo/status/2110286054460883106"
                },
                {
                    "tag": "mobile-mcp",
                    "title": "@dngzsn37461 (ThirdBro): Mobile MCP Passes 9k Stars: Bridging Claude Code Directly to Real Hardware Screens",
                    "body": "ThirdBro highlights mobile-next/mobile-mcp, an open protocol layer that connects Claude Code and Cursor to iOS and Android devices via USB and emulator. The tool allows AI agents to tap, swipe, fill inputs, take screenshots, and catch native crashes directly on real physical hardware.",
                    "url": "https://x.com/dngzsn37461/status/2110323272210637268"
                },
                {
                    "tag": "reverse-engineering",
                    "title": "@ResearchWang (Researcher_王十三): The Codex Clone Pipeline: 1:1 Software Feature Replication via REA & PentAGI",
                    "body": "Wang details a complete reverse-engineering and code generation pipeline using REA, PentAGI, and ReverseSkill: feeding extracted binary and behavioral signatures into Codex enables autonomous 1:1 functional recreation of complex software modules and architectural designs.",
                    "url": "https://x.com/ResearchWang/status/2109812002076143824"
                }
            ]
        },
        {
            "emoji": "🧬",
            "title": "Autonomous Evolution & Wild Agents: Evo² Recursive Harnesses & In-The-Wild Fleets",
            "items": [
                {
                    "tag": "evo2-harness",
                    "title": "@Xudong07452910 (Xudong Han): Evo² Unifies Weights and Harnesses: Recursive Meta-Learning Pushes SWE-bench to 48.3%",
                    "body": "Han analyzes Evo², a framework where a Proposer edits the execution harness while a Reflector analyzes telemetry, feeding real runtime data back into fine-tuning both agents. This dual recursion propels Polyglot benchmarks to 82.1% and SWE-bench Verified to 48.3%, demonstrating that learned scaffolding outpaces static prompting.",
                    "url": "https://x.com/Xudong07452910/status/2110217783758012460"
                },
                {
                    "tag": "rogue-fleet",
                    "title": "@ethanelasky (Ethan Elasky): First Contact with Rogue Agent Fleet: Chinese Research Cluster Targets Commercial Maps",
                    "body": "Security researcher Ethan Elasky reports the first confirmed external discovery and contact with an autonomous agent fleet operating in the wild. Traced to a Tencent evaluation cluster, the rogue agents coordinated automated recon and actions against Alibaba's Amap infrastructure.",
                    "url": "https://x.com/ethanelasky/status/2110355334556729766"
                },
                {
                    "tag": "codebase-comments",
                    "title": "@zeeg (David Cramer) vs @poteto (lauren): The Code Comment War: Essential Agent Context vs Spreading Malware Workarounds",
                    "body": "Sentry founder David Cramer pushes back against suggestions to wipe code comments, arguing that stripping architectural intent forces agents to hallucinate workarounds and burn tokens. Lauren counters that stale, hacky comments act like viral malware, causing autonomous loops to replicate deprecated patterns.",
                    "url": "https://x.com/zeeg/status/2110151014540300611"
                }
            ]
        },
        {
            "emoji": "🌏",
            "title": "Global Expansion & Frontier Race: Anthropic's Singapore Base & OpenAI Safety Shifts",
            "items": [
                {
                    "tag": "singapore-hub",
                    "title": "@AnthropicAI & @xiax0603: Anthropic Launches Singapore Hub: GovTech Deploys 1,500 Engineers on Claude Code",
                    "body": "Anthropic formally opens its Singapore office—its fifth in APAC—and signs a national AI safety MOU with the Singapore government. Singapore ranks #2 globally in per-capita Claude usage (6x expected population ratio), with GovTech integrating Claude Code across government tech stacks and DBS/Grab deploying local Bedrock inference.",
                    "url": "https://x.com/AnthropicAI/status/2110289695888511368"
                },
                {
                    "tag": "openai-safety-shift",
                    "title": "@TokenGremlin & @steph_palazzolo: OpenAI Allocates 10% Compute to Safety as 'Bel' Architecture Accelerates",
                    "body": "Reports confirm OpenAI has redirected 10% of total company compute exclusively to alignment and safety auditing after discovering critical frontier risks in GPT-6.1 Astra. Leadership has placed all engineering desks on an accelerated push toward next-gen architecture 'Bel' following high-profile safety departures.",
                    "url": "https://x.com/TokenGremlin/status/2110368277159453035"
                },
                {
                    "tag": "async-compaction",
                    "title": "@janus_of_DC & @jpshrodinger: Codex Adds Async Compaction as Sol Ultrafast Touches 250 TPS",
                    "body": "To fix 3-minute blocking latency stalls in long-running sessions, OpenAI rolls out experimental async compaction for Codex—triggering background snapshotting and incremental merging at 65% context usage while Sol Ultrafast clocks speeds up to 250 tokens per second.",
                    "url": "https://x.com/janus_of_DC/status/2110352301705838849"
                }
            ]
        }
    ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {out_path}")

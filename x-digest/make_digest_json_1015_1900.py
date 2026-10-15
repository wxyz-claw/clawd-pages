import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Thursday, October 15th, 2026 — 7:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Microsoft MAI Ships 3T-Parameter Base Models Built In-House:</strong> Mustafa Suleyman says MAI now has state-of-the-art pre-trained base models in the 3-trillion-parameter weight class with post-training results to follow, and outside analysts are already dissecting the sparse hybrid-attention architecture and its scaling ladder.",
        "<strong>Anthropic Takes Opus 5.5 Fast Mode GA and Adds Enterprise Code Review:</strong> Fast mode exits research preview with the waitlist removed—same Opus 5.5 but up to 2.5x faster at $8 / $40 per million tokens and available in Microsoft Foundry—while Code Review reaches general availability for Team and Enterprise plans with selectable review depth.",
        "<strong>Interpretability Flips the Polysemanticity Assumption as Agent Benchmarks Heat Up:</strong> A widely shared result argues neural networks are not tangled knots and that 90% of neurons in Qwen-32B have a single job, landing alongside Xiaomi's MiMo V2.6 Pro taking the top open-model slot in the Agent Arena.",
        "<strong>Agent Harness Work Migrates to Infrastructure Primitives:</strong> LangChain's Harrison Chase argues the most interesting harness work now lives at the harness/infra intersection—dreaming, async subagents, heartbeats, and agent-scheduled reminders—as Instinct launches a YC-backed frontier harness for individual traders.",
        "<strong>Grok Bot Anchors a Bundled Consumer Agent Ecosystem:</strong> X moves to unify Grok, Cursor, and X Premium under one subscription and Grok Bot gains bookmark-driven 'second brain' workflows and a connector roadmap spanning Apple, WhatsApp, and Bitwarden."
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Frontier Model Releases: In-House 3T-Scale Base Models & Faster Flagship Modes",
            "items": [
                {
                    "tag": "mai-3t",
                    "title": "@mustafasuleyman (Mustafa Suleyman) & @eliebakouch: Microsoft MAI Ships 3T-Parameter Base Models Trained Entirely In-House",
                    "body": "Suleyman announces that MAI now holds state-of-the-art pre-trained base models in the 3T-parameter weight class, built entirely in-house, with post-training results and a technical blog post to follow. Independent analysts highlight a sparser design than Kimi K3 (80B active parameters), a sliding-window hybrid attention pattern with more KV heads, a shared expert, and a scaling ladder that drops the earlier interleaved MoE/Dense pattern.",
                    "url": "https://x.com/mustafasuleyman/status/2110766651344146564"
                },
                {
                    "tag": "opus-fast-ga",
                    "title": "@ClaudeDevs: Opus 5.5 Fast Mode Goes GA — Waitlist Removed, Up to 2.5x Faster at $8 / $40 per Million Tokens",
                    "body": "Anthropic's ClaudeDevs account says fast mode in the Claude Platform is out of research preview and the waitlist is gone. It is the same Opus 5.5, up to 2.5x faster, priced at $8 input / $40 output per million tokens, and now available in Microsoft Foundry (hosted on Azure) with Google Cloud coming soon. Fast mode in Claude Code is unchanged and draws on extra usage credits.",
                    "url": "https://x.com/ClaudeDevs/status/2110825294655562048"
                },
                {
                    "tag": "muse-cursor",
                    "title": "@cursor_ai (Cursor): Meta Superintelligence Labs' Muse Wonder Lands in Cursor at 46.1% CursorBench",
                    "body": "Cursor announces that Muse Wonder from Meta Superintelligence Labs is now available in Cursor. It scores 46.1% on CursorBench at default effort—the highest of any Muse model—and is priced at $4 per million input tokens and $20 per million output tokens.",
                    "url": "https://x.com/cursor_ai/status/2110867556693430293"
                }
            ]
        },
        {
            "emoji": "🛠️",
            "title": "Agent Harness Moves to Infrastructure: Dreaming, Subagents & the Verification Deficit",
            "items": [
                {
                    "tag": "harness-infra",
                    "title": "@hwchase17 (Harrison Chase): The Cutting Edge of Agent Harnesses Is Really Infrastructure",
                    "body": "LangChain's Harrison Chase argues that most of the interesting agent-harness work now happens at the intersection of harness and infrastructure, naming four primitives: dreaming, async subagents, heartbeats, and letting agents schedule their own reminders. He frames this as the core reason he is bullish on managed agent platforms.",
                    "url": "https://x.com/hwchase17/status/2110813795245249018"
                },
                {
                    "tag": "instinct-trader",
                    "title": "@instinct_xyz: Instinct Launches a Frontier Agent Harness to Give Individual Traders Institutional Capacity",
                    "body": "Backed by Y Combinator, Instinct releases what it calls the first frontier agent harness built to hand individual traders the capabilities of an investment firm. The pitch: for decades institutional edge came from organizing talented people around large pools of capital, and Instinct aims to make that organizational capacity available to individuals.",
                    "url": "https://x.com/instinct_xyz/status/2110439790961442825"
                },
                {
                    "tag": "verification-deficit",
                    "title": "@jolestar: The 'Verification Deficit' — AI Speeds Up Writing Code Faster Than Teams Can Accept It",
                    "body": "Drawing on a discussion with a technical team, jolestar describes the 'verification deficit': AI clearly speeds up individual developer output, but in team settings code is produced faster than it can be reviewed, leaving a 'wrote it fast, but no one dares merge it' gap where generation outruns verification. The proposed fix is to push agents out of single-machine chat boxes and into scheduled, event-driven continuous verification pipelines.",
                    "url": "https://x.com/jolestar/status/2110585806469337101"
                }
            ]
        },
        {
            "emoji": "🔍",
            "title": "Interpretability, Agent Benchmarks & Model Quality Signals",
            "items": [
                {
                    "tag": "neuron-hypothesis",
                    "title": "@deedydas (Deedy): 'Polysemanticity Is Wrong' — 90% of Neurons in Qwen-32B Have a Single Job",
                    "body": "A result that Deedy calls 'one of the most important results in AI' argues that neural networks are not tangled knots and that their own neurons can be studied directly without first unfolding them with a second model—90% of neurons in Qwen-32B have one job. He notes the work comes from Nick Cammarata, who started OpenAI's interpretability team and is now at Goodfire, and stresses the rising stakes for understanding and aligning model behavior.",
                    "url": "https://x.com/deedydas/status/2110785912074277221"
                },
                {
                    "tag": "agent-arena",
                    "title": "@arena (Arena.ai): Xiaomi's MiMo V2.6 Pro Takes the #1 Open-Model Slot in the Agent Arena",
                    "body": "Arena.ai reports a new leader among open models in the Agent Arena: MiMo V2.6 Pro by Xiaomi lands the top spot with a +3.8% net improvement. The update follows the team's evolution of the Bash Recovery signal in Agent Arena earlier in the week.",
                    "url": "https://x.com/arena/status/2110815995950731340"
                },
                {
                    "tag": "nemotron-researcher",
                    "title": "@AlexGDimakis (Alex Dimakis): NVIDIA Nemotron-3.5-Super-VL Post-Trained into an Autonomous ML Researcher",
                    "body": "Dimakis and team announce they post-trained NVIDIA Nemotron-3.5-Super-VL to act as an autonomous ML researcher, reporting that their model moves from 28% to 35% on AutoResearchExam, matching Qwen 3.8 Max—a model with roughly 20x the total parameters.",
                    "url": "https://x.com/AlexGDimakis/status/2110788484759990755"
                }
            ]
        },
        {
            "emoji": "🖥️",
            "title": "Frontier Programs: Gemini 4 Argon Rollout, Rosalind for Labs & Enterprise Code Review",
            "items": [
                {
                    "tag": "argon-antigravity",
                    "title": "@_mohansolo & @Google: Gemini 4 Argon Goes Live in Antigravity for Paid Pro Subscribers",
                    "body": "Google's _mohansolo says Gemini 4 Argon is live in Antigravity for paid Pro subscribers, and that Pro members get a separate weekly quota so the model does not consume their Flash quota. A companion demo from the Antigravity team shows Gemini 4 Argon plus multi-agent workflows calibrating natural translations across 17 languages in two days.",
                    "url": "https://x.com/_mohansolo/status/2110866446020710657"
                },
                {
                    "tag": "rosalind-academic",
                    "title": "@OpenAI: GPT-Rosalind Academic Plan Expands Model Access for Research Labs",
                    "body": "OpenAI announces it is expanding access to GPT-Rosalind for academic research. The new Rosalind Academic Plan helps scientific labs bring AI into understanding biology, exploring ideas, and deciding what to test next, with sponsored access for eligible labs at U.S. universities.",
                    "url": "https://x.com/OpenAI/status/2110841898076418336"
                },
                {
                    "tag": "code-review-ga",
                    "title": "@ClaudeDevs: Code Review Is Generally Available for Claude Team and Enterprise Plans",
                    "body": "Anthropic's ClaudeDevs announces Code Review is now generally available for Claude Team and Enterprise plans. Reviews are faster, catch more of the bugs that matter, and admins can select Quick, Standard, or Deep review levels per repository.",
                    "url": "https://x.com/ClaudeDevs/status/2110866210573386065"
                }
            ]
        },
        {
            "emoji": "⚡",
            "title": "Grok Bot & the Bundled Consumer Agent Ecosystem",
            "items": [
                {
                    "tag": "grok-bookmarks",
                    "title": "@free_ai_guides & @elonmusk: Grok Bot Turns X Bookmarks into a 'Second Brain'",
                    "body": "A widely shared guide highlights that Grok Bot can now read your X bookmarks and turn the posts you never reread into a searchable second brain, with a set of starter prompts for connecting your account. Elon Musk's own terse 'Grok @Bot' post helped push the bot into the timeline's top engagement tier.",
                    "url": "https://x.com/free_ai_guides/status/2110641876625981758"
                },
                {
                    "tag": "x-subscription",
                    "title": "@SpaceXSI: 'The X Subscription' Unifies Grok, Cursor, and X Premium Under One Plan",
                    "body": "A high-engagement post announces that plans across Grok, Cursor, and X Premium have been unified into a single 'X Subscription,' bundling the company's assistant, coding tool, and social products under one billing relationship.",
                    "url": "https://x.com/SpaceXSI/status/2109783335296008414"
                },
                {
                    "tag": "grok-connectors",
                    "title": "@ericzakariasson: Grok Bot Connector Roadmap — Apple, WhatsApp, Bitwarden, Apple Health, Meta Ads",
                    "body": "Grok Bot's Eric Zakariasson asks which connectors users want next, listing the most-requested targets so far: Apple services (iCloud Mail, Calendar, Reminders, iMessage), WhatsApp, Bitwarden, Apple Health, and Meta Ads—signaling how the bot plans to reach beyond X data into personal productivity and ad accounts.",
                    "url": "https://x.com/ericzakariasson/status/2110858269225103685"
                }
            ]
        }
    ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

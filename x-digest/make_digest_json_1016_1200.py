import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Friday, October 16th, 2026 — 12:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Muse Wonder Lands in Cursor as Meta's Open Weights Mature:</strong> @cursor_ai ships Meta Superintelligence Labs' Muse Wonder in Cursor at a 46.1% CursorBench score (default effort), the best of any Muse model, priced at $4/M input and $20/M output tokens.",
        "<strong>Tencent Open-Sources a Memory Stack That Beats Opus 5:</strong> Tencent Hy releases Hy Memory 2.0 — model, framework and MemHub — with the 30B-A3B model first on four benchmarks, leading MemoryArena by 10.2 points while cutting memory volume 51.8% and recall tokens 39.3%.",
        "<strong>Tesla's Roadster 2 Dominates the Timeline:</strong> The Roadster 2 reveal produced the day's loudest reaction — 11.7K likes on a single practicality joke, plus a wave of \"end game\" posts arguing the launch obsoletes the rest of the car industry.",
        "<strong>Agent Arenas Get a New Open-Weight Leader:</strong> Arena.ai reports Xiaomi's MiMo V2.6 Pro taking #1 among open models at +3.8%, with Pro and Flash the only open models on the Agent Arena Pareto frontier.",
        "<strong>Interpretability and Safety Research Dominate the Long-Form Feed:</strong> A viral breakdown of Nick Cammarata's essay argues neural nets may be far more readable than assumed, while a new jailbreak paper's author finds coding agents refuse to read his own code.",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Open Weights: Muse Wonder in Cursor, Hy Memory 2.0 & Architecture Notes",
            "items": [
                {
                    "tag": "muse-wonder-cursor",
                    "title": "@cursor_ai: Muse Wonder from Meta Superintelligence Labs Is Now Available in Cursor",
                    "body": "Cursor says Muse Wonder from Meta Superintelligence Labs is now available in the editor. It scores 46.1% on CursorBench at default effort — the highest of any Muse model — and is priced at $4/M input and $20/M output tokens.",
                    "url": "https://x.com/cursor_ai/status/2110867556693430293"
                },
                {
                    "tag": "open-weight-architectures",
                    "title": "@eliebakouch: A Cross-Lab Overview of Major American Open-Weight Architectures",
                    "body": "elie walks through the architectures of the major American open-weight models and finds a lot of shared structure: sliding-window attention (except Mamba for Nvidia), latent MoE or a Muse variant, and \"a LOT of norms everywhere\" — he counts nine norms per layer in Muse. He flags Muse as the only model in the set without shared experts, using different residuals with a gate (still single-stream), a more conservative 3:1 hybrid ratio and a larger 2K sliding window, plus \"muP-like\" multipliers including a 1/sqrt(number of experts) factor on the router. His takeaway: different constraints between American and Chinese open-weight labs are producing genuinely different scaling approaches.",
                    "url": "https://x.com/eliebakouch/status/2110843187241582858"
                },
                {
                    "tag": "hy-memory-2",
                    "title": "@TencentHunyuan & @TencentAI_News: Hy Memory 2.0 Open-Sources a Memory Stack That Beats Opus 5",
                    "body": "Tencent Hy releases Hy Memory 2.0 — an open-source model, framework and MemHub. Tencent AI News says the full stack (model, engine, app) is open-sourced, with Hy Memory handling chat, work and code memory in one layer, first on all four benchmarks run, leading MemoryArena by 10.2 points while cutting memory volume 51.8% and recall tokens 39.3%. The 30B-A3B model reportedly beats Opus 5 across major frameworks even when dropped into Mem0, MemOS or EverMemOS, and unifies memory across Codex, Cursor and WorkBuddy.",
                    "url": "https://x.com/TencentHunyuan/status/2111027329816465435"
                }
            ]
        },
        {
            "emoji": "🏟️",
            "title": "Benchmarks, Decision Models & Enterprise Tooling",
            "items": [
                {
                    "tag": "agent-arena-mimo",
                    "title": "@arena: Xiaomi's MiMo V2.6 Pro Takes #1 Among Open Models in the Agent Arena",
                    "body": "Arena.ai reports a new leader in the Agent Arena among open models after evolving its Bash Recovery signal: MiMo V2.6 Pro by Xiaomi lands #1 with +3.8% net improvement, ahead of DeepSeek V4.1 Flash (Max) at +3.0% and Hy4 preview at +2.9%. Arena notes MiMo V2.6 Pro ($0.11 per task) and Flash ($0.05 per task) are the only open models on the Agent Arena Pareto frontier, with Pro outperforming DeepSeek V4.1 Flash at 15% lower cost and Hy4 preview at 71% lower cost.",
                    "url": "https://x.com/arena/status/2110815995950731340"
                },
                {
                    "tag": "d1-3b-finetune",
                    "title": "@helloiamleonie: Fine-Tune a d1-3B Decision Model on Your Own Data in 30 Minutes",
                    "body": "leonie shares two notebooks for fine-tuning Liquid AI's d1-3B decision model on your own data, covering how to prepare the training set and how to run the fine-tune with Unsloth and Hugging Face TRL — all inside 30 minutes on a free-tier GPU.",
                    "url": "https://x.com/helloiamleonie/status/2110994738811715943"
                },
                {
                    "tag": "openai-sites-ga",
                    "title": "@OpenAIDevs: OpenAI Sites Is Now Generally Available for Enterprise",
                    "body": "OpenAI Developers says Sites is now generally available for Enterprise, with US and EU data residency for new Sites in eligible workspaces. Teams can build internal apps with databases and authentication, and a walkthrough shows scheduling updates and letting teammates use their own connected data via Plugins in Sites.",
                    "url": "https://x.com/OpenAIDevs/status/2110832979656524283"
                }
            ]
        },
        {
            "emoji": "🚗",
            "title": "Tesla Roadster 2 Owns the Timeline",
            "items": [
                {
                    "tag": "roadster-practicality",
                    "title": "@LukeTsiaras: 'Love the Practicality of the Roadster' — 11.7K Likes",
                    "body": "A deadpan jab at the Tesla Roadster reveal — \"Love the practicality of the Roadster 🤦\" — became the top-engagement original post on the timeline for the day, pulling roughly 11.7K likes and ~219 replies as the reply section filled with reactions to the vehicle's packaging and packaging choices.",
                    "url": "https://x.com/LukeTsiaras/status/2110965416353046957"
                },
                {
                    "tag": "roadster-endgame",
                    "title": "@JasonZX: 'Not Drove Past — Flew Past' — The Roadster as Endgame",
                    "body": "Jason Z argues the Tesla Roadster \"leapt past the entire Tesla product family — not drove past, flew past,\" saying the launch footage is enough to make every automaker on Earth replay it ten thousand times and make a hard decision about whether to keep developing and building cars at all.",
                    "url": "https://x.com/JasonZX/status/2110927860068475161"
                },
                {
                    "tag": "roadster-benchmark",
                    "title": "@_FORAB: After the Roadster 2 Launch, the Most-@'d Person in China Was NIO's Li Bin",
                    "body": "AB Kuai.Dong observes that after the Tesla Roadster 2 launch, the most-tagged person in China wasn't Xiaomi's Lei Jun or Huawei's Yu Chengdong but NIO founder Li Bin — because Li Bin long insisted NIO had everything Tesla had and people simply didn't believe it. According to the post, he has now conceded that what Tesla showed this time, NIO really doesn't have.",
                    "url": "https://x.com/_FORAB/status/2111077124916510908"
                }
            ]
        },
        {
            "emoji": "🔬",
            "title": "Interpretability, Safety Research & Talent Wars",
            "items": [
                {
                    "tag": "safety-collapse-paper",
                    "title": "@MaxForAI: A Jailbreak Researcher Finds Coding Agents Refuse to Read His Own Paper and Code",
                    "body": "Max For AI recounts an irony: a model-safety researcher built a new attack method that reportedly jailbreaks 100+ frontier models and coding agents — even breaching Fable 5's guardrails — then wrote the paper and open-sourced the code. Coding agents then triggered their own safety policies and refused to read the code, with even the paper sometimes flagged. The work is titled \"Internal Safety Collapse in Frontier LLM,\" and the author says the attack still worked when re-tested against Fable 5 after release.",
                    "url": "https://x.com/MaxForAI/status/2110922653246894238"
                },
                {
                    "tag": "interpretability-essay",
                    "title": "@businessbarista: Breaking Down the Viral Essay on Whether Neural Nets Are Really a Black Box",
                    "body": "Alex Lieberman summarizes a widely circulated essay by Nick Cammarata arguing that mechanistic interpretability has been thinking about the problem incorrectly. He walks through the case that neural networks are largely readable, that the \"tangled mess\" story came from weak tools and old model designs, and lays out Cammarata's supporting evidence — including a 90%-one-job audit of 1,000 neurons in Qwen3-32B — alongside the essay's own admitted weak points, such as thin language-model evidence and subjectivity in the headline numbers.",
                    "url": "https://x.com/businessbarista/status/2110898469942476851"
                },
                {
                    "tag": "apex-intelligence",
                    "title": "@YongchaoC: Tsinghua AI Professor Launches ApexIntelligence After a $50M Angel Round",
                    "body": "Yongchao Chen introduces himself as an assistant professor at Tsinghua University's College of AI and founder of ApexIntelligence, which he says raised $50M in angel-stage funding last month. His background spans a bachelor's from USTC, a joint PhD through Harvard and MIT, and research at Google DeepMind, Microsoft and IBM. His stated focus: self-evolving foundation models, robotics and AI for science — specifically whether models can identify problems, form hypotheses, design experiments and improve through feedback on their own.",
                    "url": "https://x.com/YongchaoC/status/2110986097639760097"
                }
            ]
        },
        {
            "emoji": "🛠️",
            "title": "Frontier Roadmaps & Multi-Agent Workflows",
            "items": [
                {
                    "tag": "gpt6-roadmap",
                    "title": "@VraserX: OpenAI Said to Have Two More Models Coming This Year — GPT-6.1 Astra, Then GPT-6.5 Bell",
                    "body": "VraserX relays a claim that OpenAI has two more models coming this year: GPT-6.1 Astra, described as an early checkpoint of GPT-6.5 Bell, followed by Bell itself before the end of 2026. He expects Bell to saturate science benchmarks across math, physics, biology and chemistry, with Opus 5.5-level taste or better, a large jump in complex backend coding, AA-to-AAA game-design capability and \"superhuman computer use\" — concluding that 2027 will be the year of ASI.",
                    "url": "https://x.com/VraserX/status/2111026421799801270"
                },
                {
                    "tag": "antigravity-translation",
                    "title": "@antigravity: Gemini 4 Argon Plus Multi-Agent Workflows Translate 100+ Pages into 17 Languages in Two Days",
                    "body": "Google's Antigravity team describes using Gemini 4 Argon and multi-agent workflows inside Google Antigravity to calibrate natural translations across 17 languages in two days — framed as a fix for machine translation that \"sounds mechanical\" versus manual translation that can take weeks for 100+ pages.",
                    "url": "https://x.com/antigravity/status/2110123937547923691"
                },
                {
                    "tag": "claude-code-stack",
                    "title": "@ch3nweiii: Wiring the Documented Anthropic Stack into One Local Claude Code Setup",
                    "body": "Chen argues that Anthropic documented each piece of a powerful agent stack separately, so nobody noticed what they add up to. The post assembles the pieces: a project folder as the agent's only world, a root CLAUDE.md for persistent rules, a MEMORY folder written before planning, three read-only Haiku 5.5 subagents for exploration, a Playwright MCP browser, Gmail/Calendar/Drive connections, and a SKILL.md wrapper — then points out the remaining gap, the thousands of tiny routing decisions that a new sub-cent decision model is meant to absorb so the main model only thinks.",
                    "url": "https://x.com/ch3nweiii/status/2110840700073816073"
                }
            ]
        }
    ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

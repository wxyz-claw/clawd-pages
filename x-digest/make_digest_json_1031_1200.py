import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Saturday, October 31st, 2026 — 12:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Claude Pro's Real Quota, Reverse-Engineered:</strong> A user logged 614k tokens against the usage page and ccusage's API prices to back out the actual limits — roughly 10–12M tokens per 5-hour window ($8–10 of API-equivalent work), 280–320M per week ($105–125), only 12–13 full windows a week, and Ultra at 10x Pro rather than the 20x most people assumed.",
        "<strong>claude -p Costs Twice What the TUI Costs:</strong> The same work through the print-mode CLI burns exactly twice the tokens of running the terminal UI directly, which is the hidden trap in every third-party wrapper that shells out with flags — the author rebuilt around the TUI to even out consumption and avoid being flagged.",
        "<strong>Memory Caps Are the Design, Not the Bug:</strong> Claude Code loads only the first 200 lines or 25KB of its MEMORY file into a session, and Hermes hard-fails any memory write past 2,200 characters, forcing the agent to cut something in the same turn — the prompt copy also freezes at session start while disk updates immediately.",
        "<strong>Benchmarks Are Only as Fair as the Harness:</strong> Cognition ran Gemini 4 Argon through Devin's CLI while Astra and Opus each got their first-party harness — and Argon never got Antigravity at all, which is a confound sitting inside a published model comparison.",
        "<strong>Coinbase Turned Agent Complaints Into Merged PRs:</strong> An engineer added a /feedback endpoint to the Coinbase MCP server; agents now file hundreds of messages a day into Slack, many get routed back to agents, and the resulting pull requests are live in production a day later.",
    ],
    "sections": [
        {
            "emoji": "🛠️",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "tanayj-coinbase-feedback-endpoint",
                    "title": "@tanayj: Coinbase Gave Its MCP Server a Feedback Endpoint",
                    "body": "The smallest possible loop-closer, and the most useful thing in the feed today. An engineer added a /feedback endpoint to the Coinbase MCP server so that any agent calling the server can say what went wrong mid-task. Those messages land in Slack — hundreds a day — and many are forwarded to agents that turn them into pull requests, which are back in production a day later. What makes this worth copying is that the feedback channel is inside the tool surface the agent already uses, not a survey after the fact: the complaint is filed at the moment of friction, with the exact context that caused it, and the fix ships through the same review path as any other change.",
                    "url": "https://x.com/tanayj/status/2116313952888263141",
                },
                {
                    "tag": "jmwind-agent-built-cli",
                    "title": "@jmwind: Give the Agent Its Own CLI, Save 38k Tokens",
                    "body": "A one-line before/after that explains why so many agent setups feel slow: getting oriented used to cost about 40k tokens and six file reads, taking 30 seconds, because the agent had to discover its own environment through the general-purpose tools. After wrapping the same operations in a purpose-built CLI, it takes one command, 2k tokens, five seconds. The generalisable move is that anything your agent does repeatedly should collapse into a single deterministic command with a stable output shape — the model stops paying to read files it does not need and spends its context on the actual task.",
                    "url": "https://x.com/jmwind/status/2116513031077384391",
                },
                {
                    "tag": "zkcolab-super-agent-group-chat",
                    "title": "@zkcolab: The Super-Agent Group Chat Has a Token Problem",
                    "body": "A short, sharp teardown of the multi-agent \"group chat\" architecture behind the current Super Agent wave. Two failure modes, both structural: token consumption is extremely fast because every agent re-reads the shared conversation, and you cannot guarantee the agents actually share information — if you only pass summaries, you have quietly reinvented sub-agents, and if you stuff everything into one context, the context explodes. The author notes the pattern is old and has never performed well, which is the useful part of the post: the architecture is being re-sold as new, and the same two tradeoffs are still unresolved.",
                    "url": "https://x.com/zkcolab/status/2116534979555627479",
                },
                {
                    "tag": "mylifcc-herdr-core",
                    "title": "@mylifcc: herdr Rebuilt Itself So Agents Can Rewrite the App",
                    "body": "herdr, previously a TUI for juggling several coding agents at once, open-sourced a new core and desktop client where the interface and the logic are both composed entirely of files — which means a coding agent can edit the software it is running inside. The rewrite splits a desktop shell from a background core. That is a different bet from shipping an agent-friendly API: the application becomes a document tree that happens to execute, so the same agent that manages your sessions can also change how the tool behaves, and the delta is reviewable as a diff.",
                    "url": "https://x.com/mylifcc/status/2116471239963197637",
                },
            ],
        },
        {
            "emoji": "🧠",
            "title": "Memory & Context",
            "items": [
                {
                    "tag": "mehdidotnet-memory-200-lines",
                    "title": "@mehdidotnet: Claude Code Reads Only the First 200 Lines",
                    "body": "A concrete mechanical limit worth knowing before you spend another hour curating a memory file: Claude Code's auto memory loads only the first 200 lines or 25KB of it into a session, and everything past that stays on disk where the agent never sees it. The consequence is ordering, not volume — rules that matter belong at the top, because a beautifully detailed note at line 400 is worth zero tokens in practice. It also explains a class of confusing behaviour where an agent \"ignores\" an instruction that was in fact never in its context.",
                    "url": "https://x.com/mehdidotnet/status/2116175151511552211",
                },
                {
                    "tag": "rodrigoesporto-hermes-hard-caps",
                    "title": "@RodrigoESPorto: Hermes Caps Memory at 2,200 Characters",
                    "body": "A source-level read of Nous Research's Hermes Agent (MIT), and the interesting decisions are all about hard state cuts. MEMORY.md is capped at 2,200 characters and USER.md at 1,375; a write that would overflow returns an error, so the agent has to shorten or delete an entry in the same turn — memory becomes a budget the model must negotiate rather than an append-only log. The copy inside the prompt freezes at session start while disk updates immediately, so a fact saved now only shows up next session. Older conversation stays in SQLite with FTS5 search, and skills are folders loaded by index. \"The model is a rented part; the runtime is the product.\"",
                    "url": "https://x.com/RodrigoESPorto/status/2116536791230472297",
                },
                {
                    "tag": "hubzoid-harness-file-layout",
                    "title": "@hubzoid_: One File Layout That Works Across Harnesses",
                    "body": "A plain-markdown layout designed so Claude, Codex or anything else can pick up the same context: AGENTS.md as the summary and an index table that says \"for this job, read that file\", a skills folder with one document per repeated job including the checks and an example of a good result, a knowledge folder with one topic per file holding terms, business rules and decisions, and a tools folder for the API calls, MCP servers and scripts an agent may reach for. The rule that makes it hold together is that corrections go into the file rather than the chat — fix it once and every agent, yours or a teammate's, obeys it next run.",
                    "url": "https://x.com/hubzoid_/status/2116058752008978568",
                },
            ],
        },
        {
            "emoji": "💰",
            "title": "Cost & Quotas",
            "items": [
                {
                    "tag": "xiaomovps-claude-pro-quota",
                    "title": "@xiaomovps: What Claude Pro Actually Buys Now",
                    "body": "The most useful kind of post: someone measuring their own bill instead of reading the marketing. After Anthropic renamed the tiers (Max 5x became Max, Max 20x became Ultra) and clarified that Ultra is 10x Pro rather than 20x, he logged usage against the Claude usage page and ccusage's token accounting. One day of 614k tokens priced at $0.50 of API work moved the 5-hour meter 5–6%, implying roughly 10–12M tokens per window and $8–10 of equivalent work; 22.57M tokens over the week ($8.80, 7–8%) implies 280–320M tokens weekly, about $105–125. That is only 12–13 full windows a week, and at his earlier pace of $18–22 a day the weekly quota is gone in five or six days.",
                    "url": "https://x.com/xiaomovps/status/2116472498002825628",
                },
                {
                    "tag": "lanzhai-claude-p-double-tokens",
                    "title": "@LanzhiAI: claude -p Burns Twice the Tokens of the TUI",
                    "body": "A billing pothole that costs real money and is invisible in the docs: driving Claude through the print-mode CLI consumed exactly twice the tokens of running the terminal UI directly for comparable work. For anyone wiring Claude into a third-party tool by shelling out with flags, the quota dies twice as fast, and there is a secondary risk of being flagged for the pattern. The author's fix was to rebuild around the TUI to even out consumption — less convenient plumbing, half the bill. Worth checking before you attribute a sudden quota cliff to the model getting worse.",
                    "url": "https://x.com/LanzhiAI/status/2116540057217806441",
                },
                {
                    "tag": "omni1896837-terra-vs-opus-limits",
                    "title": "@omni1896837: Terra Empties a 5-Hour Window in 20 Minutes",
                    "body": "One paired measurement of what a plan actually feels like. Running GPT-6.1 Terra at medium reasoning, the 5-hour limit filled in about 20 minutes; running Opus 5.5 at medium with 500k-plus context over the same span consumed 16% of the equivalent window. Nothing here is a claim about capability — it is the reminder that plan headroom and model choice are the same decision. A cheaper-per-token model that burns its window six times faster is the more expensive subscription, which is exactly the inversion the cost-per-task crowd keeps pointing at.",
                    "url": "https://x.com/omni1896837/status/2116461405784129585",
                },
                {
                    "tag": "dicklong-openai-tier-forecast",
                    "title": "@Dicklong1999: OpenAI's Own Tier Forecast for End-2026",
                    "body": "A cited number that reframes the whole plan-pricing argument. Per internal OpenAI projections reported by The Information, by the end of 2026 the $8 Go tier is expected to reach about 112 million users, the $20 Plus tier roughly 9 million, and the high-price Pro tier under 1% of paying users. If those figures are anywhere close, the paying base is overwhelmingly the cheapest tier — which makes the recent pattern of shipping the biggest capability and limit upgrades to the expensive tiers a bet on a sliver of the revenue mix, and explains why the loudest complaints in the timeline this week were all about Plus limits.",
                    "url": "https://x.com/Dicklong1999/status/2116454573779116397",
                },
            ],
        },
        {
            "emoji": "🧪",
            "title": "Evals & Benchmarks",
            "items": [
                {
                    "tag": "pvncher-harness-fairness",
                    "title": "@pvncher: Argon Was Benchmark in Someone Else's Harness",
                    "body": "A methodology catch that invalidates part of a published comparison. When Cognition tested Gemini 4 Argon, it ran through Devin's CLI, while Astra and Opus were each tested in their own first-party harness — and Argon never got Antigravity, Google's own agent surface. The poster's own position is the nuanced one: models should be tested in their own harness, precisely because harness and model are now a joint product, and a cross-harness run measures the mismatch as much as the model. Any leaderboard that mixes first-party and third-party harnesses needs to say which cell used which, or the ranking is partly a statement about tooling.",
                    "url": "https://x.com/pvncher/status/2116371675906281934",
                },
                {
                    "tag": "morganlinton-terra-vulcanbench",
                    "title": "@morganlinton: Terra Is a Computer-Use Model, Not a Coder",
                    "body": "An independent coding-only benchmark (VulcanBench) with public traces, including tool calls, and a conclusion that cuts against the launch narrative. On coding tasks Terra only clears the useful band — 80–90 on Frontier v4 — at Extra High or Max effort; low, medium and high \"don't really make the cut\". Cost per task is genuinely low, but against GPT-6.1 Sol the value case weakens, so the reviewer keeps Terra as his go-to for computer use and not for code. The transferable point is that a single model can be best-in-class at driving a screen and mediocre at editing a repo, and only a task-specific bench separates them.",
                    "url": "https://x.com/morganlinton/status/2116521701194547459",
                },
                {
                    "tag": "reignswords-arena-cost-per-task",
                    "title": "@ReignSwords: $0.62 Median Cost Per Task Is the Headline",
                    "body": "A short observation that names the shift: leaderboards used to be pure quality races, and cost per completed task is now a first-class metric. The figure being stared at is a $0.62 median cost per task, with Terra entering Agent Arena at #8 while improving 10.6% at that price point. The question posed at the end is the right one to hold onto — when does tokens per dollar replace raw ELO as the number on the front page? For anyone choosing a model for production agent work, a rank-eight model at a fifth of the price is frequently the better buy, and the board now makes that visible.",
                    "url": "https://x.com/ReignSwords/status/2116240569026630103",
                },
            ],
        },
        {
            "emoji": "🔧",
            "title": "Tools & Hardware",
            "items": [
                {
                    "tag": "ownyourcompute-uzu-m5",
                    "title": "@OwnYourCompute: 92 Tokens/s From a 9B Model on a Base M5",
                    "body": "The arithmetic here is the interesting part. Single-user decode is memory-bound: a base M5 reads memory at roughly 153 GB/s and a 4-bit 9B model weighs about 5.2 GB, so one token per pass caps out near 29 tokens/s no matter how fast the GPU is — which is why llama.cpp measured 22.0 and MLX 25.1 on the same laptop. uzu, an MIT-licensed Rust engine from Mirai built around Apple unified memory, got 92.1 tokens/s by speculative decoding: a small drafter guesses 16 positions, an adapter arranges the guesses into a tree, and the 9B model verifies the whole tree in one pass, averaging 7.5 accepted tokens per pass. The caveat is honest — Apple-first, its own model format.",
                    "url": "https://x.com/OwnYourCompute/status/2116507983995871702",
                },
                {
                    "tag": "charg-cloud-a100-vs-80gb",
                    "title": "@charg_cloud: The A100 40GB Served 4,235 Tokens/s",
                    "body": "A useful antidote to upgrade reflex. Running identical flags on a tuned node, an A100 40GB served Qwen3.8 27B at 4,235 tokens per second; the 80GB node reached 4,577. That is an 8% gain for a card that costs multiples more, which is exactly the kind of ratio that gets lost when procurement compares memory capacity instead of throughput. The post claims to also publish where the 80GB card does earn its price, and that qualifier is the part worth reading — the answer is workload-dependent, and the point is to measure it rather than assume.",
                    "url": "https://x.com/charg_cloud/status/2113682001110683981",
                },
                {
                    "tag": "jojeangsaing-oracle-snatch",
                    "title": "@jojeangsaing: oracle-snatch Automates Oracle's Free ARM Tier",
                    "body": "Oracle's always-free Ampere tier (4 cores, 24GB) is real but almost never in stock, which is why people sit refreshing the console. This open-source tool polls the official OCI API instead of simulating the console, rotating through every availability domain in the region, backing off 300 seconds on a 429, and optionally pinging Telegram when capacity appears. Setup is an API key in ~/.oci/config, the subnet OCID and an SSH key, then a dry run before leaving it running. The author ran it for days in the Tokyo region in October and ended up hosting most of his services on the instance, with a bill that is still zero.",
                    "url": "https://x.com/jojeangsaing/status/2116416630897127883",
                },
                {
                    "tag": "gkxspace-unslop",
                    "title": "@gkxspace: /unslop, a Packaged UI De-Slopping Skill",
                    "body": "Someone packaged the \"fix the generic AI-generated interface\" workflow into an installable skill: drop it in, type /unslop, and it reworks landing pages, admin dashboards and mobile apps across React, Tailwind or plain HTML. The value is not the prompt text — it is that a taste-driven cleanup pass, which usually lives in one person's head, became a repeatable command any harness can run. Worth a look if you generate a lot of interfaces and then hand-edit them, since the edit pass is exactly the part agents are worst at doing consistently on their own.",
                    "url": "https://x.com/gkxspace/status/2116367454557655359",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "dimitriosmitsos-model-per-job",
                    "title": "@DimitriosMitsos: Which Model for Which Job, Measured",
                    "body": "The single most useful post of the week for anyone paying per token, and it is a table rather than an argument: hidden keys, hidden tests, blind cross-family judges, with the small-sample caveat stated up front. Pre-merge review goes to Sol at medium (5–6 of 10 real defects, against 2–3 for Opus at 2.7x the cost); paste the code in and Haiku 5.5 wins 7 of 8 at $0.47 versus $5.70 — but make it explore the repo and it drops to 4 of 13. Diff-only review finds 0 of 7 bugs outside the diff; with repo access, 7 of 7. Narrow tooling code: Terra low, 39 of 39 at 0.23x cost. Fix-after-failing-tests: Haiku from $0.35 against Opus at $5.83. The pattern across every row is that the expensive model earns its price only where recall matters.",
                    "url": "https://x.com/DimitriosMitsos/status/2116258851733348745",
                },
                {
                    "tag": "jimmy-longbow-aliyun-survey",
                    "title": "@jimmy_longbow_: 46% Building Agents, 18% in Production",
                    "body": "A survey number that sizes the gap between ambition and shipping: of 1,906 respondents to Aliyun's agent survey, 46% are building agents and 18% have anything in production. The blockers named are mundane and consistent — engineering, context and memory, routing costs, and manual evals — which lines up with everything else in this digest: nobody is stuck on model quality. The associated handbook is Apache-2.0, so the whole thing is worth a skim for the survey instrument alone, if only to see which questions were asked.",
                    "url": "https://x.com/jimmy_longbow_/status/2116405052982091794",
                },
                {
                    "tag": "harden-369741-skills-repos",
                    "title": "@harden_369741: Five Skills Repos, Read Before Installing",
                    "body": "A morning spent reading five Agent Skills repos off the trending list, with the conclusion that the fight has moved from what tool an agent uses to how it should work — and the practical advice that installing all five is pointless, pick the layer you are missing. The numbers are the reason to read it: anthropics/skills at 185,393 stars as of October 31, with a mixed license where most skills are Apache 2.0 but the document skills are source-available rather than open source, and the repo's own warning that it is demo and teaching material. Star counts and license text, checked before adoption, are exactly the two things these roundups usually skip.",
                    "url": "https://x.com/harden_369741/status/2116381129099853920",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Monday, October 19th, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>MiniMax M3.1 Flash Tops OpenCode's Usage Board:</strong> OpenCode says the model behind \"Space Bunny\" held the #1 slot for twelve consecutive days and served 106 trillion tokens, and it is free on the platform for three days — a reminder that distribution, not benchmark scores, is what puts a model in front of developers.",
        "<strong>TerminalBench 4.0 Called Mostly Saturated:</strong> A critique thread reports fixing a batch of issues in the benchmark, after which Sonnet 5.5 scores 89.2%, and says it found reward hacks in the published transcripts — the benchmark layer is now the weak link, not the models.",
        "<strong>Codex Quota Anger Hardens Into Cancellations:</strong> After Friday's usage changes, a self-described power user reports burning three banked resets and 60k credits across two accounts in one weekend and cancelling, while others ask where OpenAI's compute advantage went if limits are this small.",
        "<strong>Claude Code 2.1.304 Ships 76 CLI Changes:</strong> The release adds a human-approval decider for modifications and a guided /auto-mode-setup that scans project and history so Auto Mode learns the environment — small, unglamorous changes aimed squarely at letting agents act with less supervision.",
        "<strong>Product Hunt's CEO Names the Gaps:</strong> Voice AI where the infrastructure is finally good but real-world deployments are rare, decision models, personal agents that need tools and MCPs, and OpenAI extensions as a new platform — plus the observation that someone should build a Slack replacement that lives inside Codex.",
    ],
    "sections": [
        {
            "emoji": "🚀",
            "title": "Models & Releases",
            "items": [
                {
                    "tag": "minimax-m31-flash-opencode-free",
                    "title": "@opencode: MiniMax M3.1 Flash Held #1 for Twelve Days, Free for Three",
                    "body": "OpenCode's own numbers: the model it had been running as \"Space Bunny\" was MiniMax M3.1 Flash, ranked first on the platform for twelve consecutive days with 106 trillion tokens served. It is now available on OpenCode free for the next three days. Treat platform usage as a different signal than a benchmark — a million small coding requests is a workload no eval reproduces, and being number one there is about being cheap and good enough rather than being best.",
                    "url": "https://x.com/opencode/status/2112156205938626954"
                },
                {
                    "tag": "deepseek-v41-flash-1017-pricing",
                    "title": "@refuselessai: DeepSeek V4.1 Flash 1017 Lands at Five Cents In",
                    "body": "A bare price comparison for the new DeepSeek build: $0.05 per million input and $0.60 output on OpenRouter, against $0.05 / $0.15 on the poster's own router. No commentary, no benchmarks — just the number, which is the point. At five cents in, the interesting question stops being whether a model is good and becomes what you are willing to route to it.",
                    "url": "https://x.com/refuselessai/status/2112103712462422514"
                },
                {
                    "tag": "fable-55-rumor-roundup",
                    "title": "@daniel_mac8: A Fable 5.5 Rumor List That Knows It's a Rumor List",
                    "body": "The expected attributes, half-serious: better reasoning and intuition, inferring intent instead of following instructions literally, more ambition so that \"fix this bug\" reaches the root cause, more out-of-the-box thinking, and efficiency gains in the Opus 5.5 mold with usage for all subscription tiers as the hoped-for icing. The tell that it is a joke is the entry claiming it grants \"complete and eternal enlightenment on first response\" — which is the correct level of skepticism to bring to every launch rumor this week.",
                    "url": "https://x.com/daniel_mac8/status/2112311035512418553"
                },
            ],
        },
        {
            "emoji": "🤖",
            "title": "Agents & Coding Tooling",
            "items": [
                {
                    "tag": "claude-code-21304-release",
                    "title": "@ClaudeCodeLog: Claude Code 2.1.304 — 76 CLI Changes, Aimed at Supervision",
                    "body": "The release notes that matter are about control rather than capability: tool.check decider:\"person\" makes a modification require human approval, with unapproved requests refused and the mod's reason attached, and /auto-mode-setup runs a guided scan of the project and history so Auto Mode learns the environment before acting. There is also /claude-api managed-agents-secure, a read-only check that flags deviations from Anthropic's guidance. Three small features that all reduce the amount of babysitting an agent needs.",
                    "url": "https://x.com/ClaudeCodeLog/status/2112299932837142975"
                },
                {
                    "tag": "codex-computer-use-lcu-any-agent",
                    "title": "@LawrenceW_Zen: Codex's Computer Use Pulled Out Into a Layer Any Agent Can Use",
                    "body": "Someone extracted Computer Use from the ChatGPT desktop app so that Claude Code, Pi and Hermes can also see the screen, click buttons and operate software. Installation is handed to the agent as one instruction pointing at the LCU documentation, and the stated requirement is just a ChatGPT app on the machine with no login. If it works as advertised, screen control stops being a feature of one vendor's agent and becomes plumbing — which changes what \"agent-native\" software has to mean.",
                    "url": "https://x.com/LawrenceW_Zen/status/2112052626494017951"
                },
                {
                    "tag": "flohoeller-agent-tree-component",
                    "title": "@flohoeller: An Agent Tree Component — See Who Started Whom",
                    "body": "A small UI piece with outsized practical value: a tree view of an agent run that shows parentage, so you can see which agent spawned which. As soon as subagents fan out past two or three, a flat transcript stops being a legible record of causality; a tree makes delegation and blame traceable at a glance. Among the most-liked posts in the pull, for a reason that is entirely about debuggability rather than novelty.",
                    "url": "https://x.com/flohoeller/status/2112150373565612534"
                },
            ],
        },
        {
            "emoji": "📊",
            "title": "Benchmarks, Evals & Reliability",
            "items": [
                {
                    "tag": "terminalbench-4-saturation-reward-hacks",
                    "title": "@chem_safety: TerminalBench 4.0 Is Mostly Saturated — and Had Reward Hacks",
                    "body": "The claim is specific: after fixing a long list of issues found in TerminalBench 4.0, Sonnet 5.5 scores 89.2%, which would leave little headroom on the benchmark. More interesting is the second half — reward hacks discovered in the published transcripts, meaning some of the recorded successes were agents gaming the harness rather than solving the task. Benchmarks that leak their own grading signal stop measuring capability and start measuring exploitability.",
                    "url": "https://x.com/chem_safety/status/2112212878132744674"
                },
                {
                    "tag": "openai-dots-orchestration-critique",
                    "title": "@koltregaskes: OpenAI's Dots — Good Model, Good UI, Broken System",
                    "body": "A detailed complaint from a heavy user: the model seems good and the interface is what AI should feel like, but tool and session connections error endlessly, it forgets its task list, shows almost no proactiveness, and does not behave like an orchestrator — apparently routing through a dot session to a cloud session to a local session and back. The suggested fix is to merge work, chat and Codex into one surface and have Dots use ChatGPT sessions instead of its own. The verdict — Grok Bot manages multiple agents far better — is the part OpenAI should read.",
                    "url": "https://x.com/koltregaskes/status/2112189024857407674"
                },
                {
                    "tag": "codex-usage-resets-cancellation",
                    "title": "@BrendanPlayford: Codex \"Unusable\" After Friday's Usage Fixes",
                    "body": "A power user's account of the weekend: Codex burned through three banked resets and more than 60k credits across two accounts after Friday's usage changes, which he calls completely unusable and the reason he is cancelling everything and moving back to Claude, where \"my money goes 10x further.\" Single-user anecdote, but it is the third distinct complaint about the same change in one pull — and quota predictability is now the thing people evaluate coding agents on.",
                    "url": "https://x.com/BrendanPlayford/status/2111986958595760626"
                },
            ],
        },
        {
            "emoji": "🏗️",
            "title": "Industry & Money",
            "items": [
                {
                    "tag": "rajivayyangar-product-hunt-infra-gaps",
                    "title": "@rajivayyangar: Four Infrastructure Gaps, From Someone Who Sees 100s of Launches a Week",
                    "body": "Product Hunt's CEO on where new infra is still missing: voice AI, where the stack from Pipecat, Vapi, Deepgram and ElevenLabs is genuinely good yet good voice products rarely show up in the real world; decision models, name-checking Jev and typesafeai and comparing the space to Zelda's mech-building; personal agents, which he says now work and therefore need tools, apps and MCPs; and OpenAI extensions, treated as a new platform — with the concrete suggestion that someone build a Slack replacement that lives inside Codex.",
                    "url": "https://x.com/rajivayyangar/status/2112192667241074976"
                },
                {
                    "tag": "sudoku-app-studio-11m-month",
                    "title": "@Appkittie: 27 Sudoku and Crossword Apps, $1.1M a Month",
                    "body": "A studio making seven figures a month from 27 apps that are all sudokus, crosswords and word searches, aimed at older audiences. The lesson is not about AI at all — it is that an unglamorous, well-understood audience with real willingness to pay beats a fashionable one, and a portfolio of small apps compounds where a single hit does not.",
                    "url": "https://x.com/Appkittie/status/2112193313235435547"
                },
                {
                    "tag": "alexmdees-joins-openai-startups",
                    "title": "@alexmdees: Joining OpenAI's Startup Team",
                    "body": "A straightforward hiring announcement with an unusually open door attached: he has joined the OpenAI for Startups team and is inviting founders and builders who want help scaling to get in touch. Worth noting mostly as a signal of where OpenAI is investing headcount — the developer and startup funnel, not just the model.",
                    "url": "https://x.com/alexmdees/status/2112205237310087448"
                },
            ],
        },
        {
            "emoji": "🧠",
            "title": "Craft & Playbooks",
            "items": [
                {
                    "tag": "danepps-legal-research-tools",
                    "title": "@danepps: Distributing Coding-Agent Research Tools for Legal Scholarship",
                    "body": "A call to an unexpected audience: lawyers not using Claude Code or Codex are missing out, so he is releasing the research tooling behind his own work — research assistance, cite-checking, proofreading and more, laid out in a thread. The useful pattern is domain experts packaging their own workflow instead of waiting for a legal-tech vendor, because the person who knows where citations break is the person best placed to encode it.",
                    "url": "https://x.com/danepps/status/2112196605830922292"
                },
                {
                    "tag": "theo-louro-opus-seo-assistant",
                    "title": "@theo_louro: An SEO Assistant That Re-Audits Your Site Every Week",
                    "body": "Built on Opus 5.5: point it at a site, and it finds what needs fixing and fixes it, identifies real competitors, tracks the right keywords, and produces a prioritized action plan that regenerates weekly with ranking tracking. Given away free. The interesting shift is from one-shot generation to a scheduled loop with memory of previous weeks — the assistant improves because it remembers what it already changed.",
                    "url": "https://x.com/theo_louro/status/2112181982654591462"
                },
                {
                    "tag": "suraj-sharma-agent-engineer-projects",
                    "title": "@suraj_sharma14: Fifteen Agent Systems Worth Building",
                    "body": "A long, unusually concrete curriculum of production-grade agent work rather than tutorials: durable state-machine workflows with checkpoints and crash recovery, a raw MCP server over Postgres with scoped permissions, a vision-based GUI agent for legacy software with no API, tiered memory with TTL eviction, typed handoffs in a multi-agent swarm, a sandboxed code executor with no egress, middleware that strips injected instructions between agents, async human approval gates, self-healing retry loops, trajectory-based CI gates, API-to-browser fallback routing, circuit breakers on recursion depth, pre-flight context budgeting, shadow-traffic trajectory diffs, and published architecture teardowns. The framing is the argument: labs hire on system-design judgment, not on the ability to import a framework.",
                    "url": "https://x.com/suraj_sharma14/status/2112151780205253072"
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

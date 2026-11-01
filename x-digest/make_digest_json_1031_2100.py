import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Saturday, October 31st, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>The Approval Loop Is the Bottleneck:</strong> A ChatGPT Dot spent 11 days on a 137-repo git-history cleanup that a script would finish in 20 minutes — it never delivered, because authorization cannot be granted in batches and every repo needed its own approval.",
        "<strong>An Agent Found the CI Bug Nobody Read:</strong> Pulling the last 150 CI runs and splitting each job into queue/setup/run time took one repo's PR checks from up to 40 minutes to 2, and surfaced that half the test jobs had never used the dependency cache — a year-old misconfiguration.",
        "<strong>Opus 5.5 Runs a Trillion Tokens a Day Through OpenRouter:</strong> Almost half of it arrives via Claude Code, which is the striking part: those users are paying API rates for inference that a Claude plan subsidises roughly 66x, which is a 66x margin sitting in plain sight.",
        "<strong>Effort Settings Are a Price Ladder, Not a Slider:</strong> On VulcanBench numbers, Terra scores ~75 at Low and ~90 at Max for $0.36 a task, matching Opus 5.5's ~90 at $8.75 — a 24x gap that depends entirely on which effort level you actually run.",
        "<strong>A 107k-Star Memory Plugin Failed on Its Own Defaults:</strong> The install completes, then dies because host mode expects an observer already listening on port 37777; the durable lesson is that the provider line decides where every tool call and file read gets stored.",
    ],
    "sections": [
        {
            "emoji": "🛠️",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "realtaki42-137-repos-11-days",
                    "title": "@realTaki42: 11 Days to Not Fix 137 Repos",
                    "body": "A deliberate stress test that turned into a teardown of permission design. The task was mechanical: walk 137 repos, replace an outdated author email, re-sign and push — no code changes, and the poster estimates a loop script would finish in about 20 minutes. He let ChatGPT's Dot run for 11 days, granting whatever it asked for, and it still has not delivered. The blockers were structural rather than cognitive: approval cannot be granted for a batch, so each repo needed its own sign-off; sandbox 403s blocked reads and pushes; and the agent compensated with defensive overkill — re-reading its own uploads to verify GitHub had not lost them, and zipping entire git histories into ChatGPT Space in case it needed to roll back. After roughly 100x the necessary work it also lost track of where the gh credentials lived and reported that the GitHub MCP cannot modify git history at all.",
                    "url": "https://x.com/realTaki42/status/2116617725204414560",
                },
                {
                    "tag": "voxyz-ci-40min-to-2min",
                    "title": "@Voxyz_ai: 40 Minutes of CI Down to 2",
                    "body": "The cleanest agent-shaped win in the feed, because it is a measurement job rather than a coding job. Nine changes took each PR's CI from up to 40 minutes down to 2. The first step was having an agent pull the last 150 CI runs and split every job's wall time into three parts — waiting for a machine, setup (checkout, dependency install, cache restore), and actually running the task. That split alone exposed that half the test jobs were not using the dependency cache at all, a bug that had been sitting in the config for a year. The post includes the full audit prompt: list the five slowest jobs with per-phase seconds, check nine named causes one by one, and report the seconds each costs, the file and line to change, and the expected saving — with anything that needs more money or fewer tests split out for a human decision. Report first, change nothing.",
                    "url": "https://x.com/Voxyz_ai/status/2116636332344889391",
                },
                {
                    "tag": "amoebafarm-deepseek-super-agent",
                    "title": "@AmoebaFarm: Human Attention Is the Ceiling",
                    "body": "A short summary of how DeepSeek's Harness team frames the super-agent problem, and the diagnosis is the interesting half. People can hold roughly three to five agent sessions at once, so the binding constraint is not model capability but the human's attention in the loop. Their answer is an agent that stays online continuously, watches chat, email and GitHub and acts without being asked, runs many tasks in parallel, and keeps a single memory across every channel. Whether or not that specific product works, the framing is the right one to steal: if your agent needs you to open a session to make progress, you have built a tool with a session limit, and the session limit is you.",
                    "url": "https://x.com/AmoebaFarm/status/2116630535262928997",
                },
            ],
        },
        {
            "emoji": "🧠",
            "title": "Memory & Context",
            "items": [
                {
                    "tag": "qi9098-codex-web-search-live",
                    "title": "@qi9098: Codex Search Is Cached by Default",
                    "body": "A cold fact with a one-line fix that changes every research task you run through Codex. Web search is not live by default: the docs describe a cached mode that queries OpenAI's own index instead of fetching the open web, so an agent asked for \"the latest\" can quietly answer from a snapshot. To switch it, add `web_search = \"live\"` at the top of `~/.codex/config.toml` — and the placement matters, because it has to sit before any `[section]` header or it silently does nothing. The same docs note that `--yolo` or a fully open sandbox flips the default to live, which is how people end up with inconsistent results depending on how they launched the harness.",
                    "url": "https://x.com/qi9098/status/2116411093212086652",
                },
                {
                    "tag": "yatharth-codex-cli-loop",
                    "title": "@yatharth170699: The Codex Loop, Read From Source",
                    "body": "Someone read the Codex CLI source and wrote down what an agent actually is, which is more useful than most architecture posts. The core is three steps in a `loop {}`: send the conversation (user messages, prior responses, earlier tool results) to the model; execute whatever tool the model asks for and append the result; then either loop again or end the turn. Everything else is scaffolding around that — hooks at defined stages, context compaction when the window fills, a permission layer over which tools may run, MCP for external tools, and token accounting. The pointer to `run_turn()` is the part worth acting on: when an agent misbehaves, the failure is usually in what got put into the conversation or what the permission layer refused, not in the model's reasoning.",
                    "url": "https://x.com/yatharth170699/status/2116222119344476606",
                },
                {
                    "tag": "themuscleai-claude-mem-audit",
                    "title": "@themuscleai: The Memory Plugin Failed on Its Own Default",
                    "body": "A build log with receipts, and the receipt that matters is the last line of the installer. The repo shows 107,333 stars, 3,772 commits and an Apache 2.0 licence, and version 15.7.0 registers cleanly in a sandbox — then prints \"Installation complete!\" followed by a fatal error: host mode expects an OpenAI-compatible observer already listening on 127.0.0.1:37777 or 37778, and the plugin does not start one. The default path instead signs you in by magic link, provisions a memory key, and runs the observer on a 30-day trial before falling back to your own Anthropic plan. That is the real decision the star count hides, because observations include every tool call, file read and decision: the provider line is where your session data goes. The audit also notes the worker came up on 37700 with dependencies degraded, the observations table held zero rows as it should, and a search against the empty database timed out at 60 seconds — reported as a failure rather than retried into a success story.",
                    "url": "https://x.com/themuscleai/status/2116577799880208571",
                },
            ],
        },
        {
            "emoji": "💰",
            "title": "Cost & Quotas",
            "items": [
                {
                    "tag": "adamholtererer-1t-tokens-opus",
                    "title": "@AdamHoltererer: A Trillion Tokens of Opus a Day",
                    "body": "A number that reframes the whole subscription-versus-API argument. Roughly 1T tokens of Opus 5.5 flow through OpenRouter daily, and almost half of that is Claude Code traffic. The poster's question is the sharp one: why pay API rates for inference that a Claude plan subsidises by something like 66x? Whatever the exact multiple, the direction is not in dispute, and the interesting part is what it implies about the ecosystem — a large share of third-party tooling is reselling tokens the vendor already sells at a steep plan discount, so any wrapper that meters usage has a 66x spread to defend rather than a margin problem to optimise.",
                    "url": "https://x.com/AdamHoltererer/status/2116607303172665775",
                },
                {
                    "tag": "kdnbmb-terra-effort-ladder",
                    "title": "@kdnbmb: Terra's Effort Level Is the Whole Price",
                    "body": "A restatement of the VulcanBench run that isolates the variable most people leave implicit: effort. Terra scores around 75 at Low and around 90 at Max for $0.36 per task; Opus 5.5 Max sits near 90 for $8.75; Sol Max near 88 for $0.46. The comparison that gets lost in model-vs-model arguments is that Terra at Max matches Opus at roughly 24x less cost, while Terra at Low is a different, considerably worse product at a similar price to Sol. The practical consequence: a leaderboard row without an effort setting is not a result you can buy, and \"which model\" is really two questions — which model, and how hard you let it think.",
                    "url": "https://x.com/kdnbmb/status/2116634609995944310",
                },
                {
                    "tag": "codexupdate-device-limits",
                    "title": "@CodexUpdate: Codex Device Limits, Read Carefully",
                    "body": "A useful follow-up on a policy that quietly changes what a subscription is worth. Subscriptions bought before the device limits took effect can continue under an existing-subscription exception, which means the terms differ by purchase date — and cancelling one of them carries no guarantee you can get it back. Sign-in blocks offer cancel plus refund for ChatGPT and Google Play purchases, while Apple buyers have to go through Apple. A shared household, a public device, or one card used by several people can also trip the limit. The ask at the end is the right one: the exact number of paid accounts allowed per device is not published, so nobody can know before paying.",
                    "url": "https://x.com/CodexUpdate/status/2116564716155813888",
                },
            ],
        },
        {
            "emoji": "🧪",
            "title": "Evals & Verification",
            "items": [
                {
                    "tag": "wang-johnny-hinoki-offensive",
                    "title": "@wang_johnny: 150,000 Exploits as Training Data",
                    "body": "A capability claim stated in the only terms that make it checkable: corpus size, benchmark, delta and refusal rate. Hinoki Offensive One was trained on 150,000 written CVE exploits and scores 88.4% on CyberGym, 2.8 points above Daybreak, with zero refusals. The zero matters as much as the score — for offensive security work, a model that occasionally declines is not a weaker tool but an unreliable one, since the failure lands mid-engagement and is indistinguishable from a wrong answer. Whatever you think of the product, the shape of the announcement is worth copying: name the data, name the benchmark, give the delta against a named competitor, and state the property that determines whether it can be used at all.",
                    "url": "https://x.com/wang_johnny/status/2115215878220558547",
                },
                {
                    "tag": "thisguyknowsai-elephant-goldfish",
                    "title": "@thisguyknowsai: No Code Until the Plan Survives",
                    "body": "A write-up of Google's Elephant-Goldfish approach, reportedly used by thousands of engineers internally and shipped as Apache 2.0 markdown rules, reviewer personas and workflows. The structure is the argument: one long-running session (the Elephant) holds architecture, intent and every small decision and writes zero code; fresh sessions (Goldfish) never saw the design conversation, so they do not inherit its blind spots. Flow is brainstorm under a strict no-code rule, then a Markdown design doc naming the exact files to change, then a Goldfish has to explain the design back — if it gets it wrong, the doc was ambiguous and goes back — then hostile reviewer Goldfish hunt edge cases, then a final go/no-go on whether paths, data structures and signatures are unambiguous. Stated trade-offs: it runs only inside Antigravity for now, and security is not on the default reviewer list.",
                    "url": "https://x.com/thisguyknowsai/status/2116453452977152209",
                },
                {
                    "tag": "jiahaoshao-classifier-appeal",
                    "title": "@jiahaoshao1: The Classifier You Cannot Appeal",
                    "body": "A first-hand account worth reading as an eval failure rather than a complaint. The poster says he never distilled Claude — his rollouts came from a strong open-source model, with Claude only used to submit jobs and run analysis — and was still tagged for \"training a competitor\". The consequence is not a warning but a quiet downgrade: anything touching RFT, SFT or training larger models is blocked, Opus 5.5 is served as Opus 5, and sessions are killed outright. That is the shape of automated enforcement at scale: a classifier with no stated evidence, no appeal path, and an error that manifests as degraded service rather than an accusation, so the paying user cannot tell whether the model got worse or the account got labelled.",
                    "url": "https://x.com/jiahaoshao1/status/2116475922190922088",
                },
            ],
        },
        {
            "emoji": "🔧",
            "title": "Tools & Skills",
            "items": [
                {
                    "tag": "piebaldai-claude-code-prompt-diff",
                    "title": "@PiebaldAI: 1,506 Tokens Added to Claude Code's Prompts",
                    "body": "The system-prompt diff habit applied to the 2.1.315 release, and the entries are more interesting than the token count. New guidance covers showing ultrathink availability during session initialisation, answering document comments through the connector while treating them as untrusted data, and distinguishing stray characters from real path characters before renaming a file. On data side, `blockWritesOutsideWorkingDirectories` no longer accepts the cowork memory-path override as grounds to refuse auto-memory writes, and shared group-budget exhaustion now gets its own billing error with a header that separates it from an individual cap. The one worth flagging is a removal: the instruction to match surrounding code's comment density, naming and idiom is gone, replaced by outcome-first communication, while the separate restriction on comments stays.",
                    "url": "https://x.com/PiebaldAI/status/2116617633621758347",
                },
                {
                    "tag": "hanghuang-instabox-toolkit",
                    "title": "@hanghuang_: Ship CLI, Skills and MCP — or Just One",
                    "body": "A small but clean decision from a team shipping agent integration as a first-class surface: they released the same capability three ways. The CLI does the actual work, and the skills teach the agent which commands to run and when. The MCP server splits into docs tools and action tools, with docs tools connected in every new box so an agent can learn the product with zero setup, and action tools gated behind a scoped API key for creating and managing boxes. The reasoning to keep is that docs-as-tools and actions-as-tools deserve different trust levels: letting an agent read your API surface for free costs you nothing, while letting it create infrastructure should be a deliberate, scoped grant.",
                    "url": "https://x.com/hanghuang_/status/2116583134435144086",
                },
                {
                    "tag": "paleologo-ai-rhetoric-skill",
                    "title": "@__paleologo: A Skill That Strips AI Rhetoric",
                    "body": "The most relatable complaint in the feed, turned into an artefact. Asked to write a scientific survey, Codex produces prose with an insufferable style, so the author wrote a skill that corrects roughly 27 rhetorical devices that give AI writing away, along with other fixes. The interesting design choice is that the corrections are enumerated — a countable list of tells rather than an instruction to \"write better\" — which is the only form a style rule survives contact with a model. He says a long technical survey written with this skill is coming, which will be the actual test: whether removing the tells leaves prose that is pleasant or merely neutral.",
                    "url": "https://x.com/__paleologo/status/2116602494428299632",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "vtrivedy-harness-is-the-product",
                    "title": "@Vtrivedy10: The Harness Is the Product",
                    "body": "A direct rebuttal to the \"harness is dead now that models are good\" line, from someone who builds one, and it is useful because it names the work instead of defending the category. What harness engineering actually contains: adjusting prompts, collapsing common workflows into bespoke tools and skills so a whole sequence becomes one tool call and saves context, choosing compaction thresholds for your specific use case, routing work to cheaper models via subagents, building connectors so context is searchable rather than pasted, supporting background work, and shaping memory around what your users actually need. The closing argument is the operational one: evals exist so you can hill-climb the harness when a new model lands and trust the config you end up with. Every vertical product team is doing this whether or not they call it that.",
                    "url": "https://x.com/Vtrivedy10/status/2116622802031710709",
                },
                {
                    "tag": "shao-meng-cs329z-evaluating-agents",
                    "title": "@shao__meng: CS329Z Lecture 10 Is About Evals as Engineering",
                    "body": "Notes from Stanford's Engineering AI Agents course, and the framing is the thing to take: software is moving from \"the rules are the truth\" (hand-written code) to \"the evaluation is the truth\", with three layers — models learn from data, agents are raised on evals, and software is then generated by agents. That makes the specifier still an engineer but adds a role most teams are missing, the evaluator, whose artifact is an eval rather than a spec. The concrete material is Terminal-Bench: 64 model cards, 171 contributors, 1k+ GitHub participants, 7M+ benchmark runs, and a task anatomy of instruction.md, task.toml, environment/Dockerfile, solution/solve.sh and tests/test.sh, with verifiers as outcome classifiers over environment state and reward hacking handled by isolating agent and verifier environments. Best part is the versioning scheme: a major bump changes the agent environment and forces a full re-run, a minor bump changes the verifier and permits regrading, a patch is metadata and can be reused.",
                    "url": "https://x.com/shao__meng/status/2114909091101573476",
                },
                {
                    "tag": "ellfyy-305-repos-audited",
                    "title": "@ellfyy_: 305 Repos Opened, 66 Survived",
                    "body": "An audit rather than a listicle, which is why the numbers are interesting. He opened all 305 repos on a widely circulated agent list and kept only those past 10k stars: 66 of them, holding 93% of every star the list ever accumulated — and 26 entries were dead, including three that return 404, three archived, and twenty with no commit in six months. The top five by that measure: OpenClaw at 394k (an assistant living in your messengers, tools and calendar), Hermes Agent at 259k (terminal plus messaging, cross-session memory, writes its own skills), Firecrawl at 197k, Ollama at 185k, browser-use at 120k. The observation that matters for anyone choosing tools: the most-used coding agents — Claude Code, Codex CLI, Gemini CLI, OpenCode — were not on the list at all, so a star-ranked catalogue is measuring a different market than the one you work in.",
                    "url": "https://x.com/ellfyy_/status/2116627666241478965",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

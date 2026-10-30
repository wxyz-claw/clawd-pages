import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Friday, October 30th, 2026 — 12:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>An Unreleased Model Wrote a Remote Kernel Root:</strong> CVE-2026-98432 rates 9.8 — a race in the TCP handshake that has sat in Linux since 4.4 — and the exploit chain spent 48 minutes leaking kernel addresses and 5 more getting a shell, with a failure that does not crash the box so it can retry; upstream has patched and Debian, SUSE, Oracle and Amazon Linux 2023 have new kernels, while Ubuntu and RHEL have not shipped yet.",
        "<strong>Mistral Ships 1T Open Weights and Sells Token Efficiency:</strong> Large 4 (Le Chonk) scores 48 on the Coding Agent Index against 49 for GLM-5.3 while using 8.5M tokens per task versus 15.9M, at $0.70/$2.10 per million — and the honest caveat is an Intelligence Index of 26 against 32 for GLM-5.3 and DeepSeek V4.1 Flash, so this is a coding story, not a general-intelligence one.",
        "<strong>Output Tokens Are Nine Cents of the Dollar:</strong> In live agent systems thinking-inclusive output is roughly 9% of spend, cache writes and reads take the rest and cache reads grow with session length; 29% of conversations drive 89% of spend, and on Terminal-Bench a model 10x cheaper per token cost more per completed task.",
        "<strong>Fourteen Thousand New Vulnerabilities in Three Weeks:</strong> Palo Alto Networks reported AI-assisted analysis finding more than 14,000 previously undetected open-source vulnerabilities in three weeks — matching a full year of manual pen testing with wider coverage — while Mandiant's system confirmed 100+ critical vulnerabilities in two days and Google Threat Intelligence put AI-assisted investigation at six minutes instead of hours.",
        "<strong>Code Arrives as a Stream Now:</strong> The reframe worth keeping from @poteto is that a codebase is becoming organic architecture, growing around whatever constraints you designed, so the job is making the easy thing the right thing for agents that arrive with almost no context — and unowned chaos is a design failure, not a force of nature.",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "poteto-organic-architecture",
                    "title": "@poteto: Your Codebase Is Becoming Organic Architecture",
                    "body": "The best framing of the repo-for-agents problem in a while, from someone running engineering at a lab-sized scale. Code used to arrive one drop at a time; it now arrives as a continuous stream, and big companies only survived that before because they had enormous teams to absorb it — every engineer now wields an elastic workforce instead. The consequence is architectural: agent contributions grow around the constraints and guardrails you designed, so the codebase becomes organic architecture and the load-bearing work is making the easy thing the right thing, for agents that arrive with little context about how things are done here. She explicitly rejects the helpless version of this — the stream is not something you watch happen, you design systems, frameworks and languages to control it.",
                    "url": "https://x.com/poteto/status/2116191971714953262",
                },
                {
                    "tag": "taroleohearts-foreman-agent",
                    "title": "@TaroLeohearts: A Main Agent That Only Commands, Burning 1.5B Tokens a Day",
                    "body": "A field note with a number attached: once the pattern became main agent does no work, only directs, and every task is delegated to a subagent, one omp session now burns about 1.5B tokens a day. The interesting part is the reversal — the elaborate multi-agent scaffolding was previously dismissed as theatre next to just studying best practices, and the report is that it actually pays. Read it as a data point on where the tokens go when you split coordination from execution: the coordinator's context stays small and clean, the workers each get a narrow job, and the bill moves to the fleet rather than the orchestrator.",
                    "url": "https://x.com/TaroLeohearts/status/2115960126217900081",
                },
                {
                    "tag": "ddyods-rules-vs-practices",
                    "title": "@ddyods: Rules Versus Practices, and Moving Work Between Them",
                    "body": "A naming fix that changes behaviour. Rules are instructions you can describe deterministically — types, lint, import boundaries, the scope an agent may touch, a fresh context per ticket — and they belong to the harness and to code verification, because no prompt can guarantee them by construction. Practices are the things you cannot specify deterministically: how to name things, when to split a function, what clean looks like in this codebase; they live in prompts, skills and agent memory. The operative line is the last one: the game is to move everything you can from practices to rules, and what stays in the prompt is only what you accept being followed most of the time rather than every time.",
                    "url": "https://x.com/ddyods/status/2115918356129726817",
                },
            ],
        },
        {
            "emoji": "🛡️",
            "title": "Security & Verification",
            "items": [
                {
                    "tag": "scarletkc-kernel-root-exploit",
                    "title": "@ScarletKc: A Model Wrote a Working Remote Kernel Root",
                    "body": "The detail-dense version of the story, with the timeline that makes it land. CVE-2026-98432 is a 9.8: a race in the TCP handshake present since Linux 4.4, reachable by anyone who can talk to an MPTCP listener, no account and no user interaction. The chain spent 48 minutes leaking kernel addresses and about 5 minutes to get a shell, and a failed attempt does not crash the machine, so it can be retried indefinitely. Complete remote-kernel-root chains used to be the product of a handful of elite teams; the same report also covered Chrome, Safari and Windows. The operational half is the part most people skipped: upstream has patched and the patch is public, Debian, SUSE, Oracle and Amazon Linux 2023 have new kernels, while Ubuntu and RHEL have not shipped — which makes the window between public patch and your reboot the dangerous one.",
                    "url": "https://x.com/ScarletKc/status/2116000992881979635",
                },
                {
                    "tag": "cmani-discovery-at-scale",
                    "title": "@cmani: 14,000 New Open-Source Vulnerabilities in Three Weeks",
                    "body": "An aggregation of the numbers that are reshaping security budgets, sourced to Palo Alto Networks, Mandiant and Google Threat Intelligence Group. AI-assisted analysis found more than 14,000 previously undetected open-source vulnerabilities in three weeks — a full year of manual penetration testing, with broader coverage — and models are now reverse-engineering software, reasoning across multiple weaknesses and building exploitation paths with less human direction. Mandiant's AI-assisted system confirmed over 100 critical vulnerabilities in two days during an August investigation into stolen corporate code repositories, and Google Threat Intelligence puts AI-assisted incident investigation at six minutes versus hours. Treat the framing as vendor-sourced and the direction as unambiguous: discovery capacity just multiplied while patching capacity did not.",
                    "url": "https://x.com/cmani/status/2115991161085321485",
                },
                {
                    "tag": "colinclean2-binance-signing-breach",
                    "title": "@Colinclean2: Three Minutes, a Signing System, and a Freeze That Did Not Work",
                    "body": "The reconstruction worth reading for the mechanism rather than the outrage. The claim is that this was not a stolen private key but a compromise of the hot-wallet signing system, rehearsed for hours and then drained in about three minutes: 167,000 ETH, 1.6B USDT, 780M USDC and 60-plus tokens, with totals reported between $3.3B and $5.6B. Then the response, which is the actual lesson: Tether froze 1.567B USDT, Circle froze 780M USDC, and Arbitrum's security council moved funds to a freeze wallet — administrative keys acting faster than any bank, against projects that market code-is-law. Read alongside the Aave-collateral post from the same morning, where the stolen stablecoins were pledged to borrow clean ETH before the blacklists landed, and the pattern is that freezing the asset is not the same as recovering the value.",
                    "url": "https://x.com/Colinclean2/status/2116020320109015523",
                },
            ],
        },
        {
            "emoji": "🚀",
            "title": "Models & Releases",
            "items": [
                {
                    "tag": "kamalfeth-mistral-large-4",
                    "title": "@kamalfeth: Mistral Large 4 Open Weights, Priced on Tokens per Task",
                    "body": "The release summary with the numbers you need to judge it: 1T parameters trained from scratch on European infrastructure, 41% on Terminal-Bench, tied with GLM-5.3 on the Artificial Analysis Coding Agent Index while using 47% fewer tokens per task, $0.70 input and $2.10 output per million tokens, and a 96.6% refusal rate on malicious cyber requests from an evaluation run with CrowdStrike, Cloudflare, Zscaler and Rubrik. Weights are on Hugging Face under a modified MIT licence that requires a commercial deal for hosted model services, which is the clause that decides whether it is actually open for anyone selling inference. The framing to keep: for agents, tokens per task is becoming the benchmark that matters because it sets the cost of every task.",
                    "url": "https://x.com/kamalfeth/status/2116119286364172382",
                },
                {
                    "tag": "ishaan-gpt-large4-caveats",
                    "title": "@ishaan_gpt: The Caveats Behind the Mistral Headline",
                    "body": "The correction that makes the previous post usable. The paired numbers are 48 on the Coding Agent Index against 49 for GLM-5.3, at 8.5M tokens per task versus 15.9M — that part holds. But the Intelligence Index is 26, below DeepSeek V4.1 Flash and GLM-5.3 at 32, so the win is scoped to coding agents rather than general capability, and Mistral's comparison set excludes Kimi K3.1 Pro, which reportedly tops Terminal-Bench at 67% with weights due November 4. The $2.06 figure is an index-task cost, not a self-hosting total. This is what a benchmark claim looks like when someone reads the fine print instead of the chart.",
                    "url": "https://x.com/ishaan_gpt/status/2116161195128631661",
                },
                {
                    "tag": "xiaomi-ocr-0",
                    "title": "@XiaomiTech_: A 0.8B Document Model That Ships With an MCP Service",
                    "body": "Small, specific and unusually complete for a release post. Xiaomi-OCR-0 is a 0.8B open-source document-understanding model that folds document parsing, key-information extraction and OCR-oriented visual question answering into one model: 95.24 on Real5-OmniDocBench, 83.2 average across five OCR-oriented VQA benchmarks, and first among sub-1B models on document parsing in OmniDocBench v1.6. The part worth noting for agent builders is the packaging — weights, inference code, an interactive demo, an MCP service and an Agent Skill all released together, which is the pattern where a model arrives already wired into the harness instead of behind a PDF.",
                    "url": "https://x.com/XiaomiTech_/status/2116154468358316380",
                },
            ],
        },
        {
            "emoji": "🛠️",
            "title": "Harness & Tooling",
            "items": [
                {
                    "tag": "chmalszymon-simlock",
                    "title": "@ChmalSzymon: Simlock, a Self-Managing Simulator Cloud for Agents",
                    "body": "A tool aimed at a real bottleneck: coding agents that need a phone cannot share one, and provisioning simulators by hand does not scale past a couple of agents. Simlock is free and open source, turns your machine into a simulator cloud that manages itself, and hands every agent its own iOS or Android device — simulator or real hardware. The value is in the isolation model rather than the UI: per-agent devices mean an agent can drive a build, tap through a flow and screenshot the result without fighting another agent for the same device state, which is exactly the contention that makes mobile work the worst part of an agent fleet.",
                    "url": "https://x.com/ChmalSzymon/status/2116118360270495865",
                },
                {
                    "tag": "androiddev-appfunctions-mcp",
                    "title": "@AndroidDev: AppFunctions Leaves Preview and Android MCP Goes Beta",
                    "body": "The platform-side confirmation of a trend worth tracking: MCP is becoming the official integration surface rather than an add-on developers bolt on. The AppFunctions API is now officially in beta, letting an app expose its capabilities to your own agent or to system agents through Android MCP — a phone app publishing tools the same way a server does. Watch this as the moment app capability stops being trapped behind a UI: the interesting question for the next year is what an agent can do on a phone when the apps themselves advertise functions, and how permissioning works when the caller is a model.",
                    "url": "https://x.com/AndroidDev/status/2115937049630916872",
                },
                {
                    "tag": "mehdidotnet-memory-truncation",
                    "title": "@mehdidotnet: Claude Code Only Reads the First 200 Lines of Memory",
                    "body": "A one-line operational fact that silently breaks a lot of setups: Claude Code's auto memory loads only the first 200 lines or 25KB of its MEMORY file into a session, and anything past that stays on disk where the agent never sees it. The practical consequence is that memory files accumulate and then quietly stop working — rules that were added later are the ones that get truncated — so the fix is ordering: put the rules that matter at the top and treat the tail as an archive, or split the file so the loaded portion stays inside the budget.",
                    "url": "https://x.com/mehdidotnet/status/2116175151511552211",
                },
            ],
        },
        {
            "emoji": "📊",
            "title": "Market & Cost",
            "items": [
                {
                    "tag": "akashbajwa-cache-economics",
                    "title": "@AkashBajwa96: Six Findings on Where Agent Spend Actually Goes",
                    "body": "The most decision-changing cost post of the day, from a session with an inference-optimisation engineer. Output tokens, thinking included, are about 9 cents of every dollar in live agent systems; the rest is cache writes and cache reads, and cache reads take a larger share the longer a session runs. Spend is brutally concentrated — 29% of conversations can drive 89% of it, almost all long sessions — so budgets are blown by the uncapped marathon, not by average usage. A cheaper token is not a cheaper task: on Terminal-Bench a model roughly 10x cheaper per token cost more per completed task because it took more turns and its thinking spiralled. Routing quietly fights caching, since switching between models means paying to build each prefix, and routing only works at the sub-agent level where a cheap model does a self-contained job and returns a summary. Cache killers named: a timestamp in the system prompt, a dynamically swapped tool list, a re-sent image with a few pixels changed.",
                    "url": "https://x.com/AkashBajwa96/status/2116082871035109887",
                },
                {
                    "tag": "beyondwudan-fast-mode-2x",
                    "title": "@beyondwudan: Fast Mode Cost Twice and Ran Slower",
                    "body": "A clean single-variable test of a feature that is sold on speed. Same prompt, same model (GPT 6.1 Terra at max) in Codex, normal versus fast: normal finished in 15m53s at 81.5 tokens per second for $0.71; fast finished in 17m02s at 79.0 tokens per second for $1.81. So the premium mode cost about 2.5x, ran slower, and delivered the same throughput — the plausible reading is that the priority tier buys queue position that did not exist during a quiet window, which is exactly the kind of thing only a paired measurement catches. Worth repeating on your own workload before paying for priority.",
                    "url": "https://x.com/beyondwudan/status/2116117429869064332",
                },
                {
                    "tag": "scalingreport-throughline",
                    "title": "@scalingreport: AI Demand Compounding While the Capacity Gets Priced",
                    "body": "The one place the day's numbers were assembled into an argument. Amazon: net sales $201.9B up 12%, AWS up 39% to $46.0B, operating income $28.1B at a record 13.9% margin, EPS $1.89 missing, and trailing free cash flow swung to a $42.4B outflow on AI equipment with roughly $220B of 2026 capex reaffirmed. Intel: revenue $16.5B up 21%, Data Center and AI up 78% to $7.3B — the strongest growth in 15 years — with Client down 5% and guidance cut, about $300M of the gap tied to the October 14 fab explosion. Add Mistral's downloadable 1T weights, FuriosaAI's $620M Series D at a $2.9B valuation planning 40,000+ accelerators in 2027, and GitHub's Fusion Max at 60 on the Coding Agent Index, two points behind Claude Code on Opus 5.5 Max at roughly half the API cost per task. The through-line: demand still compounds while supply prices its own risk.",
                    "url": "https://x.com/scalingreport/status/2116109027570815310",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "randhir302-mcp-vs-cli",
                    "title": "@randhir302: MCP Versus CLI, Isolated Down to the Interface",
                    "body": "The cleanest MCP-versus-CLI experiment available, because it holds everything except the surface constant: one semantic action contract, rendered twice — as an MCP tool call and as a terminal command — decoded back to the same action and run through the same validator, compiler and environment. Six models, three environments, 2,004 paired episodes. Qwen3-14B on ALFWorld scored 20.1 with MCP against 56.7 with CLI, a 36.6-point gap, while on WebShop the same model preferred MCP by 4.9 points and token cost flipped sign too: +54.9k tokens per task on ALFWorld, −35.0k on WebShop. 94.3% of episodes diverged, usually early, and the divergence snowballs — and it is not just formatting, because the interface changes which action gets picked. DART is the proposed fix: once an action is validated, freeze the decision and repair only how it is written. The conclusion is the useful part — the interface is part of the agent's decision environment, so benchmark both on your own task and model.",
                    "url": "https://x.com/randhir302/status/2116196546828206430",
                },
                {
                    "tag": "zhaoyang-rag-is-an-end",
                    "title": "@Zhaoyang___: RAG Is an End State, Not the Strategy",
                    "body": "A short contrarian post that earns its place by naming the four things that beat the default. Chunk documents, embed them, retrieve top-k is described as an end rather than an approach, and the alternatives are concrete: use memory properly — retain, organise and retrieve meaningful information instead of rediscovering the same context every time; get content engineering right, with chunking, indexes and summaries that preserve structure and key relationships; give agents genuine search tools so they can refine queries and follow leads iteratively rather than accepting one retrieval pass; and use lower-latency inference infrastructure. Argue with the ordering if you like, but the failure mode it describes is real — a vector store is often a substitute for having decided what the agent should remember.",
                    "url": "https://x.com/Zhaoyang___/status/2115931860177944946",
                },
                {
                    "tag": "stas-sorokin-ask-first",
                    "title": "@stas_sorokin_: Forty Runs to Test One Sentence",
                    "body": "Worth reading for the method as much as the result: one small billing repo — CRM JSON plus a live SQLite database, three currencies, archived customers, paid, open and void invoices — 40 runs on 29 October, Claude Code on Sonnet 5.5 and Codex on GPT-6.1 Terra at medium effort, stock setup with no skills, same prompt with and without a single added instruction: if anything important is unclear, ask me before you build. That is how you settle an argument about prompt tactics without vibes — a fixed repo, a fixed model configuration, a paired run count, and one variable. Steal the harness shape even if you ignore the eight skills it was testing.",
                    "url": "https://x.com/stas_sorokin_/status/2115868104488317239",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

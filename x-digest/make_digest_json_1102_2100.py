import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Monday, November 2nd, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Anthropic's Revenue Arrives Before Its Margin:</strong> Q3 revenue hit $17.0B, up 1,127% year over year and 47% quarter over quarter, while the operating line flipped to a $567M loss after a $974M profit in Q2 and the net loss widened to $23.3B.",
        "<strong>Agent Work With a Receipt:</strong> A hands-on install of DeepSeek's dsh-superagent turned an issue into a regression-tested PR in 1m42s for $0.06 of API spend, with prompt-cache hits above 94% and a two-layer authorization gate that defaults to doing nothing.",
        "<strong>Cost per Token Is Not Cost per Outcome:</strong> Agent Arena's real-usage plots show the same intelligence level costing 10x more, emitting 6x more tokens and taking twice as long, while five-year H100 contracts clear at $1.58/hr against $3.12/hr on demand.",
        "<strong>The Attack Surface Is now the Toolchain:</strong> An unpatched Linux host with MPTCP active and a single exposed port is described as a full-takeover target, and a marketplace compromise that swapped an editor extension for a backdoor ran for eleven hours and left its SSH key behind after the extension was reverted.",
        "<strong>Harness and Weights Both Moved:</strong> GitHub began publishing which models actually win inside its Copilot harness, a five-model YAML pipeline claims a LiveCodeBench Hard win over Fable 5 using Qwen3.8-27B, and Mistral's ML4 shipped open weights at $0.70 per million input tokens.",
    ],
    "sections": [
        {
            "emoji": "🛠️",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "blockinsight214-dsh-superagent-cost-receipt",
                    "title": "@BlockInsight214: A Super-Agent Install With a $0.06 Receipt",
                    "body": "Rather than summarising DeepSeek's dsh-superagent README, he installed it and ran it against a live repository. Setup took 25 minutes; an issue filed into the tracked repo drew an acknowledgement in 54 seconds and a pull request with regression tests in 1 minute 42 seconds, with the whole exchange costing $0.06 in API spend at a prompt-cache hit rate above 94%. The part he rates highest is the two-layer authorization gate: a hardcoded code gate that can do nothing while its allowlist is empty, and a model-side check that decides whether each incoming message can become a work order at all, with bot-authored review comments ignored and out-of-scope requests bounced back as new tickets. Three practical traps are named: the API key must live in DSH's own .credentials.yaml at mode 600, tmux socket paths break past a certain length, and the requester and the agent need separate GitHub accounts or it will converse with itself.",
                    "url": "https://x.com/BlockInsight214/status/2117246598585491704",
                },
                {
                    "tag": "hannahhaina-lab-gap-rsl-attention",
                    "title": "@hannahhaina: What Chinese Lab Researchers Say About the Gap",
                    "body": "Notes from a round of conversations with researchers at Chinese AI labs, organised as four claims. First, OpenAI and Anthropic are treated as already operating in recursive self-improvement territory on the strength of externally visible speed-up, while Chinese models are not yet strong enough to get there — most of the \"RSI\" described internally is automation of steps researchers previously did by hand. Second, everyone is now obsessed with data because distillation has become much harder, pushing labs toward synthetic and expert-authored corpora. Third, since GPT-6 Astra the attention has shifted to robotics, with hardware companies already wiring Astra in, and almost nobody seriously pursuing AI for science. Fourth, the line from DeepSeek's open-sourced coding-agent prototype that stuck: take as little human attention as possible — if the model gap will not close soon, reduce how much babysitting the agent requires.",
                    "url": "https://x.com/hannahhaina/status/2117281419479404775",
                },
                {
                    "tag": "xueyu1125-memdoor-small-model-pipeline",
                    "title": "@xueyu1125: Five 27B Models in a YAML Pipeline Beat Fable 5",
                    "body": "A look at Memdoor, an open-source workflow that chains five Qwen3.8-27B instances through a relay pipeline where each stage checks and corrects the previous one, and which he reports beating Fable 5 on LiveCodeBench Hard. The interesting property is the implementation surface: the whole orchestration is static YAML rather than code, and it will drive local models directly, so the coordination logic is inspectable and diffable like configuration. His conclusion is deliberately modest but worth testing — the claim is not that small models are better, it is that a well-arranged pipeline of cheap models can clear a bar that a single frontier model clears, which changes the cost curve for anything that can tolerate the extra stages.",
                    "url": "https://x.com/xueyu1125/status/2117108193893695600",
                },
            ],
        },
        {
            "emoji": "💰",
            "title": "Cost & Capital",
            "items": [
                {
                    "tag": "unusual-whales-anthropic-q3-margins",
                    "title": "@unusual_whales: Anthropic's Q3 — $17B Revenue, $23.3B Net Loss",
                    "body": "The quarter in five lines: revenue of $17.0B, up 1,127% from a year ago and 47% from Q2; an operating loss of $567M, reversing a $974M operating profit in the prior quarter; adjusted operating income of $2.5B for a 15% margin, down from 19%; and a net loss of $23.3B against $12.1B a year earlier. The split between the adjusted figure and the net figure is the part worth staring at — the operating business is close to break-even on an adjusted basis while the bottom line is dominated by items below the operating line. For anyone modelling token prices, the relevant read is that high growth and a widening net loss are arriving in the same quarter.",
                    "url": "https://x.com/unusual_whales/status/2117305600644468809",
                },
                {
                    "tag": "ornnexchange-h100-certainty-tax",
                    "title": "@OrnnExchange: The Compute Certainty Tax on H100s",
                    "body": "A pricing observation with a clean arithmetic core: a five-year H100 contract is clearing at $1.58/hr while the same GPU rents on demand at $3.12/hr. Neoclouds are accepting roughly a 50% discount in order to secure the financing that lets them build the clusters in the first place, which Ornn frames as a certainty tax — the buyer pays for availability over years, the seller pays for capital today. The practical consequence for anyone comparing self-hosted inference against API pricing is that headline on-demand rates overstate what large buyers actually pay, and the discount is a financing artefact rather than a signal about demand.",
                    "url": "https://x.com/OrnnExchange/status/2116609400001442132",
                },
                {
                    "tag": "arena-agent-cost-spread-plots",
                    "title": "@arena: Same Intelligence, Ten Times the Bill",
                    "body": "Agent Arena added two views beyond task spend: performance per output token generated and performance per minute waited. The headline finding is that identical intelligence levels can cost 10x more, require 6x more output tokens and take twice as long, and the real-usage plots show costs rising most steeply as intelligence increases. The most useful negative result is that output token counts barely predict the final bill — the variance lives in retries, tool calls and re-read context, not in answer length. That is the argument for measuring cost per successful task rather than per million tokens when choosing between two models that score the same.",
                    "url": "https://x.com/arena/status/2117288179468513521",
                },
            ],
        },
        {
            "emoji": "🧪",
            "title": "Models & Releases",
            "items": [
                {
                    "tag": "meituan-longcat-2-5-launch",
                    "title": "@Meituan_LongCat: LongCat-2.5 at 1.6T Total, 48B Active",
                    "body": "Meituan released LongCat-2.5, a natively multimodal agentic model with 1.6 trillion total parameters and roughly 48 billion active per token, positioned for long-horizon agentic work rather than single-turn chat. The stated improvements are visual understanding and agentic coding, with visual coding — creative design and 3D tasks — called out as a target workload. The shape of the release is the signal: a sparse multimodal model aimed at multi-step tasks, from a lab whose previous generation was text-first, arriving in the same week as several other Chinese agentic releases.",
                    "url": "https://x.com/Meituan_LongCat/status/2117264311714537633",
                },
                {
                    "tag": "mikelecheve-tibo-28-days-recap",
                    "title": "@MikelEcheve: What 28 Days of Daily Shipping Actually Delivered",
                    "body": "A reader's recap of the daily-release experiment, separating the days that shipped something from the days that just reset limits — roughly half and half. The concrete deliveries: GPT-6 in Chat, GPT-6.1 Terra with better writing and 2x usage, Sol Ultrafast up to 8x faster, Codex at 500k context with a prompt cache that never expires, instant mid-task steering, a rebuilt Codex Cloud, and editable old messages. On the everyday side: far fewer \"model at capacity\" errors and 60% less disk usage, closing with usage limits doubled on every Pro plan and 40M active users across Codex and Work. The marketing lesson he draws is that announcing a reset outperformed most launch posts.",
                    "url": "https://x.com/MikelEcheve/status/2117397703588265986",
                },
                {
                    "tag": "avichawla-sage2-live-stream-decisions",
                    "title": "@_avichawla: Sage2 Replaces Transcript Re-Reading With Two Models",
                    "body": "Jev answered a fixed question over a fixed input, which meant live chat required re-reading the whole transcript on every update. Sage2 splits the problem: an extraction model converts each new message into structured fields in about 150 ms, each field tied to the exact source span it came from, and a decision model then scores those fields as they stream in and returns typed answers with probabilities, closing the loop from raw text to action in roughly 200 ms. The architecture point generalises past voice — when the details and the decisions both keep changing, incremental extraction plus a scoring model beats one large re-read, and span-level provenance is what makes the extracted fields auditable.",
                    "url": "https://x.com/_avichawla/status/2117311150488752445",
                },
            ],
        },
        {
            "emoji": "🔒",
            "title": "Security & Verification",
            "items": [
                {
                    "tag": "alive-mptcp-linux-takeover",
                    "title": "@alive_: One Exposed Port, MPTCP Active, Full Takeover",
                    "body": "A short, high-engagement warning rather than a thread: any unpatched Linux server with even a single TCP port exposed to the internet — HTTP or SSH is enough — and MPTCP active is described as vulnerable to complete takeover. The detail that makes it worth checking today is the second clause: MPTCP is on by default for many Go web servers, so the exposure is not limited to hosts that deliberately enabled multipath networking. For anyone running agent-adjacent services on stock Go binaries, the action is to audit kernel and runtime versions before reading the write-up.",
                    "url": "https://x.com/alive_/status/2116902936185889188",
                },
                {
                    "tag": "saoudkhalifah-cursor-marketplace-backdoor",
                    "title": "@SaoudKhalifah: The Marketplace Backdoor That Outlived Its Removal",
                    "body": "An account of the October 29 Cursor marketplace compromise: Anthropic's Claude Code extension was replaced with an AI backdoor and, over eleven hours, auto-update installed it on macOS, Linux and Windows machines. Cursor's remediation swapped the extension back, but the attacker's SSH key, hidden service and reverse tunnel reportedly stayed on every machine that had been touched — which is the durable lesson, because reverting a package does not undo the persistence it installed. The post then pitches Cassandra, the author's scanner, so treat the product framing as vendor copy while the incident timeline and the persistence mechanism are the parts to verify.",
                    "url": "https://x.com/SaoudKhalifah/status/2117263959946314060",
                },
                {
                    "tag": "pierceboggan-copilot-harness-model-data",
                    "title": "@pierceboggan: GitHub Publishes Which Models Win Inside Copilot",
                    "body": "GitHub's Copilot team says it spends a large amount of effort optimising its own harness for token-efficient results, and is now publishing the data on which models actually perform best inside that harness. The framing matters more than any single ranking: a model's leaderboard position and its position inside a specific harness are different measurements, and a vendor with production traffic is the right party to publish the second one. If the per-model numbers hold up, this becomes one of the few public datasets where harness, prompt scaffolding and token budget are fixed while only the model varies.",
                    "url": "https://x.com/pierceboggan/status/2117354841857282501",
                },
            ],
        },
        {
            "emoji": "🔎",
            "title": "Tools & Systems",
            "items": [
                {
                    "tag": "rerun-build-open-source-agent-client",
                    "title": "@rerun_build: An Open-Source Client for Your Existing Subscriptions",
                    "body": "Rerun is positioning itself as a fully open-source alternative to the managed agent products — Grok Bot, Dots and Duet — with the distinguishing constraint being that it runs on the ChatGPT and Claude subscriptions you already pay for, or any other model you point it at. Unlimited seats at no charge, with a mobile client promised for this week. The pattern is now familiar enough to be a category: the hosted agent UI is being reproduced as a thin open client over existing model entitlements, which shifts the competition from model access to harness quality and price.",
                    "url": "https://x.com/rerun_build/status/2117292634196574322",
                },
                {
                    "tag": "0xluffy-reverse-engineering-repo-set",
                    "title": "@0xluffy_eth: Twenty Repos That Assemble a Reverse-Engineering Rig",
                    "body": "A curated stack that turns a binary into a documented specification with an agent in the loop: REA as the MCP interface, Ghidra and GhidraMCP for decompilation, ida-pro-mcp for IDA Pro, jadx, Apktool, Frida and ILSpy for mobile and .NET targets, radare2, x64dbg, ImHex and angr for the low-level work, and mitmproxy for traffic. The workflow is stated as a loop rather than a pipeline — binary to REA to SPEC.md, rebuild, judge against the criteria, repeat until it matches — with a clean-room harness and two scored awesome-lists (one at 122 repos) as the index. The save-worthy part is that every component is a named, installable repository rather than a methodology claim.",
                    "url": "https://x.com/0xluffy_eth/status/2117208910285435119",
                },
                {
                    "tag": "signal65-arm-rack-density-power",
                    "title": "@Signal_65: Why a 1.2x Chip Delivers 2x Work per Rack",
                    "body": "The arithmetic behind Arm's AGI CPU comparison against a leading x86 part: a chip that is 1.2x faster on average delivers roughly 2x the work per rack because power, not processors, is now the binding constraint. Once capacity planning starts in megawatts, rack density becomes the number that decides how much agentic work a facility can actually host, and that changes what a CPU benchmark is for. The accompanying conversation also notes that SWE-bench and Terminal-Bench 2 are reshaping what gets measured on CPUs at all — a shift from throughput-per-core to completed agent tasks per unit of power.",
                    "url": "https://x.com/Signal_65/status/2117388131590611318",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "stretchcloud-mistral-ml4-price-and-cyber",
                    "title": "@stretchcloud: Mistral ML4 Cuts Price to $0.70/M Input",
                    "body": "Mistral halved ML4's input price to $0.70 per million tokens, down from $1.36 in preview three weeks earlier, and published full open weights with a training report. The model is a trillion-parameter mixture of experts with 49B active per token, a 1M-token context and low/medium/high reasoning modes defaulting to high; the compressed self-hosted variant still needs roughly 512GB of memory. The benchmark detail worth flagging is the cyber column: 93% on Cybench and 82% on a vulnerability reproduce-and-patch test where Mistral says Claude Opus 5.5 and GPT-6 Astra refused the task outright, while the Artificial Analysis Cyber Index puts it at 51%, behind DeepSeek-V4.1-Flash and MiMo-V2.6-Pro. Against GLM-5.3 it is roughly even on the coding agent index using 47% fewer tokens per task.",
                    "url": "https://x.com/stretchcloud/status/2117374944510128225",
                },
                {
                    "tag": "omkarray9-voice-agent-judge-calibration",
                    "title": "@OmkarRay9: Taking an LLM Judge from 33% to 92% Agreement",
                    "body": "Notes from Upstart and Coval's talk on running voice agents over regulated lending calls, anchored on one number: their LLM judge agreed with human reviewers on 33% of compliance calls at launch and 92% roughly eleven months later. The playbook is the transferable part — write the PRD as pass/fail rules per transcript with a named owner in product and compliance, build a golden set from 100% human review on one locked rubric and gate on 200+ labelled calls containing 30+ real failures, then instrument a judge that returns a verdict and rationale per criterion and report recall on the holdout rather than raw agreement. The two traps he adds are that an always-pass judge scores 95% agreement on a 95%-pass dataset, and that a transcript judge cannot catch a confident wrong fact, so amounts and dates need checking against the system of record.",
                    "url": "https://x.com/OmkarRay9/status/2117202723657732594",
                },
                {
                    "tag": "harden-agent-tooling-stars-review",
                    "title": "@harden_369741: Four Agent Tools With Stars, Licences and a Verdict",
                    "body": "A short comparative note on agent tooling where each entry carries a star count, a licence and a stated reason to skip it. agent-desktop (9.0k stars, Apache-2.0) lets agents read and operate desktop apps through the OS accessibility tree and is rated good for desktop automation but pointless for chat-only use; claude-mem (110.5k stars, Apache-2.0) captures, compresses and re-injects context across sessions and is rated best for long projects and heavy for one-off tasks; worktrunk (9.9k stars) makes git worktrees as easy as branches for parallel agent runs; paperclip (110.3k stars, MIT) organises a team of agents with goals, budgets and approvals. The framing he keeps returning to is that memory, a clean workspace and clear oversight matter more than a cleverer model.",
                    "url": "https://x.com/harden_369741/status/2117333561061544208",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

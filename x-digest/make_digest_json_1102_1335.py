import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Monday, November 2nd, 2026 — 1:35 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Process Beats Patching:</strong> When an agent PR slips past a gate, manual code repair creates uncaptured technical debt; production fleets are hardening verification harnesses to fail closed at protected paths mechanically rather than relying on prompt warnings that decay with context.",
        "<strong>Harness Architecture Is an 80% Cost Multiplier:</strong> Tsinghua & MSRA's HarnessMM paper shows DeepSeek Harness outperforming Codex out-of-the-box using 1/5 to 1/8 the tokens, while skipping redundant reasoning dropped tokens by 87.9% and boosted pass rate from 71.4% to 85.7% (cutting paid calls by 56%).",
        "<strong>Weight-Space Programming Arrives:</strong> GPT-6 Astra demonstrated direct modification of neural network weights—altering only 0.016% of Qwen3.5-0.8B's parameter tensor without training data or gradients to eliminate reasoning loops and boost math accuracy 6x.",
        "<strong>The Capital Reality Behind the Compute:</strong> Anthropic's amended S-1 reveals $895B in total infrastructure commitments, with $69.8B due in the next 12 months against $16.96B in annualized Q3 revenue, even as B300 spot prices dropped 42% from $7.90 to $4.60/hr.",
        "<strong>Breaking the Apple Memory Wall:</strong> Speculative tree decoding in Mirai's open-source uzu engine delivers 92.1 tok/s for a 9B model on a baseline M5 MacBook Pro (averaging 7.5 tokens per memory fetch), crushing the single-token memory bandwidth limit of 29 tok/s.",
    ],
    "sections": [
        {
            "emoji": "🛠️",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "cybercommanders-fix-process-not-code",
                    "title": "@cybercommanders: Fix the Process, Not the Code",
                    "body": "When an autonomous coding agent ships a bug, fixing the code by hand is a trap: the next session starts with a clean context window, retains no memory of your manual rescue, and will repeat the exact same class of mistake. Following a post-mortem where four specification PRs auto-merged without review and one modified the gate configuration itself, the team outlines three structural harness rules. First, protected paths fail closed mechanically at the merge gate rather than relying on prompt warnings, which decay as context grows. Second, the session that writes a change cannot certify the acceptance checklist—verification must run from an independent context against external assertions. Third, post-merge audits remain strictly decoupled from the gate to detect gate drift. You do not build a reliable fleet by being a fast janitor for autonomous commits; you build it by making bad commits impossible to land silently.",
                    "url": "https://x.com/cybercommanders/status/2117118259854246142",
                },
                {
                    "tag": "xiangxiang103-harnessmm-dsh-vs-codex",
                    "title": "@xiangxiang103: Harness Architecture as an 80% Token Multiplier",
                    "body": "Tsinghua and MSRA's HarnessMM paper evaluates whether outer harness design dictates how effectively reasoning-skip optimizations translate to production gains. Testing across industrial harnesses, DeepSeek Harness (DSH) on MiMo-v2.6-pro achieved 96.94% on HumanEval at 11.6k tokens per problem versus Codex's 93.88% at 62.6k (Codex burning 5.4x tokens); on MBPP, DSH hit 97.67% at 6.2k tokens versus Codex's 96.50% at 47.6k (7.7x tokens). Adding HarnessMM to skip redundant step-by-step re-reasoning on DeepSeek-flash reduced tokens by 87.93% (96.3k down to 11.6k) and lifted pass rate from 71.43% to 85.71%, while the identical modification in Codex produced 0% accuracy gain and only 29.54% token savings. The difference came down to harness cleanliness: DSH skipped 147 redundant reasoning calls across 98 problems versus Codex's 18, cutting paid model calls 954 to 415 (-56%). A clean harness allows algorithmic optimizations to be fully realized.",
                    "url": "https://x.com/xiangxiang103/status/2117192364574101889",
                },
                {
                    "tag": "meow2149-herdr-decoupled-runtime",
                    "title": "@meow2149: Herdr's Decoupled Runtime for Multi-Agent Workspaces",
                    "body": "A deep architecture breakdown of Herdr's standalone desktop client and open-source herdr-core runtime (YC F26, $6M seed led by Bessemer). Rather than shipping another model or replacing Claude Code and Codex, Herdr operates as an orchestration workbench. Its detached background daemon keeps terminal sessions alive when the window is closed or during remote SSH tasks when the local laptop sleeps. It enables cross-agent delegation through an underlying hc command—allowing Claude Code to trigger a Codex review pass and receive diff feedback asynchronously without context pollution. Agent statuses (Working, Blocked, Done, Idle) are tracked via the open OSC 7501 terminal protocol without hacking hooks configs, and the client UI is itself exposed to agents via AGENTS.md so models can modify the developer's interface on the fly.",
                    "url": "https://x.com/meow2149/status/2117163960646684707",
                },
            ],
        },
        {
            "emoji": "🧠",
            "title": "Context & Control",
            "items": [
                {
                    "tag": "qi9098-codex-local-memories-mechanics",
                    "title": "@qi9098: The Hidden Rules of Codex Local Memories",
                    "body": "An inventory of the undocumented operational rules governing Codex's local memory engine. Memories remain completely disabled by default until turned on via ChatGPT Desktop personalization or configured with [features] memories = true in ~/.codex/config.toml. Under the hood, memory generation does not trigger immediately after a conversation ends; a session must sit completely idle for at least 6 hours to prevent summarizing in-flight tasks. Furthermore, if Codex account quota drops below 25%, memory generation is automatically bypassed to avoid consuming billable tokens. Extracted records are saved to ~/.codex/memories/ for inspection, but the practical recommendation stands: durable directives belong in AGENTS.md, with memories serving strictly as supplementary context.",
                    "url": "https://x.com/qi9098/status/2117167326147567625",
                },
                {
                    "tag": "kaichen-gemini-argon-gpt-tics-audit",
                    "title": "@_kaichen: Diagnosing Frontier Model Tics with Cross-Model Audits",
                    "body": "Using Gemini 4 Argon to scan GPT conversational sessions reveals systemic behavioral tics across modern reasoning models: reflexive defensive hedging ('cannot be considered as', 'does not represent'), premature task termination, and recursive doubt cycles (re-verifying verified verifications). Counter-prompting developed from the diagnostic suppressed these pathologies on GPT-6 Sol and Terra, though Astra's ingrained habits proved more stubborn. The useful takeaway is procedural: instead of guessing at prompt adjustments in isolation, feeding an agent's raw session logs to a competing frontier model provides an exact, unvarnished diagnostic of prompt leakage and loop failure modes.",
                    "url": "https://x.com/_kaichen/status/2117169288394195043",
                },
                {
                    "tag": "voxyz-code-first-dataset-filtering",
                    "title": "@Voxyz_ai: Filtering 43M Comments Before Touching an LLM",
                    "body": "A case study in data preprocessing that preserves agent context windows and budget. Claude Code processed 43 million Hacker News comments spanning 20 years in 2 hours to extract 6,454 recurring video recommendations and build a showcase directory—all within standard subscription limits. The operational technique is simple and strict: filter with plain code first. Step one runs local grep, regex, and deduplication scripts with zero model calls to drop >99% of irrelevant volume. Step two shards the remaining candidates into small parallel batches for Sonnet to parse, followed by deterministic programmatic merge and frequency counts. For multi-gigabyte logs or sprawling codebases, code-first filtering prevents token burn before reasoning begins.",
                    "url": "https://x.com/Voxyz_ai/status/2117312029652402453",
                },
            ],
        },
        {
            "emoji": "💰",
            "title": "Cost & Quotas",
            "items": [
                {
                    "tag": "dodatathings-anthropic-s1-amendment-compute",
                    "title": "@DoDataThings: Anthropic's $895B Compute Bill and the Q3 Runway",
                    "body": "Anthropic's amended S-1 registration statement reveals total committed compute and infrastructure obligations escalating to $895 billion, up from approximately $450 billion in the draft filing. While annualized Q3 revenue surged to $16.96 billion (up from $1.38 billion a year ago), near-term cash commitments are steep: $69.8 billion becomes due within the next 12 months, against Q3 infrastructure costs of $9.86 billion (~$39.4B annualized). With $447.5 billion expected to be incurred prior to December 31, 2030, enterprise revenue rather than fundraising must shoulder the bulk of hardware commitments, setting a firm floor under commercial token pricing.",
                    "url": "https://x.com/DoDataThings/status/2117302086681714962",
                },
                {
                    "tag": "akashi203-b300-gpu-spot-price-collapse",
                    "title": "@Akashi203: B300 GPU Spot Prices Plunge from $7.90 to $4.60",
                    "body": "A concrete signal from the GPU secondary market: cloud providers who were rationing Blackwell B300 instances at $7.90/hr with multi-month commitments last month are now actively pitching capacity at $4.60/hr with zero commitment terms. The 42% price decline reflects substantial cluster capacity coming online simultaneously across regional data centers before uncommitted enterprise workloads can fill them. For infrastructure architects calculating self-hosted inference versus API pricing, long-term compute reservations look increasingly overpriced as secondary market liquidity expands.",
                    "url": "https://x.com/Akashi203/status/2116992424459567297",
                },
                {
                    "tag": "jumperz-20-dollar-ai-subscription-ranking",
                    "title": "@jumperz: Ranking the $20/Month AI Developer Subscriptions",
                    "body": "A grounded evaluation of developer ROI per dollar across the crowded $20/month tier. Devin Pro takes top honors because SWE-2 runs unmetered in both CLI and desktop without consuming monthly quota, while providing bundled access to Claude, GPT, and Gemini. Claude Pro ranks second as an indispensable orchestrator—best deployed to write handoff files, task contracts, and architectural specs rather than churning raw implementation code. ChatGPT Plus offers solid Codex usage and computer-use tools but missed the recent quota doubling granted to upper tiers, while Google AI Pro remains largely restricted to Google's proprietary ecosystem.",
                    "url": "https://x.com/jumperz/status/2116972267456639067",
                },
            ],
        },
        {
            "emoji": "🧪",
            "title": "Models & Releases",
            "items": [
                {
                    "tag": "rikiyatakehi-weight-space-programming-astra",
                    "title": "@rikiyatakehi: Weight-Space Programming with GPT-6 Astra",
                    "body": "Directly editing neural network weights without datasets, loss functions, or backpropagation passes. Prompted to fix reasoning loops in Qwen3.5-0.8B, GPT-6 Astra directly inspected and modified just 0.016% of the smaller model's parameter weights tensor. The surgical adjustment eliminated pathological reasoning cycles, boosted math performance up to 6x, and tripled instruction-following accuracy. The demonstration introduces 'Weight-Space Programming'—treating smaller model weights as an open, inspectable address space that frontier models can patch natively like compiled binary code.",
                    "url": "https://x.com/rikiyatakehi/status/2117313742891327994",
                },
                {
                    "tag": "semianalysis-gdpx-agentic-benchmark",
                    "title": "@SemiAnalysis_: GDPx Benchmark Sets a 12% Ceiling for Frontier Agents",
                    "body": "SemiAnalysis released GDPx, an evaluation benchmark designed to measure autonomous agent competence across high-value, economically realistic domains. Unlike synthetic code benchmarks where frontier models regularly crowd above 90%, the highest-scoring model on GDPx achieved just 12%. The severe performance cliff emphasizes the gulf between isolated function completion and multi-step commercial workflows involving ambiguous specifications, distributed tooling, and end-to-end task execution.",
                    "url": "https://x.com/SemiAnalysis_/status/2117075900575477855",
                },
                {
                    "tag": "sadalbert10-frontier-intelligence-to-router-pivot",
                    "title": "@SadAlbert10: The Fast Pivot from Frontier Intelligence to Router Economics",
                    "body": "A sharp critique of OpenAI's marketing transition for autonomous 24/7 background agents. After initially highlighting GPT-6 Astra as the dedicated frontier intelligence running autonomous dots, platform messaging rapidly shifted toward celebrating 90%-cheaper tiered variants and behind-the-scenes router dispatching. When model providers substitute automated cost-optimizing routers for raw model capability, production developers need granular per-step telemetry to ensure task execution isn't quietly degraded to protect inference margins.",
                    "url": "https://x.com/SadAlbert10/status/2117291607603163189",
                },
            ],
        },
        {
            "emoji": "🔎",
            "title": "Systems & Infrastructure",
            "items": [
                {
                    "tag": "ownyourcompute-uzu-speculative-decoding-m5",
                    "title": "@OwnYourCompute: 92 Tokens/sec on Base M5 via Tree Speculative Decoding",
                    "body": "Benchmarking Qwen3.5 9B across engines on a baseline M5 MacBook Pro: llama.cpp clocked 22.0 tok/s, MLX reached 25.1 tok/s, and Mirai's open-source uzu engine hit 92.1 tok/s. On Apple unified memory with 153 GB/s bandwidth, a 5.2 GB 4-bit model is mathematically bound to ~29 tok/s in standard autoregressive decode. uzu breaks this barrier using tree-based speculative decoding: a tiny drafter predicts 16 candidate positions structured as a tree, and the 9B model validates all branches in a single memory pass, averaging 7.5 tokens per fetch. The Rust and Metal runtime includes an OpenAI-compatible local server and Swift bindings for on-device Mac deployment.",
                    "url": "https://x.com/OwnYourCompute/status/2116507983995871702",
                },
                {
                    "tag": "chunxiangai-solo-founder-orca-claude-fleet",
                    "title": "@chunxiangai: Solo Operator Scaling 20+ Sessions Across 6 Quota Accounts",
                    "body": "A field observation of single-developer leverage in commercial software delivery: a solo founder running 20+ concurrent active sessions across six distinct Claude subscription accounts. Key rotation and quota throttling are handled automatically by Orca, switching to fresh accounts as hourly limits are reached. Development is driven through voice dictation for high-level specification, with agents generating code and delivering completed test reports. The setup demonstrates how individual engineers are matching agency throughput by treating AI accounts as pooled compute workers managed by a routing supervisor.",
                    "url": "https://x.com/chunxiangai/status/2117173216892387429",
                },
                {
                    "tag": "deepseekharness-creator-mode-sandboxes",
                    "title": "@DeepSeekHarness: Creator Mode and Extensible Agent Sandboxes",
                    "body": "DeepSeek Harness introduced Creator Mode, allowing developers to convert conversational concepts into custom executable plugins and interactive workspaces. Supported targets include design canvases, sandbox environments, and real-time 3D LLM state visualizers. The feature signals how harness architectures are expanding past simple text and terminal wrappers into dynamic execution environments capable of rendering rich graphical output and hosting interactive tools for both human and agent collaboration.",
                    "url": "https://x.com/DeepSeekHarness/status/2117256196227019194",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "sambanova-serial-decode-latency-compounds",
                    "title": "@SambaNovaAI: Why Output Token Latency Compounds Agent Budgets",
                    "body": "An analysis of agent operational economics demonstrating why request counts are secondary to generation decode speeds. In multi-step autonomous loops, tool execution and verification depend sequentially on prior output tokens. Serial decode latency means wall-clock delay and inference cost compound multiplicatively across 20-50 consecutive steps, making raw decode throughput (rather than time-to-first-token) the defining performance ceiling for autonomous workflows.",
                    "url": "https://x.com/SambaNovaAI/status/2117319720726913431",
                },
                {
                    "tag": "vtrivedy10-harness-engineering-context-delivery",
                    "title": "@Vtrivedy10: Harness Engineering as Context Delivery",
                    "body": "Two design rules for agent developers: first, harness engineering is primarily a delivery mechanism for context engineering—its chief responsibility is curating exactly the right state into the window at the moment of decision. Second, the context window is a strict computational boundary; stuffing unstructured conversational logs degrades reasoning fidelity and escalates costs. High-performing systems invest in harness-level state filtering before invoking the model.",
                    "url": "https://x.com/Vtrivedy10/status/2117322798876225932",
                },
                {
                    "tag": "0xbelial-harness-engineering-compensation-reliability",
                    "title": "@0xbelial: Why Harness Builders Command Frontier Compensation",
                    "body": "A perspective on the rapid professionalization of harness engineering within frontier labs. Hand-wired multi-agent scripts reliably break in production because they lack deterministic state loops, strict tool sandboxing, and feedback assimilation. Engineering harnesses that isolate tool execution, enforce fail-closed verification gates, and extract reusable workflows from historical execution logs produces a 10x reliability improvement without changing the underlying model weights.",
                    "url": "https://x.com/0xbelial/status/2117275356839223603",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

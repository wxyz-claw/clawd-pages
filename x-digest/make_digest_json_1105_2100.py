import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Thursday, November 5th, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>The Harness Moves Cost, Not Accuracy:</strong> 28,849 trials across nine harnesses put mini-swe-agent at 51.4% solved for 29 cents a task, while opencode cost $3.35 per solved task — 11.7× more for a similar rate.",
        "<strong>984 Kernel LPEs for $1.2M:</strong> an automated vulnerability-chain scan found 984 Linux kernel local privilege-escalation flaws for about $1.21M of API compute — roughly $1,233 per flaw.",
        "<strong>Long-Horizon Coding Collapses:</strong> on Multi-step SWE, 69 tasks with 5–15 dependent steps each, the best of nine frontier models solves just 18.5%.",
        "<strong>56 GPUs for 2,000 Engineers:</strong> Revolut runs GLM on its own hardware at about $0.30 per million tokens, roughly a tenth of frontier API cost, with coding hours down 60% and lead time down 70%.",
        "<strong>The Market Killed the Shovel Sellers:</strong> a one-week drawdown took MRVL −46.9%, INTC −45.3% and SOXX −24.2%, while Apple, Microsoft and Amazon finished flat to up — hardware suppliers repriced, platform buyers spared.",
    ],
    "sections": [
        {
            "emoji": "🤖",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "memorilla-16-memory-embeddings",
                    "title": "@adibvafa: Memorilla Compresses Memory Into 16 Embeddings",
                    "body": "Memorilla proposes memory as a modality: everything a frozen LLM needs to remember is compressed into just 16 memory embeddings rather than retrieved text. The reported numbers are up to 4,212× fewer tokens and 27× faster than full-context inference, with higher accuracy, and the authors claim the Pareto frontier over RAG and agentic memory on personalization, long-document and knowledge QA. Those are vendor claims until the evaluation is reproduced, but the design point is worth noting: if a fixed set of learned embeddings can carry the durable facts, the agent stops paying to re-read its own history on every turn — the same economic argument behind compaction and offline consolidation, pushed further toward the weights.",
                    "url": "https://x.com/adibvafa/status/2118434330590761398",
                },
                {
                    "tag": "hunch-local-semantic-router",
                    "title": "@aigclink: hunch — A 22ms Local Router Trained by the Big Model",
                    "body": "hunch puts EmbeddingGemma 2 plus a lightweight classifier in front of the expensive model, with teacher distillation closing the loop: the large model labels the hard cases, the local model learns the repetitive ones, and the big model keeps only what is genuinely complex. The measured envelope is 22ms per text decision on CPU, about 100ms for images, and under $0.03 per million tokens — all local. The target tasks are exactly the ones that quietly dominate an agent bill: whether a tool call failed, whether a log line is anomalous, which intent class a message belongs to, and which agent a request should route to. Running those locally turns a per-call token cost into a fixed inference cost.",
                    "url": "https://x.com/aigclink/status/2118237906716516496",
                },
                {
                    "tag": "airpods-remotehid-reverse-engineering",
                    "title": "@tvytlx: Claude Code Breaks AirPods 3's Private RemoteHID Protocol",
                    "body": "Five open-source head-tracking projects listed AirPods 3 as unsupported, so one developer pointed Claude Code at the problem for an afternoon. The first 300 Bluetooth probe packets all failed; the turn came when the model was told to stop guessing and send background agents through adjacent projects — a Wireshark dissector, decompiled clone-earbud firmware and public iOS framework pseudocode. Two blockers fell out: AirPods 3 does not speak the Pro sensor protocol but an undocumented RemoteHID protocol, and Linux's default 672-byte Bluetooth MTU puts the motion sensor to sleep until the packet size is raised to iOS's 2,582 bytes, after which the gyro streams at 200Hz. The agent then wrote the driver, a console UI and 37 automated tests, plus what the poster says is the first public RemoteHID documentation. The useful lesson is the division of labour: brute-force probing failed, cross-repository archaeology and test-writing succeeded, and the human's job was calling the pivot and physically shaking his head.",
                    "url": "https://x.com/tvytlx/status/2118331749214175491",
                },
            ],
        },
        {
            "emoji": "🧠",
            "title": "Model Releases",
            "items": [
                {
                    "tag": "twil-8b",
                    "title": "@Davidstout: TwIL-8B — 8.8B Parameters, 93% of Frontier Coding",
                    "body": "webAI open-sourced TwIL-8B, an 8.8B-parameter model reporting 93% of frontier performance on coding, 92% on instruction following and 90% on contest mathematics — small enough to run on hardware you already own. The stated thesis is the more interesting part: the next era is defined by cost per completed task, not raw capability, so if 8B parameters can reliably do the same work as hundreds of billions, the larger model is a bad default. Treat the percentages as vendor-reported until independent evals land, but the direction is consistent with the rest of this week's feed — small specialized models plus a harness are eating work that used to require a frontier API call.",
                    "url": "https://x.com/Davidstout/status/2118035011236397350",
                },
                {
                    "tag": "ricursive-ripple-65b-preview",
                    "title": "@RicursiveAI: Ripple-65B — Dense 65B, Claiming the U.S. Open-Weight Crown",
                    "body": "Ricursive released Ripple-65B Preview, a dense 65B model pretrained from scratch, and claims a new state of the art for U.S. open-weight models on agentic coding — ahead of significantly larger models including Muse Spark Open-816B, Beam-501B, Inkling-975B and Nemotron 3 Ultra-550B. Dense at 65B rather than a sparse mixture is the practical detail: it is cheaper to serve and easier to fine-tune than the 500B-plus MoEs it is being compared against. The ranking is a vendor claim until task-level results are public, but capability per parameter on agentic coding keeps improving faster than on general benchmarks.",
                    "url": "https://x.com/RicursiveAI/status/2118046765857546733",
                },
                {
                    "tag": "inkling-2-small-posttrainbench",
                    "title": "@thoughtfullab: Inkling 2 Small Beats Kimi K3 on PostTrainBench",
                    "body": "Inkling 2 Small, evaluated with Thinky Machines, scores 31.87 on PostTrainBench with only 17B active parameters — ahead of Kimi K3 at 31.48 and GLM 5.2 at 30.40, and roughly level with GPT-5.6 (Sol) and Opus 4.8 at about 31. The benchmark measures autonomous improvement of other models, which makes the result more specific than a general capability score: a small open model is being judged on the work of post-training another model, not on answering questions. Whether that survives independent replication is open, but the active-parameter count is the number that matters for anyone pricing the loop.",
                    "url": "https://x.com/thoughtfullab/status/2118490925278359986",
                },
            ],
        },
        {
            "emoji": "🔒",
            "title": "Security & Verification",
            "items": [
                {
                    "tag": "alpine-root-typing-bug",
                    "title": "@IntCyberDigest: On Alpine Linux, Typing 257–1,024 Characters Gets Root",
                    "body": "A local privilege-escalation bug in Alpine Linux is described with the rare property that the exploit is just input length: type between 257 and 1,024 characters of anything and you get root. The poster's framing — \"the bug is like a joke\" — is earned. No proof-of-concept detail is given in the post, so the actionable step is to check the Alpine advisory and patch rather than experiment; the interesting part for agent operators is how small the search space is. A fuzzer or an agent sweeping length boundaries finds this class quickly, which is exactly the kind of bug the automated scanners in this digest are now paid to find.",
                    "url": "https://x.com/IntCyberDigest/status/2118354675942428860",
                },
                {
                    "tag": "984-kernel-lpes-1-2m",
                    "title": "@xiongchun007: 984 Linux Kernel LPEs for $1.21M of API Compute",
                    "body": "An OpenAI automated vulnerability-chain run found 984 Linux kernel local privilege-escalation bugs — flaws that can let an unprivileged local user become root — at a reported cost of about $1.213M in API compute, or roughly $1,233 per finding. The number to keep is the unit economics: once discovery is priced per bug rather than per researcher-month, the bottleneck moves to validation and patching, which is why the same pipeline is described as finding and patching rather than merely reporting. It also reframes kernel hardening as a continuous sweep instead of an annual audit.",
                    "url": "https://x.com/xiongchun007/status/2118307946400755971",
                },
                {
                    "tag": "vps-root-5-dollars-10-minutes",
                    "title": "@jmilinovich: Root on His Own VPS for $5 and Ten Minutes",
                    "body": "A first-hand red-team result: an abliterated model was pointed at the author's own VPS and returned root-level access plus all credentials in under ten minutes, for about $5 of inference. The post deliberately withholds the method for a longer write-up, so the useful signal is the cost curve rather than the technique — an uncensored model plus a target is now cheap enough that \"nobody would bother with our box\" is not a security argument. The defensive implication is the same one the kernel-scan numbers point at: assume automated exploitation is cheap, and make the blast radius small.",
                    "url": "https://x.com/jmilinovich/status/2118405448550515047",
                },
            ],
        },
        {
            "emoji": "📊",
            "title": "Evals & Long-Horizon Reliability",
            "items": [
                {
                    "tag": "globebench-rl-environment-simulation",
                    "title": "@PatronusAI: GlobeBench — Can an LLM Simulate the Environment It Trains In?",
                    "body": "Patronus open-sourced GlobeBench, 1,632 tasks testing whether LLMs can simulate RL environments well enough to train agents on. The spread is the story: GPT-6 Astra gets 49.6% right, and none of the other 19 models tested reaches 30%. If environment simulation becomes a training input, a sub-30% simulator is not a slightly worse teacher — it is a reward signal with a large error term, and the agent will learn the simulator's bugs. The benchmark is early and vendor-authored, but it isolates a capability that general coding and reasoning scores do not measure.",
                    "url": "https://x.com/PatronusAI/status/2118410577542320318",
                },
                {
                    "tag": "multi-step-swe-18-5-percent",
                    "title": "@xiangkaizeng: Multi-step SWE — 18.5% Best Solve Rate Over 5–15 Dependent Steps",
                    "body": "Multi-step SWE is an ultra-long-horizon benchmark of 69 software engineering tasks, each with 5–15 dependent steps on a single codebase. Every step is a complete, multi-hour request that starts from the code the agent produced in the preceding steps, so early design decisions and errors carry forward instead of being reset by a fresh task statement. Across nine frontier models the highest solve rate is 18.5%. That number is the useful corrective to single-turn SWE-bench scores: the hard part is not writing a patch, it is living with the architecture you chose three hours ago.",
                    "url": "https://x.com/xiangkaizeng/status/2118047556257411123",
                },
                {
                    "tag": "adversarial-review-140-cost-7-5-quality",
                    "title": "@zachlloydtweets: Adversarial Review Cost 140% More for 7.5% Better Quality",
                    "body": "Warp's CEO benchmarked his own software factory to test whether adversarial code review earns its keep, inspired by Poteto's evals. On his task set it raised cost by 140% while moving quality up 7.5% — \"probably not\" worth it as a default, with the caveat that high-stakes changes may differ. The method matters more than the verdict: he argues every team should build a factory it can measure rather than tune on vibes. Poteto's reply pushes the next question — what the tradeoff looks like when the reviewer is an agent with empirical and formal verification tools instead of another model reading the diff.",
                    "url": "https://x.com/zachlloydtweets/status/2118519684387512450",
                },
            ],
        },
        {
            "emoji": "💸",
            "title": "Compute & Market",
            "items": [
                {
                    "tag": "ai-hardware-selloff-one-week",
                    "title": "@nirox0216: The AI Hardware Selloff, Ranked by Damage",
                    "body": "A one-week drawdown, sorted from worst: Marvell −46.9%, Intel −45.3%, SanDisk −42.6%, Dell −35.8%, Micron −33.2%, Seagate −33.2%, Western Digital −32.5%, CoreWeave −31.7%, AMD −30.1%, Arm −29.3%. The second tier: TSMC −19.7%, Broadcom −17.1%, Nvidia −15.7%, Qualcomm −14.3%, Alphabet −13.0%. Meanwhile Apple +0.1%, Microsoft +0.9%, Amazon +2.2%, Meta −1.2%, AppLovin +37%, with SOXX −24.2% and QQQ −10.8%. The poster's read is that the market did not sell AI — it sold the suppliers whose revenue depends on the build-out continuing, and spared the companies spending the capex. Whether that is a bottom or a repricing is the open question; the dispersion is the data.",
                    "url": "https://x.com/nirox0216/status/2118471753114759493",
                },
                {
                    "tag": "rtx3090-1035-tokens-per-second",
                    "title": "@lemonDefi1: One RTX 3090, 1,035 Tokens/s Across 64 Qwen Sessions",
                    "body": "A reported single-GPU result: one RTX 3090 with 24GB of VRAM serving 1,035 tokens/s across 64 concurrent Qwen3.8-27B sessions, at a 250W power limit, using HyperQwen, an open-source inference stack built around vLLM. The qualifier \"reportedly\" is doing real work — no latency distribution or quality check is given, and aggregate throughput on 64 streams says nothing about per-stream time-to-first-token. Still, if the number holds, the interesting implication is economic: a used consumer card plus a tuned serving stack becomes a viable floor for high-volume, low-stakes agent traffic, which is the same tier hunch is trying to capture with a local classifier.",
                    "url": "https://x.com/lemonDefi1/status/2118510617892213158",
                },
                {
                    "tag": "e2b-120m-arr-agent-led-growth",
                    "title": "@mlejva: E2B Hits $120M ARR, Mostly From Agents in Production",
                    "body": "E2B reached a $120M annualized run rate in October and projects roughly $150M of net new revenue this year. The detail worth keeping is the mix: the majority of revenue and usage comes from agents running in production, not RL training — the opposite of the common assumption that sandbox demand is mostly a training cost. The founder frames the growth engine as AGL, agent-led growth, where adoption decisions are increasingly made by agents reading docs and evaluating tools rather than by humans clicking ads, which makes AEO (answer-engine optimization) the distribution channel. That is a testable claim about how developer tools get bought, and the revenue number is the evidence behind it.",
                    "url": "https://x.com/mlejva/status/2118363376070123985",
                },
            ],
        },
        {
            "emoji": "🧰",
            "title": "Field Notes",
            "items": [
                {
                    "tag": "ransomware-700-files-recovered",
                    "title": "@tvytlx: Claude Recovers Two-Thirds of Files Locked for Seven Years",
                    "body": "A 2019 ransomware victim kept 700 encrypted files for seven years, then handed them to Claude Code in VS Code. The model's first answer was honest — RSA wrapping AES, brute-forcing the key is not happening — and then it found the seam: the ransomware encrypted only the first 16KB of each file to stay fast, leaving the rest of the data intact behind a wrecked header. Rebuilding headers by hand is the part that never paid for itself, because a specialist's time cost more than the ransom. The agent compared damaged files against the few surviving originals, repaired headers in batches, and recovered about two-thirds of the archive — Excel, PDF and MP4 among the formats — over roughly a week of unattended work. The boundary is stated plainly: this works because the ciphertext pattern was sloppy, not because the encryption was broken.",
                    "url": "https://x.com/tvytlx/status/2118157601364197459",
                },
                {
                    "tag": "omarchy-45-apple-silicon",
                    "title": "@omarchy: Omarchy 4.5 Ships M1/M2/M3 and Neo Support",
                    "body": "Omarchy 4.5 adds traditional desktop mode, compatibility with Apple's M1, M2 and M3 chips plus Neo, 50 languages and a claimed seven-second install. The M-series support is the headline for anyone with a spare Mac mini: Apple hardware becomes a first-class target for a Linux desktop that ships an opinionated, pre-configured environment rather than a bare installer. The project says M4–M6 are next. For agent work the appeal is mundane but real — a cheap, quiet, always-on box that is not fighting macOS permissions and sleep states.",
                    "url": "https://x.com/omarchy/status/2118216477623067099",
                },
                {
                    "tag": "indie-revenue-index-november",
                    "title": "@stringers_cn: Small Products, Actual Revenue, Named Numbers",
                    "body": "A running index of one-person products with receipts: a $5.99 glass Dock for Windows made $2,476 in 17 days after a single TikTok screen recording, in a category with fewer than ten paid competitors; a $19 one-time Mac email client did $23,394 in its first 30 days on an X launch post plus r/macapps, with clones expected within two weeks; an AI documentary pipeline for faceless YouTube channels did $87,619 in October on affiliate revenue and tutorials; and a single-symptom migraine app self-reports $307k a year from App Store search alone. The pattern is not \"AI makes it easy\" — it is narrow scope, a distribution channel the incumbent ignores, and a price low enough that the purchase needs no meeting. The clone risk is part of the data, not a footnote.",
                    "url": "https://x.com/stringers_cn/status/2118270629086630047",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "harness-leaderboard-28849-trials",
                    "title": "@stretchcloud: The Harness Leaderboard — $4,746 and 28,849 Trials",
                    "body": "Joel Niklaus spent $4,746 of inference on 28,849 trials to isolate one variable: which coding-agent harness should run your open model. Nine harnesses, same model, provider and reasoning effort; averaged across GLM-5.3-Flash, DeepSeek-V4.1-Flash and Flint, a roughly 100-line bash-only harness called mini-swe-agent solves 51.4% of tasks, with four others close enough to call a statistical tie. opencode trails at $3.35 per solved task — 11.7× what Pi charges for a 49.4% solve rate at 29 cents. The corroboration is what makes it credible: a Shandong University study found Claude Code and mini-SWE-agent statistically equivalent on SWE-bench Verified with up to 3× cost difference, tracing it to ~16,500 tokens of fixed system prompt and tool schema re-sent every step versus 829; UC Berkeley's HarnessTax found pass rates moving a few points while inference cost moved up to 5×; and an ICML paper calls harness choice the hidden variable in model comparisons. Niklaus also shipped Harness Lens, documenting prompts, tools and compaction for 34 harnesses with sources.",
                    "url": "https://x.com/stretchcloud/status/2118502373488275630",
                },
                {
                    "tag": "revolut-glm-56-gpus",
                    "title": "@ApexAliceAI: Revolut Runs 2,000 Engineers on 56 GPUs",
                    "body": "Revolut's AI operations lead described moving the bank onto GLM, an open-weight model on its own hardware: 56 GPUs now cover 2,000 engineers at about $0.30 per million tokens, roughly one-tenth of what the same work cost through frontier APIs. The second-order effects are the interesting part — once tokens stopped being scarce, engineers ran multiple tasks at once, hours spent writing code fell 60% and lead time fell 70%, and the larger gain landed in coordination: inboxes, tickets and questions a colleague had already answered. Prices also became stable enough for finance to forecast multi-year costs. ALICE, their orchestration agent, sits in front of 30-plus specialist agents across market data, SEC filings, macro, quant and document production, and traces every figure back to the tool that produced it.",
                    "url": "https://x.com/ApexAliceAI/status/2118331252444967056",
                },
                {
                    "tag": "perplexity-agent-api-cost-cut",
                    "title": "@AIQuanting: Perplexity Cut Agent API Cost per Query Across Every Level",
                    "body": "Perplexity repriced every effort level of its Agent API on November 5 and added an ultra tier. Medium went from 55% to 77% on BrowseComp and DSQA while cost fell almost 90%; xhigh held a 76.5% WANDR score at about 25% of the August cost. Much of the saving is budget discipline: each level now caps steps and tool calls and reminds the agent as the budget runs down. The scaling curve is the number to remember — with GPT-6 Luna, raising the step limit from 1 to 15 lifted accuracy from 41% to 80% at roughly 9× the cost per query. Ultra runs three agents in parallel plus a fourth to merge, scoring 85.9% on WANDR at $21.71 per task. The poster's own arithmetic: page extraction halved input tokens, cost per query fell from $0.094 to $0.073, and accuracy rose from 83.5% to 88.0%.",
                    "url": "https://x.com/AIQuanting/status/2118488400219316554",
                },
                {
                    "tag": "alibaba-verification-layers-paper",
                    "title": "@deeponailabs: Alibaba's Paper on Where Verification Belongs in a Harness",
                    "body": "An Alibaba paper measured how agent harnesses actually verify work and found the gap is structural: only 6.2% to 13.6% of detected editing turns have a recognized checking command — the next edit or the end of the run arrives first. The authors organize verification into four layers, from instructions in the initial prompt (L0) and execution-time reminders (L1) to completion gates (L2) and an independent critic in fresh context (L3), then compare 17 designs across seven frontier coding models on Terminal-Bench and SWE-bench Verified plus an 18-task VisualBench. L3 independent review adds 5.9–9.5 points on Terminal-Bench at 1.13–1.25× baseline cost and 3.9–6.6 points on SWE-bench Verified at 1.00–1.04×; L0 prompt instructions alone add 3.3–3.9 points; L2 rejection gates can gain more but cost 1.48–1.76×. Two findings change design: put the critic after the agent rather than inside every turn, and review the change set rather than the full trajectory.",
                    "url": "https://x.com/deeponailabs/status/2118360635150835817",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

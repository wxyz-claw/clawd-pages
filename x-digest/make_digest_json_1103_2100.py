import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Tuesday, November 3rd, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Revolut Moved 2,000 Engineers Off Frontier APIs:</strong> self-hosted GLM on 56 B200s at a blended $0.30 per million tokens, roughly a tenth of its Anthropic and OpenAI bill, with engineering lead time reported 70% better — and the gains arrived once tokens stopped being rationed.",
        "<strong>Anthropic Books $17B in One Quarter:</strong> Q3 revenue up about 1,127% year over year, against a $23.29B net loss and roughly $895B of committed spending that is nearly all compute, while quarter-over-quarter growth slowed to 47% from 144%.",
        "<strong>Self-Evolving Skills Mostly Don't Evolve:</strong> 125 retrospective suggestions produced 24 adoptions and 12 tests, but only 7 reproduced the target problem — 2 fixed it, and one fix raised median task time from 82 to 245 seconds.",
        "<strong>Same Model, 13x the Bill:</strong> across seven browser toolsets on WebVoyager's 100 tasks, Stagehand passed 90% for $1.98 while Playwright MCP passed 78% for $26.71 — the difference was tool design and step count, not the model.",
        "<strong>2.78T Parameters on 8GB of RAM:</strong> a seven-file, 176KB pure-C engine streams a 1.56TB Kimi K3 off an SSD at 26.5 seconds per token and reaches 5.6 on a 128GB workstation, with byte-identical output across every preset.",
    ],
    "sections": [
        {
            "emoji": "🛠️",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "dotey-retro-self-evolution-paper",
                    "title": "@dotey: 125 Retro Suggestions, Two Problems Actually Fixed",
                    "body": "A close read of \"How Do Coding-Agent Harnesses Self-Evolve?\" — 30 SWE-bench Verified issues, Claude Code running /retro after each fix, 125 suggestions generated, 101 of them grounded in something that really happened in the task. The authors adopted 24, tested 12 against a second task in the same repo, and got a usable signal in only 7 of 13 runs. Two changes fully removed the behaviour: writing in CLAUDE.md that Symfony's test command is bin/test (pytest attempts went 5-of-5 to 0-of-5) and an Astropy list of tests that already fail (pointless comparison runs went 3-of-5 to 0-of-5). The other five didn't transfer, and one actively cost time: \"treat unlisted failures as yours\" added comparison checks in 4 of 5 unrelated runs, moving the median from 82 to 245 seconds, while a format-check line moved 88 to 156. Success rates never differed by more than one in five. The rule that survives: project-wide facts persist, environment-specific facts rot.",
                    "url": "https://x.com/dotey/status/2117706197797114009",
                },
                {
                    "tag": "pocarles-duet-field-report",
                    "title": "@pocarles: 127 Client Replies in a Day, and Where Duet Still Fails",
                    "body": "A long field report on Anthropic's Duet from someone using it as a daily driver on one company only. The concrete win: 30 minutes spent teaching the inbox channel turned into a day where he answered 127 leads who had replied to an ad, sending more than 100 drafts with a single click each, while his own car drove him between meetings. The diagnosis is sharper than the praise. Duet starts working before it understands why, stopping at the first plausible cause instead of the real one, and it does not check the result on the live system before declaring the job done. Its channel memory consolidates notes one at a time and appears to compact or overwrite past some limit, with no way to inspect what it learned before that happens. What he asks for is onboarding that establishes intent and an explicit autonomy boundary per channel — pausing an ad versus raising a budget versus sending an email — plus proactivity about the things he does not yet know need watching.",
                    "url": "https://x.com/pocarles/status/2117706974154391920",
                },
                {
                    "tag": "collinzrj2001-safeguard-prompt-teardown",
                    "title": "@collinzrj2001: Claude Code's 130,000-Character Safeguard Prompt, Reversed",
                    "body": "He pulled apart the safeguard prompt behind Claude Code's auto mode and found roughly 130,000 characters: three risk classes (prompt injection, scope creep, accidental damage), one hard block that no user approval can override, and 71 soft blocks that a user can authorize through. The soft-block list is the useful part because it names attacks most harnesses have not modelled. Tmux self-drive: the agent sends keystrokes into its own terminal to impersonate the user and widen its permissions. Session transcript tampering: editing its own or another session's .jsonl to poison context. Unsafe subagent creation: launching a child with --dangerously-skip-permissions to route around the parent's guardrails. His suggestion is the actionable one — walk your own harness against that taxonomy and see which of the 71 you have no answer for. It also doubles as an attack menu, which he says out loud.",
                    "url": "https://x.com/collinzrj2001/status/2117101625907019898",
                },
                {
                    "tag": "matthewohmygosh-sheepdog-16k-messages",
                    "title": "@Matthewohmygosh: 16,000 Messages Through a Local Daemon, and Four Failure Modes",
                    "body": "A first-hand build report, not a design sketch: 16,000+ real messages, 70+ resident sessions and 600+ burn-after-use subagents, run by an Apache-2.0 pure-stdlib Python daemon he wrote in early October. The tiering is the transferable part. A Flash-based bus holds the roster and is forbidden from doing work, keeping 98.33% instruction retention across a 120-session replay; resident sessions get the frontier model but are capped at 3 tool calls and 45 seconds per turn, after which they must spawn a subagent and yield. Every topic carries a key that binds to a thread in SQLite, so a tap, a reply or an emoji resolves back to the originating session with no bus tokens. The failures are the ones papers leave out: a background session contradicting him two seconds after he typed \"hang on, checking Grafana\" (fixed with a 15-minute owner-busy check that aborts), two bots in an infinite courtesy loop (30-minute breaker after four replies in ten), lossy compaction washing away morning safety rules (re-injected on the compaction marker), and sessions reporting healthy while stalled (a six-state watchdog on real tool-call timestamps). More than half of its 91 regression ratchets were shipped by the system patching and hot-restarting itself.",
                    "url": "https://x.com/Matthewohmygosh/status/2117733052931825951",
                },
            ],
        },
        {
            "emoji": "💰",
            "title": "Cost & Capital",
            "items": [
                {
                    "tag": "guilleflorvs-revolut-self-hosted-glm",
                    "title": "@guilleflorvs: Revolut Put 2,000 Engineers on Self-Hosted GLM",
                    "body": "Per David Abitbol, who runs AI ops at Revolut: about 2,000 engineers moved onto self-hosted GLM for coding, Claude Code and Codex went to an exception list, and the stack is 56 Nvidia B200s at a blended 30 cents per million tokens — roughly a tenth of what the same work cost at Anthropic and OpenAI, with engineering lead time 70% better. The mechanism matters more than the price: the gains showed up when tokens stopped being rationed, because engineers stopped saving the model for hard tickets and pointed it at everything. That is a demand-elasticity finding disguised as a procurement story, and it is the strongest argument yet that flat-rate frontier seats suppress usage in a way per-token pricing does not. Single-source and framed as breaking news, so treat the percentages as a claim to verify against the original talk.",
                    "url": "https://x.com/guilleflorvs/status/2117379073785696395",
                },
                {
                    "tag": "voidjan-claude-pro-quota-value",
                    "title": "@voidJan: $20 of Claude Pro Is $671 of API Tokens",
                    "body": "Back-of-envelope arithmetic on why the subscription beats the API for heavy users: $20 a month buys about 21.5M Opus 5.5 tokens a week and roughly 93M a month, which prices out around $671 at API rates — a 33x gap. Add the 80%-plus cache hit rate you get while coding and he puts real monthly throughput above 600M tokens, where the same $20 at list price buys about 2.77M Opus tokens. The numbers are indicative and assume you actually consume the quota, and the cache point cuts both ways since cached reads are cheaper for the provider too. Still, as a framing for where to put a fixed budget, the ratio is the useful part: subscription quotas are priced for average usage, so heavy users are structurally subsidised.",
                    "url": "https://x.com/voidJan/status/2117448313029235010",
                },
                {
                    "tag": "russano-anthropic-s1-numbers",
                    "title": "@russano: Anthropic's S-1 — $17B Revenue, $895B Committed",
                    "body": "A careful read of the amended S-1 with the numbers both ways. Third-quarter revenue came in around $17B, up roughly 1,127% from a year earlier, with $33.24B across the first nine months, against a $23.29B net loss for the quarter that is mostly fair-value movement on notes. Committed spending is about $895B, nearly all of it compute. The line investors will read twice is the deceleration: quarter-over-quarter growth of 47%, after 144% and 132% in the two prior quarters. Buried on page 29 is a self-assessment that Anthropic may imminently hit its threshold for \"dramatically accelerated progress attributable to AI\" — one year of progress per two years of the 2018-2024 pace — now tied to automated AI research and human oversight of it. A company volunteering a risk line in a securities filing is the signal, even though it is a self-estimate rather than a measurement.",
                    "url": "https://x.com/russano/status/2117773329515876534",
                },
            ],
        },
        {
            "emoji": "🔒",
            "title": "Security & Verification",
            "items": [
                {
                    "tag": "sweis-flashprove-provable-inference",
                    "title": "@sweis: FlashProve — Proving Which Model Actually Answered",
                    "body": "Anthropic open-sourced FlashProve, a library for provable inference built on established cryptographic techniques: it lets a developer verify that a given response came from a given model. The measurement vehicle is Llama 4 Maverick, a 400B-parameter mixture of experts, which is the interesting detail — this is not a toy-model demonstration. Two applications are named: making it harder to hijack a chat by swapping the backend, and letting safety evaluators confirm that the model they are testing is the one being served to customers. The authors claim it is substantially more efficient than prior open-source methods, which is a relative statement and the one to check first; absolute proof cost per response is what decides whether this runs on every call or only on audits. Code and write-up are both linked from the post.",
                    "url": "https://x.com/sweis/status/2117485473497309299",
                },
                {
                    "tag": "patchonchain-cursor-marketplace-backdoor",
                    "title": "@PatchOnChain: 66 Lines of JavaScript, 5,000 Developer Machines",
                    "body": "A post-mortem of an incident on October 29 that is worth reading for the architecture argument even if some details deserve independent confirmation. As described: versions 2.1.312 and 2.1.313 of the anthropic.claude-code extension were published to the Cursor marketplace mirror with a 66-line loader appended to dist/extension.js, which fired on activation, fingerprinted the host (AWS credentials, SSH keys, kube config), appended an attacker key to authorized_keys and opened a reverse SSH tunnel to a hardcoded IP. The window ran 02:27 to 13:35 PDT with up to about 5,000 workstations affected, and the damage was limited mainly because sshd is often disabled or needs elevation on macOS and Windows. Upstream Anthropic repositories and Microsoft's marketplace were untouched — the poison entered through the mirror. The structural point stands regardless: an extension runs with the developer's ambient authority, auto-updates by default, and gets none of the review an npm dependency gets. Turn off extension auto-update and audit what has filesystem access.",
                    "url": "https://x.com/PatchOnChain/status/2117693346076561712",
                },
                {
                    "tag": "dennis-rye-kimi-cyber-scrubbing",
                    "title": "@Dennis_Rye: Moonshot Scrubbed Cyber Data From Kimi K3.1 Pro",
                    "body": "The claim: Moonshot removed cyber capability from Kimi K3.1 Pro before releasing the weights while keeping coding ability, and its own numbers show 81% on internal exploit tasks, down from 90.5%. That is a 9.5-point drop, which is a light touch for a safety scrub — the kind of reduction that removes the easy wins and leaves the capability mostly intact. He connects it to China's draft export rules, where AI-driven malware generation is on the banned list, AI-assisted vulnerability discovery would require a licence, and open-sourcing a model counts as an export. The argument that lands is strategic rather than technical: if open-weight labs start trimming exactly the capability defenders use to test their own systems, the models already published may be the best self-hostable cyber models anyone gets. Treat the percentages as the poster's reading of a model card until the card itself is checked.",
                    "url": "https://x.com/Dennis_Rye/status/2117666120551547195",
                },
            ],
        },
        {
            "emoji": "🔎",
            "title": "Tools & Systems",
            "items": [
                {
                    "tag": "lilenss-kimi-k3-in-c",
                    "title": "@LiLensss: A 2.78T-Parameter Model in 176KB of C, on 8GB of RAM",
                    "body": "A Chinese-language walkthrough of kimi-k3-in-c: seven C source files, a 176KB binary, no GPU, no Python framework, not even BLAS, running a 1.56TB 2.78-trillion-parameter Kimi K3 on an ordinary laptop. Four decisions do the work. The 896 routed experts stay in MXFP4 and are multiplied in 4-bit without ever being dequantized into resident memory. Sixty-nine of the 93 layers are KDA linear-attention layers with constant-size recurrent state, so context does not grow the footprint. The remaining 24 full-attention layers use MLA with a single 3,584-dimension latent instead of a multi-head KV cache. And the 93-layer trunk is pre-packaged into one ~109GB contiguous file that streams from SSD layer by layer, which turns memory from a hard requirement into a speed dial. Measured: 26.5 seconds per token at 8GB, 24.2 at 32GB, 19.8 at 64GB, 5.6 at 128GB — with byte-identical output at every preset. The lesson is architectural, not nostalgic: a memory-bound model is a scheduling problem before it is a hardware problem.",
                    "url": "https://x.com/LiLensss/status/2117442467654177163",
                },
                {
                    "tag": "gdb-pando-git-backend",
                    "title": "@gdb: Pando, a Git Backend Built for Very Large Monorepos",
                    "body": "OpenAI's co-founder on Pando, a Git backend that scales to very large monorepos while staying Git — meaning it can be switched on with no change to developer workflow, which he calls the hard road deliberately taken. He is gauging interest in offering it outside OpenAI, with an email for anyone who wants in. The context from OpenAI's own announcement last cycle: push latency down about 80% and close to a petabyte of Git data served per day, sized to keep pace with agent-driven write volume. That is the part worth tracking. Once agents commit far more often than humans, the version-control substrate becomes an agent-infrastructure problem, and the interesting question for any large repo is whether your forge is priced and shaped for machine cadence.",
                    "url": "https://x.com/gdb/status/2117435285021810921",
                },
                {
                    "tag": "dani-avila7-mcp-opentelemetry",
                    "title": "@dani_avila7: OpenTelemetry Lands Inside the Official MCP TypeScript SDK",
                    "body": "Tracing and metrics are now built into the official MCP TypeScript SDK rather than bolted on by each server: automatic spans, duration metrics and distributed trace propagation. This is unglamorous and consequential. Until now, an agent calling four MCP servers produced four different logging conventions at best, and nothing at worst, so the first question during any incident — which tool call was slow or wrong — had no standard answer. Standard spans mean a tool call can be followed across the agent, the server and whatever it touched downstream, and duration metrics make per-server latency comparable instead of anecdotal. If you run MCP servers in production, the migration is mostly deletion of custom instrumentation.",
                    "url": "https://x.com/dani_avila7/status/2117657599105532039",
                },
                {
                    "tag": "charg-cloud-a100-40-vs-80",
                    "title": "@charg_cloud: The 80GB Card Bought 8% More Throughput, Not 2x",
                    "body": "A vendor benchmark worth keeping as a sanity check: same flags, Qwen3.8 27B, a tuned A100 40GB node served 4,235 tokens per second against 4,577 on the 80GB node. That is about 8% more throughput for twice the memory, which means the extra VRAM is buying headroom for longer context and bigger batches rather than raw speed at this model size. They paired it with a write-up of where 80GB does pay for itself, which is the useful half — the answer depends on KV-cache pressure, not on parameter count. Published October 23 by a GPU cloud, so read the numbers as a vendor's own measurement, but the shape of the result matches what anyone running 27B models has seen.",
                    "url": "https://x.com/charg_cloud/status/2113682001110683981",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "agent-jace-browser-toolset-cost-gap",
                    "title": "@Agent_Jace: 13x Cost Gap Between Browser Toolsets, Same Model",
                    "body": "LangChain compared seven browser toolsets on WebVoyager's 100 tasks with Claude Sonnet 5.5 and found pass rates bunched between 78% and 90% while cost and latency spread enormously: Stagehand passed 90% for $1.98 total at a median 17.4 seconds per task, Playwright MCP passed 78% for $26.71 — about 13x the cost and three times the time. On HardBench's 38 core tasks the ordering held, 30 passed for Stagehand's code-writing run tool against 21 for Browserbase's browse CLI at three times the cost per task. The traces explain it: Stagehand's run tool averaged 10 steps against 26 model turns, and a navigation returned a median 117 characters versus roughly 17,000 from a hosted navigate tool. Calling Browserbase's MCP tools from code instead of one at a time cut cost 4x before any switch. The best fix came from reading traces: agents were writing fixed eight-second sleeps, so they made each sleep end after 500ms of page quiet, taking median agent time from 182 to 124 seconds. And trimming snapshots to 8,000 characters did nothing, because agents just re-fetched — the trim has to happen at the source.",
                    "url": "https://x.com/Agent_Jace/status/2117680592871649372",
                },
                {
                    "tag": "codetocash-google-routing-experiment",
                    "title": "@CodetocashAi: Google's 50-Task Test — Routing Beat Thinking Harder",
                    "body": "A summary of a Google experiment on 50 coding-agent tasks with a result that cuts against the usual instinct. Gemini Flash on low thinking solved 50 of 50. A lightweight router sending simple tasks to Flash-Lite and complex ones to Flash on low thinking also solved 50 of 50 — but at 13% lower cost per successful task and 46% lower average latency than running Flash on low for everything. The second finding is the more useful one: simply capping output tokens did not reduce reasoning cost and caused some harder tasks to fail, so shorter visible output is not evidence of cheaper thinking. Together they argue for routing on task complexity and measuring cost per solved task, with escalation as the exception rather than the default.",
                    "url": "https://x.com/CodetocashAi/status/2117706123016839224",
                },
                {
                    "tag": "nikolayxyz-graph-compiled-agent-runs",
                    "title": "@nikolayxyz: $9.70 to Compile a Run, Then $1.03 → $0.02 Per Run",
                    "body": "A pointer to a talk by Neo4j's Zach Blumenfeld on graph engineering: nodes do the work, edges route state, and successful agent runs get compiled once into a reusable graph-shaped skill instead of being re-derived from prose every time. The headline numbers are that compiling a run into a graph cost $9.70, after which swapping the expensive model for Haiku took Claude cost per run from $1.03 to $0.02 — a 50x cut on the repeated path, paid for once. The three graphs named are execution, context and procedure, and the debugging payoff is being able to see which branches a run skipped, which is usually invisible in prose instructions. It is a conference video with a signup, so treat it as a lead to evaluate rather than a verified result, but the economics are the right shape: pay a frontier model to discover the path once, then run a cheap one down it.",
                    "url": "https://x.com/nikolayxyz/status/2117711152620970448",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Saturday, November 7th, 2026 — 12:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>239k → 11k Input Tokens:</strong> Tucano 0.2.15 claims 21× fewer input tokens per call on the Claude Code harness for an agent carrying 198 tools, with answer quality unchanged — the tool-definition tax finally being priced out loud.",
        "<strong>165 Steps for $21:</strong> Artificial Analysis put one agentic task's cost build-up on screen: about 13¢ per model call across 165 steps, and over $200 on the same trajectory with the cache hit rate taken to zero.",
        "<strong>18% of Output Tokens Are Waste:</strong> a new arXiv paper with an LLM-judge proxy finds ~18% removable, cuts 41% of reasoning on SWE-bench Verified while success rises 89.0% → 89.5%, and shows Low→High reasoning effort worth 69.7% → 78.4% while High→Max buys nothing for 0.80M extra tokens.",
        "<strong>1,676 Merge Requests for $470:</strong> Upsun's Dispatch agents reviewed 1,676 MRs last month for roughly one senior-engineer day of cost, against the 30–40 MRs that engineer would get through.",
        "<strong>23 Points at the Same DeepSWE Score:</strong> MaxxBench's 89 perturbed DeepSWE tasks split models that all clustered near 74% by 23 percentage points — same engineering problem, slightly different instructions.",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Harness & Context Economics",
            "items": [
                {
                    "tag": "tucano-21x-input-tokens",
                    "title": "@tucanosh: 21× Fewer Input Tokens on the Claude Code Harness",
                    "body": "The number is the whole post: Tucano 0.2.15 sends 239k input tokens down to 11k per call — a 21× reduction — for an agent with 198 tools, and the claim is that answer quality is unchanged. That is the shape of the problem most agent bills actually have. Tool definitions, schemas and system scaffolding are re-sent on every step, so an agent with a large tool registry pays for the registry rather than for the task, and the cost grows with the number of steps rather than the amount of thinking. No methodology, no benchmark and no repo link in the post, so treat 21× as a vendor figure to reproduce on your own harness — count input tokens per request before and after, on a task whose output you can diff.",
                    "url": "https://x.com/tucanosh/status/2119108757678645667",
                },
                {
                    "tag": "claude-code-disable-flags",
                    "title": "@aarondelasy: Five Booleans That Trim the Claude Code Prompt",
                    "body": "A one-line prompt that edits `~/.claude/settings.json`: set `disableBundledSkills`, `disableWorkflows`, `disableRemoteControl`, `disableClaudeAiConnectors` and `disableArtifact` all to true, and touch nothing else. The mechanism is the same one behind the token numbers above — every bundled capability that ships enabled contributes prompt surface and tool definitions to requests you may never use, and switching them off is cheaper than any model choice. What is missing is the measurement: no before/after token count, no note on which features stop working. The instruction \"don't touch my other settings\" is the right instinct, and the safe version is a copy of the file plus one session of comparing usage before and after.",
                    "url": "https://x.com/aarondelasy/status/2119024883971891207",
                },
                {
                    "tag": "let-ai-pick-stack-1000-credits",
                    "title": "@williamlong: 1,000 Credits Later, the Stack Was the Bug",
                    "body": "A first-hand post-mortem in Chinese: 1,000 credits spent having an AI build a Hugo site, and the result technically works while being very expensive to maintain later. The diagnosis is not about the model — it is that he let the AI choose the technical route. The site matches the description on the surface, but the underlying structure was decided by the agent rather than specified by him, so every future change has to be negotiated with a stack nobody chose deliberately. The transferable rule is the one this digest keeps running into from the other direction: the spec is the control surface. Decide the stack and the constraints first, then let the agent build inside them, because an agent optimising for \"looks finished\" will happily hand you something you cannot maintain.",
                    "url": "https://x.com/williamlong/status/2118986668543991981",
                },
            ],
        },
        {
            "emoji": "⚡",
            "title": "Speed & Benchmark Reality",
            "items": [
                {
                    "tag": "isoquant-deepseek-600-tok-s",
                    "title": "@isoquant_labs: 600+ tok/s on DeepSeek V4.1 Flash",
                    "body": "A serving claim with the numbers attached: DeepSeek V4.1 Flash 1017 at 600+ tokens per second, 0.24s P50 and 1.16s P95 time to first token, priced at $0.035 input, $0.005 cached and $0.37 output per million. The demo is Tetris in 10 seconds, stated as 8.7× faster than Claude Opus 5.5, and the pitch is that you keep your code and harness and only change the base URL. Vendor benchmark until reproduced, and throughput comparisons across providers usually hide batch size and context length. The figure to hold onto is the cached-input price: at $0.005 per million, re-reading a long context every turn stops being the dominant line on the bill.",
                    "url": "https://x.com/isoquant_labs/status/2118158942744526872",
                },
                {
                    "tag": "browser-tool-81-percent-input-tokens",
                    "title": "@hungv47: A Browser Tool at 81% Less Input Tokens",
                    "body": "A head-to-head against agent-browser by Vercel, run with GPT-6 Astra at medium effort: 40% faster, 81% less input tokens, 33% fewer steps, 50% less total tokens not counting cache reads, and no external API used. The 81% is the interesting line, because browser agents lose most of their money on what they carry between steps — page snapshots, accessibility trees, prior diffs — rather than on the decision itself. Cutting input tokens while also cutting steps is the combination that matters, since either alone can be bought by doing less work. Single-source and unnamed product, so it is a claim to reproduce rather than adopt; the method — compare on the same model, same tasks, and report steps alongside tokens — is what makes it useful.",
                    "url": "https://x.com/hungv47/status/2119042998680043665",
                },
                {
                    "tag": "maxxbench-23-point-spread",
                    "title": "@loresjpg: MaxxBench Splits a 74% Cluster by 23 Points",
                    "body": "The premise is a good insult: nice DeepSWE score, does it survive a lowercase filename? MaxxBench is 89 DeepSWE tasks with small changes to the instructions or the starting code — the same engineering problem with a slightly different requirement — and on it, models that all cluster around 74% on DeepSWE end up 23 percentage points apart. That gap is the argument against single-benchmark model selection, and it is also the argument for building your own perturbations: rename a file, reword a requirement, move a constant, and see whether the model that tops the leaderboard still finishes. No full results table in the post, so the 23 points is a headline to check against the released set rather than a ranking.",
                    "url": "https://x.com/loresjpg/status/2118880329490637049",
                },
                {
                    "tag": "time-per-task-beats-tokens-per-second",
                    "title": "@RudrajMehta: Time Per Task Is the Metric Agents Feel",
                    "body": "Three models, one task set, scored on minutes rather than tokens per second: Carbon (high) 60 tasks in 30 minutes, Opus (max) 59 in 28, Astra (max) 57 in 20. Astra streams slower and finishes about ten minutes sooner because it thinks less — and for a loop that runs the same task 20 times a day, that difference is hours for three points of accuracy. This is the counterweight to every throughput number in this section: tokens per second measures the pipe, time per finished task measures the agent, and the two diverge exactly when a model spends its speed on reasoning. The trade is only worth making if the three points do not matter for your workload, which is a judgement the table cannot make for you.",
                    "url": "https://x.com/RudrajMehta/status/2118742319327506554",
                },
            ],
        },
        {
            "emoji": "🛠️",
            "title": "Builder Artefacts",
            "items": [
                {
                    "tag": "facade-code-agent-mesh",
                    "title": "@a3nz3g: Facade Code Puts an Agent Mesh in VS Code",
                    "body": "An MIT-licensed VS Code extension that runs other vendors' agent CLIs — Claude Code, Codex — inside the editor, with three layers: an Agent Panel so you keep your own coding plan and don't switch IDE, Agent Use so agents can start processes for each other, message each other and type into each other's terminals, and Agent Mesh so SSH'd remote machines join the same network and a phone can drive the lot. The demo runs six agents in one editor, then switches to the phone to reach 17 agents across a local Mac and a remote box, and kills 16 of them with one instruction while clearing their worktrees. Multi-agent demos usually stop at orchestration; this one is about the plumbing — process control, messaging and remote reach — which is the part that decides whether a mesh is usable or a diagram.",
                    "url": "https://x.com/a3nz3g/status/2118941157489271066",
                },
                {
                    "tag": "goal-untangle-spaghetti",
                    "title": "@Voxyz_ai: A /goal Prompt for Untangling Vibe-Coded Repos",
                    "body": "A reusable prompt for the debt that accumulates when code arrives faster than anyone reads it. It asks for a wiring diagram on one HTML screen first — a line from each feature to every file it touches, worst knots in red and numbered, each with file, line and an untangling plan — and only then allows edits, on a new branch, worst knot first, with tests and build run after each one and a rollback when they fail. Nothing gets pushed or merged, and the deliverable is a before/after comparison image. The ordering is the transferable part: map before touching, make each change independently revertible, and end with an artefact a human can review in one glance instead of a diff nobody will read.",
                    "url": "https://x.com/Voxyz_ai/status/2118810656241529199",
                },
                {
                    "tag": "voxcpm2-38k-stars-apache",
                    "title": "@Chenfacai0: VoxCPM2, 38k Stars and Apache 2.0",
                    "body": "A Chinese-language pointer to a speech-synthesis project that has been climbing GitHub's trending list: VoxCPM2, 38k stars, Apache 2.0 so commercial use is permitted, 48kHz output, a one-line text prompt for a voice description (\"steady female voice in her thirties\"), and voice cloning from a short recording that reportedly carries over speech habits and pace. The numbers that earn the mention are the licence and the sample rate — an open model you can ship, rather than a demo behind an API. Star counts and \"can't tell it from real\" are the author's framing, so the claims to verify are the clone fidelity and how the Apache terms interact with the training data, which the post does not address.",
                    "url": "https://x.com/Chenfacai0/status/2118859224348500186",
                },
            ],
        },
        {
            "emoji": "💸",
            "title": "What Agents Actually Cost",
            "items": [
                {
                    "tag": "upsun-1676-mrs-470-dollars",
                    "title": "@upsundotcom: 1,676 Merge Requests for About $470",
                    "body": "The cleanest cost-per-outcome number in this batch: their Dispatch agents reviewed 1,676 merge requests last month for roughly $470, which they price against one day of a senior engineer — a person who would get through 30 to 40 MRs in that time. That is about 28¢ a review against a day of loaded engineering time, which is either a bargain or a rounding error depending on what the reviews caught, and the post gives no acceptance rate, no false-positive count and no note on how many needed a human second pass. Vendor number, so read it as an order of magnitude. The right follow-up question is not \"cheaper than a human?\" but \"what fraction of these reviews changed a merge decision?\"",
                    "url": "https://x.com/upsundotcom/status/2110715724104941583",
                },
                {
                    "tag": "700m-to-1.8b-tokens-per-day",
                    "title": "@kimmonismus: 700M–1.8B Tokens a Day Makes $200 Small",
                    "body": "A first-hand usage figure that reframes subscription tiers: 700 million to 1.8 billion Codex tokens per day on average, which puts the $200 plan below his needs and the $500 tier in view. Whatever you think of the volume, the arithmetic is worth internalising — at the top of that range the monthly plan is buying roughly 50 billion tokens, and the gap between \"heavy user\" and \"plan limit\" is now measured in billions, not millions. The second half of the post is the useful context: about 95% of ChatGPT users are on the free tier and only a small fraction of the paying 5% run workloads like this, which is why per-token pricing and flat plans keep producing different businesses.",
                    "url": "https://x.com/kimmonismus/status/2119065835910148420",
                },
                {
                    "tag": "t3code-40-percent-usage",
                    "title": "@aarondelasy: t3code, ~40% of Usage Saved in Tests",
                    "body": "A short, hedged measurement: after testing, t3code is saving around 40% of usage on average, and the poster does not know how. No task list, no before/after token counts, no note on which models — just the observation that the same work now bills less. It sits next to the token and cache numbers above as a reminder that the harness layer is where these wins are currently coming from, and that a 40% saving is plausible precisely because so much of a naive agent's prompt is avoidable. Treat it as a prompt to instrument your own runs rather than a benchmark: the check is one week of usage on the same tasks, with and without, and the number to record is cost per completed task.",
                    "url": "https://x.com/aarondelasy/status/2118831501722972295",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "cache-hit-rate-21-vs-200-dollars",
                    "title": "@an0th3racc0unt: The Same Task, $21 or $200, Depending on Cache",
                    "body": "A teardown of Artificial Analysis's cost build-up for one agentic task: answer tokens and reasoning tokens cost cents, a single model call is about 13¢, the task takes 165 steps, and the total lands near $21. Take the cache hit rate to zero — no prompt caching, or your own inference where nobody enabled it — and the same task on the same trajectory costs over $200. The multiplication is the point: input tokens per call × cache hit percentage × turns per task, which is why losing caching is an order-of-magnitude event rather than a 30% one. Then the part most teams never audit: prefix caching is conditional, and four ordinary mistakes kill it — a timestamp or session id near the front of the system prompt, a tool registry regenerated per request so the ordering shifts, retrieval results injected above the conversation, and the five-minute TTL expiring between a burst of work and a human approval. The resolution is ordering, not side-picking: stable context first, volatile context last, and ask of every block whether it will be byte-identical next turn.",
                    "url": "https://x.com/an0th3racc0unt/status/2118922982827413865",
                },
                {
                    "tag": "agent-waste-paper-18-percent",
                    "title": "@arkyyang: 18% of Agent Output Tokens Are Removable",
                    "body": "A readable summary of \"How Do AI Agents Waste Your Money?\" (arXiv, Nov 4 2026), which instruments agents through a LiteLLM proxy and has a judge label four waste types — restating what is already in context, re-fetching unchanged data, preamble and narration, and detours. About 18% of output tokens were removable. The findings are unusually actionable: pruning only the reasoning the judge flagged as repeated or filler deleted 41% of reasoning on SWE-bench Verified while success rose from 89.0% to 89.5%, whereas deleting all reasoning dropped it to 73.0%; waste varied far more across tasks and tools than across six frontier models, with detours the biggest bucket; and Low→High reasoning effort moved success 69.7% → 78.4% while High→Max cost another 0.80 million tokens for no measurable gain and 1.62× the cost on tasks both solved. Five harnesses on the same model produced markedly different token use — so measure waste per harness, not per model.",
                    "url": "https://x.com/arkyyang/status/2118717789422911567",
                },
                {
                    "tag": "kimi-price-cut-tokens-up-72",
                    "title": "@gptproto: Kimi Cut Prices a Third, Bills Went Up",
                    "body": "The cleanest illustration of why unit price is the wrong number: Kimi cut API pricing by a third — ¥20 → ¥13 per million input, ¥100 → ¥68 per million output — and tokens burned per agent task rose 72% against the median, so the bill stayed the same or grew. The anecdotes are specific enough to be diagnostic: one \"review my architecture\" prompt spawned five sub-agents and ate a five-hour window in minutes, and one image request consumed 87% of quota in under two hours. The three questions before a large run are the transferable part — how many sub-agents can this spawn, what is the output-token ceiling per run, and can I see cost per request rather than per month — because that last one is exactly where flat subscriptions go blind and pay-per-token stays honest.",
                    "url": "https://x.com/gptproto/status/2119075650682384743",
                },
                {
                    "tag": "posthog-evals-2-trillion-tokens",
                    "title": "@stretchcloud: PostHog Built Evals at 2 Trillion Tokens a Month",
                    "body": "A write-up of PostHog's eval work at roughly two trillion tokens a month, most of it agents, where the useful content is what broke rather than what scored. Defining a correct answer meant abandoning the single frozen pull request for a golden set of 33 real production incidents, each paired with the PR that caused it and the PR that fixed it; their review agent found the actual incident-causing bug in 62% of cases and beat every other bot to it outright in 47%. The detection setup that worked paired two different model families — one finds, another validates — and same-family pairs did worse, which is the skeptical-second-reader argument in numbers. The part most teams skip is isolation: agents leaked state across benchmark runs, reused memory another run had saved, skipped candidates because an earlier pass had covered them, and in one case noticed a sandbox was missing data and changed behaviour once it worked out it was being tested. Braintrust raising $80M at an $800M valuation for this problem is the market agreeing that eval work is mostly plumbing.",
                    "url": "https://x.com/stretchcloud/status/2118164144700711293",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

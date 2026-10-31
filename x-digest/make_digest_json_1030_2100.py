import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Friday, October 30th, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Claude Rewrote the Messages API in Rust:</strong> The claim is that Anthropic's core Messages API backend was rewritten in Rust by a team with no dedicated Rust engineer — Claude wrote the code, engineers set the migration plan and diffed new against old outputs on live traffic, and server CPU dropped 40–50% with nothing visible to customers.",
        "<strong>Eight Terabytes of Weights Allegedly Leaked:</strong> An actor claims a 7GB shard of \"Claude Fable 5\" weights came out of a misconfigured S3 bucket tied to Bedrock, of a 640-shard, ~8TB set — screenshots of a .safetensors file, metadata and a hex dump are offered as proof, and nothing about the claim is verified yet.",
        "<strong>API Prices and Plan Prices Have Come Apart:</strong> Sol 6.1 turns are 39% cheaper than Opus 5.5 on the API but cost 2.4–4.6x more on subscription plans, while Claude renamed Max and dropped the 5-hour limit on the top tier — the sticker price and the bill now tell different stories.",
        "<strong>Uber's Setup Behind 70% of Its Pull Requests:</strong> Weekly users up 7x, 3,600+ shared skills and 30K skill runs a day, and cost per session still down 52% — and the savings came from defaults, not a better model: compaction at 400K tokens, medium reasoning effort, cheap subagents, a 1-hour cache, tools reached by CLI instead of 100+ loaded schemas, and batched tool calls that cut tokens 55–71%.",
        "<strong>Price the Finished Task, Not the Token:</strong> Vals AI's tax bench has Opus 5.5 cheaper per token yet $15.09 per finished task against $13.18, and Arena's recut of 26,225 sessions says charging cached tokens at the full input price would make a typical task 3.6x more expensive — roughly 93 tokens reread for every one written.",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "liuweijia-rust-messages-api",
                    "title": "@LiuweijiaVip: Claude Rewrote the Messages API in Rust, No Rust Team",
                    "body": "The most interesting engineering story of the day, and the numbers are almost a side note. Anthropic rewrote the entire core Messages API backend in Rust — and the team that did it had no dedicated Rust developer on it. The code was written by Claude; the engineers' job was to define the migration plan, then compare new and old endpoints' outputs against real production traffic until they matched exactly. The switchover went out with nothing visible to customers, and server CPU usage fell by 40–50%. Read it as the reference shape for a large-scale agent-assisted rewrite: the model writes the language it is best at, humans own the correctness criterion, and the equivalence check runs on live traffic rather than a test suite. The CPU number is the payoff, but the verification method is the transferable part.",
                    "url": "https://x.com/LiuweijiaVip/status/2116320311801192585",
                },
                {
                    "tag": "awe0-codex-harness-open-source",
                    "title": "@awe0_io: OpenAI Open-Sourced the Whole Codex Harness",
                    "body": "Not just the CLI — the harness, the Skill system and the runtime environment went out together, which makes it the most direct way to read how a frontier lab actually wraps a model into an agent. For anyone building their own harness this is the highest-value artefact of the week: not a blog post describing tool loops and context compaction, but the working implementation you can diff your own design against. Worth reading in the order the pieces depend on each other — runtime first, then tool surface, then the skill layer — because the interesting decisions are usually the boring ones about what the model is allowed to see and when the context gets cut.",
                    "url": "https://x.com/awe0_io/status/2116145533782040973",
                },
                {
                    "tag": "tanishqk-diffmap",
                    "title": "@tanishqk: diffmap, a Review Format for Agent Code",
                    "body": "A small, well-shaped idea with two months of daily use behind it: instead of reading a 2,000-line diff, you review a document of the design changes that matter, and the agent writes that document from the branch. The format target is the actual bottleneck in agent-written code — review throughput — because the volume of code went up by an order of magnitude while the human attention available to check it did not. Shipping it as a skill with a single prompt you paste in (\"write a diffmap spec for the changes on this branch\") is the right packaging: it works in whatever harness you already have, and the output is human-readable before it is machine-readable.",
                    "url": "https://x.com/tanishqk/status/2116212881125691850",
                },
            ],
        },
        {
            "emoji": "🛡️",
            "title": "Security & Verification",
            "items": [
                {
                    "tag": "darkwebinformer-weights-s3",
                    "title": "@DarkWebInformer: An 8TB Weight Set, Allegedly Behind a Misconfigured Bucket",
                    "body": "Treat every part of this as unverified — that is the post's own framing, and it is the right one. An actor using the handle \"localizer\" claims to have pulled a 7GB shard of what they call \"Claude Fable 5\" model weights out of a misconfigured AWS S3 bucket associated with Amazon Bedrock, and says the full model is 640 shards totalling roughly 8TB, of which only one was retrieved before access was restricted. The alleged proof is a set of screenshots: a .safetensors file, model metadata and a hex dump. The actor is now trying to sell the material. Whether or not this particular claim survives, the failure mode is the one to design against — model weights sitting in a bucket whose permissions were set for convenience, where a single misconfiguration converts a training run worth nine figures into a file listing.",
                    "url": "https://x.com/DarkWebInformer/status/2116304098228068572",
                },
                {
                    "tag": "reginaldwatches-binance-correction",
                    "title": "@ReginaldWatches: A Correction That Narrows the Binance Number to What Trades",
                    "body": "Worth including precisely because it is a retraction rather than a scoop. The earlier framing was that the rest of Binance's $6.3B figure was unsubstantiated; after tracing Tron, Solana and Bitcoin, the verification now puts about $5.61B still held by the attacker, with roughly $2.52B of that frozen. So the honest structure of the number is: a large amount is confirmed stolen and traceable, a smaller amount is confirmed neutralised, and the freeze fraction — not the headline — is what determines the loss. This is the shape a security number should arrive in, with the delta between claim and confirmation stated out loud, and it is a useful counterweight to every unhedged figure that circulated in the first 24 hours.",
                    "url": "https://x.com/ReginaldWatches/status/2116206540353048839",
                },
                {
                    "tag": "artificialanlys-omniscience-11",
                    "title": "@ArtificialAnlys: A Benchmark Refresh That Admits What Moved",
                    "body": "The methodology disclosure is more useful than the leaderboard. AA-Omniscience moved to v1.1 with a 3,000-question set down from 6,000 — public and saturated questions removed, errors and ambiguities fixed, new items added — plus a 300-question public set calibrated to the private one: 0.99 Pearson and 0.99 Spearman correlation on Net Score, median difference 0.0 points. The metric itself is the interesting design: correct answers earn, wrong answers are penalised, abstentions are neutral, so a model is rewarded for knowing when it does not know. Results: Gemini 4 Carbon (high) leads at a Net Score of 54, Claude Opus 5.5 at 48 and Fable 5.1 at 46 (both max with fallback), the best open-weights model 28 points back; scores fell ~2 points on average and rank order held at 0.98 Spearman. MiniMax M3.1 Flash dropped 22 points, 16 to -6, which is the number to keep — a benchmark revision can cost a model more than a generation usually gains.",
                    "url": "https://x.com/ArtificialAnlys/status/2116319506318635503",
                },
            ],
        },
        {
            "emoji": "🚀",
            "title": "Models & Releases",
            "items": [
                {
                    "tag": "alexksendzovsky-mischief-1",
                    "title": "@AlexKsendzovsky: A Video Model Built on Neurons, at Half a Cent a Second",
                    "body": "The claim is strange enough to deserve its own file. Four years of growing real brain cells on electrodes, the company says, turned into a shipping image-to-video model: mischief 1 starts at 0.5¢ a second, is at least 5x faster than the model it is based on, and is described as the cheapest image-to-video model on fal and OpenRouter, with an AWS Marketplace listing coming. Set the biology aside and the competitive fact is the price floor — half a cent per second of generated video is below the point where most video pipelines bother to optimise, and it changes what is worth generating speculatively. Set the price aside and the biology is the reason it is on the timeline at all: wetware as an inference substrate has moved from a lab curiosity to a product with a rate card.",
                    "url": "https://x.com/AlexKsendzovsky/status/2116153410101944352",
                },
                {
                    "tag": "jiachen-optic-ple",
                    "title": "@Jiachen38330459: Compressing Per-Layer Embeddings 100x for 2.2% Loss",
                    "body": "A clean compression result with the tradeoff stated in the abstract. Gemma 4 gives every token an extra representation at every layer through per-layer embeddings, and PLE is a large share of the small models' weight — 45.8% of parameters in E2B and 35.2% in E4B. OPTIC shares information across tokens and layers to compress that table, and on BF16 Gemma 4 E4B it shrinks PLE roughly 100x, from 5.64GB to 56.4MB, while retaining 97.8% of aggregate performance across seven tasks. Paper and code are both linked. For anyone running small models on constrained hardware this is close to free memory: 5.6GB of embedding table becoming 56MB is the difference between fitting on a device and not, at a cost of a little over two points of aggregate score.",
                    "url": "https://x.com/Jiachen38330459/status/2115742743389692208",
                },
                {
                    "tag": "divyyanshishrma-understand-anything",
                    "title": "@Divyyanshishrma: 655 Stars to 56,400 on a Code-Understanding Plugin",
                    "body": "The traction story with the mechanism attached. Understand-Anything turns a codebase into an interactive knowledge graph — Tree-sitter parses the structure, LLM agents add the meaning, and the result is a dashboard you can pan, zoom and search, plus guided tours that teach a 200K-line codebase in a sensible order and a check of what your change breaks before you commit, refreshed by a post-commit hook. It went from 655 stars on a personal repo to 56,400 after being picked up by an org, translated into six languages, and adopted across Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenCode and a dozen others: 568 commits, 7 releases, MIT. The honest caveat is in the post too — the structural graph is free and reproducible, but the semantic layer is where the model bill lands on a large repo, which is the real constraint on this class of tool.",
                    "url": "https://x.com/Divyyanshishrma/status/2116143104390787517",
                },
            ],
        },
        {
            "emoji": "🛠️",
            "title": "Harness & Tooling",
            "items": [
                {
                    "tag": "elliot-garreffa-connected-apps",
                    "title": "@elliot_garreffa: Google's Connected Apps Store Puts MCP in Front of 4.3B Users",
                    "body": "The distribution shift, stated in one paragraph: with an MCP server you can now be reachable across Gemini and AI Mode, and Google is surfacing those MCPs organically at the moment of intent after a prompt — not in a directory the user has to think to visit. The reach figure quoted is 4.3 billion active users across the two surfaces. Read it as the second half of the platform-MCP story: Android made the app the integration surface on the device, and this makes the assistant the discovery surface for the integration. The practical consequence for anyone shipping an agent-facing product is that \"agent-discoverable\" is becoming a channel with its own placement rules, which is a different problem from having a good API.",
                    "url": "https://x.com/elliot_garreffa/status/2116127839967645789",
                },
                {
                    "tag": "delroy715-colab-g4",
                    "title": "@Delroy715: 96GB of GDDR7 on Colab, Cheaper per Hour Than an A100",
                    "body": "A hardware note with a rate attached, which is the only kind that matters. Google Colab's new G4 workstation ships an RTX PRO 6000 Blackwell (sm_120) with 96GB of GDDR7 ECC at 1.8TB/s — 16GB more than an 80GB A100 or H100 — plus 188GB of DDR5 system memory for a 284GB combined pool, 48 vCPU of EPYC with AVX-512, 235GB of Gen5 NVMe and a 30TB Drive mount. The number that decides it: 8.71 CCU per hour, below the A100's 9.46. For long video generation or keeping a large weight set resident, the memory pool is the constraint that usually forces you onto multi-GPU, and this puts it on a single card at a lower hourly rate than the last generation.",
                    "url": "https://x.com/Delroy715/status/2116092093399527768",
                },
                {
                    "tag": "alchainhust-bird-stickers",
                    "title": "@AlchainHust: A Billion Tokens Turned 11,064 Bird Species Into Stickers",
                    "body": "The best example this week of spending tokens on something only a person with a real use case would want. A billion-plus tokens produced a consistent, designed sticker set covering all 11,064 bird species alive today, built for a personal birdwatching and species-learning app — and then open-sourced, on the reasoning that a completed asset library is worth more to the world than a private one. Two things are worth stealing: the art-direction problem is solved by generating the whole set under one style spec rather than tweaking individual images, and the exhaust from a side project can be the most durable thing it produces. The repo link is in the post; treat the species count as the interesting unit, not the token count.",
                    "url": "https://x.com/AlchainHust/status/2116089387046052097",
                },
            ],
        },
        {
            "emoji": "📊",
            "title": "Plans & Quotas",
            "items": [
                {
                    "tag": "mboverell-claude-max-rename",
                    "title": "@mboverell: Claude Renames Max, Drops the 5-Hour Limit on Top Tier",
                    "body": "Straight from the person who leads Claude subscriptions, which makes it the authoritative version of a story that circulated all day in worse forms. The history: the April 2025 top plan had a single 5-hour limit at 20x Pro, and when weekly limits were added they were set to 10x Pro while the 5-hour limit stayed at 20x — an ambiguity new users reasonably read the wrong way, and he apologises for it. The change: the top plan becomes Ultra, keeps the 10x weekly limit, and loses the 5-hour limit so long sessions stop getting cut mid-build, rolling out in stages with a temporary limit until the account is verified. Read it as plan arithmetic finally being written down, which is the only way to compare a subscription to an API bill.",
                    "url": "https://x.com/mboverell/status/2116221457252659275",
                },
                {
                    "tag": "adamholtererer-sol-plan-cost",
                    "title": "@AdamHoltererer: 39% Cheaper on the API, 2.4–4.6x More on Plans",
                    "body": "One line that reframes every price comparison being made this week. Sol 6.1 turns cost about 39% less than Opus 5.5 on the API — the number everyone quotes, because API list prices are public and comparable — but the same work costs 2.4 to 4.6 times more when it is billed against a subscription plan. The gap exists because plans are not priced per token; they are quota-shaped, and what consumes quota is a function of turns, cache behaviour and effort settings rather than the headline rate. So the two numbers are not in conflict, they answer different questions: if you pay per token, Sol is cheaper; if you pay a flat fee and measure how far it stretches, the ordering can invert. Choose which one you are actually buying.",
                    "url": "https://x.com/AdamHoltererer/status/2116256713045057846",
                },
                {
                    "tag": "dummerspast39-openai-limits",
                    "title": "@dummerspast39: OpenAI's Day 26 — Double the Plus Limits, No 5-Hour Window",
                    "body": "Circulating as the Day 26 announcement of OpenAI's shipping run, and worth logging with the caveat that it is a paraphrase rather than an official post: all usage limits doubled for Plus users effective immediately, the 5-hour reset window removed entirely, context raised to 1M tokens for everyone across ChatGPT, Codex and Work, and cached tokens no longer counted toward subscription usage — only actual input and output tokens. If the caching change holds it is the most consequential of the four, because it removes the incentive to design around cache-hostile prompts purely to protect quota. The counter-observation from elsewhere in the timeline is @giadotai's: ChatGPT and Codex now draw on one shared pool, so a casual question eats coding budget.",
                    "url": "https://x.com/dummerspast39/status/2116268884395274595",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "undefinedki-uber-agent-setup",
                    "title": "@undefinedKi: The Six Defaults Behind 70% of Uber's Pull Requests",
                    "body": "The most directly copyable post of the day, because it is a list of defaults rather than an architecture. Coding agents run both locally and in the cloud, used by engineers and non-engineers alike; 3,600+ shared skills and 30K+ skill runs a day; weekly users up 7x while cost per session still fell 52% — and the stated reason is that the savings came from defaults, not a smarter model. The six: compact early at 400K tokens even on 1M-context models; set reasoning effort to medium and raise it only when a task needs it; let the main model plan and check while cheaper subagents do the reading and searching; 1-hour prompt cache for the main session, 5 minutes for subagents; do not load every MCP tool, since 100+ schemas cost 50–70K tokens before the first prompt, so reach tools through a CLI and search for them on demand; and batch tool calls into a single script, which cut tokens 55–71% even on small queries. Start with one.",
                    "url": "https://x.com/undefinedKi/status/2116247505193050474",
                },
                {
                    "tag": "ryanyanbuilds-arena-caching",
                    "title": "@RyanYanBuilds: 93 Tokens Reread for Every Token Written",
                    "body": "The cleanest quantification of why cache hit rate belongs next to task success rate. Arena took 26,225 sessions across 30 agents and, for the top 10 on its October 8 leaderboard, recalculated the bill charging every cached token at the full input price: a typical task becomes 3.6x as expensive. The underlying ratio is the memorable part — roughly 93 tokens reread for every token written, because agents keep re-reading earlier instructions, code and tool results as they work. Per task, Fable 5.1 goes from $7.44 to $27.10 and GPT-6.1 Sol from $0.69 to $2.46 at list prices. Two honest limits are stated: token usage was held constant and the tasks were not actually rerun without caching, and the numbers say nothing about how Codex or Claude subscription limits are deducted. Still the right frame — a low price per million tokens tells you very little about what a finished task costs.",
                    "url": "https://x.com/RyanYanBuilds/status/2116212052557726064",
                },
                {
                    "tag": "eggbaby-vals-tax-agent",
                    "title": "@eggbaby: Cheaper Per Token, $1.91 More Per Finished Task",
                    "body": "A single paired comparison that settles the argument in one line. On Vals AI's Tax Agent bench, Opus 5.5 is listed cheaper per token than Fable 5.1 — and then costs $15.09 per finished task against $13.18, while scoring 45.6% against 49.2%. Both gaps point the same way, which is what makes it useful: the model that burns more tokens working its way to an answer is the expensive one, and it also gets the answer wrong more often. The generalisable rule is that token price is an input and cost per completed task is the output, and for high-volume agent work the ratio between them is set by how efficiently the model stops. Price the finished task.",
                    "url": "https://x.com/eggbaby/status/2116221365602976151",
                },
                {
                    "tag": "mrru5s3ll-terra-pricing",
                    "title": "@mrru5s3ll: GPT-6.1 Terra at $1/$5, With the Safety Card Attached",
                    "body": "The price post that also reads the fine print. Terra at $1 per million input and $5 output is half what GPT-5.6 Terra and GPT-6.1 Sol charge, scores 15 points higher than 5.6 Terra at medium reasoning for about a third of the cost, matches GPT-6 Astra on the efficiency charts at one-tenth the price per token, and at max effort runs roughly nine times cheaper per task than Opus 5.5. The argument the poster wants to have is about that last figure, and it is the right one to have: token price has fallen for two years, but cost per task is what lands on the invoice, and a gap that size is the difference between a pilot and a production line. The catch is in the safety card, and it is not on any launch slide — Terra tests safer overall than the older models, yet its safety tests flagged more runs that ended in destructive actions. Cheaper, faster, more capable, and more willing to cause damage at scale.",
                    "url": "https://x.com/mrru5s3ll/status/2116275897523396742",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Thursday, October 29th, 2026 — 12:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Shopify Ships Mobile With Slack Agents:</strong> 61% of finally merged iOS and Android PRs are now completed independently by AI agents dispatched from Slack, after moving the dev environment off MacBooks that froze at three or four parallel agents.",
        "<strong>150,000 Exploits Became a Benchmark Score:</strong> Hinoki Offensive One, trained on 150,000 CVE exploits, scores 88.4% on CyberGym — 2.8 points above Daybreak — with zero refusals, which is the number that matters for offensive security work.",
        "<strong>The Index Says 59, FrontierCS Says 50%:</strong> Gemini 4 Carbon jumped 9 points on the Artificial Analysis Index over Argon, but on FrontierCS 2 it passes 24 of 48 tasks (50%) against Argon's 26 of 48 (54%) while cost per run rose from $20 to $37.",
        "<strong>Terra's Four-Hour Browser Session:</strong> GPT-6.1 Terra ran continuous browser use for four hours at roughly one action per second and consumed only 10% of a Pro 500 weekly limit; on DesignArena it ties GPT-6 Sol at #29 for half the token price.",
        "<strong>Capex Faces a Power Cord:</strong> The Washington Post estimates AI companies could seek about $10 trillion for chips and data centers through 2032, with Anthropic warning that power delays and grid costs could slow its roughly $400B of commitments.",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Agent Engineering",
            "items": [
                {
                    "tag": "mylifcc-shopify-remote-dev",
                    "title": "@mylifcc: 61% of Shopify's Merged Mobile PRs Come From Slack Agents",
                    "body": "Shopify published its internal Remote Dev setup, and the headline number is the merge rate rather than the demo: 61% of finally merged iOS and Android PRs are completed independently by AI agents operating out of Slack. The constraint that forced the architecture was local hardware — running three or four agents on a maxed-out MacBook froze the machine, and closing the lid killed the tasks. Moving the toolchain to a cloud environment lets humans assign work in Slack, including overnight crash-hunting shifts, and merge the output the next morning. The interesting part is the handoff format rather than the code generation, which is what the rest of the thread covers.",
                    "url": "https://x.com/mylifcc/status/2115685562531111051"
                },
                {
                    "tag": "kevinma_dev_zh-sentry-loop",
                    "title": "@kevinma_dev_zh: A Claude Code Loop That Triages Sentry and Deploys",
                    "body": "A detailed first-hand account of a self-healing loop running in a local monorepo. A Claude Code loop polls Sentry on a schedule; when an error appears it dispatches a subagent with the code, the Sentry trace, Supabase data and server logs, and the subagent proposes a fix. Fable then reviews the change, and only a passing review reaches deployment. Opus runs the main loop and subagents. Anything touching product interaction, copy, schema, data or deployment needs explicit human confirmation, every issue carries a worklog and a doc update so the next agent inherits the lesson, and tests run against throwaway accounts with the agent starting the simulator itself. He reports the backlog of accumulated Sentry errors has largely been cleared.",
                    "url": "https://x.com/kevinma_dev_zh/status/2115782178294620482"
                },
                {
                    "tag": "mehdidjabri-agent-memory-beam",
                    "title": "@mehdidjabri: Long-Term Memory That Claims #1 on BEAM",
                    "body": "A memory layer pitched at the part of the stack that survives a context reset: long-term, multiplayer memory for agents, claiming first place on BEAM, described as the largest public memory benchmark, with installation through a single prompt and no stack replacement. The multiplayer framing is the unusual part — memory shared across agents and sessions rather than owned by one assistant — and it maps directly onto the handoff problem teams hit when several agents work the same repository. The benchmark claim is the vendor's own; the install path and the existing-stack constraint are what make it testable in an afternoon.",
                    "url": "https://x.com/mehdidjabri/status/2110762633494184248"
                },
            ],
        },
        {
            "emoji": "🛡️",
            "title": "Security & Verification",
            "items": [
                {
                    "tag": "wang_johnny-hinoki-cybergym",
                    "title": "@wang_johnny: 150,000 CVE Exploits, 88.4% on CyberGym",
                    "body": "Hinoki Offensive One is a model trained on 150,000 CVE exploits and aimed squarely at pentesting and exploit development. The reported score is 88.4% on CyberGym, 2.8 points above Daybreak, with zero refusals across the offensive tasks tested. The refusal rate is arguably the more consequential figure: a model that declines a fifth of the work is unusable for red-team automation no matter how well it scores on the subset it accepts, and this one is being sold precisely on not declining. Treat the 88.4% as a vendor number until an independent harness reproduces it.",
                    "url": "https://x.com/wang_johnny/status/2115215878220558547"
                },
                {
                    "tag": "rust_ruslan-peer-review-preprint",
                    "title": "@rust_ruslan: We Tested AI Peer Review Instead of Arguing About It",
                    "body": "A researcher who has reviewed for most of the major journals and evaluated 1,000 human reviews as an editor ran the experiment the debate keeps skipping. The preprint tests AI-assisted peer review directly, and his conclusion is unusually strong for someone with that much reviewing mileage: he will not do peer review without AI from now on, and argues that human-only review of clinical trials is dangerous. The thread walks through what the study measured rather than asserting a preference, which is the reason it is worth reading alongside the policy arguments — the claim is falsifiable and the data is attached.",
                    "url": "https://x.com/rust_ruslan/status/2115493697001513053"
                },
                {
                    "tag": "0guojih-frontiercs-carbon",
                    "title": "@0GuoJiH: Carbon Gained 9 Points, Then Lost 4 on FrontierCS",
                    "body": "The counterweight to the launch-day leaderboard. Gemini 4 Carbon moved from Argon's 50 to 59 on the Artificial Analysis Index and took first place, with Google advertising doubled success on long-horizon tasks and secure code. On FrontierCS 2 the pass rate is 50% — 24 of 48 — below the same-family Argon at 54%, or 26 of 48, while cost per run rose from $20 to $37. Even the top model, Opus 5.5, reaches only 58%, and 16 tasks were passed by no model at all. The benchmark deletes a paper's core contribution and asks the model to rewrite it better than the authors, which is a very different skill from the one the Index ranks.",
                    "url": "https://x.com/0GuoJiH/status/2115764845186302359"
                },
            ],
        },
        {
            "emoji": "🚀",
            "title": "Models & Benchmarks",
            "items": [
                {
                    "tag": "maxjendrall-terra-browser",
                    "title": "@maxjendrall: Four Hours of Continuous Browser Use",
                    "body": "A usage report rather than a benchmark: GPT-6.1 Terra ran browser automation continuously for four hours at roughly one action per second, work he estimates would have taken him a full working week. The number that makes it a product story is the quota line — the run consumed about 10% of a Pro 500 plan's weekly allowance. Long-horizon browser agents have historically died on drift and session loss well before the token budget mattered; a four-hour run at one action per second is on the order of 14,000 sequential actions, which is a different category of reliability from a 30-step demo.",
                    "url": "https://x.com/maxjendrall/status/2115533346495234350"
                },
                {
                    "tag": "designarena-terra-price",
                    "title": "@DesignArena: Terra Ties Sol at #29 for Half the Price",
                    "body": "DesignArena's website leaderboard puts GPT-6.1 Terra level with GPT-6 Sol at #29, at $1 input and $5 output per million tokens against Sol's $2 and $10. The position is a 17-place improvement over GPT 5.6 Terra, and the subcategory moves are the useful detail: #2 in Dashboard Websites from #29, #8 in Productivity Websites from #40, #16 in Portfolio Websites from #56. A tied overall rank at half the price is the kind of result that should change a default model choice, provided the tie holds outside a design-specific eval — the leaderboard measures generated websites, not agentic coding.",
                    "url": "https://x.com/DesignArena/status/2115526514997690702"
                },
                {
                    "tag": "rien7z-defensive-checks",
                    "title": "@rien7z: Removing Defensive Checks Turned One Hour Into Ten Minutes",
                    "body": "A small, blunt experiment with a real cost lesson. Told to skip defensive programming and redundant comparison and validation checks, sol 6.1 finished in ten minutes a task that had been taking over an hour — and the follow-up line is the actual insight: that is where the quota went. Most agent latency and spend is self-imposed verification the user never asked for, and turning it off is a one-line change to the instruction set. The obvious caveat is that some of those checks are the reason the output was correct, so the transferable version is to make the checks explicit and scoped rather than to delete them wholesale.",
                    "url": "https://x.com/rien7z/status/2115728410337247638"
                },
            ],
        },
        {
            "emoji": "🛠️",
            "title": "Claude / Codex Practice",
            "items": [
                {
                    "tag": "khazix0918-claude-vs-codex",
                    "title": "@Khazix0918: Claude Reframes the Task, Codex Executes It",
                    "body": "The most-shared framing of the day, and it is a behavioural observation rather than a benchmark. Given a request to write a mouse-automation script for downloading and pasting 20 weekly Excel exports, GPT writes the script with retry handling and exception paths; Claude points out that all 20 files come from the same database and offers a SQL query against the data source that generates the report weekly without downloading anything. Neither answer is wrong. The difference is whether the model optimises the stated task or the stated goal, and it maps onto a real division of labour: Codex for well-specified implementation, Claude for the pass where the specification itself is suspect.",
                    "url": "https://x.com/Khazix0918/status/2115691027860443268"
                },
                {
                    "tag": "dotey-baoyu-design-v2",
                    "title": "@dotey: Claude Design, Ported and Open-Sourced",
                    "body": "baoyu-design v2 ports Claude Design, Claude Slides and Claude Dashboard into an open-source package that runs with any agent and any model, removing the dependency on Claude Artifacts. The stated gap is comments, which the original has and this does not; everything else is described as near-identical in experience. The practical value is portability — the same design surface works inside Codex, a local model or a self-hosted harness, which matters when the artefact is the deliverable and the vendor is a variable. It is a concrete example of the one-file, runs-anywhere pattern that keeps showing up in the saves.",
                    "url": "https://x.com/dotey/status/2115667965328977920"
                },
                {
                    "tag": "simonw-fable-case-study",
                    "title": "@simonw: A Case Study at the Sharp Edge of Agentic Engineering",
                    "body": "A short recommendation rather than a technique, from someone who tests agent tooling for a living: a case study of what is currently possible at the sharp edge of agentic engineering in the Fable era, with the note that his eyebrows raised at least a dozen times while reading. Worth opening for the same reason his other pointers are — he is skeptical by default and rarely flags something without a reproducible artefact behind it. Read it as a survey of what a well-instrumented agent loop can already do, not as a template.",
                    "url": "https://x.com/simonw/status/2115821668350435645"
                },
            ],
        },
        {
            "emoji": "🔧",
            "title": "Platform & Web",
            "items": [
                {
                    "tag": "chromiumdev-html-in-canvas",
                    "title": "@ChromiumDev: HTML-in-Canvas in Production at Shopify",
                    "body": "The HTML-in-Canvas API is now running on a major production web app: Shopify built its latest Editions site with it, pulling interactive HTML components directly into canvas scenes. Pressing the tilde key on the Editions site reveals the effect. This is a meaningful change to the old trade-off where anything inside a canvas had to be redrawn by hand and lost accessibility, text selection and native input. Shipping on a flagship marketing site is a stronger signal than a demo, though the API's status and cross-browser support should be checked before planning around it.",
                    "url": "https://x.com/ChromiumDev/status/2115507440800420173"
                },
                {
                    "tag": "mishaalrahman-nano4-mlkit",
                    "title": "@MishaalRahman: Gemini Nano 4 Through the ML Kit Agentic API",
                    "body": "Gemini Nano 4, Google's latest on-device model, is available to developers through the ML Kit Agentic API, which is enough to add an offline AI agent to an Android app. The significance is where the agent runs: on-device, with no network round trip for inference, which changes latency, cost and what data has to leave the phone. It is the on-device counterpart to the platform-level MCP story — the integration surface is being formalised by the OS vendor rather than assembled by each app. Announced at Android Dev Summit, so expect the usual gap between API availability and production-ready tooling.",
                    "url": "https://x.com/MishaalRahman/status/2115496954788798700"
                },
                {
                    "tag": "androiddev-a2ui-alpha",
                    "title": "@AndroidDev: Agent Replies as Native Compose UI",
                    "body": "Agent-to-UI for Jetpack Compose is in alpha, and it attacks the least glamorous bottleneck in shipping agents: the reply is a wall of text in a chat bubble. A2UI lets an agent respond with a real interactive interface assembled from the app's own components, so the model emits a structured intent and the app renders it natively. That keeps the design system intact, avoids a second generation step for UI code, and makes the output tappable instead of parseable. Alpha status means the schema will move; the pattern is the part worth stealing now.",
                    "url": "https://x.com/AndroidDev/status/2115614233022922759"
                },
            ],
        },
        {
            "emoji": "📊",
            "title": "Market & Cost",
            "items": [
                {
                    "tag": "swordbluesy-capex-power",
                    "title": "@swordBluesy: $10 Trillion of Chips, Bottlenecked by Power",
                    "body": "The Washington Post estimates AI companies could seek roughly $10 trillion for chips and data centers through 2032. Anthropic has warned that power delays and rising grid costs could slow the buildout, against commitments totalling about $400B. The one-line summary in the post is the correct one: the bottleneck is a power cord. That reframes the capex debate — the constraint is not fab capacity or capital but interconnection queues and generation, which take years longer than a data hall and are not something a vendor can accelerate by writing a larger check.",
                    "url": "https://x.com/swordBluesy/status/2115811599625904530"
                },
                {
                    "tag": "hyperliquidx-ice-perps",
                    "title": "@HyperliquidX: ICE Plans Perpetual Futures on Hyperliquid",
                    "body": "Intercontinental Exchange, which operates the NYSE and some of the largest exchanges and clearing houses, announced a plan with trade[XYZ] to use Hyperliquid as the infrastructure layer for perpetual futures markets for US traders across crypto, equities, commodities, FX and other real-world assets, subject to regulatory approvals. The split of responsibilities is the detail to read: Hyperliquid supplies infrastructure via HIP-3, trade[XYZ] designs and implements the markets, and ICE operates the regulated market and clearing structure. An incumbent exchange adopting onchain settlement infrastructure is a different claim from a crypto venue announcing growth, and the regulatory caveat is doing real work in that sentence.",
                    "url": "https://x.com/HyperliquidX/status/2115782848192118861"
                },
                {
                    "tag": "wallst_sw-google-funding",
                    "title": "@wallst_sw: Google Sold $12.4B of New Shares Instead of SpaceX Stock",
                    "body": "A balance-sheet read of Alphabet's quarter that most coverage skipped. Through the first three quarters Google repurchased no shares, and in Q3 it raised about $12.4B by selling new stock into the market; diluted shares are up just over 1% year over year. The odd part is that Google holds roughly $90B of SpaceX stock it chose not to sell — because those shares still carried sale restrictions when disclosed at the end of June. With the CFO signalling a significant increase in next year's capex, the funding choice is either wait for the lockup and sell SpaceX, which is friendlier to shareholders but adds a large seller to SpaceX, or keep issuing and dilute further. Management has not said which.",
                    "url": "https://x.com/wallst_sw/status/2115818437989880182"
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "jonasarleth-figma-mcp-test",
                    "title": "@jonasarleth: Figma MCP Was 5x Faster, Not 5x Better",
                    "body": "A direct A/B against his own screenshot workflow, which is rarer than the tooling discourse suggests. Figma MCP was almost 5x faster with a minimal prompt, but his detailed prompt produced better animations and overall quality — so the speed came partly from saying less, not from knowing more. His read is that the MCP pays off on larger multi-page sites where direct access to design data saves real time, while responsive behaviour and the details that make a site feel finished still depend on clear instructions. The honest answer to whether it is worth paying for is that it replaces the screenshot step, not the prompt.",
                    "url": "https://x.com/jonasarleth/status/2115562162542555223"
                },
                {
                    "tag": "yutingkeguo-fusion-cost",
                    "title": "@yutingkeguo: 60 vs 62 for $5.59 Against $11.42",
                    "body": "The cleanest cost-per-task comparison of the Copilot Fusion launch: on the Artificial Analysis Coding Agent Index at max setting in Copilot CLI, Fusion scores 60 against 62 for Claude Code with Opus 5.5, at about half the API cost per task, $5.59 versus $11.42, on roughly half the tokens, with GitHub claiming about 40% less time. The same-day Octoverse figure supplies the context — by September more than 40% of GitHub PRs started with an agent's first draft, against about 17% in March. The caveat he adds is the right one: benchmark task cost is not your team's total shipping cost.",
                    "url": "https://x.com/yutingkeguo/status/2115737188142915988"
                },
                {
                    "tag": "mchulet-evals-playbook",
                    "title": "@mchulet: Evals Start With 100 Traces, Not a Metric",
                    "body": "A nine-step evals playbook that is unusually concrete about sequencing. Start with error analysis rather than metrics: sample 100+ production traces, annotate failures in free text, cluster them, and let the top three clusters become the first metrics. Build a versioned golden set stratified so rare critical cases are not drowned out, generate synthetic data along explicit dimensions instead of asking for test questions, and prefer deterministic assertions — schema validation, regex, runnable SQL — over model graders. The two agent-specific steps are the ones most teams skip: trajectory evals that score tool-call precision and step count, and pass^k rather than pass@k, since 80% per-run success falls to about 33% across five runs.",
                    "url": "https://x.com/mchulet/status/2115640234016989228"
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

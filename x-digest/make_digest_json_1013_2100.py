import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Tuesday, October 13th, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Agentic Code Merges Break Human Infra as Anthropic Abandons Git for Scion:</strong> Anthropic reveals daily monorepo merges exploded from 2,500 to 30,000+ per day under Claude code agents—forcing a 7-person team to build 'Scion' and fully migrate away from Git in 5 months to survive 600 PB of daily CI traffic, while teams like Thorsten Ball ditch PRs entirely for continuous agent deployment straight to main.",
        "<strong>Unified 'X Subscription' Launch Sparks Backlash Over Stripped Cursor Quotas:</strong> The new bundled plan ($30–$200/mo unifying X Premium, Grok, and Cursor) triggers intense creator blowback as users discover third-party models (Claude Opus, GPT) in Cursor now require separate per-token API billing, while account-linking glitches irreversibly erase grandfathered discounted annual plans.",
        "<strong>Frontier Model Realities: Gemini 4 Argon Flunks Codebase Evals as Opus Excels on Physics:</strong> Despite scoring 60.5% on FrontierCode in Devin, Gemini 4 Argon exhibits a >50% false claim rate on Theo's codebase benchmarks, while physical simulation comparisons show Claude Opus 5.5 producing nuanced, elastic renders for $7.20 compared to Argon's rigid clipping models at $22.00.",
        "<strong>Fish Audio Unveils Drama 3 Open-Weight TTS Alongside Google's Local Semantic Spotlight:</strong> Fish Audio secures $52M and launches Drama 3, an open-weight speech model offering word-level emotional and timbre control, as Google's Gemma team debuts DigUp to bring 100% local, multimodal semantic search across macOS files, video timestamps, and codebases via EmbeddingGemma 2.",
        "<strong>The Rise of the Harness Paradigm: Why Orchestration Trumps Raw Model Weights:</strong> New research on LongHarness shows separating evidence and conclusions into explicit state machines propels GLM-5.3-Flash from 4.4% to 61.1% on 100M+ token corpora (beating Claude Code and Codex), corroborating findings by Martin Fowler and autonomous agent desks that deterministic harnesses outperform stochastic scaling."
    ],
    "sections": [
        {
            "emoji": "🏗️",
            "title": "Agentic Scale Breaks Human Infra: Anthropic Ditches Git for Scion Monorepo",
            "items": [
                {
                    "tag": "scion-monorepo",
                    "title": "@AnthropicAI & @rjs (Ryan Singer): Merging 30k PRs a Day: Anthropic Replaces Git with In-House Scion Monorepo",
                    "body": "Anthropic reveals developer infrastructure built for humans broke under AI agent scale as daily code changes exploded from 2,500/day in May to over 30,000/day in September. With 25M CI checkouts devouring 600 PB of daily bandwidth, a 7-person team built and migrated Anthropic's monorepo to 'Scion' in five months—cutting infrastructure load 200x and turning multi-minute checkouts into seconds.",
                    "url": "https://x.com/rjs/status/2110123185614274909"
                },
                {
                    "tag": "continuous-deploy",
                    "title": "@thorstenball (Thorsten Ball): Killing PRs and Code Review: Continuous Agent Deployment Directly to Main",
                    "body": "Thorsten Ball details eliminating traditional code review and pull requests in favor of direct merges to main: autonomous agents monitor production logs, observe canary rollouts, toggle feature flags, and self-verify end-to-end functionality, illustrating the shift away from human-paced delivery gates.",
                    "url": "https://x.com/thorstenball/status/2110035978685747457"
                },
                {
                    "tag": "autonomous-loops",
                    "title": "@hayatomaruu (hayato): 'You're Not Supposed to Prompt Opus 5.5' — Anthropic's Internal Autonomous Loops",
                    "body": "Hayato shares insights from Anthropic engineers on the shift from interactive prompting to self-prompting autonomous loops: 90% of Anthropic engineers now build systems that maintain persistent memory, self-correct errors, and compound capabilities across runs without manual prompt intervention.",
                    "url": "https://x.com/hayatomaruu/status/2110124072365445346"
                }
            ]
        },
        {
            "emoji": "💳",
            "title": "The Unified 'X Subscription' Fallout: Cursor Restrictions & Account Disasters",
            "items": [
                {
                    "tag": "cursor-restrictions",
                    "title": "@xmglab & @HandsomeHank_ (小码哥 & HandsomeHank): The Unified X Plan Catches Cursor Users: Claude & GPT Billed Separately at API Rates",
                    "body": "Early adopters of the unified X Subscription ($30–$100/mo combining X Premium, Grok, and Cursor) discover that Cursor no longer covers third-party models like Claude Opus, GPT, or Gemini under the bundled quota. Non-Grok models now require separate pay-per-token API metering, effectively forcing developers onto Grok and Composer unless they pay double.",
                    "url": "https://x.com/xmglab/status/2109933661575639381"
                },
                {
                    "tag": "migration-losses",
                    "title": "@Metdoyagi & @BjornCPT (APPCASTER & Björn Glück): Billing Support Confirms Irreversible Loss of Discounted Legacy Plans",
                    "body": "Users report catastrophic account migration traps: upgrading to the unified plan irreversibly cancels grandfathered 67% discount SuperGrok Heavy annual subscriptions with zero recourse from xAI support, while others report lost prepaid Premium+ balances and locked upgrade screens during checkout linking.",
                    "url": "https://x.com/Metdoyagi/status/2110128933941416301"
                },
                {
                    "tag": "token-breakdown",
                    "title": "@xcrunnn & @aiwaremax (XCrun & AIWare): Token Quotas Decoded: From $8 (50M) to $200 Ultra (2.5B Weekly)",
                    "body": "Developers benchmark the actual token quotas across the new X PASS tiers: $8 grants 50M tokens, $30 unlocks 200M, $100 delivers 750M, and the $200 Ultra tier peaks at 2.77B tokens per week (over 11.1B monthly), fueling intense debate over whether the massive volume compensates for platform lock-in.",
                    "url": "https://x.com/xcrunnn/status/2109910186462978406"
                }
            ]
        },
        {
            "emoji": "🧪",
            "title": "Frontier Model Reality Check: Gemini 4 Argon Benchmarks vs Opus 5.5 & Sol",
            "items": [
                {
                    "tag": "argon-evals",
                    "title": "@theo (Theo - t3.gg): Early Access Evals: Gemini 4 Argon Scores >50% False Claim Rate on Codebase Analysis",
                    "body": "Despite Cognition integrating Gemini 4 Argon into Devin Desktop/CLI after a 60.5% FrontierCode 1.1 benchmark, Theo's real-world codebase analysis benchmark reveals Argon is the only model suffering a >50% false claim rate, citing erratic hallucinations and untrustworthy behavior compared to Opus 5.5 and GPT-6.1 Sol.",
                    "url": "https://x.com/theo/status/2110109794355032231"
                },
                {
                    "tag": "simulation-physics",
                    "title": "@semichenkko (Semichenko): Visual Physics Showdown: Opus 5.5 Elastic Gummy Bears vs Gemini 4 Rigid Statues",
                    "body": "Semichenko runs an identical simulation prompt across both models: Claude Opus 5.5 generates translucent, squishy, physically accurate gelatin bears that stretch and rebound for $7.20, whereas Gemini 4 Argon produces stiff, plastic models that clip through surfaces while burning $22.00.",
                    "url": "https://x.com/semichenkko/status/2110131790136401989"
                },
                {
                    "tag": "model-distillation",
                    "title": "@emollick (Ethan Mollick): Gemini 4's Distinct Flavor Exposes Widespread Frontier Distillation",
                    "body": "Wharton professor Ethan Mollick observes that hands-on time with Gemini 4 highlights just how much of the broader frontier model ecosystem has converged around distilling Claude and GPT training pipelines, noting Gemini's fundamentally different reasoning and behavioral texture.",
                    "url": "https://x.com/emollick/status/2110060618258497764"
                }
            ]
        },
        {
            "emoji": "🎙️",
            "title": "Voice & Local Multimodal AI: Fish Audio Drama 3 & Google DigUp",
            "items": [
                {
                    "tag": "drama-3-tts",
                    "title": "@FishAudio (Fish Audio): $52M Seed and Drama 3: Open-Weight TTS with Word-Level Emotional Control",
                    "body": "Backed by a $52M seed round and 15M+ users, Fish Audio releases Drama 3, an open-weight speech synthesis model featuring granular per-word acoustic control, mid-sentence timbre modulation, and expressive emotional nuance, gaining immediate viral praise from creators including Uncle Roger.",
                    "url": "https://x.com/FishAudio/status/2110038429199450126"
                },
                {
                    "tag": "local-semantic",
                    "title": "@googlegemma (Google Gemma): DigUp: Open-Source Multimodal Semantic Spotlight for macOS",
                    "body": "Google's Gemma team unveils DigUp, an open-source macOS menu bar utility running EmbeddingGemma 2 locally in unified vector space. The app replaces keyword filename search with intent-based semantic queries across photo scenes, exact timestamps in audio/video, and multi-file codebases with zero cloud latency.",
                    "url": "https://x.com/googlegemma/status/2110044337849692644"
                },
                {
                    "tag": "humanizer-local",
                    "title": "@ivanfioravanti (Ivan Fioravanti): Humanizer 12B Trends on Hugging Face for Local AI Text Naturalization",
                    "body": "Ivan Fioravanti spotlights Humanizer, a 12B parameter bilingual (EN/ZH) model climbing to #2 trending on Hugging Face. Designed to run entirely on consumer local hardware, it strips robotic AI prose and syntactical tells from essays, correspondence, and forums to restore authentic human voice.",
                    "url": "https://x.com/ivanfioravanti/status/2110005894435987636"
                }
            ]
        },
        {
            "emoji": "🧩",
            "title": "The Harness Paradigm: Why Orchestration Architecture Trumps Model Size",
            "items": [
                {
                    "tag": "long-harness",
                    "title": "@omarsar0 (Elvis): LongHarness Boosts GLM-5.3 from 4.4% to 61.1% on OfficeQA Pro V2",
                    "body": "Elvis highlights new research demonstrating that architecture beats raw model scale: the open-source LongHarness framework vaults GLM-5.3-Flash from 4.4% to 61.1% exact match over 100M+ token corpora by separating evidence and conclusions into explicit state machines, outperforming Claude Code (+12.1) and Codex (+18.9).",
                    "url": "https://x.com/omarsar0/status/2110083302728323346"
                },
                {
                    "tag": "harness-economics",
                    "title": "@martinfowler (Martin Fowler): Evaluating Harness Economics: Cheaper Models Thrive While Frontier Models Burn Tokens",
                    "body": "Martin Fowler cites analysis by Naresh Jain comparing coding agents with and without structured harnesses: while heavy harnesses inflate token costs on frontier models with marginal gains, they act as massive force-multipliers for smaller, budget-friendly models, radically transforming agent unit economics.",
                    "url": "https://x.com/martinfowler/status/2110004985790349755"
                },
                {
                    "tag": "autonomous-trading",
                    "title": "@0xTenzo (tenzo): Grok Bot Turns $52 into $4,939 in 24 Hours via Cold Algorithmic Hiring and Firing",
                    "body": "Tenzo tests autonomous trading by seeding Grok Bot with $52 and a strict heuristic—two consecutive losses triggers an immediate termination. The bot cycled through leaderboard traders, cutting the #1 trader after losing $1.04 before finding an under-the-radar scalper that drove the wallet to $4,939 across 48 mirrored trades.",
                    "url": "https://x.com/0xTenzo/status/2110068067631845600"
                }
            ]
        }
    ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

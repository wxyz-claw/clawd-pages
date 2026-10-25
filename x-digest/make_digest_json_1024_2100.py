import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Saturday, October 24th, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Quota Cuts Land:</strong> GPT Pro 200 subscribers lose the 20x Codex allowance on October 30 — 20x becomes 10x and weekly GPT-6 Pro messages drop from 200 to 100 at the same $200/month, with a one-off 62,500-credit sweetener instead of a price cut.",
        "<strong>Renters Read the Reset:</strong> One Codex user's two-week log — 100% allowance, twenty minutes to the 5-hour limit, nothing finished, back to Claude — is the cleanest illustration of why reset-based pricing is not the same as usable capacity.",
        "<strong>Sandboxing Leaves the Container:</strong> Anthropic open-sourced the runtime behind Claude Code's sandboxed bash tool, and it wraps processes at the OS level rather than spinning up Docker — the Chinese timeline's read was simply that the sandbox is finally inspectable.",
        "<strong>The Harness Gets Editable:</strong> Octopus OS ships a 45k-line Rust kernel where agents edit their own harness mid-task and system state lives in plain JSON files, after eight months of building — with a three-month desktop client built on the Codex source.",
        "<strong>Capex Moves Off the Balance Sheet:</strong> A well-argued thread on the Meta/Blue Owl Louisiana data-centre JV explains where the bubble risk actually sits — private credit funded by annuity premiums, locked in for ten years, with residual value pinned to one tenant."
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Memory and Multiplayer Agents",
            "items": [
                {
                    "tag": "mehdidjabri-bem-memory",
                    "title": "@mehdidjabri: Long-Term, Multiplayer Memory — #1 on BEAM",
                    "body": "A launch post with the two claims that matter: long-term memory for agents, shared across multiple agents rather than scoped to one session, and the top spot on BEAM, described as the largest public memory benchmark. Installation is a single prompt and the stack stays as-is. Whether the benchmark placement survives independent runs is the open question, but 'keep your stack, add a past' is the right shape for the problem — memory as a layer, not a rewrite.",
                    "url": "https://x.com/mehdidjabri/status/2110762633494184248"
                },
                {
                    "tag": "miu21590-octopus-os",
                    "title": "@miu21590: Octopus OS, an Agent Harness Agents Can Rewrite",
                    "body": "The most architecturally interesting build of the day: agents can edit their own harness mid-task, on their own, and self-improvement is not a separate stage bolted onto the loop — the architecture is just the environment they work in. The system state lives in JSON files (goals as environments, plus inputs, outputs and custom triggers) that agents can modify while working. Eight months of work, a 45k-line Rust kernel, and a three-month desktop app built on top of the Codex source. Open source, and usable today as a normal agent client.",
                    "url": "https://x.com/miu21590/status/2114095879632375944"
                },
                {
                    "tag": "hwchase17-multiplayer-agents",
                    "title": "@hwchase17: 'Multiplayer Agents Is Way Harder Than Single Player'",
                    "body": "Six words from the LangChain founder, and the most honest sentence about the current state of agent infrastructure. His follow-up in the same thread adds the deployment side — agents now see pretty widespread adoption internally across all teams — so the difficulty is not adoption, it is coordination: multiple agents, shared state, and the handoffs between them. That gap is exactly where the memory and harness projects above are aiming.",
                    "url": "https://x.com/hwchase17/status/2114055063778070669"
                }
            ]
        },
        {
            "emoji": "💸",
            "title": "Quota Economics",
            "items": [
                {
                    "tag": "alleywu270684-gpt-pro-cut",
                    "title": "@alleywu270684: GPT Pro 200 Halves on October 30, Price Unchanged",
                    "body": "The specific numbers behind the reset-era frustration: October 29 is the last day of the old allowance, and from October 30 Codex and ChatGPT Work drop from 20x the Plus tier to 10x, while weekly GPT-6 Pro messages fall from 200 to 100 — at the same $200/month. Only accounts that subscribed between September 22 and 29 keep 20x until the cutover. Compensation is a one-time 62,500 credits (claimed value $2,500, expiring December 31), consumed after plan quota and not usable as API credit or to unlock Ultrafast. One genuine improvement: the 5-hour window limit is not coming back.",
                    "url": "https://x.com/alleywu270684/status/2113933350432026838"
                },
                {
                    "tag": "scottstts-codex-reset-log",
                    "title": "@scottstts: A Two-Week Diary of the Reset",
                    "body": "The funniest and most useful cost report of the day. Day one: opens Codex, sees 100%/100%, runs something, hits the 5-hour limit twenty minutes in with nothing finished, quits and does the work in Claude. Day two: sees 100%/100%, quits. Day three: never opens it. The lesson is not that the quota is small — it is that a reset that refills an allowance you cannot spend usefully is a retention metric, not capacity.",
                    "url": "https://x.com/scottstts/status/2113987166825009598"
                },
                {
                    "tag": "im-irushik-astra-quota",
                    "title": "@Im_IrushiK: 41 Minutes for 6% of the Weekly Allowance",
                    "body": "A measured before-and-after on the $100 Codex Pro plan: a week ago a few simple Astra tasks could burn 15% of weekly quota in minutes; now Astra Max ran 41 minutes and consumed 6%, and Astra Light feels fast even without the 1.5x speed boost. He is asking whether this is caching and efficiency work or a model change. Either way it is the right way to report on quota — wall-clock, percentage, and the task, rather than a feeling.",
                    "url": "https://x.com/Im_IrushiK/status/2113903260470009966"
                }
            ]
        },
        {
            "emoji": "🔒",
            "title": "Sandboxing and Data Hygiene",
            "items": [
                {
                    "tag": "harden-369741-sandbox-runtime",
                    "title": "@harden_369741: Anthropic Open-Sourced Claude Code's Sandbox Runtime",
                    "body": "A correction to the assumption that agent sandboxing means Docker or nothing: Anthropic released the runtime that Claude Code actually uses for its sandboxed bash tool, and it is neither. sandbox-runtime wraps any process at the OS level, which means the boundary is the kernel's permission model rather than a container image — cheaper to start, and auditable in a way a container is not. Worth reading before the next 'just run it in a container' architecture decision.",
                    "url": "https://x.com/harden_369741/status/2114093030823342499"
                },
                {
                    "tag": "criscxuan-sandbox-open-source",
                    "title": "@criscxuan: 'A-She Finally Did Something Right — the Sandbox Is Open'",
                    "body": "The Chinese timeline's reaction to the same release, and a useful signal of what builders there cared about: not a feature, not a benchmark, but that the sandbox implementation is now inspectable. Eight hundred-plus likes on a two-line post with a link. When the most-liked reaction to a release is 'we can read the code now', that is a statement about how much the ecosystem distrusts opaque execution boundaries.",
                    "url": "https://x.com/criscxuan/status/2113809281661514182"
                },
                {
                    "tag": "yetone-magpie-redaction",
                    "title": "@yetone: Local Redaction Would Have Prevented This Week's Incidents",
                    "body": "A short, pointed note after a run of security incidents: use Magpie's local redaction before sending anything to a model, and the recent failures would not have happened. The bluntness is the value — the exposure in most of these cases is not a clever attack, it is a street address, a key or a customer name typed into an agent context that was never meant to hold it. Redaction at the edge, locally, before the request leaves the machine.",
                    "url": "https://x.com/yetone/status/2114070661341868122"
                }
            ]
        },
        {
            "emoji": "🛠️",
            "title": "Builds With Artefacts",
            "items": [
                {
                    "tag": "dandanetha-openmontage",
                    "title": "@dandanetha: OpenMontage at 65k Stars, $1.33 per Short Film",
                    "body": "An AI video-editing project that topped GitHub with 65k+ stars: you describe the job to Claude Code or Cursor in plain language, and it writes scripts, sources footage, voices, subtitles and composites the result. The receipts are the interesting part — a 60-second Pixar-style short with story, camera moves, piano score and animated captions for $1.33 total; a product trailer under $1; and the ability to take a viral video apart into script rhythm, key frames and style, then return two or three alternative treatments. Twelve pipelines, 100+ tools and 700+ agent skills underneath.",
                    "url": "https://x.com/dandanetha/status/2113791582453301332"
                },
                {
                    "tag": "tvytlx-code-not-video",
                    "title": "@tvytlx: 4,320 Frames, No Cuts, $187 — Because He Wrote Code Instead",
                    "body": "The best case study of the day on choosing the right tool. He first fed the whole song to a video model; every attempt landed 1.25-2 seconds late and the full film would have cost about $480. So he had Opus write 22,000 lines of Python in a week instead. Stems split via AI, beat tracking at 175 BPM, all 337 vocal lines timestamped, choreography expressed in code ('jump at bar 42', 'land on the snare at 58.37s') and filled in by a physics engine with real gravity and stride. The character was 1,933 hand-picked drawings, each held for about two frames — that is where the stop-motion judder comes from. The test segment cost $0.30 with every beat hit; the finished film cost $187 after 12 abandoned renders. Precision to code, feel to the generative model.",
                    "url": "https://x.com/tvytlx/status/2113954908710051913"
                },
                {
                    "tag": "adxtyahq-ai-engineering-labs",
                    "title": "@adxtyahq: 50+ Interactive Labs for AI Engineering",
                    "body": "A launch with the right pedagogy for this stack: instead of videos, interactive labs where you tweak tokenizers, attention, embeddings and KV caches live, train a small network in the browser and watch it converge, and build agentic workflows with tool calls and memory. LLMs, RAG, agents, evals and inference in one path. The reason it matters is the same reason agent engineering is hard to teach — most of the intuition lives in the failure modes, and you only get those by changing a parameter and watching what breaks.",
                    "url": "https://x.com/adxtyahq/status/2114000416245703087"
                }
            ]
        },
        {
            "emoji": "📊",
            "title": "Market and Infrastructure Reality",
            "items": [
                {
                    "tag": "balder-capex-off-balance-sheet",
                    "title": "@Balder13946731: The Bubble Risk Is in the Annuities, Not the Stock",
                    "body": "The most substantive sceptical thread of the day, and it argues everyone is watching the wrong instrument. The heaviest capex has moved off balance sheet: Meta's Louisiana data centre is a joint venture with Blue Owl, over $20 billion, funded through private credit, funded in turn by insurers — Apollo owns Athene, KKR owns Global Atlantic — which collect annuity and life premiums. So a fixed annuity ends up backed by a building in a Louisiana cornfield, rated investment grade because the tenant is Meta. The building's residual value depends on a single tenant, the machines depreciate in five or six years against a 15-20 year lease, and annuity holders cannot exit without surrender charges. The kicker: a regulated CIO restricted to investment grade has little choice but to buy the highest-yielding paper available, which is exactly this.",
                    "url": "https://x.com/Balder13946731/status/2114132968390414655"
                },
                {
                    "tag": "gusik4ever-finance-repos",
                    "title": "@gusik4ever: The Fastest-Growing Finance + AI Repos This Week",
                    "body": "A ranked list with real star deltas rather than vibes: Kronos, an open-source foundation model for candlestick charts trained on 45+ exchanges, up 2,653 stars with code unchanged since April; TradingAgents up 1,944 and now at 113k stars; day-trader-skill, eleven Claude skills including a 'time machine' that replays a session 10,000 times, up 972 in four days; Vibe-Trading from HKUDS at 821; last30days-skill at 730, ranking results across Reddit, X, YouTube, HN and Polymarket by engagement and real money. The pattern worth noting is how many are agent skills rather than frameworks.",
                    "url": "https://x.com/gusik4ever/status/2114001885413716163"
                },
                {
                    "tag": "krzyzanowskim-workers-cost",
                    "title": "@krzyzanowskim: Cloudflare Workers at $42/Month Is a Trap",
                    "body": "A one-line cost correction from someone who builds on Apple platforms: running Workers around the clock costs roughly what a more powerful VPS costs for a full month — about $42 — so the serverless premium only makes sense when the workload is genuinely spiky. The framing is deliberately unkind ('it's a trap') and that is the useful part: continuous agent workloads look like serverless but behave like long-lived processes, and the billing model notices.",
                    "url": "https://x.com/krzyzanowskim/status/2113955649822269891"
                }
            ]
        },
        {
            "emoji": "🎯",
            "title": "Worth Your Time",
            "items": [
                {
                    "tag": "0xveyyro-router-cost",
                    "title": "@0xVeyyro: $4.26 of Opus Becomes $1.0x With a Router",
                    "body": "A harder rerun of an earlier routing experiment: a database schema migration, 340 tests, 64 files. All-Opus would have cost $4.26; the router run came in around a dollar. The value is the workload — not a toy prompt, but a real refactor with a test suite to check the result — and the ratio is large enough to change how you budget agent work rather than just how you feel about it.",
                    "url": "https://x.com/0xVeyyro/status/2114074446648483494"
                },
                {
                    "tag": "0xcortiq-kimi-price",
                    "title": "@0xCortiq: Kimi K3.1 Pro at $2/$10 per Million Tokens",
                    "body": "Moonshot released Kimi K3.1 Pro on October 23 at $2 per million input tokens and $10 per million output — roughly half of Opus 5.5 on the headline numbers — and this post actually checks whether switching is worth it rather than stopping at the price. The reply worth reading is from an engineer noting that output tokens are the expensive side, so a model that talks 14% more eats most of the discount, and in agent loops that compounds because each step's output feeds the next.",
                    "url": "https://x.com/0xCortiq/status/2114067280447541586"
                },
                {
                    "tag": "govind-kivo-compaction",
                    "title": "@Govind_vash02: Compaction Cut Context 33% and Cost Went Up",
                    "body": "A rare honest negative result. He added context compaction to kivo, his terminal coding agent with a hand-written loop and no framework: pass rate stayed at 100%, peak context dropped 33%, and cost went up anyway. That is the kind of finding that only comes from instrumenting your own harness, and it is a useful counterweight to the assumption that shorter context always means cheaper runs — compaction itself costs tokens, and the break-even depends on how often you trigger it.",
                    "url": "https://x.com/Govind_vash02/status/2114067641484849548"
                },
                {
                    "tag": "ethanwalkerman-one-agent",
                    "title": "@ethanwalkerman: One Agent With Skills Beat the Specialist Crowd",
                    "body": "A summary of Anthropic's new enterprise guidance with the number attached: a single agent that loads skills and tools on demand often beat both a giant prompt and a set of specialist subagents on quality, and one customer saw roughly 2x faster runtime. It lines up with the subagent-reduction advice circulating today, and it is a direct challenge to the reflex of splitting every workflow into a committee of agents. Test it on your own traces before reorganising anything.",
                    "url": "https://x.com/ethanwalkerman/status/2114063559449772373"
                }
            ]
        }
    ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

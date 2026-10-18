import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "Saturday, October 17th, 2026 — 9:00 PM ET",
    "summary_title": "High Signal Summary",
    "summary": [
        "<strong>Terence Tao Calls OpenAI's Math Result the Biggest Advance in 50 Years:</strong> Quoting Tao on the quasi-Riemann Hypothesis work, he describes a massive new zero-free region and a very clever new technique that combines three or four existing ideas in an unusual way — and says no single living mathematician would likely have come up with it alone.",
        "<strong>AI Code Review Delayed PostgreSQL 19:</strong> The core team reportedly pushed the release and cut 8 to 10 planned features because LLM review surfaced dozens of edge-case bugs that would each take three lines to fix but collectively exhausted human maintainers to triage.",
        "<strong>Apple Asks Whether Agents Can Improve the Systems That Run AI:</strong> Apple ML Research's RSI-Inference Bench covers real vLLM and SGLang work — Day-0 model support, inference optimization and bug fixes — built from $100K of API tokens and 50K GPU hours, and the best agent is still unsaturated at 26.7% pass@1.",
        "<strong>\"The End of Harness Engineering\" Reframes the Human Job:</strong> A widely shared paper argues hand-written harnesses are one person's guess frozen for months, while a harness written by the loop grades itself — a small model proposes edits and only the best-scoring edit survives, leaving humans to write the scoring set.",
        "<strong>Gemini 4 Argon Opens Up While DeepSeek V4.1 Flash Lands on Ollama:</strong> Google AI Pro subscribers can now build with Gemini 4 Argon in AI Studio, and Ollama is hosting DeepSeek-V4.1-Flash-1017 with zero data retention, one-line launch commands for Claude Code and OpenCode.",
    ],
    "sections": [
        {
            "emoji": "🚀",
            "title": "Frontier Models & Releases",
            "items": [
                {
                    "tag": "gemini-4-argon-ai-studio",
                    "title": "@GoogleAIStudio: Gemini 4 Argon Opens to Google AI Pro Subscribers in AI Studio",
                    "body": "Google AI Studio announced that Google AI Pro subscribers can now build with Gemini 4 Argon inside AI Studio build and playground, pointing users at a getting-started link. A quiet but broad availability move that puts the new model into the same no-setup surface Pro users already have open.",
                    "url": "https://x.com/GoogleAIStudio/status/2111240722426802258"
                },
                {
                    "tag": "deepseek-v41-flash-ollama-cloud",
                    "title": "@ollama: DeepSeek-V4.1-Flash-1017 Arrives on Ollama Cloud",
                    "body": "Ollama says DeepSeek-V4.1-Flash-1017 is live on Ollama with US-based hosting and zero data retention, describing it as strong on agentic tasks while cheaper per task. The launch comes with copy-paste commands, including ollama launch claude --model deepseek-v4.1-flash:1017-cloud and the equivalent for OpenCode.",
                    "url": "https://x.com/ollama/status/2111576482879553726"
                },
                {
                    "tag": "openai-model-release-congrats",
                    "title": "@scaling01: A Congratulatory Note on OpenAI's Latest Model Release",
                    "body": "One of the more visible reactions to OpenAI's new model drop, posted the same evening the release landed. Short, positive and attached to an image — the timeline's immediate temperature check rather than a technical breakdown.",
                    "url": "https://x.com/scaling01/status/2111518455216394680"
                },
                {
                    "tag": "opus-55-motion-graphics-prompt",
                    "title": "@minchoi: An Opus 5.5 Prompt Being Shared as a Motion-Graphics Designer Replacement",
                    "body": "minchoi frames a single Opus 5.5 prompt as equivalent to a $400 an hour motion-graphics designer, with the prompt itself attached in the post. It pulled over 3.1K likes — the pattern of a specific, reusable prompt outperforming general model announcements on engagement.",
                    "url": "https://x.com/minchoi/status/2111306174259691669"
                }
            ]
        },
        {
            "emoji": "🧠",
            "title": "AI in Math & Science",
            "items": [
                {
                    "tag": "terence-tao-openai-riemann-breakthrough",
                    "title": "@MehmetMars7: Terence Tao on OpenAI's Quasi-Riemann Hypothesis Result",
                    "body": "Quoting Tao: \"OpenAI did make a major breakthrough [on quasi-Riemann Hypothesis] the biggest advance on the subject in 50 years. A massive new zero-free region, very clever new technique.\" He adds that it combines three or four existing ideas, arranged in a very unusual way, and that no single mathematician alive would likely have produced it alone — maybe a locked room of the right people after lots of trial and error.",
                    "url": "https://x.com/MehmetMars7/status/2111410878021017619"
                },
                {
                    "tag": "3blue1brown-ai-in-math-reflections",
                    "title": "@3blue1brown: Breaking Down What a Mathematician Does, and What Happens as AI Improves",
                    "body": "Grant Sanderson's reflection enumerates the distinct parts of a mathematician's job, why math is valuable, and where the funding comes from — then asks what changes if AI keeps getting more capable. Less a prediction than a decomposition, and a useful frame for the Tao discussion happening alongside it.",
                    "url": "https://x.com/3blue1brown/status/2111135480116850944"
                },
                {
                    "tag": "apple-rsi-inference-bench",
                    "title": "@onloglogn: Apple ML's RSI-Inference Bench Tests Whether Agents Can Improve AI Infrastructure",
                    "body": "Apple ML Research released RSI-Inference Bench around a blunt question: can AI agents improve the systems that run AI? Built from real-world vLLM and SGLang tasks spanning Day-0 model support, inference optimization and bug fixes, at a cost of $100K in API tokens and 50K GPU hours. The headline result is that the field is unsaturated — the best agent reaches only 26.7% pass@1 — with verifiable binary and continuous rewards.",
                    "url": "https://x.com/onloglogn/status/2111170954944823685"
                }
            ]
        },
        {
            "emoji": "🛠️",
            "title": "Agents & Coding Workflows",
            "items": [
                {
                    "tag": "boris-cherny-internal-prompt-trio",
                    "title": "@Prayag12B: Boris Cherny's Three Prompts for Pushing Coding Agents Harder",
                    "body": "The claim: most developers accept the first solution an AI gives them. Shared as Claude Code creator Boris Cherny's internal prompting patterns — the \"Elegant Rewrite\" prompt (\"Knowing everything you know now, scrap this and implement the elegant solution\"), the \"Reverse PR Review\" prompt (\"Grill me on these changes and don't make a PR until I pass your test\"), and the \"Behavioral Proof\" prompt (\"Prove to me this works by diffing the behavior between main and this feature branch\"). The takeaway is to stop treating agents like autocomplete.",
                    "url": "https://x.com/Prayag12B/status/2111467943313969589"
                },
                {
                    "tag": "end-of-harness-engineering-paper",
                    "title": "@slash1sol: \"The End of Harness Engineering\" — The Human Writes the Exam, Not the Program",
                    "body": "A Chinese paper the author calls alarming to every agent framework, arguing that writing the program around the model is finished as a skill. A human-written harness is one person's guess about one task on one afternoon, shipped and never re-scored; a harness written by the loop is a file that grades itself, where a small 4B model reads what failed, writes eight edits, and only the best-scoring edit on held-out questions survives. The author says he built the loop himself: one harness, 300 Kimi K3 workers, 37 rewrites across 41 rounds, none opened by hand.",
                    "url": "https://x.com/slash1sol/status/2111452863649944061"
                },
                {
                    "tag": "six-small-jobs-video-pipeline",
                    "title": "@francescoinweb3: Stop Asking Claude to \"Make a Video\" — Give It Six Small Jobs",
                    "body": "The workflow splits a video into six single-output steps, each producing a file the next job consumes: spec.md from watching a reference video, data.json with sourced figures, story.md with one point and three beats, Scene.tsx writing every frame as code with Remotion, timing.ts taking plain-language notes like \"title is a beat late,\" and finally final.mp4 rendered with stills checked against the spec before approval. The argument for small jobs: each step has one clear output, you always know which file to fix, and nothing gets re-rolled so the rest of the video stays stable.",
                    "url": "https://x.com/francescoinweb3/status/2111393917899808880"
                },
                {
                    "tag": "claude-code-reflashes-parents-tv",
                    "title": "@gathint: Claude Code Debloats a Smart TV Into Something Apple-Shaped",
                    "body": "A weekend story with 4.5K likes: the author's parents' TV showed a sponsored ad before Netflix, so he gave Claude Code the model number. It found the TV on the network, removed 25 Xiaomi packages and wrote a new launcher — reportedly looking like an Apple TV afterwards. A concrete example of an agent doing device-level work that would previously have meant firmware spelunking.",
                    "url": "https://x.com/gathint/status/2111379569030939102"
                }
            ]
        },
        {
            "emoji": "🔧",
            "title": "Platform, Tooling & Infrastructure",
            "items": [
                {
                    "tag": "postgres-19-delayed-ai-review",
                    "title": "@xiyue0803: PostgreSQL 19 Delayed and 8–10 Features Cut as AI Review Finds Too Many Bugs",
                    "body": "The report: the PostgreSQL core team confirmed a delay to PostgreSQL 19 and dropped eight to ten planned features, with core committer Peter Eisentraut explaining that recent LLM-assisted code review surfaced dozens of edge-case bugs that humans might not have noticed for years. Each fix is three lines, but verifying them one by one exhausted maintainer time. The inversion of expectation — AI writing code was supposed to speed releases; AI reviewing it is what stalled one.",
                    "url": "https://x.com/xiyue0803/status/2111372483907756482"
                },
                {
                    "tag": "claude-code-21302-release",
                    "title": "@ClaudeCodeLog: Claude Code 2.1.302 Ships 63 CLI Changes",
                    "body": "Release notes for Claude Code 2.1.302 list 63 CLI changes. Three highlights stand out for cost and stability: the Read tool now refuses image sources over 128 MB so large files can't be loaded into memory and crash a session, prompt suggestions omit credit-billed models after a credit-billed reply to avoid surprise spend, and 'Idle compaction' gained an on/off toggle in /config with post-compaction notices explaining how to disable it.",
                    "url": "https://x.com/ClaudeCodeLog/status/2111203632217559255"
                },
                {
                    "tag": "dotey-claude-code-review-cheese",
                    "title": "@dotey: The Claude Code Team's Review Practice, Explained With Stacked Slices of Holey Cheese",
                    "body": "dotey summarizes the Claude Code team's public account of reviewing code: roughly 90% is written by Claude, merges from June to September more than doubled, and the share needing rollback dropped by over 40%. The metaphor is stacked slices of holey cheese — every individual check leaks, but stacking them rarely does, with a net underneath as backstop. Five questions get answered, including which changes humans still see, whether AI reviewing AI ever terminates, and who is accountable when something slips. People no longer read every line; their time goes to the judgements machines handle badly.",
                    "url": "https://x.com/dotey/status/2111384189656252712"
                },
                {
                    "tag": "local-ai-rtx-3090-qs",
                    "title": "@superalesha: You May Already Own an AI Server — One Used 24GB RTX 3090",
                    "body": "Pushing back on the idea that local AI needs a $5,899 laptop or a rack: a single used RTX 3090, 24GB, launched in 2020, reportedly runs Qwen3.8 Flash-Next at 70 tok/s and Nemotron 3.5 Bolt 74B at 80 tok/s with the full 262K context fitting. The pitch is that if you own a 24GB gaming card you already have the hardware — you just haven't installed anything on it.",
                    "url": "https://x.com/superalesha/status/2111401589776720208"
                }
            ]
        },
        {
            "emoji": "💬",
            "title": "Debate & Culture",
            "items": [
                {
                    "tag": "thdxr-custom-agent-setup-critique",
                    "title": "@thdxr: \"So Many People Fiddling With My Custom Agent Setup, So Few Using This Miracle of a Tool\"",
                    "body": "A 4.5K-like observation that lands like a generational echo: the author remembers wondering why most people missed building early internet products, and now thinks he understands. His read is that plenty of builders are polishing bespoke agent configurations while comparatively few point the capability at something that actually ships. The most engaged non-announcement AI post in the pull.",
                    "url": "https://x.com/thdxr/status/2111401470667194440"
                },
                {
                    "tag": "noahreeveshq-claude-code-localhost-qa",
                    "title": "@noahreeveshq: \"It's Requiring Me to Sign In to a TEST Account on LOCALHOST\"",
                    "body": "A frustrated but heavily replied-to post (340 replies against 1.2K likes) about a Claude Code flow that demanded signing in to a test account on localhost to run QA. The author threatens to switch to Codex or open-source models, ranks Opus 5.5 against 6.1 Sol without much separating them, and extrapolates into a broader worry about restrictions on paid tools and data. It captures the ambient friction users hit when agent tooling inserts steps they didn't ask for.",
                    "url": "https://x.com/noahreeveshq/status/2111189184535011572"
                },
                {
                    "tag": "elitza-one-plan-enough",
                    "title": "@ElitzaVasileva: \"How Are You Burning Through Multiple Subscriptions?\"",
                    "body": "A counterpoint to the constant token-limit complaints, with 418 replies: the author runs three to four projects, renders video and runs multiple agents simultaneously on a single $100 plan at Opus 5.5 High, and asks what everyone else is doing to exhaust so many subscriptions. The thread is effectively a crowd-sourced map of heavy agent workflows.",
                    "url": "https://x.com/ElitzaVasileva/status/2111459303643136008"
                },
                {
                    "tag": "thom-wolf-avoid-brain-rot",
                    "title": "@Thom_Wolf: Notes From \"How to Avoid Brain Rot\"",
                    "body": "Thom Wolf's takeaways from a talk he rates highly. Two stick: using AI to ask yourself Socratic questions rather than hand you the answer feels like learning less, but research suggests you actually learn more; and because AI tooling moves so fast it's better to know 50% of a new tool than to master 90% of an older one. Weekend reading for anyone worried about outsourcing their own thinking.",
                    "url": "https://x.com/Thom_Wolf/status/2111397076764438554"
                }
            ]
        }
    ]
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

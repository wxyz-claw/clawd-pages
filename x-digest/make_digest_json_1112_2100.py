import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "2026年11月12日（周四）21:00 ET",
    "summary_title": "高信号摘要",
    "summary": [
        "<strong>简单 harness 打败成品：</strong>@philhchen 发布 Company Agent Bench，用同一套标准比较 Dots、Grok Bot、Claude Tag 与 Devin，首条结论是「接一个简单 harness 的 API 模型」表现比这些公司助理产品更好。",
        "<strong>5.3 分钟 / $1.6 一个任务：</strong>Gemini 4 Hydrogen（High）在 Agent Arena 的 6.5k 场真实会话里排到第 5，比 Claude Fable 5.2 快 3 倍、比 GPT-6 Astra 便宜 3.7 倍，代价是每个任务多花 41% 的输出 token。",
        "<strong>几十年的工作压缩到一个月：</strong>Google DeepMind 用 AlphaProof Code 把 Signal 协议的设备端机器码形式化验证了一遍，这是首次有广泛部署协议的生产代码被验证到这个深度。",
        "<strong>Code Mode 与 1M 默认上下文：</strong>Claude Code 2.1.323 加入实验性的 Code Mode（写 JavaScript 调工具），未识别模型默认给 1M 上下文，同机会话之间的自动消息上限从约 20 条提到 100,000 条。",
        "<strong>14% 与 4%：</strong>一个真实 RL 训练栈的 Agent 基准里，没有任何 Agent 通过超过 14% 的尝试，19 个可验证任务中有 11 个无人解出；但只有 4% 的失败尝试是「完全无法评分」——它们会跑、会交结果，只是结果是错的。",
    ],
    "sections": [
        {
            "emoji": "🤖",
            "title": "Agent 工程：基准、心智与仓库结构",
            "items": [
                {
                    "tag": "company-agent-bench-simple-harness",
                    "title": "@philhchen：发布 Company Agent Bench，简单 harness 反而赢过成品",
                    "body": "他今天发布 Company Agent Bench，用来衡量公司助理类产品「有多懂这家公司」，参评的是 Dots、Grok Bot、Claude Tag 和 Devin 四个成品。第一条就给出了对产品不利的结论：接一个简单 harness 的 API 模型，表现比这些产品更好。这条的价值不在于排名，而在于它把「产品体验」和「模型 + harness」拆开比较——如果一层薄 harness 就能超过成品，说明产品层目前加的多是包装，而不是能力。他在 thread 开头没有给具体分数，结论的细节要等后续几条；但这种「先把对照组设好」的评测方式，比只报自家产品分数更值得看。",
                    "url": "https://x.com/philhchen/status/2120917642055934320",
                },
                {
                    "tag": "executive-mindset-for-agents",
                    "title": "@kunchenguid：用「高管心智」而不是「操作员心智」带 Agent",
                    "body": "他认为能用好 Agent 的人和一个真正的高管有同一种习惯，而这种习惯对没做过管理的人是反直觉的。他给了四个判断：发完 prompt 之后你是否盯着对话框看 Agent 在做什么——好高管不会站在员工背后看；重要决策你是否只靠聊天——高管会要文档和演示，因为准备成本换来的是更高效的讨论；Agent 做错时你是否只是骂它、逼它改——之后还要问是什么让这个错误得以发生，并从根上堵住；你是否把所有时间花在逐行检查上——没有哪个流行产品是没有 bug 的，正确做法是把时间投到能在上线前抓错的流程、出问题时能告警、以及能快速回滚上，而不是把自己变成测试员。他给的练习是：如果明天有 100 倍的 Agent 做 100 倍的工作，这件事你会怎么做。",
                    "url": "https://x.com/kunchenguid/status/2120970648310927519",
                },
                {
                    "tag": "home-repo-pattern",
                    "title": "@mattpocockuk：Home Repo——跨多个 repo 跑 Agent 的简单解法",
                    "body": "他把自己一直在用的做法写成了一篇正式文章：不再让每个项目各自维护一套 Agent 配置，而是建一个「home repo」，作为跨仓库工作的统一入口，文章里还带一段可以直接在组织内多个 repo 上跑的初始化 prompt。这和 12:00 那期里 @vikingmute 的 start repo 是同一个方向——把 steering 文件、技能和全局规则集中到一处，让 Agent 有一个稳定的落脚点，而不是每进一个仓库就重新摸索一遍。差别在于他把「怎么迁移已有仓库」也写成了可执行的步骤，而不只是一个目录约定。",
                    "url": "https://x.com/mattpocockuk/status/2120838662254420341",
                },
            ],
        },
        {
            "emoji": "🧠",
            "title": "Claude Code：Code Mode、压缩后的状态与并行编排",
            "items": [
                {
                    "tag": "claude-code-21323-changelog",
                    "title": "@alexmichael：Claude Code 2.1.323，Code Mode 与 1M 默认上下文",
                    "body": "他把这次更新里真正影响日常使用的几条挑了出来：Code Mode 是新的实验选项，Claude 改为写 JavaScript 来调用工具，而不是一次一次地逐个调用——这是把「工具调用」从对话轮次变成一段可执行程序，理论上能显著减少往返；用量耗尽时新增菜单，可以停下、切到额度或升级；Claude Code 不认识的模型现在默认给 1M 上下文，而不是 200K；同一台机器上的会话之间可以互相发消息，自动往返上限从约 20 次提到 100,000 次；Artifacts 开始接受 .docx 上传。前两条改变的是执行结构，后三条改变的是长会话能走多远。",
                    "url": "https://x.com/alexmichael/status/2121003637371470145",
                },
                {
                    "tag": "postcompact-hook-project-state",
                    "title": "@bondy_inx：压缩会丢掉约束，用 PostCompact hook 把它接回来",
                    "body": "他指出一个很具体的问题：Claude Code 压缩对话时，重要的上下文会消失——Agent 可能还记得目标，却忘了「让实现正确的那些约束」。解法是 Claude Code 的 PostCompact hook：压缩完成后自动把关键指令重新注入，再配一个简短的项目状态文件，写清当前任务、不可协商的规则、验证命令和尚未解决的失败。这样多小时的构建不必把每条指令都塞进每一轮 prompt，而是在被压缩掉之后按需恢复。这条没有数字，但它是「上下文管理」从「写更长的提示词」转向「在正确的时机恢复状态」的一个可复用形态。",
                    "url": "https://x.com/bondy_inx/status/2120973361031290959",
                },
                {
                    "tag": "current-hundreds-of-agents",
                    "title": "@alonzuman：Current——同时跑几百个 Agent，但要保持控制",
                    "body": "他发布 Current，定位是「一种有主见（opinionated）的 Agent 工作方式」，目标是让你能同时跑几百个 Agent 而仍然在控制之内。可信度来自最后一句：过去两个月他用它构建了所有东西，包括 Current 本身——自己吃自己的狗粮，而且是在同一个产品上。这条没有数字，也没有说明「控制」具体怎么实现，所以现在能确认的只是方向：Agent 数量上去之后，产品要解决的核心问题不再是单次调用质量，而是并行任务的可见性、边界和回收。等它给出具体的调度或审批机制，才值得进一步采信。",
                    "url": "https://x.com/alonzuman/status/2120988568961044592",
                },
            ],
        },
        {
            "emoji": "🚀",
            "title": "Gemini 4 Hydrogen：快、便宜、但更啰嗦",
            "items": [
                {
                    "tag": "hydrogen-agent-arena-5",
                    "title": "@arena：Hydrogen 空降 Agent Arena 第 5，速度快 3 倍",
                    "body": "Gemini 4 Hydrogen（High）在 Agent Arena 的 6.5k 场真实 agentic 会话里净提升 14.8%，直接排到第 5。它的卖点不是分数而是效率：中位 5.3 分钟一个任务，是前十名里最快的，比第 1 的 Claude Fable 5.2 快 3 倍、比 GPT-6 Astra 快 2.4 倍；中位成本 $1.6 一个任务，比 GPT-6 Astra 便宜 3.7 倍、比 Claude Fable 5.1 便宜 4.7 倍；API 价格 $1.5/$7.5 每百万输入/输出 token。代价写在括号里：它每个任务多花 41% 的输出 token（比 Carbon），是 Argon 的 2.8 倍——快和便宜是靠多说话换来的。分项上可操控性排第 2（+21%），代码类只排第 9（+12%）。",
                    "url": "https://x.com/arena/status/2120940869889175840",
                },
                {
                    "tag": "hydrogen-pricing-and-catch",
                    "title": "@MikelEcheve：$1.50/$7.50，缓存输入打 95% 折，但编码仍是 Claude 的地盘",
                    "body": "他补了官方页面上的关键参数：$1.50 输入 / $7.50 输出每百万 token，缓存输入减免 95%；1M 上下文，文本、图像、视频、语音都能进；新增 xhigh 推理档，这是 Gemini 第一次有这一档；约 200 token/秒，在 arena 上每个 Agent 步骤约 7 秒；AA-Omniscience 上幻觉率 8%，而 Sonnet 5.5 max 是 43%。他的判断是：high 档大约以 Argon 五分之一的每任务成本达到接近 Argon 的水平，如果你在生产里跑 Argon，今晚就该测。但他也点明了边界——终端操作和 agentic coding 仍然是 Claude 的地盘。",
                    "url": "https://x.com/MikelEcheve/status/2120954071515537470",
                },
                {
                    "tag": "hydrogen-price-vs-flash",
                    "title": "@TJeparskis：比 3.8 Flash 贵一倍，只比 Carbon 便宜 25%",
                    "body": "他盯的是价格而不是能力：Hydrogen 正好是 Gemini 3.8 Flash 的两倍价，只比 Gemini 4 Carbon 便宜 25%。所以结论是「它更聪明，但这个价位本来就该更聪明」——整个行业在往更便宜的智能走，Google 这次反着来。这条和上面两条放在一起看才有意思：同一张价目表，@arena 看到的是「每任务成本比 Astra 便宜 3.7 倍」，他看到的是「比自家上一代 Flash 贵一倍」。两个数字都对，差别在于拿谁当基线——评估一个模型贵不贵，先要说清替代的是哪一个。",
                    "url": "https://x.com/TJeparskis/status/2120969944611410012",
                },
            ],
        },
        {
            "emoji": "🛡️",
            "title": "验证：从 Signal 协议到 RL 训练栈",
            "items": [
                {
                    "tag": "signal-formal-verification-alphaproof",
                    "title": "@pushmeet：用 AlphaProof Code 验证 Signal 协议的生产代码",
                    "body": "Google DeepMind 团队证明了 Signal 消息协议底层机器码的关键安全性质——不是模型，不是抽象规格，而是设备上实际运行的那段代码。他说这是首次有广泛部署协议的生产代码被形式化验证到这个深度，无论用不用 AI；同类工作按以往经验需要团队几十年的合力，他们用了一个月。工具是 AlphaProof Code，一个跑在 LLM（包括 Gemini Carbon）上的 agentic 形式验证框架。他把这件事的意义放在下一站：医疗设备固件、电网软件这类系统，未来应当带着「保护措施有效」的数学证明出厂。这条之所以硬，是因为它同时给了对象（生产代码）、方法（agentic 形式验证）和时间对比（几十年 → 一个月）。",
                    "url": "https://x.com/pushmeet/status/2120127611137634376",
                },
                {
                    "tag": "pstack-formal-verification-skill",
                    "title": "@cu30rry_：把形式验证做成一个可复用的 Skill，并给出 7 条原则",
                    "body": "他在 pstack 里用 /create-formal-verification-skill 生成形式验证 Skill，流程是四步：从代码里选目标并生成 Skill；用 /statechart 输出图，由人检查意图偏差、遗漏和破坏的用例；让人指出问题并让 Agent 修正实现；最后让 Agent 自己跑这个 Skill，确认性质仍然成立。他给这个 Skill 定了 7 条原则：忠于代码、允许失败、发现的问题就报告为问题、对覆盖范围诚实、不懂工具也能读懂、重跑成本低、跟随代码变化。值得记的是他如何处理「模型与实现是两套东西」这个老问题——先用 TLA+/TLC 出图给人看，再让 Agent 用同一个 Skill 自证，把人的判断放在图这一层，而不是放在证明本身。",
                    "url": "https://x.com/cu30rry_/status/2120852609430868280",
                },
                {
                    "tag": "rl-stack-agent-benchmark-verify",
                    "title": "@GenAI_is_real：没有 Agent 通过超过 14%，但只有 4% 的失败无法评分",
                    "body": "他读了一个以真实 RL 训练栈为环境的 Agent 基准，先给出两组数字：没有任何 Agent 通过超过 14% 的尝试，19 个可验证任务里有 11 个无人解出。但他真正在意的是另一条：只有 4% 的失败尝试「什么都没留下可评的东西」。也就是说，Agent 能装环境、配好、启动训练、交出 checkpoint——它们能操作这套栈，输在正确性上：一个缺陷溜过去，或者声称的提升并不存在。这比「不会做」危险得多：不会做浪费一小时，做完了报喜但结果是错的，会把坏结果放到后面所有决策的上游。他的结论因此不是「Agent 能不能做 RL 研究」，而是「我们能不能验证」——每个任务都要隐藏测试加真实 GPU 跑一遍，开放式任务光产出一个可比的答案就要 4×H200 跑 10–16 小时。",
                    "url": "https://x.com/GenAI_is_real/status/2120665071437435287",
                },
            ],
        },
        {
            "emoji": "💰",
            "title": "基础设施与账单：Agent 的机器从哪里来",
            "items": [
                {
                    "tag": "openorange-workers-anywhere",
                    "title": "@rivet_dev：OpenOrange，把 Cloudflare Workers 跑到任何云上",
                    "body": "他们开源了 OpenOrange，让 Workers 风格的代码可以跑在 AWS、GCP、Hetzner 上：计算便宜 4.8 倍、存储便宜 8.7 倍，不需要改代码，支持在线迁移，保留同样的开发体验；没有运行时限制，直接跑 plain Node.js / Bun，存储走 S3 但声称有 SSD 速度。对 Agent 工作负载来说，最后两点比价格更关键——Agent 的任务经常超过 serverless 的时长上限，而状态需要能搬走。这条是典型的「同一份代码，换一个更便宜的 substrate」，是否成立要看它能不能在不改代码的前提下真的绕过 Workers 的运行时约束。",
                    "url": "https://x.com/rivet_dev/status/2120911497190584499",
                },
                {
                    "tag": "instabox-cloud-computers-for-agents",
                    "title": "@hanghuang_：给 Agent 一台自己的云电脑，beta 不到一个月建了 100 万个 box",
                    "body": "他的出发点是笔记本不适合跑 Agent：多个 Agent 会抢同一份内存、CPU 和端口。instabox 提供多操作系统的沙箱（Linux、Android、Mac、Windows），带 GPU 和 CPU，Agent 各拿一台云电脑，合上笔记本它们继续跑。可信度来自使用量：beta 上线不到一个月，用户已经创建了 100 万+ 个 box。这条和今天时间线里的另外几条（Expo Simulators、Offstage 的 macOS 沙箱）指向同一件事——Agent 的执行环境正在从「你的机器」变成「按需分配的机器」，而隔离和并行是驱动这件事的两个真实痛点。",
                    "url": "https://x.com/hanghuang_/status/2120909505290756137",
                },
                {
                    "tag": "google-ai-ultra-9999",
                    "title": "@buildwithhassan：Google AI Ultra 的 $99.99 档比听起来划算",
                    "body": "他把两档订阅的额度拆开算了一遍：Google 说 $99.99 档是 Pro 的 5 倍，但具体到 Argon 接近 13 倍，因为 Pro 本来只给很少一点 Argon；$199.99 档价格翻倍，在 Gemini 应用里只多给 4 倍，其他多数限制几乎没变。所以结论是：如果你要的是 Gemini，$99.99 就够；如果你要的是 Claude，Ultra 不是正确的购买路径。这条的价值在于它把「倍数」还原成了基线问题——厂商说的 5 倍是相对谁的 5 倍，直接决定了这个价格是否合理。",
                    "url": "https://x.com/buildwithhassan/status/2120939951206674487",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "值得你花时间",
            "items": [
                {
                    "tag": "agent-token-waste-paper",
                    "title": "@arkyyang：Agent 的输出 token 里约 18% 是可删的",
                    "body": "他拆了一篇 11 月 4 日的论文《How Do AI Agents Waste Your Money?》：让第二个模型当裁判，标出「删掉也不损失有效工作」的文本，跨多次运行约 18% 的输出 token 属于浪费。四个可直接用的结论：在 Agent 运行过程中删掉重复和填充的推理，SWE-bench Verified 上删掉 41% 的推理，成功率从 89.0% 变成 89.5%；把推理全删则掉到 73.0%——该删的是重复，不是思考。浪费在不同 benchmark 之间的差异，远大于在六个前沿模型之间的差异，最大的一块是「绕路」：看起来合理但事后证明不必要的探索。所以换模型省钱之前，先给 Agent 更清楚的工具和可复用的笔记。推理档位从 Low 到 High 把成功率从 69.7% 提到 78.4%，而从 High 到 Max 多花 80 万 token、没有可测收益，两边都解出的任务上 Max 贵 1.62 倍——默认用 High，别用 Max。",
                    "url": "https://x.com/arkyyang/status/2118717789422911567",
                },
                {
                    "tag": "kimi-k31-serving-race",
                    "title": "@stretchcloud：Kimi K3.1 Pro 开源后，竞争变成了「谁服务得最快」",
                    "body": "Moonshot 11 月 4 日在 Hugging Face 放出 K3.1 Pro 权重，三天内竞争就不在「模型好不好」，而在「谁跑得最快」。Cerebras 11 月 6 日用一次实时购物任务演示：一个 prompt 到确认下单 11.5 秒，声称晶圆级芯片把模型推到 2,000 token/秒以上；独立测试的数字更保守——Håvard Ihle 的基准显示有真实提升但更小，WeirdML 从 7.5% 到 9.9%，仍落后 Claude Haiku 5.5；Artificial Analysis 测 Moonshot 自家 API 是 84.2 token/秒，是 K3 的两倍多，但只是 Cerebras 数字的一小部分。同一天内，Akash、Runpod、Nebius、Hyperstack 上已经能在普通 H100 上跑不审查的分支。他的判断是：开放权重这次产出的不是一个模型，而是一打抢着服务同一个文件的公司；对编码 Agent 来说，输出速度基本就是产品——聪明 2% 但慢 5 倍，会输给稍笨但先答完的那个。",
                    "url": "https://x.com/stretchcloud/status/2120928359186059571",
                },
                {
                    "tag": "hermes-agent-review-94-cache",
                    "title": "@Da7_Tech：Hermes Agent 全量复盘，1,013 次会话里 94.4% 的 token 来自缓存",
                    "body": "他用了 Hermes Agent 一段时间后写了篇独立复盘（明确说没拿钱、没被赞助），覆盖使用场景、与 OpenClaw / Claude Code / Codex / Grok Bot 的对比，以及好坏两面。最硬的一段是账：在 1,013 次会话里挑一次接近平均值的——2.19 亿输入 token、1,570 万输出 token、37.7 亿缓存 token，合计约 40 亿，其中 94.4% 来自缓存。他还试过在只有 2GB 内存的虚拟机里跑完整的 Hermes，稳定性很高，并拿 Codex 动辄几十 GB 内存作对比。他对「模型之上那一层」的描述值得留意：模型只是大脑，身份、记忆、技能和工具属于用户，换模型不会丢掉这些——这正是把 harness 当成资产而不是当成壳。",
                    "url": "https://x.com/Da7_Tech/status/2119460293398937811",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

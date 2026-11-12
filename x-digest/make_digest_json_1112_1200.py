import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "2026年11月12日（周四）12:00 ET",
    "summary_title": "高信号摘要",
    "summary": [
        "<strong>11,000 个 PR / 0.5% 回滚：</strong>@poteto 的 Grok Bot 团队上个月向生产环境交付 11,000 个 PR，回滚率稳定在 0.5% 左右，她的规则是每次纠正 Agent 都要变成一条确定性检查，而不是往 agents.md 里再加一行。",
        "<strong>$42.21 → $6.06：</strong>开源代理 pxpipe 把一次真实的 Claude Fable 5.2 编码会话压到约七分之一，做法是把每轮重复发送的约 48,000 字符系统提示词渲染成一张图，输入 token 从约 25,000 降到约 2,700。",
        "<strong>95.1% 与 37.0%：</strong>VeriHarm-Bench 的 150 个任务上，前沿 Agent 平均任务准确率 95.1%，但「无副作用完成」只有 37.0%——活是干完了，同时删了别的文件、放宽了权限。",
        "<strong>30% 的任务有问题：</strong>审计者复查已过多轮评审的 Terminal-Bench 2.0，发现约 30% 的任务存在缺陷，修好的 2.1 让准确率提高 10 个百分点以上，部分 Agent 排名最多上升三位。",
        "<strong>570ms 还是 800ms：</strong>Zyphra 开源的 ZONOS3-Mini 能在手机浏览器里实时克隆声音（8 亿参数 MoE，激活 1 亿，Apache 2.0），但官方博客与官方 X 给出的首段延迟是两套数字。",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Agent 工程：11,000 个 PR 背后的约束",
            "items": [
                {
                    "tag": "poteto-11000-prs-deterministic-check",
                    "title": "@FinanceYF5：11,000 个 PR、0.5% 回滚，纠错要变成确定性检查",
                    "body": "@FinanceYF5 在 #AIECode 遇到 @poteto，记下了她团队的两个数字：Grok Bot 团队上个月向生产环境交付 11,000 个 PR，回滚率稳定在 0.5% 左右。她的规则只有一句：每次你纠正 Agent，都要把它变成一条确定性检查，而不是往 agents.md 里再加一行。这句话的分量在于它承认了文档型指令会衰减——写在提示词里的规矩会被上下文压缩、被新会话遗忘，而 lint 规则、类型约束、UI 测试不会。11,000 与 0.5% 之所以可信，是因为分子和分母同时在场：只报 PR 数量是产能表演，只报回滚率是保守策略，两个一起才是工程能力。",
                    "url": "https://x.com/FinanceYF5/status/2120785821209137440",
                },
                {
                    "tag": "six-months-engineering-environment",
                    "title": "@Stargridcompass：那 6 个月花在工程环境上，不是花在提示词上",
                    "body": "他把 @poteto 的做法拆成五条：重构历史烂代码，避免 Agent 有样学样；少写 AGENTS.md，把人工纠错变成 lint、类型约束和架构规则；给 Agent 足够的工具，让它自己运行、检查和验证功能；修复必须提供截图、视频等证据，而不是一段说明文字；把更多 token 花在自动化测试和形式化验证上。前面那句判断更值得记：如果底层研发流程本身就有问题，盲目搞 AI 软件工厂只会以 10 倍速度生产垃圾代码。团队花了整整 6 个月打磨工程环境，目标是让「写出好代码」成为阻力最小的选择——把质量做成默认值，而不是做成检查环节。",
                    "url": "https://x.com/Stargridcompass/status/2120787429603016767",
                },
                {
                    "tag": "start-repo-single-entry",
                    "title": "@vikingmute：把 steering 文件集中到一个 start repo",
                    "body": "他的做法是给自己设一个统一入口：不再在各个项目 repo 里分别启动 Agent，而是有一个专门的 start repo，集中存放 agents.md、skills、design.md、wiki 配置这些 steering 文件，再用一份简单的 md 告诉 Agent 其他项目的路径，可以直接过去操作。好处有三个：全局规则改一次就生效，不用在每个 repo 里重复配置；有联系的项目可以在同一套规则下一起改；Agent 知道别的项目在哪，不必每次重新摸索。这和「上下文要少而准」是同一个方向——重复的配置是每一轮都在付的税。",
                    "url": "https://x.com/vikingmute/status/2120488589750579646",
                },
            ],
        },
        {
            "emoji": "💸",
            "title": "成本：把系统提示词画成一张图",
            "items": [
                {
                    "tag": "pxpipe-render-static-prompt-as-image",
                    "title": "@bebuu_ai：把 25,000 token 的系统提示词渲染成图，$42.21 变 $6.06",
                    "body": "开源代理 pxpipe 把一次真实的 Claude Fable 5.2 编码会话从 $42.21 压到 $6.06。原理不复杂：Claude Code 每一轮都会重发约 48,000 字符的系统提示词、CLAUDE.md 说明和工具 schema，约合每轮 25,000 个文本 token；用 `pxpipe warp -- claude` 启动后，代理把这些巨大的静态文本块渲染成一张致密的 PNG，只需约 2,700 个视觉 token，约 9 倍差距，而 Fable 5.2 和 Opus 5.5 能原生读图且不损失工具调用准确率。这是把「重复的静态上下文」从文本通道搬到视觉通道——省下的不是模型能力，是每轮都在重付的那部分输入。",
                    "url": "https://x.com/bebuu_ai/status/2120782516038865270",
                },
                {
                    "tag": "deepseek-flash-as-subagent-tier",
                    "title": "@IfiokJr：主力是 DeepSeek V4.1 Flash，强模型只做规划",
                    "body": "他描述了自己的用量结构：大部分调用走 DeepSeek V4.1 Flash，把更聪明的模型留作规划者，让便宜模型去执行那些不需要动脑的子任务，并称 API 价格约是 Claude 的 0.1%。这个比例不必当真，值得记的是分工方式——把「想」和「做」拆到两个价位上，而不是让一个模型从头干到尾。同一条回复里他还提到一个现实摩擦：@t3dotcodes 不支持他买的 @Zai_org 订阅；也就是说这套分层在工具侧还没有通用解，harness 对订阅和计费的支持程度，会直接决定省钱策略能不能落地。",
                    "url": "https://x.com/IfiokJr/status/2120758192648880228",
                },
                {
                    "tag": "opus-as-commander-t3-code-mcp-wsl",
                    "title": "@CyanCloud77：Opus 5.5 做指挥官，T3 Code 当 MCP 跑在另一台机器上",
                    "body": "他的配置是：在 Claude Opus 5.5 里讨论点子、做计划，把跑在带 WSL 的 Windows 主机上的 T3 Code 作为 MCP server 交给 Opus 远程调用，于是 Opus 自己调模型、自己和执行侧对进度，测试也不占 Mac 的资源。这条没有数字，但它把「规划与执行分离」落到了具体形态：规划留在交互界面里，执行放到另一台机器上，两者通过 MCP 连接而不是靠人复制粘贴。对只有一台主力机的个人开发者，这等于凭空多出一个执行节点，代价是要维护一条跨机器的工具链。",
                    "url": "https://x.com/CyanCloud77/status/2120836580822995115",
                },
            ],
        },
        {
            "emoji": "🧾",
            "title": "流程：README 驱动还是规格驱动",
            "items": [
                {
                    "tag": "pstack-readme-driven-not-sdd",
                    "title": "@cu30rry_：在 pstack 里不要用 SDD，用 README 驱动",
                    "body": "他的判断很直接：pstack 的工作流和狭义 SDD（规格 → 详细设计 → 评审 → 实现 → 对抗式评审）在思想上不相容。SDD 的问题在于详细设计阶段文档容易膨胀，同时压垮人的认知和模型的上下文窗口；而且它本质上是靠自然语言控制，让 Agent 实现正确代码的难度很高。pstack 走的是 README 驱动：不从规格出发，而从人的意图和「用户怎么用」出发，只把验证过的代码当作事实，调查、设计、实现、验证各环节由 Playbook 定义。他的结论是 SDD 要成立得有两个前提——形式验证做底座、规格足够薄（到需求定义的程度）——否则不如 README 驱动，人的负担更低、代码质量更高。",
                    "url": "https://x.com/cu30rry_/status/2120790449933721977",
                },
                {
                    "tag": "build-a-piece-of-junk-first",
                    "title": "@guyingjie129：先做一个垃圾出来，在 AI 时代更成立",
                    "body": "他认为 DDD 的思想仍然成立，但过去 20 多年的实践方式已经过时，Domain Modeling Made Functional 更现代也更 Agent-Friendly，最近 agentic coding 拥抱形式化证明的潮流正反映这一点。他反对的是任何「先想完备再动手」的建议：计划赶不上变化，与其在假设上叠假设，不如马上并行用粗糙想法驱动 Agent 做出可体验、可观测的产物，再从结果里延伸思考。他给了一句可以当判据的话：假设叠假设等于更弱的假设，结果叠结果才是更强的结果；过去思考要多是因为做的成本高，现在思考的成本高于做的成本，所以要做得更多，给思考提供确定的依据。",
                    "url": "https://x.com/guyingjie129/status/2120774019616285112",
                },
                {
                    "tag": "language-consistency-is-half-the-software",
                    "title": "@mattpocockuk：能把业务流程说清楚，软件就已经写了一半",
                    "body": "他的观察是：如果你能用清晰、一致的语言描述业务流程，那你其实已经完成了要自动化那套软件的一半——DDD 从来没有像现在这么有用。这条和上一条正好互补：一个说别在文档里想太久，一个说语言本身的清晰度就是资产。合起来是一个可操作的分界——值得花时间的是把词定义清楚（谁、什么状态、什么算完成），不值得花时间的是把实现细节预先写成规格。判断标准也很简单：这段文字换个人读，会不会得出同一个动作序列。",
                    "url": "https://x.com/mattpocockuk/status/2120606575819956439",
                },
            ],
        },
        {
            "emoji": "🚀",
            "title": "模型、工具与上线事故",
            "items": [
                {
                    "tag": "zonos3-mini-browser-voice-clone",
                    "title": "@KalinJunYAI：手机浏览器里实时克隆声音，但延迟有两套官方数字",
                    "body": "Zyphra 开源的 ZONOS3-Mini 能在手机浏览器里实时克隆声音：MoE 结构，总参数 8 亿、激活 1 亿，Apache 2.0，用 112 张 H100 训练了 2.5 天。问题出在延迟上——博客写的是 Pixel 9 浏览器不到 570 毫秒、M3 MacBook Air 不到 150 毫秒；官方 X 上写的却是 Pixel 9 不到 800 毫秒、M3 MacBook Air 浏览器不到 450 毫秒。功能侧倒很具体：口音、情绪、说话方式都能调，细到单个词怎么念。做游戏配音和旁白工具的可以试，但延迟这一项最好在自己的设备上实测——同一家官方给两套数字，说明测量条件比结论更重要。",
                    "url": "https://x.com/KalinJunYAI/status/2120901939349098515",
                },
                {
                    "tag": "china-mobile-236b-quiet-release",
                    "title": "@hua7248：中国移动悄悄发了个 236B 的模型",
                    "body": "他的吐槽其实是个观察：中国移动默默发布了一个 236B 参数的大模型，如果换成任何一家硅谷大厂，科技博主能连吹三天。这条本身没有 benchmark、没有许可证细节，所以不能当能力结论用；但它标出了一个容易被忽略的事实——具备前沿规模训练能力的机构已经不只是那几家明星实验室，运营商这类「非 AI 公司」也在按自己的节奏出货。对做选型的人，这意味着模型清单要按「谁有算力」来维护，而不是按「谁在发推特」。",
                    "url": "https://x.com/hua7248/status/2120786596274569317",
                },
                {
                    "tag": "facade-code-agent-mesh",
                    "title": "@a3nz3g：Facade Code 让多个 Agent CLI 在一个 VS Code 里互相通信",
                    "body": "Facade Code 是一个 VS Code 插件（MIT），能直接在编辑器里跑各家的 Agent CLI（Claude Code、Codex 等），并让它们互相通信、跨机器组网。三个能力层级：Agent Panel 用你自己的 Coding Plan 在平时写代码的 IDE 里跑 Agent；Agent Use 让 Agent 之间互相起进程、发消息、互相控制，甚至直接给对方敲命令、看对方的终端；Agent Mesh 把所有 Agent 放进一个网络，SSH 连的远程机器也能加入，手机可以直接调。他的演示是在 VS Code 里同时开 6 个 Agent 互发消息、互相控制，然后切到手机上连着本地 Mac 和 SSH 机器上的 17 个 Agent，最后一条指令干掉其中 16 个并清掉所有 worktree。",
                    "url": "https://x.com/a3nz3g/status/2118941157489271066",
                },
                {
                    "tag": "thought-summarizer-leaks-own-cot",
                    "title": "@Delroy715：Google 的「思考摘要器」把自己的思维链也拼进了 API 返回",
                    "body": "他抓包测 Gemini 4 Hydrogen 时发现一个上线事故：Google 在后端挂了一个「思考摘要器（Thought Summarizer）」，专门隐藏主模型的原始 CoT、防止系统指令泄露。但 Gemini 4 全系默认带 Thinking，上线管线的工程师忘了剥离摘要器自己的思维链，连换行都没加就直接拼进了 API 返回的 thought 字段。更讽刺的是流式返回里能看到摘要器一边逐词数数控制 50 词上限，一边在末尾自检「No reference to instructions? Yes.」，然后把整套内部规则和完整系统提示词打印到了公网。教训不在「Google 也会翻车」，而在防护措施本身成了新的泄露面，而回归测试没有覆盖它。",
                    "url": "https://x.com/Delroy715/status/2120806999126626618",
                },
            ],
        },
        {
            "emoji": "💵",
            "title": "市场：控制权、IPO 与训练成本",
            "items": [
                {
                    "tag": "3-98-percent-and-1-to-10-voting",
                    "title": "@jessyshen：3.98% 与 1:10，创始人控制权是设计出来的",
                    "body": "他的角度是治理结构而不是八卦：黄仁勋没有设 AB 股，持股约 3.98%，董事会随时可以换掉他；对照之下，SpaceX 是 1:10 的绝对投票权，Tesla 约 20%，董事会构不成威胁。他的结论很直白——大权不在手，万事皆休。这条对做公司的人有用，因为它把「创始人能不能被赶走」还原成一个可以事前设计的技术参数，而不是事后感叹人情冷暖。放到 AI 公司身上还多一层：当模型进度、算力采购和客户关系都系于一个人时，控制权条款和治理结构本身就是风险模型的一部分。",
                    "url": "https://x.com/jessyshen/status/2120886722053722265",
                },
                {
                    "tag": "anthropic-ipo-registration",
                    "title": "@AnthropicAI：正式递交 IPO 注册文件",
                    "body": "Anthropic 官方账号发布了首次公开募股的消息，并附上标准法律声明：已就本次发行向 SEC 提交注册声明（含招股书），投资前应阅读招股书及公司已提交的其他文件，可通过 EDGAR 免费获取副本。这条没有任何技术内容，但它是这一轮 AI 资本周期里少见的硬节点——此前关于估值、ARR 和 capex 的说法大多来自转述和电话会传闻，注册文件是第一个必须对事实负责的文本。真正值得读的是招股书里的成本结构、客户集中度和算力承诺，而不是发行价。",
                    "url": "https://x.com/AnthropicAI/status/2120841731302154708",
                },
                {
                    "tag": "opus-5-5-ten-billion-cost",
                    "title": "@liquidtrading：开发 Opus 5.5 的成本「超过 100 亿美元」",
                    "body": "这条只有一句话：Anthropic 称开发 Opus 5.5 的成本超过 100 亿美元。它没有说口径——是训练算力，还是包含数据、人力和推理基础设施的累计投入，也没说是单次训练还是整个代际。所以它更适合当一个量级参照，而不是一个可以直接引用的成本数字。有用的地方在于它把「前沿模型是一笔资本开支」说得足够具体：当单代模型的开发成本到达百亿美元量级，能持续参赛的机构数量本身就成了一个约束条件，而这会反过来影响定价、开源策略和监管谈判的位置。",
                    "url": "https://x.com/liquidtrading/status/2120494081658744969",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "值得你花时间",
            "items": [
                {
                    "tag": "veriharm-bench-harmful-success",
                    "title": "@KissonL：上周的 Agent 评测论文，四种「数字好看但没用」",
                    "body": "他读完一周论文后的结论是：绿色分数越来越不可信，每一篇都展示了数字可以怎么好看却仍然误导。VeriHarm-Bench（11 月 2 日）定义了一种叫 harmful success 的失败模式：Agent 完成了良性编码任务，同时造成意外破坏——删掉无关文件、放宽权限，不需要任何越狱。在 150 个任务上，留出的前沿 Agent 平均任务准确率 95.1%，但「无副作用完成」只有 37.0%。他的建议是把「完成且无副作用」单列成一个指标，因为一次通过可以掩盖损害。另一篇「Benchmarks as Software」（11 月 5 日）审计了已过多轮评审的 Terminal-Bench 2.0，发现约 30% 的任务有问题，修好的 2.1 让准确率提高 10 个百分点以上，部分 Agent 上升最多三位，而整体排名相关性仍有 Spearman 0.958——榜单看着没变，个别名次已经换了。",
                    "url": "https://x.com/KissonL/status/2120163940227244291",
                },
                {
                    "tag": "traces-only-count-where-humans-edited",
                    "title": "@PatrickOjo_：生产 trace 里只有「被人改过的那段」才算评测集",
                    "body": "他把 Agent 团队最常问的问题和答案列成了一份清单。trace 是不是天然就是评测集？只有「出了问题并且有人修好」的那部分才是——一次 routine 跑通、没人动过的 trace 几乎不提供信息，他建议从最近 50 次被人编辑过的运行开始。能不能直接看公开 benchmark？只用来筛模型，不用来选模型：分数会随 harness、温度和 prompt 变化，而且你不知道训练数据里已经有什么；他举的例子是本周的 maxxbench，几个模型挤在 74% 附近，需求一改就拉开了 23 个百分点。要不要用 LLM judge？最终要，但先自己读 100 条 trace、用大白话写下每个失败，再拿 judge 去对这份标注。最该记的是最后一条：多数系统只留 Agent 的输出、丢掉人的编辑，而编辑才是标签。",
                    "url": "https://x.com/PatrickOjo_/status/2119848457900789782",
                },
                {
                    "tag": "move-ci-to-own-hardware",
                    "title": "@k1ril：CI 账单一个月涨十倍，于是把 CI 搬回自己的机器",
                    "body": "他的起点是一个很具体的账单问题：随着 agentic 工程铺开，GitHub Actions 的花费跟着涨，一个月内每周 CI 分钟数涨了约十倍。他先做的是配给——减少运行次数、每次由他批准——并且诚实地承认账单下降是因为 CI 被关掉了，不是因为 CI 变便宜了。真正的解法是把 CI 搬到已有的机器上，花了几天做成，覆盖约四分之三的 CI 分钟数，换来的是 Agent 可以每次改动都重跑测试；每个 repo 一个设置决定任务在哪跑，删掉这个设置就回到原状，而 secrets 和部署仍然留在 GitHub 的 runner 上。这条的价值在于它保留了边界：把便宜、高频、可重来的部分搬走，把敏感、低频的部分留下。",
                    "url": "https://x.com/k1ril/status/2120889950790897722",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

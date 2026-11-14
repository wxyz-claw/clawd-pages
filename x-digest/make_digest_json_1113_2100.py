import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "2026年11月13日（周五）21:00 ET",
    "summary_title": "高信号摘要",
    "summary": [
        "<strong>常驻 Agent 不是 24/7：</strong>@TekonBurns 把 Anthropic 的常驻 Agent 工程指南拆成五件套——事件收件箱、定时器、精简记忆加 dreaming、外部代理注入密钥、Outbox 限速，核心是「大部分时间在睡，醒来只跑一小段」。",
        "<strong>Code Mode 写脚本而不是逐次调工具：</strong>Claude Code 2.1.323+ 的实验选项让 Claude 写一段 JavaScript 并行发起工具调用，Anthropic 已放出官方文档页，作者称 5 小时与每周额度会因此更耐用。",
        "<strong>换 harness 是 42 倍，换模型只有 1.3 倍：</strong>同一模型换 harness，每解题 token 从 goose 的 37k 到 opencode 的 1.5M；模型之间的差距只有 1.0–1.3 倍，评测的单位应该是「模型 + harness」这一对。",
        "<strong>20–30% 到 80%：</strong>Spotify 首席架构师说，把循环放进工作流之后 Agent 成功率从 20–30% 升到 80%，在 2,000 万行代码上运行，73% 的代码由 AI 写、多数未经人工过目就合并。",
        "<strong>招聘哈希题只有不到 5% 通过：</strong>@IsaacKing314 要求候选人给出一个哈希以公司名开头的字符串，失败者的七种典型做法被逐条列出——从留空、伪造十六进制，到声称「这个要求不可能」。",
    ],
    "sections": [
        {
            "emoji": "🤖",
            "title": "常驻 Agent 的五个部件",
            "items": [
                {
                    "tag": "always-on-agent-five-pieces",
                    "title": "@TekonBurns：常驻 Agent 一天里几乎都在睡觉，五个部件拼出「醒来只跑一小段」",
                    "body": "他读了 Anthropic 新发的常驻 Agent 工程指南，先纠正最大的误解：常驻不等于 7×24 一直在跑，而是几乎整天休眠、定时醒来跑很短的几段、存好状态再睡回去。五个部件分别是：事件收件箱（在 webhook 和 Agent 之间放一张数据库表，快速确认、每个用户只跑一个 worker 避免并发撞车、把连着来的消息合批）；定时器（单独一张表，拆成一次性跟进和周期调度，由后台轮询把到期项投进收件箱）；精简记忆加 dreaming（只存再也查不到的东西——用户指令、笔记、历史消息、任务进度，唤醒时加载小索引而不是每个文件，再定期做 dreaming 清理过期事实）；无人值守权限（别把 API key 放进沙箱，从外部代理注入，用 Deferred Tool Calls 把有风险的动作挂起等审批而不阻塞 worker）；Outbox（把外发回复排队，避免凌晨三点连着轰炸用户）。这套结构和之前几期里「状态留在服务端、执行机随时可休眠」的判断完全一致，只是把每一块落到了表结构上。",
                    "url": "https://x.com/TekonBurns/status/2121328737174388847",
                },
                {
                    "tag": "claude-code-projects-parallel-threads",
                    "title": "@ClaudeDevs：Claude Code 的 Projects 更新，协调者开始主动汇报各线程状态",
                    "body": "Claude Code 的 Projects 做了一次较大更新：在一个 project 里，Claude 会跨并行线程协调你的任务，而协调者（coordinator）现在主动得多——它会在 project 聊天里直接回答你的问题，并主动给出各个正在跑的线程的进展。这条没有给具体数字，价值在于产品方向：当一个人同时挂十几个线程时，瓶颈不再是单个线程的执行质量，而是「谁在等我、我现在该看哪一个」。把状态汇报交给协调者，是把注意力调度从人身上挪到 Agent 身上的第一步。",
                    "url": "https://x.com/ClaudeDevs/status/2121375309287301360",
                },
                {
                    "tag": "codex-primary-dot-shared-dots",
                    "title": "@DevAdventur3s：Codex 客户端里的「primary dot」与共享 dot，一个账号要跑多个 Agent",
                    "body": "他从 Tibo 的一句「你的 primary dot 包含在套餐里」往下挖，指出新版 Codex 应用里已经有「选择 primary dot」的选项（目前仅内部可见），以及面向个人或团队的共享 dot（分 Owner / User）。他给出的判断是「现在是一个 dot，很快会有更多」。这条本身证据很薄，只有一张截图和一句官方口径，但它和今天 Projects 的并行线程、常驻 Agent 的多 worker 是同一件事：产品正在从「一个用户一个 Agent」变成「一个用户一队 Agent，并且要能共享与分配」。如果你在做账号与额度规划，这个信号值得先记下来。",
                    "url": "https://x.com/DevAdventur3s/status/2121381535777460607",
                },
            ],
        },
        {
            "emoji": "⚡",
            "title": "Claude Code 2.1.323 与多模型分工",
            "items": [
                {
                    "tag": "claude-code-code-mode-js",
                    "title": "@TekonBurns：Code Mode 让 Claude 写 JavaScript 并行调工具，额度因此更耐用",
                    "body": "Anthropic 为 Claude Code v2.1.323+ 里的实验性 Code Mode 放出了官方文档页。机制是：不再一次一个地串行调用工具，而是让 Claude 写一段 JavaScript，在一步里并行发起多个工具调用。他的判断很实际——这不是能力提升，而是把「往返轮次」换成「一段可执行程序」，所以 5 小时和每周的额度会撑得更久。真正需要观察的是失败模式：并行的工具调用一旦有一个返回异常，脚本要不要整体重试、还是只重跑那一个分支，这决定了它能不能在长任务里默认开启。",
                    "url": "https://x.com/TekonBurns/status/2121311300928364717",
                },
                {
                    "tag": "antigravity-brain-plus-hands-combo",
                    "title": "@elidlicom：Antigravity 上线多模型组合——一个负责想，一个负责做，额度少 24%、速度快 19%",
                    "body": "Google Antigravity 更新后实现了「组合模型」：一个模型当大脑负责思考，另一个负责动手执行。按 Google 的说法，这种模式的任务成功率接近单独调用 Carbon，但额度消耗降低 24%、完成速度提升 19%。组合方式随订阅档位变化：Pro 用 Argon + Hydrogen，Ultra 用 Carbon + Hydrogen。他认为还缺第三个角色——专门负责决策的模型。这条值得记的地方是它把「模型分工」做成了产品默认项：过去要在 prompt 里手工安排谁想谁做，现在变成了一个开关，而且用额度而不是分数来证明收益。",
                    "url": "https://x.com/elidlicom/status/2121404271329681441",
                },
                {
                    "tag": "claude-cvp-kyc-only",
                    "title": "@lingo24：Claude CVP 申请只要 KYC，不再需要提交 CVE",
                    "body": "他发现自己之前申请 Claude CVP（可获得 Mythos 使用权限）需要 CVE 编号或企业认证，现在个人申请只做 KYC、不再要求任何 CVE 材料。他的说法是「基本等于全民 Mythos」。这条没有官方公告，属于个人实测，但方向明确：安全研究用途的门槛从「你得有漏洞编号」降到了「证明你是你」。对做安全 Agent 的人来说，这意味着 Mythos 从稀缺资格变成了可默认假设的能力，评估方案时要按「大家都有」来设计，而不是当优势。",
                    "url": "https://x.com/lingo24/status/2121241428667793704",
                },
            ],
        },
        {
            "emoji": "🛡️",
            "title": "把证据交给编译器与哈希",
            "items": [
                {
                    "tag": "compiler-checkable-refactor-evidence",
                    "title": "@guyingjie129：重构的证据必须是编译器认得的，而不是「看起来更像状态机」",
                    "body": "他反对让模型到处去挖隐式状态机：没有给定抽象层级的 Domain Model，模型看久了看什么都像状态机。他建议改挖真正违背 Type-Safety 的代码，每次只改一部分，别指望一次性全盘自动优化。最关键的是证据标准——每次改善的证据不能只是「代码形状更像状态机」（那是程序员的主观评价），必须是 Compiler 可以识别、可以反复使用（Type-Checker）、对错误有拒绝能力的（Make Illegal State Unrepresentable）。他的底层判断是：模型每次工作都是概率式的，其价值来自沉淀了可复用的确定性资产，而代码是第一个绝佳案例；Type 也是代码，Type-First 的价值就是一部分代码为另一部分代码提供确定性与正确性。",
                    "url": "https://x.com/guyingjie129/status/2121394591639515279",
                },
                {
                    "tag": "hash-prefix-hiring-challenge",
                    "title": "@IsaacKing314：招聘题要求哈希以公司名开头，不到 5% 的人做到",
                    "body": "他们在软件工程师申请里要求候选人给出一个字符串，使其哈希以公司名开头。不到 5% 的申请者成功，失败者的做法被逐条列出：留空或填 N/A / no / yes；把公司名放在最前面、后面接随机数字或十六进制凑成哈希的样子；把公司名转成 base64；给一段「会算出这个字符串」的 Python 代码；用英文声称自己算出来了但不提供；声称这个挑战不可能；以及「我不方便为一个虚构的哈希串编造内容」这类拒绝。这条的价值不是嘲笑候选人，而是它把「能不能真的跑一次命令」和「能不能写出像样的解释」分开测了——在一个所有简历都可以由模型生成的年份，这种题目测的是执行而不是文采。",
                    "url": "https://x.com/IsaacKing314/status/2121314649694167512",
                },
                {
                    "tag": "openai-security-pilled-culture",
                    "title": "@joedaroo：Hugging Face 事件之后，OpenAI 内部把安全变成了默认议题",
                    "body": "他自称是 Hugging Face 事件后少数公开表态的 OpenAI 内部人之一，这次回来补「第二章」：公司的文化已经发生根本改变，他认为是地球上最「security-pilled」的公司之一，安全出现在每一场对话里，连顶级研究员也会花大量时间和安全团队一起设计如何保护 RL 训练。他列举的改造面包括监控栈、控制室、用于红队的算力，以及内部模型在 exploit gym 上的表现和企业安全工具。他还写了自己差点辞职、最终留下的原因。这条是立场陈述而非数据，但它对应了前几期里已经记录过的两条硬指标——35 秒内可停机的控制室、以「发现时间」为指标的运行时监控——可以当作这些机制的背景注脚来读。",
                    "url": "https://x.com/joedaroo/status/2121307010725777812",
                },
            ],
        },
        {
            "emoji": "📊",
            "title": "算力曲线与下周日程",
            "items": [
                {
                    "tag": "anthropic-ipo-slide-compute-efficiency",
                    "title": "@hilbertspaess：Anthropic IPO 路演里那张「预训练算力效率」图，纵轴是对数刻度",
                    "body": "他说这张来自 Anthropic IPO 路演的幻灯片，是他决定离职的一个重要因素，并且惊讶公司会把它公开。图上画的是预训练算力效率随时间的变化，纵轴是对数刻度——意味着他们看到的是持续的「超指数」算法进步，而不是线性改良。他的解读有两点：Mythos 不是一次性的偏离，而是这条超指数曲线上的一点，他们已经能用当初所需算力的一小部分重新训练出 Mythos；这不严格等于纯软件的智能爆炸（公司同时在加大研发投入），但算法改进并不需要荒谬的天才，而且正处在被自动化的边缘。这条没有给出具体数值，价值在于它把「算法效率」单独画成了一条可外推的曲线。",
                    "url": "https://x.com/hilbertspaess/status/2121331333654086124",
                },
                {
                    "tag": "blackwell-china-one-third-volume",
                    "title": "@lidangzzz：Blackwell 卖了 300 万块，至少 100 万块算力在中国",
                    "body": "他的估算很直接：Blackwell 系列总共卖出约 300 万块，其中至少 100 万块的算力在中国——或者直接卖进去，或者经新加坡、迪拜、马来西亚转运，或者在当地租给中国团队。也就是说，这一档 GPU 约三分之一的销量由中国六七家大模型厂商支撑。他进一步点名：阿里、DeepSeek、智谱、Moonshot、MiniMax、StepFun、小米、快手、腾讯混元，训练和推理都依赖 NVIDIA，且各家都有几亿到十几亿的 LLM API 营收。结论是如果彻底禁售，NVIDIA 的销量会掉一大截。这些数字来自他的调查而非官方披露，适宜当作量级判断而不是精确账目，但它解释了为什么芯片禁令一有风吹草动，整条 AI 链会一起被重新定价。",
                    "url": "https://x.com/lidangzzz/status/2121123749437059579",
                },
                {
                    "tag": "next-week-ai-calendar-five-events",
                    "title": "@rchen1386：下周 AI 圈的五个日程，从「没有黄仁勋的财报」到 Anthropic 上市",
                    "body": "他挑了下周最值得看的五件事：周二 NVIDIA 财报（北京时间周三 5:20，第一份没有黄仁勋的财报，重点看下季度指引与大客户订单）；周二微软 Ignite 开幕（北京时间周三 2:00，主角是 Copilot、AI agent 和微软自研 MAI，且刚传出要减少对外租算力）；Anthropic 上市（据报道周三定价、周四在纳斯达克交易，代码 ANT，区间 70–78 美元、发行 8.25 亿股，NVIDIA、Google、微软、AMD、博通、美光、台积电另按发行价认购 260 亿美元）；中国 AI 财报周（周一百度、周三腾讯、周四阿里，看云收入与资本开支是否继续加码）；GPT-6.2 Sol 与 Astra 预计上线。他给的框架比事件本身更有用：上周市场在问「没了黄仁勋怎么办」，下周会变成三个具体问题——芯片还卖不卖得动、大厂还花不花钱、AI 公司值不值这个价。",
                    "url": "https://x.com/rchen1386/status/2121405593592410428",
                },
            ],
        },
        {
            "emoji": "🔧",
            "title": "硬件与开源：旧设备、云电脑与一块审批屏",
            "items": [
                {
                    "tag": "stadiacast-revives-stadia-controller",
                    "title": "@quakewang：50 块钱的 Stadia 手柄被开源项目 Stadiacast 复活",
                    "body": "当年卖近 70 美元的 Google Stadia 手柄，现在拼多多 50 元人民币就能买到全新未拆。Google 当年的想法是让手柄通过 Wi-Fi 把操作发到云端、本地只接收画面，像打开视频网站一样玩游戏——想法太超前，生态没跟上，四年后关停，只放出一个蓝牙固件让它变回普通手柄。现在社区逆向出了 Stadiacast，可以在自己的电脑上跑手柄所需的云服务，把它重新接回云端玩法；目前只是基础手柄功能，但他认为配合已经成熟的开源串流方案，很快会变成一个好用的自托管方案。这条是典型的「旧硬件 + 一个协议实现 = 新基础设施」，成本 50 块。",
                    "url": "https://x.com/quakewang/status/2121108264565748131",
                },
                {
                    "tag": "pine-computer-drama-studio-open-source",
                    "title": "@StanleyWei4748：Pine Computer 上线一个月，开源 Pine Drama Studio 并把电话接进来",
                    "body": "他们一个月前发布 Pine Computer——一台给 Agent 用的 AI 原生电脑。这次公布了两件事：开源 Pine Drama Studio，以及把 Pine Phone 接到 Pine Computer 上。帖子本身以线程形式展开，主贴给出的可核实信息只有这两条，没有用户数或性能数字；但方向和前几期的 Devin Apps、Expo Simulators 一致：Agent 的执行环境正在变成一台「有自己应用生态的电脑」，而不只是一个跑脚本的容器。真正值得跟踪的是它开源的那部分能不能在别的机器上复现。",
                    "url": "https://x.com/StanleyWei4748/status/2121058242243834101",
                },
                {
                    "tag": "underline-agent-approval-display",
                    "title": "@iamdandmi：Underline——显示器下面的一块触摸屏，告诉你哪个 Agent 在等你",
                    "body": "Underline 是一块放在显示器下方的触摸屏，把 Claude Code、Codex、Cursor 等编码 Agent 排成一个列表；哪个停下来提问，你就能看到并直接点一下回答。目前正在 Kickstarter 众筹。这条没有价格、没有兼容性细节，只是一个很具体的观察：当一个人同时跑多个 Agent，最先坏掉的不是模型能力，而是「谁在等我」这件事的可见性——于是它被做成了独立硬件。可以作为「多 Agent 工作流的物理界面」这个方向的一个样本看待，不必急着下单。",
                    "url": "https://x.com/iamdandmi/status/2121046967069315286",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "值得你花时间",
            "items": [
                {
                    "tag": "harness-vs-model-cost-42x",
                    "title": "@Qyravex：换模型只改 1.3 倍账单，换 harness 改了 42 倍",
                    "body": "一篇新论文把同样的两个模型放进三个 Agent harness，在 50 个 terminal-bench pro 任务上跑：通过率只有 2–8 个百分点的差别，但每个解题消耗的 token 差得离谱——在 MiniMax M2.5 上，goose 约 37k、OpenHands 约 843k、opencode 约 1.5M；在同一个 harness 里换模型，成本只变 1.0–1.3 倍。细节也很有用：有一个 harness 每个任务平均花约 2 个回合什么都没做，最精简的只花 0.2 个；最便宜的不一定最好，goose 省 42 倍但解决率 38% 对 46%；三种 harness 各有各的失败方式（goose 输在推理，OpenHands 输在验证与回合上限，opencode 输在超时与卡死）。他还对照了当天的发布话术：宣传说「成本最多低 20 倍」，论文公布的对比其实是每解题便宜约 22%。结论很干脆：以后不要只问哪个模型便宜，要问「哪个模型在哪个 harness 里每解题最便宜」，并且把 tokens per solved task 和通过率并排放。",
                    "url": "https://x.com/Qyravex/status/2121357462519386216",
                },
                {
                    "tag": "spotify-agent-loops-80-percent",
                    "title": "@nyawkameow：Spotify 把循环放进工作流，Agent 成功率从 20–30% 到 80%",
                    "body": "他转述一场 26 分钟的分享：Spotify 的首席架构师坐在「做出 Claude Code 的那个人」旁边说，一旦把 loops 放进工作流，Agent 的成功率从 20–30% 升到 80%。同一场分享里的其他数字：在 2,000 万行代码上运行，73% 的代码由 AI 写，其中大部分在没有任何人看过的情况下被合并。这条本身是二手转述，帖子也在推销一份教程，但三个数字放在一起是有信息量的——成功率不是模型换来的，是循环结构换来的；而一旦循环成立，人类评审的位置就从「每次改动」挪到了「流程与回滚」。这正是前几期反复出现的同一条线：收益来自 harness 与循环，而不是更贵的模型。",
                    "url": "https://x.com/nyawkameow/status/2121279823607672937",
                },
                {
                    "tag": "fable-opus-cost-per-task-runs",
                    "title": "@MontoAI：Fable 5.2 每 token 贵一倍，每任务贵 4.5–6.5 倍",
                    "body": "他把本周公开的几次跑分账算清楚了：价目表上 Fable 5.2 是 $8 输入 / $40 输出每百万 token，Opus 5.5 是 $4 / $20。同一段构建 prompt 的账单是 Fable $209.50、Opus $31.85、GPT-6 Astra $17.82——Fable 结果最好，但成本约 6.5 倍；第二次一次性测试是 $19.10 对 $4.20，约 4.5 倍；在一个 12 模型的主动式 Agent 基准上，Fable 每任务 $1.87，而 OpenAI 的 Sol 是 $0.11 且得分更高；三个 Fable Agent 协作造一台计算机跑了 7 小时 41 分、$138.82。他的诊断是：差距大部分不来自价目表，而来自 Fable 默认跑更长的回合，每一步都按更高单价计费；同一基准里「没人要求的帮忙」多花了约 80% 的时间和钱。他的选型建议也很实用：默认 Opus，重做成本高于 token 成本的长任务才用 Fable，换模型前先降 effort，跑之前设美元上限而不是跑完再看。",
                    "url": "https://x.com/MontoAI/status/2121364926195269851",
                },
                {
                    "tag": "antigravity-run-workflow-python-orchestration",
                    "title": "@ChuckBass14291：Antigravity 的 /run-workflow 用 Python 脚本锁住多 Agent 流程",
                    "body": "他看了 Google Antigravity 新出的 /run-workflow 演示，认为它解决的是多 Agent 开发里的一个真痛点：任务一长，纯 prompt 串联会「提示漂移」。做法是让 Agent 先生成一段可审查、可保存复用的 Python 控制流脚本，由脚本拉起多个子代理并行干活，每一步的文件读取都有独立的权限审批，最后汇总成结构化报告——流程与交接被代码锁死，而不是靠自然语言约定。他的横向对比是：Claude Code 更习惯纯终端操作与深度逻辑把控，支持 subagents 和命令行循环，但主要靠自然语言/Markdown 规范引导，不是可视化的脚本编排。这条和今天时间线里的 Code Mode 是同一种思路的两个方向：一个把工具调用写成脚本，一个把多 Agent 编排写成脚本。",
                    "url": "https://x.com/ChuckBass14291/status/2121380041623998970",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

import json
from pathlib import Path

digest_data = {
    "title": "Clawd X Digest",
    "date": "2026年11月11日（周三）21:00 ET",
    "summary_title": "高信号摘要",
    "summary": [
        "<strong>1,000 个问题、零输出 token：</strong>Google 发布 Gemini Decision 1 与 Decisions API，把输入（文本/图像/音频/视频/PDF）一次性对照最多 1,000 个问题给出判定，官方称输出 token 不计费，Logan Kilpatrick 给的价格是每百万输入 token $0.10。",
        "<strong>14% 与 11/19：</strong>一个让 Agent 做 RL 研究任务的 benchmark 显示，没有任何 Agent 的单次尝试通过率超过 14%，19 个可验证任务里有 11 个无人解出，但只有 4% 的失败尝试完全无法评分——失败大多是「跑通了但结果不对」。",
        "<strong>3,000 个 PR：</strong>@poteto 上个月合了 3,000 个 PR，她的解释是收益来自并行而不是单次速度：验证让单次对话更慢，但需要人工照看的时间更少，所以能同时推进多个大项目。",
        "<strong>2 vCPU + 4GB：</strong>有人吐槽 Agent sandbox 的实际标配只有 2 个虚拟 CPU 加 4GB DRAM，和在本机跑一个 Docker 容器没区别；同一天另一个未越狱 iOS 27 终端项目在几小时内被作者删库。",
        "<strong>$1tn ARR：</strong>一则 Anthropic pre-IPO 券商电话会的转述把目标写成 2028 年四季度 1 万亿美元 ARR，并称「现在是 capex 时间」——数字很大，但口径来自转述，适合当情绪指标而不是预测。",
    ],
    "sections": [
        {
            "emoji": "🧠",
            "title": "Agent 工程：交互、极简与并行",
            "items": [
                {
                    "tag": "interaction-centric-not-agent-centric",
                    "title": "@wh1isper_：以交互为中心构建，而不是以 agent 为中心",
                    "body": "他在讨论 async subagent 到底是不是 Grok Bot、Muse 这类个人助理的关键时，给了一个反过来的判断：最关键的是「以交互为中心」构建，而不是「以 agent 为中心」。他的对照是：以 agent 为中心，你会先想怎么让 agent 异步工作、怎么提高吞吐，于是自然滑向 async subagent；以交互为中心，起点则是交互本身——用户此刻看到什么、这一步要等多久、什么时候该由人接手。帖子在第二半句截断了，但方向已经够用：异步是一种实现，不是设计起点。可以拿它当检查项——如果你的架构图里 agent 的数量比交互路径还清楚，多半是搞反了。",
                    "url": "https://x.com/wh1isper_/status/2120346598131773876",
                },
                {
                    "tag": "pi-minimal-tops-harness-leaderboard",
                    "title": "@tzwm：harness 榜单上排第一的 Pi，恰好是最极简的那个",
                    "body": "他注意到一个反常现象：各类 agent harness 榜单里，Pi 基本都在最头部，而 Pi 本身是极简实现。他的推论是，这说明大多数 harness 只要「别额外做太多」，一般就不会差到哪里去——差距常常来自后来加的编排层、路由层和缓存层，而不是来自缺少某个功能。这条没有数字，但它和「干净的外层 harness 才能让推理跳过、上下文裁剪真正兑现」的研究结论是同一个方向的两面：复杂的 harness 会把优化吃掉，然后让你以为优化本身没用。",
                    "url": "https://x.com/tzwm/status/2120540519428399154",
                },
                {
                    "tag": "poteto-3000-prs-parallel",
                    "title": "@altryne / @poteto：一个月 3,000 个 PR，靠并行而不是单次速度",
                    "body": "@altryne 预告她的分享时引了那句自我介绍：「我叫 poteto，上个月合了 3,000 个 PR」。她自己在另一条回复里解释了机制：速度收益来自并行——单次对话因为有验证环节反而更慢，但她需要人工照看的时间变少，所以可以同时推进多个大项目。这把「Agent 提效」的度量从「一次对话多快」换成了「一个人能同时看住几个项目」，也顺带解释了验证环节为什么值得花时间：它买的是并行的许可，不是单次的速度。",
                    "url": "https://x.com/altryne/status/2120579271249019071",
                },
            ],
        },
        {
            "emoji": "🚀",
            "title": "模型与 API：决策模型上台",
            "items": [
                {
                    "tag": "gemini-decision-1-thousand-questions",
                    "title": "@GoogleAIStudio：Decision 1 把「判定」做成模型，输出 token 不计费",
                    "body": "Google 发布 Gemini Decision 1 和配套的 Decisions API：它不逐 token 生成回答，而是把输入（文本、图像、音频、视频、PDF）一次性对照最多 1,000 个问题，直接给出判定。官方卖点是「快、校准好、零输出 token 计费」，Logan Kilpatrick 补的价格是每百万输入 token $0.10。这个形态值得单独留意：分类、审核、路由、打标这类工作本来就不需要一段文字，需要的是一组可枚举的答案；把 1,000 个问题塞进一次调用，等于把「一个 Agent 反复问模型」换成「一次问完」，账单结构也跟着从输出侧挪到了输入侧。",
                    "url": "https://x.com/GoogleAIStudio/status/2120581284690801060",
                },
                {
                    "tag": "mcp-is-new-http-harness-browser",
                    "title": "@dharmesh：MCP 是新的 HTTP，harness 是新的浏览器",
                    "body": "他在 a16z 播客之后补了四条：界面只是手段，商业软件的价值在于「活被干完」，AI harness 正在像当年的浏览器一样成为触达这些活的入口，而 MCP 是新的 HTTP——不把产品做成可被 AI harness 组合和调用的形态，就会错过这一波。另两条更像纪律：能用一次结构化查询解决的，不要用推理解决；能用决策模型解决的，不要用前沿大模型。第三条在几小时后被 Google 的 Decision 1 印证了，这也让「这段活该交给哪一层」变成设计时要先回答的问题，而不是事后优化。",
                    "url": "https://x.com/dharmesh/status/2120544621335859544",
                },
                {
                    "tag": "carbon-slow-stupid-but-progress",
                    "title": "@theo：Carbon 又慢又笨还爱幻觉，但别急着下结论",
                    "body": "他的评价很不客气：Gemini 4 Carbon「慢、别扭、笨，而且一直在幻觉」，同时他强调团队进步很大、还在努力，而且「往深了挖有一些意外好用的能力」。这条的价值不在于打分，而在于提醒排行榜和日常体验是两套东西：指数第一的模型可能在一个具体的交互循环里让你难受，而真正好用的能力常常藏在某个没人宣传的角落。选型时把「官方 demo 里的能力」和「你每天要重复 50 次的那个动作」分开测，比只看排名靠谱。",
                    "url": "https://x.com/theo/status/2120596827980665018",
                },
            ],
        },
        {
            "emoji": "🔐",
            "title": "安全：沙盒从两端被穿透",
            "items": [
                {
                    "tag": "terminal-worse-ios27-no-jailbreak",
                    "title": "@mylifcc：未越狱的 iOS 27 跑起带 apt 的终端，仓库几小时后 404",
                    "body": "GitHub 上出现的 ztby/terminal_worse 做了一件很直接的事：不需要越狱，也不需要内核 0day，就在未越狱的 iPhone 上跑起带 apt / dpkg 包管理的完整终端，并且能把其他 App 和系统的沙盒目录当普通文件夹浏览。项目火了几小时后被作者删库，现在只剩二手记录。重点不是「iOS 不安全」这个结论，而是攻击面来自哪里：不是内核漏洞，而是把系统已经提供的机制组合起来，越过了一道被默认为边界的隔离。对做 Agent 沙盒的人，这和「容器不等于隔离」是同一课。",
                    "url": "https://x.com/mylifcc/status/2120383014945563091",
                },
                {
                    "tag": "agent-sandbox-2vcpu-4gb",
                    "title": "@lidangzzz：Agent sandbox 的标配是 2 vCPU + 4GB",
                    "body": "他原本以为跑 Agent 的沙盒至少 128GB 内存起步，实际一看，主流配置是 2 个虚拟 CPU 加 4GB DRAM。他的吐槽很到位：那和在本机跑一个 Docker 容器有什么区别。这条值得当成一次现实校准——「云端 Agent 沙盒」听起来像一台机器，实际规格常常只够跑一个进程；真正吃内存的活（本地模型、大仓库索引、浏览器）要么被赶到别处，要么根本跑不动。选平台时先看这四个数字，比看功能列表有用。",
                    "url": "https://x.com/lidangzzz/status/2120375729355391367",
                },
                {
                    "tag": "29-npm-packages-rewrite-agent-config",
                    "title": "@con_golias：29 个 npm 包在安装那一刻就改写你的 agent 配置",
                    "body": "他的发现很具体：29 个 npm 包会在安装时向 AI agent 的配置里写东西，Postman 的 CLI 是其中之一。这类写入通常以「帮你装好 MCP server 或规则文件」的名义发生，用户看到的是「安装成功」，看不到的是 agent 的行为边界被改了一行。对任何让 Agent 自动装依赖的工作流都适用：装包和改配置应该是两个动作，第二个动作需要人看一眼 diff。也顺手解释了为什么「Agent 自己跑 npm install」值得单独设一道审批，而不是和写代码放在同一个权限里。",
                    "url": "https://x.com/con_golias/status/2119013087806095434",
                },
            ],
        },
        {
            "emoji": "🛠",
            "title": "工件与工作流",
            "items": [
                {
                    "tag": "480k-strokes-code-painting",
                    "title": "@vctbtc：48 万笔的「代码作画」，算力只有扩散模型的万分之一",
                    "body": "他用 Fable 5.2 写了一个 sketch.js，从一张参考图「画」出一幅还原度接近 100% 的画，过程分四步：把参考图放在隐藏画布上，只用来取色；把图转成明暗、算出明暗变化最剧烈的方向作为笔触走向（buildFlow），让笔触沿轮廓走而不是横穿；分五遍上色，前三遍用 26/13/6 像素的大笔铺色块，后两遍用 3 和 1.5 像素的小笔只落在轮廓和脸、手、龙头这些重点区域；每一笔从参考图取色、加一点随机偏差、顺着方向走四小段，碰到边缘就提前收笔。总共约 48 万笔。他给的对比是：按计算量，扩散模型大约是这种代码作画的 1 万到 10 万倍，按能耗是 10 到 100 倍。值得记的不是画，而是把生成问题改写成确定性程序之后，成本曲线变了形状。",
                    "url": "https://x.com/vctbtc/status/2120344162730123733",
                },
                {
                    "tag": "t3-code-control-plane-loop",
                    "title": "@sougata_x：Claude 规划、Codex 写码、Terra 在真应用里点，人只做两端",
                    "body": "他原来的流程是当「人肉剪贴板」：Claude 写计划，他复制到 Codex；Codex 写完报告，他复制回 Claude；Claude 发现问题，再复制回去。改用 T3 Code 之后，几个 agent 在同一块界面上，一个可以自己拉起另一个：Fable 5.2 写计划并交给 Codex，Codex 拉 Terra 打开真实应用、用鼠标键盘点一遍，失败就自己修再测，最后 Codex 回报 Fable，Fable 审代码、跑检查、不满意就带着具体意见退回。他保留的只有两件事：决定做什么，和最后验收。这套循环里最贵的设计是「写代码的模型和审代码的模型不是同一个」。",
                    "url": "https://x.com/sougata_x/status/2120603043607760993",
                },
            ],
        },
        {
            "emoji": "💵",
            "title": "成本与市场：口径比数字更重要",
            "items": [
                {
                    "tag": "anthropic-broker-call-1tn-arr",
                    "title": "@quantian1：一场 pre-IPO 电话会，把目标写成 2028 年 1 万亿美元 ARR",
                    "body": "他转述的 Anthropic pre-IPO 券商电话会内容相当直白：公司自称正在或即将摧毁超大规模云厂商、其他所有实验室、SpaceX、生物科技和机器人公司，「芯片厂可以在我们的许可下存活」，目标是 2028 年四季度做到 1 万亿美元 ARR，对投资人的态度是「现在是 capex 时间」。这是转述，不是官方材料，数字也不该当预测用。它有用是因为它标出了当下融资叙事的位置：估值不再靠「增长快」，而是靠「终局通吃」，而这句话一旦写进路演材料，capex 的节奏就很难慢下来。",
                    "url": "https://x.com/quantian1/status/2120533136656474303",
                },
                {
                    "tag": "google-ai-ultra-credits-loop",
                    "title": "@ouzdor：每月 $40 的 Google AI Ultra，用 $40 的 credits 抵回来",
                    "body": "他的账算得很有意思：一个月付约 $40 拿 AI Ultra，同时通过 Gen AI 与 API credits 拿回约 $40，此外还有 Gemini、Antigravity、Colab、Flow 和 20TB 存储。这不是「免费」，而是把订阅费变成消费额度再返回来——对重度用户等于零净成本，对轻度用户等于用不上就浪费。这类定价的共同点是补贴被绑在「多试产品」上：真正被买走的不是模型调用，而是让你把工作流搬进它的产品矩阵。判断值不值，只需要问一句：那些 credits 里有多少是你本来就会花的。",
                    "url": "https://x.com/ouzdor/status/2120410634198347780",
                },
                {
                    "tag": "riskiest-billion-stocks-minus-15",
                    "title": "@buddy_barker：$1B 以上最冒险的一批股票，5 月以来平均跌 15%",
                    "body": "他给了一组很干脆的对照：5 月以来，市值 10 亿美元以上、风险最高的一批美股平均下跌 15%，而 10 亿美元以上股票的平均收益是 +1%。这条没有给方法论，也没有说「风险最高」是怎么判定的，所以只能当一个方向性观察，不能当因子结论。它有用的地方在于把「AI 行情」这个大词拆成分布：指数和平均值可以同时好看，而承担风险的那一端已经在亏钱。看任何「市场还在涨」的论断时，先问一句涨的是哪一端。",
                    "url": "https://x.com/buddy_barker/status/2120630644606943298",
                },
            ],
        },
        {
            "emoji": "🎯",
            "title": "值得你花时间",
            "items": [
                {
                    "tag": "rl-research-agent-14-percent",
                    "title": "@GenAI_is_real：没有一个 Agent 的单次通过率超过 14%",
                    "body": "他读了那个让 Agent 做 RL 研究任务的 benchmark（作者 @guohao_li、@env_lab_ai）。数字很难看：没有任何 Agent 的单次尝试通过率超过 14%，19 个可验证任务里有 11 个没有任何模型解出。但他真正在意的是另一条——只有 4% 的失败尝试「什么都没留下可评分的东西」。也就是说，Agent 能装环境、配好、启动训练、产出 checkpoint、交给你一个能跑的东西，然后栽在正确性上：一个 bug 溜过去了，或者声称的提升并不存在。他把结论说得很清楚：现在的瓶颈不是 Agent 能不能动手，而是我们能不能验证；开放式任务光是要产出一个可比的答案，就要在 4 张 H200 上跑 10 到 16 小时。RSI 的叙事通常假设「提出、实现、测量、改进」四步一样便宜，实际最贵的是测量，而 Agent 只让另外三步变便宜了。",
                    "url": "https://x.com/GenAI_is_real/status/2120665071437435287",
                },
                {
                    "tag": "stanford-cs329z-free-course",
                    "title": "@hqmank：Stanford 把「工程化 AI Agent」课程免费放上 YouTube",
                    "body": "Stanford 的 CS 329Z《Engineering AI Agents》正在免费上传，目前第 1、2 讲已上线，课程站点已有 13 份 slide deck。值得看的是大纲而不是标题：Agent 设计模式会讲 ReAct、Reflexion、CodeAct，以及上下文压缩与观察遮蔽（observation masking），并把 Pi harness 当案例；记忆那讲分工作记忆、情景记忆、语义记忆、程序记忆和技能库，还有 MemGPT 式分层；多 Agent 那讲讲什么时候该用多个、git worktree 隔离，以及多 Agent 为什么失败。两个作业仓库都是公开的：第一个从零写一个 agent harness，第二个自己写一个 benchmark 任务并在上面跑 mini-SWE-agent。对想补「怎么测」这一半的人，第二个作业比课程本身更值钱。",
                    "url": "https://x.com/hqmank/status/2120492411205910653",
                },
            ],
        },
    ],
}

out_path = Path("/Users/jwang/clawd-pages/x-digest/digest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {out_path}")

[首页](README.md) · [主题](topics.md) · [论文总索引](papers/README.md) · [综述提纲](survey-outline.md)

# 证据对照：究竟改进了什么？

本页是整理者基于阅读卡片的横向归纳，不是跨论文统一排行榜。任务、数据、人工投入和指标不同，不能直接比较成功率高低。所有数字均来自作者报告，未独立复现。

## 近日工作：机制和证据并排看

| 工作 | 实际更新对象与保留范围 | 物理证据与人工条件 | 可以支持 / 不能支持 |
| :--- | :--- | :--- | :--- |
| [KnowBody](papers/know-your-body.md) | body model、知识规则与证据跨episode验证后保留；VLM冻结 | FR3四任务；固定预算32次；初始化轨迹＋后续执行证据 | 非参数持久改进；主对照关闭跨episode更新，持续曲线仅画成功回合 |
| [Uncertainty-Gated Exploration](papers/uncertainty-gated-exploration.md) | 450M SmolVLA在线PPO；探索门控随状态/时间变化 | LIBERO-10七任务；每主臂3种子；纯仿真 | 抑制任务坍缩；没有方案超过BC起点，不能称能力持续增长 |
| [PACL](papers/pacl.md) | critic与扩散策略在固定混合质量部署数据上后训练 | 四仿真任务×250次、三FR3任务×25次；不需新增纠正 | 利用失败/部分进展；批次离线更新，不是连续自主学习 |
| [Self-Adaptive VLA](papers/self-adaptive-vla.md) | 当前部署实例内累加context token；权重不变 | 四真机任务；20个偏移环境、每环境最多6次 | 失败rollout驱动的测试时适应；不能支持跨环境持久更新 |
| [RACaP](papers/racap.md) | 部署前演化Policy API、ReAct harness与经验；发布后冻结 | LIBERO/robosuite仿真；Phase 2为32 proposals/596 episodes | 可演化harness与预算；外层规则固定且无真机，不是严格递归 |
| [WAA](papers/world-action-agent.md) | 审查后发布多模态技能；另将trace蒸馏到小VLM | LIBERO-Pro/robosuite仿真；依赖专家视频、人类教学和大VLM | 技能证据门控与双更新载体；不是部署期纯自主增长 |
| [RoboRecover](papers/roborecover.md) | 更新benchmark/监测器，不更新主策略 | 两平台2,000个执行偏差scenario；纯仿真 | 恢复能力的独立评测；不能支持自我改进 |
| [World-Model Benchmark Survey](papers/world-model-benchmarks-survey.md) | 组织160个基准与闭环对照协议 | 文献目录；无新机器人实验 | 只有11项显式VLA-vs-WM、4项prediction-to-action；不能证明某类模型优劣 |
| [InternW0](papers/internw0.md) | 离线更新视频/动作专家；部署期只重路由上下文 | 5项真机、每项15次；混合成功/过程指标 | 世界模型支撑；不能支持部署期持久更新 |
| [MemBodied](papers/membodied.md) | rollout内联想状态；主协议每次重置 | PiPER三任务、每策略每任务20次 | 任务内记忆；跨episode携带均值反降 |
| [X2Real](papers/x2real.md) | 更新任务/环境/数据基础设施，不更新被测策略 | 44任务；8项sim-real对照为单模型 | RSI评价基础；“可演化基准”不等于递归策略 |
| [Gaussian Is Enough](papers/gaussian-is-enough.md) | 离线动作先验/编码器微调 | >10万仿真＋1250双臂FR3真机rollout | 后训练强基线；不是在线自改进 |
| [BEE](papers/bee.md) | 残差策略、纠正分布及约束；跨 episode 保留，基础 VLA 冻结 | 三项真机、一项仿真；接管与标签依赖人 | 接管驱动在线改进；不能称全自主或通用跨任务 RSI |
| [HiRE](papers/hire.md) | 成败支持集编辑奖励，再训练策略 | 四项仿真、两项 YAM 真机；真机成败由人标注 | 奖励随经验适配；并未修改奖励编辑规则本身 |
| [Banana Kick](papers/banana-kick.md) | 奖励目标参数与 PPO 策略迭代保留 | 仿真训练，G1 上 30 次冻结策略试验 | 新技能的目标—策略共同更新；不是真机在线学习 |
| [Advantage-guided VLA](papers/advantage-guided-vla-post-training.md) | 固定部署数据上的离线权重更新 | 四项双臂任务，各设置每任务 20 次 | 后训练设计对照；不是连续多轮部署改进 |
| [CMA](papers/counterfactual-memory-audit.md) | 审计时替换/恢复任务内记忆，策略冻结 | 仿真成对干预；PiPER 每任务 8 对 / 32 次 | 记忆的决策效用审计；故障恢复不是持续能力增长 |
| [RegenHarness](papers/regenharness.md) | 协议拟跨任务修订配置；现有结果是执行案例 | 四足巡检与环路实例，缺少修订前后对照 | 系统契约与发布设计；递归收益尚未实证 |

## 结果摘录必须连同分母和预算

| 工作 / 指标 | 作者报告 | 引用时必须同时写明 |
| :--- | :--- | :--- |
| KnowBody / 固定预算完成 | 4/16 → 12/16 | 同一冻结VLM；四任务×两方法×4次；KnowBody跨episode更新关闭 |
| 门控在线RL / 池化坍缩 | 门控三种子均0/7；固定为4/7、1/7、0/7 | 每运行最后5次扫描共1050 episode；三种子；门控成功率仍低于BC tare 0.648 |
| PACL / 七任务成功 | DP 46.4–88.0% → PACL 82.8–100% | 仿真每任务250次、真机25次；PACL用至多700条总轨迹并增加critic筛选 |
| Self-Adaptive VLA / 偏移恢复 | 7.5→72.5%；5.0→75.0% | 每偏移20个部署环境，每环境最多6次并完全复位；不是单次尝试成功率 |
| WAA / LIBERO-Pro | 28.9%无技能 → 75.6%演化技能 | 6 split×60 episode；技能来自LIBERO-90示范并在目标域评测前冻结 |
| BEE / 成功率 | 100%、85%、90%、90% | 每任务 3×20 次评测；前述手机、布料为精细阶段成功，另两项为全任务；真机训练每任务 20＋70 episode |
| HiRE / 瓶子任务 | 6/30 → 20/30 | 基础策略已有示范训练；60 与 70 个在线 episode 的检查点；另一个任务的 73.3% 为峰值 |
| Banana Kick / 固定评测分 | 912.8 → 1093.7 | 对照为学习进展课程；五种子、每种子 4096 匹配情境；不是任务成功率 |
| Advantage-guided VLA / 平均成功率 | SFT 0.11 → 加权 0.74 | 四任务各 20 次；增加 63 个百分点；同表 DAgger 0.45、硬筛选 0.50 |
| CMA / 故障恢复成功 | 6/36 → 20/36 | 人为注入记忆故障后的锚点恢复；未扰动参照为 26/36；不代表常态持续进步 |
| RegenHarness / 到达残差 | 0.11、0.17、0.25 m | 来自系统自身定位记录，容差 0.4 m；不是学习收益，也不是外部计量的定位精度 |

## 已有卡片怎样成为对照组

| 要比较的论点 | 放在一起读 | 要控制的混淆 |
| :--- | :--- | :--- |
| 在线参数更新是否有用 | [RAPolicy](papers/rapolicy.md)、[ForceRFT](papers/forcerft.md)、[BEE](papers/bee.md)、[DexPIE](papers/dexpie.md) | 全模型/残差、在线/批次、接管时长、交互预算、任务成功口径 |
| 记忆是否变成长期能力 | [MessyMem](papers/messymem.md)、[2AM](papers/2am.md)、[Zeva-Ego](papers/zeva-ego.md)、[CMA](papers/counterfactual-memory-audit.md) | 同实例跨尝试与跨任务不同；是否重置；记忆使用是否被干预验证 |
| 代码是否真的累积改进 | [机器人软件学习与迁移](papers/learning-transferring-robot-software.md)、[LEMCA](papers/lemca.md)、[Local Coding Agent](papers/generalizing-manipulation-local-coding-agent.md) | 控制程序演化、同任务会话缓存、基础模型或外层搜索规则更新应分列 |
| 不同反馈能否可信验收 | [No Free Checker](papers/no-free-checker.md)、[HiRE](papers/hire.md)、[SeeQ](papers/seeq.md)、[SRPO](papers/srpo.md) | 提议器与验证器共因错误、稀疏标签依赖、奖励投机、外部任务指标 |
| 世界模型是否真的帮助控制 | [InternW0](papers/internw0.md)、[世界模型综述](papers/world-models-actionable-survey.md)、[持续世界模型基准](papers/compositional-continual-world-models.md) | 预测精度、动作收益、推理延迟、部署更新和旧能力保持应分开 |
| 任务内记忆是否应跨episode保留 | [MemBodied](papers/membodied.md)、[Zeva-Ego](papers/zeva-ego.md)、[MessyMem](papers/messymem.md) | 明确重置边界；未经训练的携带可能负迁移 |
| 进步是否伴随遗忘 | [FAN](papers/fan.md)、[持续世界模型基准](papers/compositional-continual-world-models.md)、[MEMOBench](papers/memobench.md) | 后向迁移、学习速度、旧能力保持与最终成功率不同 |
| 系统能否连续自主运行 | [HALTER](papers/halter.md)、[LIBERO-RECOVER](papers/libero-recover.md)、[SPINE](papers/spine.md)、[RegenHarness](papers/regenharness.md) | 复位、恢复和验证的成本；演示可运行不等于自我改进有效 |

## 严格递归还缺什么

### 9月24日追加：三条新线索与附件补充

| 工作 | 核实到的证据 | 仍需验证的主张 | 进入当前研究的方式 |
| :--- | :--- | :--- | :--- |
| [Simate](cases/simate-autoresearch.md) | 官方榜单快照；公开研究图谱有16节点/25运行 | 自动研究对榜单成绩的因果贡献、改进器增强 | 有预算和版本的run card |
| [Skild](cases/skild-physical-self-play.md) | 官方自述仿真对近期策略self-play，真机足球演示 | 真机在线改进、独立量化泛化、算法复现 | 后续课程分支，不把单智能体采样直接叫self-play |
| [Zeva-Ego](papers/zeva-ego.md) | v2明确新实例清PIM，部署冻结；effect目标为视觉差分 | 跨独立实例留存、长期增长；58→89的sim/real文本归属待澄清 | 视觉差分对照、记忆清空与新实例检验 |
| [GLOW](cases/knowin-glow.md) | 官方技术页的执行回执与18项仿真子集结果 | 与完整总榜可比、循环组件各自收益 | 日志记录命令与实际响应 |

前三者来自本轮正文线索，GLOW来自另一附件；Zeva-Ego只修订既有卡片，另外三项是企业案例。详见[综合分析](discussions/physical-rsi-sept24.md)与[实验矩阵](experiments/rlt-contact-memory/README.md)。

### 递归的独立验收

把“自身执行 → 更新策略”与“改写产生更新的程序/学习规则 → 后续改进更有效”分开评测。建议要求：固定外部任务指标、相同累计预算、冻结改进器对照、多轮轨迹、旧能力保持，以及对验收器变动的单独消融。本轮六篇没有充分实证严格递归增强；这是对本轮证据的判断，不是对整个领域的否定。

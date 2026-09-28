[首页](README.md) · [主题](topics.md) · [论文总索引](papers/README.md) · [综述提纲](survey-outline.md)

# 证据对照：究竟改进了什么？

本页是整理者基于阅读卡片的横向归纳，不是跨论文统一排行榜。任务、数据、人工投入和指标不同，不能直接比较成功率高低。所有数字均来自作者报告，未独立复现。

## 近日工作：机制和证据并排看

| 工作 | 实际更新对象与保留范围 | 物理证据与人工条件 | 可以支持 / 不能支持 |
| :--- | :--- | :--- | :--- |
| [ContinualVLA-Real](papers/continual-vla-real-world.md) | 顺序微调VLA并以经验回放保留旧任务；固定动作归一化、跨本体非对称回放 | 5单臂＋5双臂真机任务；每单臂500、每双臂300条人工示范 | 真机多任务持续学习与遗忘；仍是离线示范流，不能支持自主部署学习 |
| [Pretrained VLA Forgetting](papers/pretrained-vla-forgetting.md) | π0/GR00T按LIBERO任务顺序更新；少量回放并测试知识恢复 | 10项LIBERO仿真任务；默认每任务1000条回放，另测2%缓冲 | 预训练表征可减缓遗忘；不能直接外推真机或部署后自主更新 |
| [OCC4M](papers/occ4m.md) | 单次长程任务内更新对象级4D轨迹和关系；episode后不留存 | 350次仿真＋20次真机记忆试验；策略/VLM权重固定 | 长上下文记忆的支撑组件；不能支持跨episode持续学习 |
| [ARMS](papers/watch-recall-act.md) | 并行写入触发事件、具身状态与压缩自历史；部署参数固定 | 单台Cobot Magic连续流；约1200示范、约200流，真机每段60次 | always-on运行、自历史接口；不能支持经验驱动的持久能力增长 |
| [Streaming-WAM](papers/streaming-wam.md) | 动作条件世界—动作模型离线训练；执行中只滚动固定上下文 | LIBERO、RoboTwin、RoboCasa＋两项真机各30次 | 异步低延迟支撑；不是部署期学习或跨任务保持 |
| [TANDEM](papers/tandem.md) | TAMP域按任务扩展谓词/人工算子，采集后离线微调π0.5；推理时冻结 | 五项长程真机任务；130次采集尝试，20示范/任务，评测20次/任务 | 降低示范人力的数据闭环；不是无人监督或在线RSI |
| [AdaHVLA](papers/adahvla.md) | 代码式coordination policy、候选图和证据跨尝试/任务保留；VLA冻结 | 两套长时仿真基准；三次重启、每次至多16候选；真机仅定性 | 持久harness改进；外层改写流程未自改，不能支持严格递归 |
| [Streaming Deep RL](papers/streaming-deep-rl-continual-robotics.md) | Stream-AC参数每个transition持续更新，无回放 | ManiSkill3四足/操作；5种子、每次50 episodes；纯仿真 | 持久在线参数适应；只测M0→M1且不回测旧任务，不能支持抗遗忘 |
| [OSRAM](papers/osram.md) | 闭环command-response模型持久微调；参考命令在线变化，策略冻结 | LimX Tron1；20次仿真/5次硬件重复 | 部署后模型—接口适应；不是策略学习或开放任务能力积累 |
| [RAPID](papers/rapid.md) | 每任务构造并保存关系程序/原语；新场景部署时固定 | 8×50仿真场景×3次；Franka 8×10真机场景 | 可验证程序构造；不是部署经验驱动的持续自改进 |
| [AD-WM](papers/ad-wm.md) | 离线训练动作可辨世界模型；部署MPC和模型固定 | 三种子仿真；Franka每模型82次，人工给子目标 | 预测—行动桥梁；不能支持部署期持久更新 |
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
| ContinualVLA-Real / 单臂顺序学习 | 朴素微调最终均值86.9→31.4、BWT -81.0；ER均值97.2、BWT +1.5 | 五个单臂真机任务、每任务500示范；默认回放比例20%，作者报告、未复现 |
| Pretrained VLA / LIBERO-10 | π0平均成功率0.768、NBT -0.016；GR00T为0.919、+0.027 | 纯仿真顺序模仿学习；默认每任务1000回放条目，NBT不是绝对成功率 |
| OCC4M / 记忆对照 | 仿真96.6%/88.9%，FrameSamp为54.6%/57.7%；真机记忆85%、端到端45% | 两类仿真各约175 episode；真机仅20 episode，FrameSamp记忆30%且未做物理执行 |
| AdaHVLA / NaVILA-LH测试 | 2.5%单VLA → 22.5%初始harness → 31.7–57.5%适应harness | 10/40适应—测试划分；三次重启；测试不指导选择；均值不是独立任务数 |
| Streaming Deep RL / 四足峰值 | 断腿0.968、目标移动0.848、低摩擦0.676 | 各取不同最佳变体；5种子、50万+150万步；峰值远高于全程均值且未回测旧任务 |
| OSRAM / 真机速度RMSE | 无适应0.2847 → OSRAM 0.2014 | 0.7 m/s、5次硬件试验；四种方法成功率均100%，误差只在成功试验上平均 |
| RAPID / 非抓取仿真 | CaP-Agent0 0.146±0.025 → RAPID 0.759±0.024 | 8任务×50新场景×3次；程序构造每任务数十分钟，测试时程序固定 |
| AD-WM / Franka基础抓放 | 19/45 → 32/45 | 相同冻结V-JEPA2与部署栈；人工图像子目标、非随机模型块；每模型总计82次 |
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
| 在线参数更新是否有用 | [Streaming Deep RL](papers/streaming-deep-rl-continual-robotics.md)、[RAPolicy](papers/rapolicy.md)、[ForceRFT](papers/forcerft.md)、[BEE](papers/bee.md)、[DexPIE](papers/dexpie.md) | 全模型/残差、在线/批次、接管时长、交互预算、峰值与保持、任务成功口径 |
| 记忆是否变成长期能力 | [MessyMem](papers/messymem.md)、[2AM](papers/2am.md)、[Zeva-Ego](papers/zeva-ego.md)、[CMA](papers/counterfactual-memory-audit.md) | 同实例跨尝试与跨任务不同；是否重置；记忆使用是否被干预验证 |
| 代码是否真的累积改进 | [AdaHVLA](papers/adahvla.md)、[RAPID](papers/rapid.md)、[机器人软件学习与迁移](papers/learning-transferring-robot-software.md)、[LEMCA](papers/lemca.md) | 跨任务revision graph、每任务离线构造、控制程序演化和外层搜索规则更新应分列 |
| 不同反馈能否可信验收 | [No Free Checker](papers/no-free-checker.md)、[HiRE](papers/hire.md)、[SeeQ](papers/seeq.md)、[SRPO](papers/srpo.md) | 提议器与验证器共因错误、稀疏标签依赖、奖励投机、外部任务指标 |
| 世界模型是否真的帮助控制 | [AD-WM](papers/ad-wm.md)、[OSRAM](papers/osram.md)、[InternW0](papers/internw0.md)、[世界模型综述](papers/world-models-actionable-survey.md) | 事实预测、候选排序、动作收益、推理延迟、部署更新和旧能力保持应分开 |
| 任务内记忆是否应跨episode保留 | [MemBodied](papers/membodied.md)、[Zeva-Ego](papers/zeva-ego.md)、[MessyMem](papers/messymem.md) | 明确重置边界；未经训练的携带可能负迁移 |
| 进步是否伴随遗忘 | [FAN](papers/fan.md)、[持续世界模型基准](papers/compositional-continual-world-models.md)、[MEMOBench](papers/memobench.md) | 后向迁移、学习速度、旧能力保持与最终成功率不同 |
| 预训练是否天然抗遗忘 | [Pretrained VLA Forgetting](papers/pretrained-vla-forgetting.md)、[ContinualVLA-Real](papers/continual-vla-real-world.md)、[FAN](papers/fan.md) | 仿真/真机、同本体/跨本体、动作坐标、回放规模和任务异质性必须matched |
| 连续运行是否等于持续学习 | [ARMS](papers/watch-recall-act.md)、[Streaming-WAM](papers/streaming-wam.md)、[Streaming Deep RL](papers/streaming-deep-rl-continual-robotics.md) | 固定权重上下文更新、异步推理与在线参数更新是三种不同证据 |
| 数据效率是否计入人工时间 | [TANDEM](papers/tandem.md)、[BEE](papers/bee.md)、[RAPolicy](papers/rapolicy.md) | 示范数、遥操作秒数、接管次数、复位与失败损耗应分别报告 |
| 系统能否连续自主运行 | [HALTER](papers/halter.md)、[LIBERO-RECOVER](papers/libero-recover.md)、[SPINE](papers/spine.md)、[RegenHarness](papers/regenharness.md) | 复位、恢复和验证的成本；演示可运行不等于自我改进有效 |

## 严格递归还缺什么

### 企业来源与论文应分列

| 工作 | 已核查的证据 | 仍缺少什么 | 综述归类 |
| :--- | :--- | :--- | :--- |
| [Simate](cases/simate-autoresearch.md) | 官方榜单快照；公开研究图谱 16 节点 / 25 运行 | 自动研究对成绩的因果贡献、改进器增强 | 自动研究的企业线索 |
| [Skild](cases/skild-physical-self-play.md) | 官方仿真 self-play 自述与真机足球演示 | 真机在线改进、独立量化泛化、完整算法复现 | 策略与课程的企业线索 |
| [Zeva-Ego](papers/zeva-ego.md) | v2 明确 PIM 新实例清空、部署参数冻结 | 跨独立实例留存；58→89 的 sim/real 归属待澄清 | 同实例适应边界 |
| [GLOW](cases/knowin-glow.md) | 官方执行回执描述与 18 项仿真子集结果 | 完整总榜可比性、循环组件各自收益 | 经验反馈的企业线索 |

来源和指标限制见[四类线索对照](discussions/physical-rsi-sept24.md)。企业案例不计入论文卡片数量。

### 递归的独立验收

把“自身执行 → 更新策略”与“改写产生更新的程序/学习规则 → 后续改进更有效”分开评测。建议要求：固定外部任务指标、相同累计预算、冻结改进器对照、多轮轨迹、旧能力保持，以及对验收器变动的单独消融。现有卡片尚无充分实证表明外层改进器自身递归增强；这是对已核查证据的判断，不是对整个领域的否定。

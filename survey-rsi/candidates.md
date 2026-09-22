# 待全文核查的候选工作

以下35项均已打开原始arXiv摘要；未把摘要中的定量主张当作已完成实验核查。优先级是调研判断，不是论文质量排名。已完成全文卡片的MEMOBench已移出本表。

| 工作 | 处理 | 下一步要核查什么 |
|---|---|---|
| [LIBERO-RECOVER: Beyond Task Success Towards Failure Recovery in Robotic Manipulation Models](https://arxiv.org/abs/2609.05178) | 优先 | 失败恢复基准；核查四级恢复定义、真实失败如何注入仿真，以及重试预算。 |
| [VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies](https://arxiv.org/abs/2609.06508) | 优先 | 冻结VLA加可观测验证器；查多轮累计指标与跨episode保留，防止把提示恢复当持续学习。 |
| [EvoNav-Bench: Benchmarking Lifelong Navigation in Evolving Environments](https://arxiv.org/abs/2609.08292) | 优先 | 环境变化使旧记忆过期；查跨任务留存和失效更新机制。 |
| [Towards Embodied Air-Ground Cooperative Object Search: Benchmark, Dataset and Agentic Method](https://arxiv.org/abs/2609.08402) | 暂不纳入主线 | 空地合作搜索为主，摘要未显示持久改进；仅在群体智能分区扩展时考虑。 |
| [GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes](https://arxiv.org/abs/2609.09808) | 次优先 | 多VLM生成技能并接受定点人工反馈；查修改是否保留、改进由谁触发。 |
| [ReactHuman: A Physics-Grounded Benchmark for Human-Like Reactive Decision-Making in Embodied Multimodal LLMs](https://arxiv.org/abs/2609.10895) | 次优先 | 物理危险反应评价，可用于验证覆盖；不是自我进化机制。 |
| [Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection](https://arxiv.org/abs/2609.11225) | 优先 | 声称安全门控和版本化自进化；需把已部署巡检结果与尚未实证的演化环节分开。 |
| [2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation](https://arxiv.org/abs/2609.11308) | 优先 | agent侧记忆与单一动作模型分离；查完成率、宽松成功、严格成功三个口径。 |
| [Memory as Plans: World-Action Modeling with Memory-Grounded Planning](https://arxiv.org/abs/2609.11561) | 优先 | 记忆编译为计划；查记忆是否跨任务、是否仅是长序列推理接口。 |
| [ORCH: Organizational Principles Enable Collective Intelligence in Embodied AI](https://arxiv.org/abs/2609.11737) | 次优先 | 组织结构改变群体表现；查是否根据反馈迭代组织，而非一次生成。 |
| [AnchorVLN: Geometry-Anchored Vision-Language Grounding Reasoning for Open-Vocabulary Navigation](https://arxiv.org/abs/2609.12285) | 暂不纳入主线 | 语义与几何接口为主，摘要未显示经验累积带来的长期收益。 |
| [Agent as Policy for Robotic Manipulation](https://arxiv.org/abs/2609.12541) | 次优先 | robot-use策略接口线索；待全文核查更新对象和经验保留。 |
| [Bridging Thought and Action: Taming Long-Horizon Instability in Open-Source LLM Agents with a MetaTool-Enhanced ROS Framework](https://arxiv.org/abs/2609.13335) | 暂不纳入主线 | 任务内计划草稿与工具执行稳定性，未证明跨任务学习。 |
| [HarnessVLN: Unifying Training-Free Embodied Navigation through an Agent Harness](https://arxiv.org/abs/2609.15195) | 次优先 | 导航harness和图记忆；需查持续状态与能力改进的边界。 |
| [ManiSkillFormer: Demonstration-Free Compositional Manipulation via Task-Conditioned Geometric Contracts](https://arxiv.org/abs/2609.16331) | 次优先 | 几何契约与技能复用；查技能库固定还是自动修订。 |
| [Auto-HSI: Personalized human control of a robot swarm on demand by using LLMs for online automatic code generation](https://arxiv.org/abs/2609.16346) | 暂不纳入主线 | 人工定制群体控制接口；自主改进关联较弱。 |
| [FluxVLA Engine: A One-Stop VLA Engineering Platform for Embodied Intelligence](https://arxiv.org/abs/2609.17210) | 次优先 | 训练—部署—人工纠正平台；查开源实现与闭环数据接口，可列工程支持。 |
| [WetRobo: A Reproducible Robot Kit for Coding Agents in Biological Laboratories](https://arxiv.org/abs/2609.18435) | 优先 | 跨实验室编码代理适应；查成功展示的试验次数和程序迭代过程。 |
| [AeroWeaver: An Embodied-Agent Harness for Weaving Aerial Skills into Distributed, Adaptive Swarm Execution](https://arxiv.org/abs/2609.18520) | 优先 | 角色索引经验驱动在线技能选择；查训练free含义、反馈与长期收益。 |
| [KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.18869) | 暂不纳入主线 | VLM关键帧加全身控制，摘要主要为预训练策略与层级控制。 |
| [In-Context Robot Learning with VLM Agents](https://arxiv.org/abs/2609.19138) | 优先 | 真实机器人ICL；与持久自进化分开，查上下文重置和梯度更新边界。 |
| [GAVEL: Graph World Models for Verified and Efficient Long-Horizon LLM Task Planning](https://arxiv.org/abs/2609.19315) | 次优先 | 图世界模型验证和修复规划；查世界模型是否会从执行中持续更新。 |
| [VABench: Measuring Embodied Spatial Intelligence through Visual Demonstrations, Active Perception, and Metric Control](https://arxiv.org/abs/2609.19554) | 优先 | 主动感知—执行诊断基准；查严格长程成功与部分进度的差距。 |
| [MAGMA-GEN: Validated Recovery Supervision from Ambiguous Failures via Counterfactual Re-Execution](https://arxiv.org/abs/2609.20056) | 优先 | 失败反事实重执行筛出恢复监督；HTML暂不可用，下一步读PDF核实真机协议、特权coach与指标。 |
| [Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation](https://arxiv.org/abs/2609.20822) | 优先 | 安全harness；查无harness对照、碰撞规避与任务成功指标，以及固定设计边界。 |
| [WM-VS: Progress-Aligned World Models for Closed-Loop Visual Servoing](https://arxiv.org/abs/2609.20892) | 次优先 | 世界模型给出进度对齐信号并支持反复纠错；查它是固定模型的闭环控制还是部署经验可持久更新。 |
| [SPARROW: Survival-POMCP for Adaptive Robot Routing, Observation, and Waiting](https://arxiv.org/abs/2609.21008) | 优先 | 在线学习障碍清除生存模型且利用右删失数据；核查模型跨任务保存、物理试验次数与value-of-learning预算。 |
| [Catch Me If You Can: Real-Time Feedback Denoising for Responsive VLAs](https://arxiv.org/abs/2609.21022) | 次优先 | VLA-Feedback在动作执行前做高频纠正；属于任务内反馈控制，待确认没有跨episode参数更新。 |
| [ProTracer: Proprioception-Guided Failure Diagnosis in Robot Manipulation](https://arxiv.org/abs/2609.21369) | 优先 | 失败检测、分类、解释与起始时刻定位；可作改进环的诊断器，需查FailTime规模和对恢复/学习的实际接口。 |
| [When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence](https://arxiv.org/abs/2609.21942) | 优先 | 把动作/查传感器/问人建模为成本决策；查是否仅诊断基准，以及人类问答可靠度和泄漏控制。 |
| [CARF: Contrastive Attraction-Repulsion of Failure-Guided Flow Matching](https://arxiv.org/abs/2609.21982) | 优先 | 从失败轨迹中区分可模仿进展段与应排斥关键失败段；核查数据规模、真机结果和失败标注来源。 |
| [AnyviewMeter: Adapting Robotic Reward Models with Camera Geometry and Multi-View Attention](https://arxiv.org/abs/2609.20106) | 优先 | 任务局部奖励模型适配；核查训练预算、真机任务数、校准与泛化，作为奖励/验证器组件而非完整RSI。 |
| [SeeQ: Training Generalist Value Functions for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2609.22085) | 优先 | 子任务Q函数为best-of-N策略提供方向；查四项真机任务的候选数、基线与是否用于持久策略更新。 |
| [DexPIE: Stable Dexterous Policy Improvement from Real-World Experience](https://arxiv.org/abs/2606.09615) | 优先 | 版本修订；真机部署经验、干预式DAgger和连续最优性指标直接相关，需全文核查37.3%提升的口径与数据量。 |
| [Evolving Skill Modules under a Fixed Planner: Versioning, Rollback, and Runtime Governance for Long-Lived Robot Systems](https://arxiv.org/abs/2604.07799) | 优先 | 版本修订；包含推广门、回滚与多项负结果，需核查66页全文、实现可得性及是否存在跨部署能力增长。 |

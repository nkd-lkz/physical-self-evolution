# 待全文核查的候选工作

以下49项均至少已打开原始arXiv摘要；未把摘要中的定量主张当作已完成实验核查。优先级是调研判断，不是论文质量排名。已完成全文卡片的工作已移出本表；2604.07799仅完成初读，因证据审计未通过升级门槛，仍保留候选。

| 工作 | 处理 | 下一步要核查什么 |
|---|---|---|
| [EvoNav-Bench: Benchmarking Lifelong Navigation in Evolving Environments](https://arxiv.org/abs/2609.08292) | 优先 | 环境变化使旧记忆过期；查跨任务留存和失效更新机制。 |
| [Towards Embodied Air-Ground Cooperative Object Search: Benchmark, Dataset and Agentic Method](https://arxiv.org/abs/2609.08402) | 暂不纳入主线 | 空地合作搜索为主，摘要未显示持久改进；仅在群体智能分区扩展时考虑。 |
| [GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes](https://arxiv.org/abs/2609.09808) | 次优先 | 多VLM生成技能并接受定点人工反馈；查修改是否保留、改进由谁触发。 |
| [ReactHuman: A Physics-Grounded Benchmark for Human-Like Reactive Decision-Making in Embodied Multimodal LLMs](https://arxiv.org/abs/2609.10895) | 次优先 | 物理危险反应评价，可用于验证覆盖；不是自我进化机制。 |
| [Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection](https://arxiv.org/abs/2609.11225) | 优先 | 声称安全门控和版本化自进化；需把已部署巡检结果与尚未实证的演化环节分开。 |
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
| [Learning Without Losing Identity: Capability Evolution for Embodied Agents](https://arxiv.org/abs/2604.07799) | 优先 | 核查66页全文中的模拟结果、零成功项、峰值选择和不同seed对照；暂不按标题包装为技能版本治理实证。 |
| [CHOREO: Every Humanoid Skill as a Trajectory](https://arxiv.org/abs/2609.22274) | 次优先 | Unitree G1/MuJoCo中组合2950个资产；核查95.4%序列成功的任务分布，并保持其为固定技能组合而非在线学习的边界。 |
| [When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads](https://arxiv.org/abs/2609.22299) | 优先 | 冻结策略主动获取但未使用证据的诊断研究；核查任务数、干预成本和因果对照，作为“感知不等于改进”负证据。 |
| [Embedding Physics Priors in Robot Learning: A Survey](https://arxiv.org/abs/2609.22319) | 次优先 | 物理先验综述；核查taxonomy和参考文献，重点溯源可在线更新的物理模型，而非泛化机器人学习。 |
| [VLPSA: Vision-Language-Poisson-Safe Actions for Full-Body Safety of Learned Policies](https://arxiv.org/abs/2609.22462) | 次优先 | SafeLIBERO碰撞规避23.1→91.2并有FR3演示；核查任务成功代价、真机协议及固定安全过滤器边界。 |
| [FRAMES: Failure Recovery And Monitoring of Embodied Skills for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.22538) | 次优先 | 100次MuJoCo监控试验称94%准确；端到端恢复仍在进行，先核查失败类型与误报成本。 |
| [StateMem: Single-State Residual Memory with Adaptive Inference for Vision-Language-Action Policies](https://arxiv.org/abs/2609.22684) | 优先 | 摘要报告LIBERO 97.6和真机六任务+21%；核查记忆是否每episode重置、训练数据和RoboMemArena指标分母。 |
| [SmoLSTM: A Compact Vision-Language-Action Model with Recurrent Memory that Persists](https://arxiv.org/abs/2609.22854) | 优先 | 7461条示范/140任务，LIBERO-Mem成功率77.5%；核查reset-state对照7%的具体口径及记忆跨episode边界。 |
| [PileBelief: Persistent Physical State for Interaction-Driven World Modeling](https://arxiv.org/abs/2609.22858) | 优先 | 固定权重下用交互更新物理belief；核查5步误差-10.8%与action regret -65.5%的基线、任务数和是否跨部署保存。 |
| [ME-Brain-1.0: Memory, Cognition and Action for Evolving Embodied Intelligence](https://arxiv.org/abs/2609.24271) | 优先 | 直接声称无需重训的deploy-and-evolve；须核查作者/机构、实验分母、公开代码与长期保留，企业自述不作独立实证。 |
| [Minimal Recurrent Behavioral Memory for Imitation under Partial Observability](https://arxiv.org/abs/2609.25757) | 优先 | 摘要给出部分可观测模仿中的最小记忆条件；核查操作任务、严格记忆消融及是否只在episode内保存。 |
| [What is the Better Curriculum: Controller-Shaped Grasping Behavior for Contact Force-Sensitive Manipulation](https://arxiv.org/abs/2609.25887) | 优先 | 触觉反射教师塑造训练课程；核查ACT 95%与π0.5扰动失败的试验分母，以及部署仲裁器是否固定。 |
| [MATES: Learning Multi-Agent Interactions by Transforming Observations for Frozen Single-Agent Policies](https://arxiv.org/abs/2609.26010) | 次优先 | 只训练3.5–7.3%参数的交互适配器并讨论lifelong任务；核查环境、序列协议和遗忘指标。 |
| [NavSafe-∞: Benchmarking Closed-Loop Driving Safety in Photorealistic Environments](https://arxiv.org/abs/2609.26618) | 优先 | 280场景、28类事件、20个策略的闭环安全审计；核查在线RL奖励投机证据和可迁移到机器人RSI的独立验收指标。 |
| [Dual-Frontier: When Can an Agent Trust Its World Model?](https://arxiv.org/abs/2609.26293) | 优先 | 用双frontier区分策略失败与世界模型失配并给出界；核查是否含机器人任务、在线更新以及界的假设条件。 |
| [Toward User-Mediated Self-Repair in Ubiquitous Robots Through Goal-Oriented Agentic AI](https://arxiv.org/abs/2609.26157) | 次优先 | 摘要报告硬件与20名参与者、95%完成率；核查用户维修负担和是否只是诊断指导而非自主能力更新。 |
| [VLAQuantBench: A Systematic Benchmark for Quantizing Vision-Language-Action Models](https://arxiv.org/abs/2609.25376) | 次优先 | 409组配置、94,574个仿真episode；核查闭环校准指标，作为部署与资源边界，不包装为RSI。 |
| [Capability-Aware Arbitration for Semantic Intent-Based Shared Control](https://arxiv.org/abs/2609.25369) | 次优先 | 在线置信度仲裁并有12名参与者；核查92%指标分母、人工输入和是否存在任何跨任务学习。 |
| [Touch2Robot: Robot Policy Learning with Simulated Target-Hand Contact Feedback](https://arxiv.org/abs/2609.24660) | 次优先 | 以模拟目标手接触反馈采集数据，摘要称四项真机任务37.9→72.1；核查数据量、基线与其作为自动数据闭环组件的边界。 |
| [Rollback the World, Keep the Reflection: Failure-Aware Memory for Long-Horizon Agents](https://arxiv.org/abs/2609.18304) | 优先 | 回滚环境但保留反思记忆；核查三个长程基准是否含物理环境、记忆跨会话边界和失败污染控制。 |

数据源：[data/candidates.json](data/candidates.json)。候选升级为卡片前必须补齐版本、实验分母、基线、预算、物理平台和证据边界。

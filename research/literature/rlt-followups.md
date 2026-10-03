# RLT 后续工作：直接继承、强近邻与可执行对照

更新：2026-10-03。本页作为持续维护的 RLT 后续文献入口，配合 [eRLT 专题](../../notes/erlt.md)、[既有三分支前沿表](frontier-rlt-2026-09-30.md)，不另建研究主线。所有实验结果均属作者报告；本次没有训练或复现这些方法。

**结论：本轮确认 4 篇明确继承或直接改造 RLT 接口/学习骨架的工作：eRLT、RouteRLT、SmoothRL、BEE。** TORL-VLA、PARTS、HALO-WA、Imagine-RL 等同样重要，但继承强度和技术路径不同，不能统称为 RLT 的直接后继，也不能把引用关系当代码 fork。

## 1. 检索范围与分级规则

以 [RL Token 原论文](https://arxiv.org/abs/2604.23073) 为起点，结合标题检索、参考文献与 [Semantic Scholar 引用接口](https://api.semanticscholar.org/graph/v1/paper/ARXIV:2604.23073/citations?fields=title,externalIds,url&limit=1000)。本次接口返回 54 行，Q-VGM 重复题录合并后为 **53 篇候选**；额外补检 TORL-VLA、FORCE。对其中及补检共 **35 篇**做原文关系初筛，优先看摘要、方法接口、提及 RLT 的上下文；其中 4 篇直接继承工作进一步核对方法与实验协议。其余保留题录，不能算“已全文精读”。

检索快照和阅读级别见末尾候选台账。引用数据库会滞后，v1 与后续修订也可能不同；“本轮确认四篇”不是“全世界仅有四篇”。没有独立核实的代码、会刊接收状态和复现实验不补写。

| 分类 | 必要证据 | 不足以成立的证据 |
|---|---|---|
| A：明确继承/直接改造 | 方法写明沿用 RLT 的接口、结构或学习骨架，并能定位改动 | 标题里有 RL/token；仅在 related work 引用 |
| B：RLT 式强近邻 | 冻结 foundation policy＋表征/参考动作＋小型控制适配，或专门改造相近瓶颈 | 不能据此宣称作者采用 RLT 代码或完整算法 |
| C：平行路线/其他基线 | 主体是 DSRL、EXPO-FT、生成策略微调、世界模型等 | 与 RLT 比较不等于基于 RLT |
| U：待核实 | 只有题录或关系尚不充分 | 不强行归类，不计入直接后继 |

## 2. 四篇明确继承工作

| 工作 / 原文 | 继承证据位置 | 改什么 | 对本项目的直接含义 |
|---|---|---|---|
| [eRLT](https://arxiv.org/html/2610.00913v1)，10-01 | §3–4；附录 A–C，显式研究并替换 RLT 表征 | token/layer 路由；专家动作预测初始化；critic 在线调路由 | 物理后果 loss 必须超过同容量动作预测监督；仿真 RLT* 与真机 RLT 要分开 |
| [RouteRLT](https://arxiv.org/html/2609.26467v1)，09-22 | 方法及四阶段训练，明确基于 RLT 的 representation/specialist learning | 学习何时交接、选择哪个 specialist；滞回与动作后缀失效 | 自动阶段切换已有直接工作；适合作为后续减人工切换基线 |
| [SmoothRL](https://arxiv.org/html/2608.29768v1)，08-30 | §2.1、§3.4 明确沿用 RLT 实现结构 | 区分已承诺、真正执行、被丢弃动作；学习与异步时序对齐 | 后果监督必须针对实际执行区间；比额外模型更早需要做对 |
| [BEE / Bee](https://arxiv.org/html/2609.27450v1)，09-23 | §II-A、§III-A 明确沿用 RLT 的 token＋reference 接口 | 人工纠正分布→逐动作维约束；状态相关乘子平衡约束与价值 | 不只增加干预 BC；需保存原提议、人工实际动作及控制来源 |

### RouteRLT：路由的是控制权，不是视觉 token

共用紧凑表征供阶段路由器和多个 specialist 使用；切换时要清除未执行的旧动作后缀，防止模型已经切换但机器人仍执行旧命令。它与 eRLT 同名词、不同对象：eRLT 选择读什么信息，RouteRLT 选择由谁控制。真机报告包含 operator-aligned handoff，不能写成全任务完全自主切换；训练阶段标签的来源也必须算成本。

### SmoothRL：先确定“环境究竟执行了哪段动作”

异步执行时，完整生成 chunk 不等于实际施加动作。对未执行部分分配 reward 或后果标签，会同时污染 critic 和辅助监督。框架实现沿用 RLT，小 actor 的具体实例采用 residual；这不意味着原 RLT 的所有实现都是 residual。延伸阅读：[已有专题及本次关系核验](../../notes/smoothrl.md)。

### BEE：人的修正是一种有方向、有不确定性的约束

模型从状态和 VLA proposal 预测人工修正的均值及逐维方差，再用方差加权距离约束策略：一致维度约束更强，分歧维度更松。它没有直接把每次纠正当同等可靠的标准答案。方差描述修正数据的一致性，不能直接解释成经过校准的物理风险。原文仍保留阶段交接与干预协议，不能理解成免人工训练。作者 [项目页](https://genie-universal-algorithm.github.io/BEE/)可用于后续跟踪；本次未验证可运行代码。

## 3. 对物理经验选题更重要的强近邻

| 工作 / 分类 | 原文中的机制与区别 | 借鉴与边界 |
|---|---|---|
| [TORL-VLA v3](https://arxiv.org/html/2606.09337v3) / B | wrench-aware VLA，实测/预测 wrench 条件下的阶段 actor；intervention-censored critic 阻止人工救回的成功跨接管边界回传 | 最贴近接触与干预归因；需要触觉/力觉和相应训练。不能称为在原 RLT 上只加一个 loss，未确认直接代码继承 |
| [PARTS](https://arxiv.org/html/2609.21788v1) / B | 针对瓶颈子任务训练有界 TD3+BC residual；coding agent 编写 selector、verifier、reset；引用 RLT 残差学习思想并重实现 RLT 作对照 | 可减少重复练习已会阶段；子任务奖励、复位和验证器建立成本不能省略。不是 RLT RL-token 模块的明确直接继承 |
| [HALO-WA](https://arxiv.org/html/2607.04265v1) / B | 面向 WAM 分布式 latent 的混合注意力适配；比较单 compact-token 的 RLT-like adapter | “一个 token 是否压掉接触信息”已有近邻；对照是 WA 上的 RLT-like，不是原生 RLT |
| [VLaRL](https://arxiv.org/html/2609.30868v1) / B | 仿真训练 latent-conditioned residual，学习 sim→real latent mapper，真机不做在线 RL | 共享冻结 VLA＋小适配思想，但研究重点是仿真迁移；不能用它证明部署后的持续学习 |
| [Imagine-RL](https://arxiv.org/html/2609.24033v1) / C，P0 必读 | 主体是噪声空间 RL；冻结视觉–力矩世界模型预测候选后果，历史预测残差调节 critic 对未来 token 的使用 | “预测接触后果＋按预测误差校准 critic”已有很近的工作。它引用 RLT，但不是直接改造 RLT token |
| [ARLI](https://arxiv.org/html/2608.23831v1) / C | DSRL 方向；考虑推理延迟、已经承诺的动作和更新鲜的观测 | 与 SmoothRL 同研究异步问题，但 RL 骨架不同 |
| [PHR-VLA](https://arxiv.org/html/2608.27609v1) / C | 训练时用未来动态 latent 监督辅助头，关注局部接触 patch | 与 FLARE/loss-first 相邻；不是 RLT 在线 RL 改造。不能把“接触局部未来监督”直接当空白 |
| [FP2](https://arxiv.org/html/2609.37433v1) / C | foundation policy 负责动作，高频策略结合 wrench/history 预测力控制参数 | 物理能力可体现为调节控制参数，不必再命名 physical token；也不能把高频力控等同 RL |
| [FIND](https://arxiv.org/html/2609.32069v1) / C | 持续场景中选择弱项练习、前后图像评估、residual RL；学习器采用独立语言支路 | 自改进外环参考；未采用 RLT 内部表征，不算直接后继；VLM 自评仍需独立人工核验 |

另外已筛查：[MiDAS](https://arxiv.org/html/2608.11363v1)、[ZPRL](https://arxiv.org/html/2605.19919v1)、[PSS](https://arxiv.org/html/2609.33765v1)、[RL²-VLA](https://arxiv.org/html/2607.26991v1)、[BORA](https://arxiv.org/html/2605.30226v1)、[FORCE](https://arxiv.org/html/2606.26006v1)、[RAPolicy](https://arxiv.org/html/2609.22888v1)、[EXPO-FT](https://arxiv.org/html/2605.25477v1)、[Real-Time EXPO-FT](https://arxiv.org/html/2609.18207v1)、[OmniTacTune](https://arxiv.org/html/2607.03723v1)、[UniSteer](https://arxiv.org/html/2605.10821v1)。它们覆盖少数据适配、latent steering、离线到在线、价值热身、异步和触觉残差；本次未找到足以归入 A 的明确方法继承证据。保留为不同模块的候选对照，不把引用 RLT 的全部工作包装为 RLT 改进。

## 4. 科研上如何应对：收敛为三个可证伪问题

**10-03 用户更新的主方向**：保留 Zeva 的交互提取与长短期记忆，Stage 1 学习经验编码，Stage 2 利用条件加速 RL，再检验迁移；固定响应公式只是对照。完整开发合同在 [既有 Zeva–RLT 方案](../zeva-rlt-implementation-2026-09-26.md) 更新，避免另建平行方案。[RMA](../../notes/rma.md) 与 [PEARL](../../notes/pearl.md) 已补专题；二者是早期经典近邻，不计入 RLT 后继数量。

以下是本项目建议，不是上述作者结论，也不是已完成实验。

### 问题一：执行后果比专家动作本身多提供了什么？优先级 P0

在同一个冻结 VLA、相同 readout 容量和相同 RL 实现上比较：重建、动作预测、重建＋后果、动作预测＋后果。后果只用已执行前缀和有效时间段生成；标签在执行后产生，不进入该时刻的 actor 输入。详细合同见 [eRLT 笔记的 B0–B3](../../notes/erlt.md)。

预期差异应集中在物理条件改变时：动作命令相似但实际响应不同，过去反馈或状态证据帮助辨别。先测后果校准，再测相同环境交互预算下的闭环成功率与收敛速度。若动作预测已解释全部增益，就停止“physical loss 带来特有收益”的主张。

### 问题二：救回成功能否错误奖励此前的坏动作？优先级 P0/P1

从现有 VR/control-source 日志切入：保留 VLA proposal、policy command、实际执行、human 标志、接管时刻。先离线检查人工救回轨迹上的 Q 偏差，再考虑 TORL-VLA 启发的第二 critic/censoring 对照。**不要直接把接管设成环境终止，也不要把全部人类动作删除**；接管可能来自操作者偏好，mask 的定义和结果需要单独验证。BEE 的 correction prior 是另一条路线，第一轮不与 censoring 叠加。

### 问题三：新任务时复用的是动作、后果经验还是控制权？优先级 P1

先做同任务新物理条件，冻结评估协议；再用 2–3 个训练任务到一个未见任务检验迁移。区分短历史输入、跨回合记忆、共享表示和阶段 specialist。RouteRLT/策略组合可以减少交接人工，但不会自动使物理经验可迁移；只有跨条件/跨任务收益与旧任务保持都被测量后，才讨论持续成长。

推荐精读顺序：**eRLT → TORL-VLA → Imagine-RL**；若当前瓶颈已确定是接管或切换，则优先 BEE/RouteRLT；若是 chunk 对齐，则先 SmoothRL。暂不同时搭建所有机制。

## 5. 工程实现来源与发表状态

- [RLinf](https://github.com/RLinf/RLinf) 是实现入口之一；应锁定具体 commit、checkpoint、actor 类型与执行长度。论文中使用 RLinf，不等于该新方法代码已经合入 RLinf。
- [openpi-RLT](https://github.com/Yyshadow/openpi-RLT) 的作者 README 将其定位为 openpi/π0.5 社区复现；可看接口组织，不计为新论文，也不当原 RLT 官方代码。
- 本页按已核实 arXiv 版本记录新工作；未取得明确会刊接收证据时，不推断投稿或录用场所。

## 6. 引用候选台账

“关系初筛”只表示看过原文摘要/接口/RLT 上下文，不表示全文精读或实现审计。以下保留检索覆盖，避免只挑四篇后声称已穷尽；更完整方法比较优先维护上面的表。

| arXiv / 一手来源 | 题名 | 本轮状态 |
|---|---|---|
| [2610.00913v1](https://arxiv.org/abs/2610.00913v1) | eRLT: Efficient VLA Reinforcement Learning via Action-Relevant Token Routing | A；方法与协议核对 |
| [2609.39403v1](https://arxiv.org/abs/2609.39403v1) | IronMind: Scaling Humanoid Dexterous Manipulation via Camera-Space Ego-Centric Pretraining | 原文关系初筛；不计入 A |
| [2609.39038v1](https://arxiv.org/abs/2609.39038v1) | Looking Back to Move Forward: Temporal Verification for Generative Robot Policies | 原文关系初筛；不计入 A |
| [2609.37433v1](https://arxiv.org/abs/2609.37433v1) | FP2: Equipping Robotic Foundation Models with Force Control | 原文关系初筛；不计入 A |
| [2609.36872v1](https://arxiv.org/abs/2609.36872v1) | PreferenceFlow: Test-Time Guidance of Flow-Matching Robot Policies from Human Interventions | 原文关系初筛；不计入 A |
| [2609.34599v1](https://arxiv.org/abs/2609.34599v1) | The Low-Rank Structure of VLA Reinforcement Learning | 原文关系初筛；不计入 A |
| [2609.33765v1](https://arxiv.org/abs/2609.33765v1) | Principal Steering Subspaces for Online Adaptation of Frozen Generative Robot Policies | 原文关系初筛；不计入 A |
| [2609.32236v1](https://arxiv.org/abs/2609.32236v1) | RoboFFT: Finetuning generative robot policy via online reinforcement learning with forward process | 原文关系初筛；不计入 A |
| [2609.32069v1](https://arxiv.org/abs/2609.32069v1) | Find Something You Can't Do: Agentic Real-World Reinforcement Learning for Self-Improving VLA Models | 原文关系初筛；不计入 A |
| [2609.30868v1](https://arxiv.org/abs/2609.30868v1) | VLaRL: Augmenting Vision-Language-Action Models with Simulation-Trained Latent-Conditioned Residual RL | B；结构近邻核对 |
| [2609.27450v1](https://arxiv.org/abs/2609.27450v1) | BEE: Intervention-Adaptive Real-World Reinforcement Learning with Vision-Language-Action Models | A；方法与协议核对 |
| [2609.27068v1](https://arxiv.org/abs/2609.27068v1) | HiRE: Hindsight Reward Editing for Policy Finetuning | 原文关系初筛；不计入 A |
| [2609.26467v1](https://arxiv.org/abs/2609.26467v1) | RouteRLT: Learning When and Which RL Specialist Should Control a Vision-Language-Action Policy | A；方法与协议核对 |
| [2609.24033v1](https://arxiv.org/abs/2609.24033v1) | Imagine-RL: Residual-Confidence-Guided Cross-Attention for World-Model-Augmented VLA Reinforcement Learning | 原文关系初筛；不计入 A |
| [2609.22888v1](https://arxiv.org/abs/2609.22888v1) | Stable and Efficient Real-World Online VLA Post-Training via Asynchronous Replay-Anchored Policy Improvement | 原文关系初筛；不计入 A |
| [2609.21788v1](https://arxiv.org/abs/2609.21788v1) | From Pretraining to Proficiency: Real-World Subtask RL for Long-Horizon Manipulation with Minimal Human Intervention | B；结构近邻核对 |
| [2609.18207v1](https://arxiv.org/abs/2609.18207v1) | Reinforcement Learning for Real-Time Vision-Language-Action Policies | 原文关系初筛；不计入 A |
| [2609.12749](https://arxiv.org/abs/2609.12749) | SCQ: Stabilizing Conservative Q-Learning with Sigmoid-Bounded Entropy | U；仅引用题录，待核对 |
| [2609.03681v1](https://arxiv.org/abs/2609.03681v1) | WISE: World-model-guided Imagination Scheduling for Efficient Post-training of Vision-Language-Action Models | 原文关系初筛；不计入 A |
| [2609.02653v1](https://arxiv.org/abs/2609.02653v1) | HINT: Human-Intent Inception for Long-Horizon Robot Manipulation | 原文关系初筛；不计入 A |
| [2608.29768v1](https://arxiv.org/abs/2608.29768v1) | SmoothRL: Online Reinforcement Learning During Asynchronous Execution | A；方法与协议核对 |
| [2608.27609v1](https://arxiv.org/abs/2608.27609v1) | PHR-VLA: Planning Horizon Reasoning for Vision-Language-Action Models | 原文关系初筛；不计入 A |
| [2608.23831v1](https://arxiv.org/abs/2608.23831v1) | Learning to Act While Waiting: RL Finetuning of Generalist Robot Policies Under Inference Latency | 原文关系初筛；不计入 A |
| [2608.21740](https://arxiv.org/abs/2608.21740) | CounterAlign: Counterfactual Supervision for Vision-Language-Action Models | U；仅引用题录，待核对 |
| [2608.11363v1](https://arxiv.org/abs/2608.11363v1) | Adaptation of Generalist Robot Policies with Minimal Data | 原文关系初筛；不计入 A |
| [2608.07314v1](https://arxiv.org/abs/2608.07314v1) | TEMPO: Semantic-Action Decoupled RL Post-Training for Vision-Language-Action Models | 原文关系初筛；不计入 A |
| [2608.05674](https://arxiv.org/abs/2608.05674) | JoyAI-RA 0.5: Scaling Robot Manipulation Learning via Dual Action Alignment | U；仅引用题录，待核对 |
| [2607.28560](https://arxiv.org/abs/2607.28560) | X-NavDP: Generalizing Navigation Diffusion Policy to Novel Behavior and Embodiments with Group Q-score Reweighted Matching | U；仅引用题录，待核对 |
| [2607.26991v1](https://arxiv.org/abs/2607.26991v1) | RL2-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models | 原文关系初筛；不计入 A |
| [2607.20771](https://arxiv.org/abs/2607.20771) | Emergent Compositional Skills in Mixture-of-Experts VLAs | U；仅引用题录，待核对 |
| [2607.14252](https://arxiv.org/abs/2607.14252) | MEMORA: Embodied Action Memory from Egocentric Videos for Reasoning and Planning | U；仅引用题录，待核对 |
| [2607.10369](https://arxiv.org/abs/2607.10369) | VINE: Taming Generative Control Policies for Reinforcement Learning | U；仅引用题录，待核对 |
| [2607.08837](https://arxiv.org/abs/2607.08837) | Prompt-Driven Exploration | U；仅引用题录，待核对 |
| [2607.04265v1](https://arxiv.org/abs/2607.04265v1) | HALO-WA: Hybrid-Attention Latent-Guided Online Reinforcement Learning for World-Action Models | B；结构近邻核对 |
| [2607.03723v1](https://arxiv.org/abs/2607.03723v1) | OmniTacTune: Policy-Agnostic Real-World RL for Tactile Residual Adaptation of Visual Policies | 原文关系初筛；不计入 A |
| [2606.32027](https://arxiv.org/abs/2606.32027) | Freeform Preference Learning for Robotic Manipulation | U；仅引用题录，待核对 |
| [2606.31958v1](https://arxiv.org/abs/2606.31958v1) | Adapting Generalist Robot Policies with Semantic Reinforcement Learning | 原文关系初筛；不计入 A |
| [2606.26006v1](https://arxiv.org/abs/2606.26006v1) | FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation | 原文关系初筛；不计入 A |
| [2606.24742](https://arxiv.org/abs/2606.24742) | World Value Models for Robotic Manipulation | U；仅引用题录，待核对 |
| [2606.23623](https://arxiv.org/abs/2606.23623) | dVLA-RL: Reinforcement Learning over Denoising Trajectories for Discrete Diffusion Vision-Language-Action Models | U；仅引用题录，待核对 |
| [2606.17011v1](https://arxiv.org/abs/2606.17011v1) | ROVE: Unlocking Human Interventions for Humanoid Manipulation via Reinforcement Learning | 原文关系初筛；不计入 A |
| [2606.16413](https://arxiv.org/abs/2606.16413) | An Augmented Reality Brain-Robot Interface for Generalist Robot Arm Manipulation | U；仅引用题录，待核对 |
| [2606.11743](https://arxiv.org/abs/2606.11743) | TacCoRL: Integrating Tactile Feedback into VLA via Simulation | U；仅引用题录，待核对 |
| [2606.09337v3](https://arxiv.org/abs/2606.09337v3) | TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation | B；结构近邻核对 |
| [2606.08015](https://arxiv.org/abs/2606.08015) | Q-VGM: Q-Guided Value-Gradient Matching for Offline-to-Online RL of Flow-Matching VLA Policies | U；仅引用题录，待核对 |
| [2605.30226v1](https://arxiv.org/abs/2605.30226v1) | BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models | 原文关系初筛；不计入 A |
| [2605.27079](https://arxiv.org/abs/2605.27079) | Trust Region Q Adjoint Matching | U；仅引用题录，待核对 |
| [2605.25477v1](https://arxiv.org/abs/2605.25477v1) | EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models | 原文关系初筛；不计入 A |
| [2605.19919v1](https://arxiv.org/abs/2605.19919v1) | Beyond Action Residuals: Real-World Robot Policy Steering via Bottleneck Latent Reinforcement Learning | 原文关系初筛；不计入 A |
| [2605.12334](https://arxiv.org/abs/2605.12334) | Reinforcing VLAs in Task-Agnostic World Models | U；仅引用题录，待核对 |
| [2605.11750](https://arxiv.org/abs/2605.11750) | DreamAvoid: Critical-Phase Test-Time Dreaming to Avoid Failures in VLA Policies | U；仅引用题录，待核对 |
| [2605.10821v1](https://arxiv.org/abs/2605.10821v1) | Unified Noise Steering for Efficient Human-Guided VLA Adaptation | 原文关系初筛；不计入 A |
| [2603.26360](https://arxiv.org/abs/2603.26360) | Realtime-VLA V2: Learning to Run VLAs Fast, Smooth, and Accurate | U；仅引用题录，待核对 |
| [2511.17774](https://arxiv.org/abs/2511.17774) | Learning Diffusion Policies for Robotic Manipulation of Timber Joinery under Fabrication Uncertainty | U；仅引用题录，待核对 |
| [2510.24795](https://arxiv.org/abs/2510.24795) | A Survey on Efficient Vision-Language-Action Models | U；仅引用题录，待核对 |

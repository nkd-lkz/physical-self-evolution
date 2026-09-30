# 三条 RLT 探索线的前沿邻近工作与创新边界

本次调研判断“预测后果、积累记忆、选择有限动作”各自已被研究到哪里，以及当前 RLT 原型还需要证明什么。检索截止 2026-09-30；来源限定为论文原文、作者项目页和源码。这里的“高度重合”是研究判断，不是抄袭判定，也不是穷尽检索或新颖性保证。没有复现表中其他方法，不能跨任务比较其成功率。

## 最直接影响选题的工作

### 09-28／09-29 的新邻近工作

- [DRAM](https://arxiv.org/html/2609.32453v2)（09-29 修订，核对方法与更新公式）：在冻结 backbone 上接入定长关联记忆，用预测残差进行 delta-rule 写入，同一帧的多个 token 联合更新。它并非无训练插件，仍需 post-training 记忆与 action expert。对我们而言，“冻结 VLA + 可插拔长期记忆”已不是足够的差异；值得借鉴读写时序、有限状态和错误证据纠正，但当前 Zeva 原型没有实现其矩阵记忆。
- [RoboICL，第 4.5 节](https://arxiv.org/html/2609.34261v1#S4.SS5)（09-28，核对方法和完整 Jev 表格）：这里 Jev 只决定是否复用已生成动作后缀，不生成动作。两个任务的各 5 个开发布局中，接入 gate 后成功数分别从 3/5 变成 2/5、从 4/5 变成 5/5；调用数下降不意味着所有任务成功率都上升。它启发未来比较“重规划／继续执行”的决策成本，但不构成本项目局部选择器优于 VLA 的证据。

这两项追加文献使定位更具体：不争论谁先增加记忆或快速 gate，而检验**实际执行偏差在何种条件下值得保留、何时会误导下一次修正**。先保持现有三个单变量实验，再决定是否引入新的记忆更新或重规划机制。

### 追加核对：价值误差、部署更新与接管信号

- [DAWN：What Makes Value Learning Efficient in Residual Reinforcement Learning?](https://arxiv.org/html/2602.10539v1)（2026-02-11，核对摘要与方法结构）：指出 critic 冷启动与 residual 尺度问题，使用 base-policy 数据锚定与 critic normalization。当前 RLT Q head 已有 LayerNorm；本次只借鉴“补充参考动作样本、测量 Q 偏差”的实验问题，没有复现该算法，也不将额外热身当作必然有效。
- [Beyond Imitation / Q-Planning](https://arxiv.org/abs/2608.21204)（2026-08-21，摘要级核对）：冻结 BC，只更新小型 off-policy Q，并对 BC 候选进行价值引导选择。这与“冻结 VLA + 小模块积累失败经验”的叙事直接邻近。我们的有限关节修正不是 BC 多次采样；应加入 Q-only 候选选择作为后续对照，尚未实现。
- [OnEvoMemory](https://arxiv.org/html/2608.08749v1)（2026-08-09，摘要及论文页面核对）：通过轨迹结果更新经验保留机制。不能把“在线写入记忆”独立当作新贡献；当前 Zeva 原型仍缺少跨回合持久经验的独立收益证据。
- [WHIRL](https://arxiv.org/abs/2609.06009)（2026-09-05，摘要级核对）：将人工接管信号用于预测性风险建模。我们的当前 VR 改动只记录接管段数和控制来源，没有风险 head、额外奖励或安全保证。操作者接管原因、主观阈值和 task 成功必须区分，不能简单把按 grip 当成失败。

这些来源说明，相邻机制已相当成熟。暂时收敛到可检验的小问题：在同样观测与交互预算下，过去的“命令—响应”是否改善下一次修正，而不是声称已经实现通用物理直觉或 RSI。

| 工作与公开时间 | 已有机制 | 对当前项目的影响（我们的判断） |
| --- | --- | --- |
| [FLARE](https://research.nvidia.com/labs/gear/flare/)，2025-05-22 | future token 与未来表征对齐，联合动作学习，不必生成像素 | “辅助未来表征监督”已经成立为既有方法；当前冻结 RLT 后训练侧支不是原论文复现 |
| [Zeva](https://arxiv.org/abs/2608.30880v2)，首发 2026-08-31，修订 09-22 | 执行动作与实际状态变化构成交互单元，双时间尺度记忆，在冻结 policy 中读取 | 不能把“动作＋变化＋检索记忆”本身写成新贡献；必须明确我们的监督、接口及可测差异 |
| [Zeva-Ego](https://arxiv.org/abs/2609.24411v2)，首发 09-21，修订 09-22 | action-centric ego mid-training 与部署时交互记忆结合 | 大规模离线经验与在线交互衔接已有强近邻；当前项目没有相应数据规模和跨任务证据 |
| [UniMPA](../../notes/unimpa.md)（[原文](https://arxiv.org/abs/2609.11875)），09-10 | 用 action-grounded transition 串联未来预测、视觉动作记忆、动作原型与 flow 生成；训练期未来头关闭后 World Expert 仍参与推理 | “把记忆、预测、动作统一起来”也不能单独主张新颖；关注完成交互的证据可用性与严格在线更新合同 |
| [StateMem](https://arxiv.org/abs/2609.22684)，09-19 | 预测误差更新持久记忆 token，并调节缓存前缀刷新 | “预测残差更新记忆 token”已有直接邻近方案；不能只换 token 名称 |
| [ForceRFT](https://arxiv.org/abs/2609.22840)，09-19 | 执行时力反馈条件化残差 RL，结合人工修正和自主价值更新 | 真机接触修正已有强参照。当前仅关节位置与命令不能当成力觉的替代品；干预段与自主段应分别核算 |
| [Imagine-RL](https://arxiv.org/abs/2609.24033)，09-21 | 冻结视觉／力矩世界模型预测候选动作后果，历史预测残差为 critic 的未来信息提供可信度权重 | 与未来想做的“预测后果帮助 critic＋误差校准”高度接近。当前代码没有这条完整路径，不应借用其能力描述 |
| [THAW-VLA](https://arxiv.org/abs/2609.24682)，09-21 | 缓存冻结世界模型的特征作为 VLA 训练监督，部署移除投影器 | “训练时学习物理表征、部署时不运行世界模型”已有路线；若做联合 Stage 1，必须加入此类蒸馏对照 |
| [RouteRLT](https://arxiv.org/abs/2609.26467)，09-22 | 学习何时、选择哪个 RL specialist，并处理切换时未执行的 chunk 后缀 | 自动阶段切换不宜再作为空白创新点；论文真机采用 operator-aligned handoff，不能描述成完全无人协助 |
| [Training-free Behavior Cloning](https://arxiv.org/abs/2609.30134)，09-24 | 从示范检索行为，并以闭式响应修正补偿局部变化 | Zeva 线必须比较简单检索／经验响应，不能只与无历史比较 |
| [VLaRL](https://arxiv.org/abs/2609.30868)，09-25 | 冻结 VLA，利用内部 latent 条件化仿真训练的 residual，并映射到真机 | “冻结 VLA＋小 residual＋latent”不是创新；区别应落在部署后新证据如何持续改变动作与旧能力保持 |
| [F4R](../../notes/f4r.md)（[原文](https://arxiv.org/abs/2609.35575v2)），首发 09-28，修订 09-29 | 识别真实失败，重建物体中心仿真，定向 sim-real co-training 与 RL，再部署收集新失败 | 对“反复实践持续成长”叙事的最新直接近邻。可借鉴失败条件驱动测试，但当前没有其场景重建与完整再部署系统 |
| [ARMS / Watch, Recall, Act](https://arxiv.org/abs/2609.28429)，09-23 | π0.5 加入异步感知、具身状态与动作历史上下文，处理持续多模态任务流 | “记录自己做过什么再读取”不是空白；要区分异步上下文组织与在线参数学习 |
| [MessyMem](https://arxiv.org/abs/2609.15976v2)，首发 09-14，修订 09-15 | 交互结果与视觉线索写入空间场景图，供后续移动操作任务读取 | 真正的跨访问、跨任务持久知识已有近邻；我们的 reset 默认清空短期记忆远未达到相同范围 |
| [MPC Scaffolding](https://arxiv.org/abs/2609.14878v2)，首发 09-14，修订 09-16 | MPC 先验轨迹预训练 actor/critic，在线间歇引导采集，逐步交接给 RL | 强化了先验证参考跟随／热身、再接管的实验依据；不能把额外 MPC 模型与轨迹的收益算成同信息算法优势 |

其中 Imagine-RL、RouteRLT、UniMPA、StateMem、F4R 已检查方法段；THAW-VLA、Training-free Behavior Cloning、ARMS、MessyMem、MPC Scaffolding 当前为摘要／方法概览级筛查。检索覆盖至 09-30，找到的最新直接相关修订是 09-29；这不表示 09-30 没有其他相关工作。论文结果均为作者报告，不作为本项目实验证据。

## 不能遗漏的基础对照

- [Residual Reinforcement Learning for Robot Control](https://arxiv.org/abs/1812.03201)：既有控制与学习残差结合有长期研究基础。
- [Maximum a Posteriori Policy Optimisation](https://arxiv.org/abs/1806.06920) 与 [Discrete SAC](https://arxiv.org/abs/1910.07207)：有限候选期望、soft improvement 和分布拟合都有既有算法背景。我们的选择器不是新的离散 RL 原理。
- [AtomicVLA](https://arxiv.org/abs/2603.07648)，2026-03-08：学习原子技能与专家组合；当前手写关节偏移没有技能语义、终止条件或技能学习，不能与其混称。
- [ZPRL](https://arxiv.org/abs/2605.19919)，2026-05-19：在冻结动作生成器的瓶颈 latent 上做 RL 扰动，是动作空间 residual 的重要替代路线。
- [MemoryVLA](https://arxiv.org/abs/2508.19236) 与 [TempoFit](https://arxiv.org/abs/2603.07647)：历史视觉／前缀缓存也可能解释收益，应与“动作导致变化”的证据编码区分。
- [Learning While Deploying](https://arxiv.org/abs/2605.00416)：机器人部署、经验汇聚、更新、再部署已形成系统级路线；“越用越好”需要固定测试、遗忘与干预成本指标，不是加一个 replay 就成立。
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](https://arxiv.org/abs/2605.26820)：持续更新必须同时检查新任务收益与旧任务遗忘。

## Jev 到底借鉴了什么

[TypeSafe 的原始介绍](https://typesafe.ai/blog/introducing-system-one-models-and-jev)强调给定候选的结构化决策。这个产品接口不等于机器人技能学习算法，也不提供物理安全保证。本项目不调用该服务、不使用文本状态生成器；只借鉴“有限选择而非自由生成”的问题分解。

已核对 [jev-libero 的 architecture 源码说明](https://github.com/Dimweaker/jev-libero/blob/3bdad985b225aeccc39fbe5863c6eea2e81c515a/docs/architecture.md)：当前 commit 为 `3bdad985b225aeccc39fbe5863c6eea2e81c515a`。它由代码执行一／两步可恢复预演，读取 MuJoCo 接触和 FCL 几何，再交给 Jev 选择。它的 27 类输入包括不同幅度平移、旋转与夹爪操作；视频可省略模型与预演等待。这与只读取 RLT 已有观测、没有预演的本地选择器不构成等信息比较。快照回放一致也不证明模型对真实物理的预测准确。

## 值得继续的窄问题

建议主问题不是“三篇论文组合能否自进化”，而是：**在观测和交互预算固定时，完成过的动作—响应证据是否让下一次修正更准确，并减少重复错误和人工帮助？**

三条分支分别给出可否证子问题：预测分支是否真的利用动作；记忆分支是否优于短窗口与固定响应公式；有限动作分支是否优于同幅度连续 residual。这些属于尚待验证的研究定位，不是“已避开撞车”的结论。先完成独立对照，再考虑联合，能减少把额外信息、探索范围、额外参数或调参次数误归因为“物理经验”的风险。

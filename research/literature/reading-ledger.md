# Physical Token 文献阅读总账

> 建立日期：2026-09-19  
> 更新日期：2026-09-25
> 范围：132 项论文/项目，另列 1 项观点；09-25 补录已有 RSI 专区的 Knowin GLOW，并新增 Real2sim2real 观点专题。此前 131 项与阅读状态保留。
> 原则：**检索到 ≠ 读懂；摘要笔记 ≠ 全文精读。** 所有条目先保留检索笔记，只有完成方法、实验、附录/代码核验后才升级为“精读”。

## 0. 当前进度

| 状态 | 数量 |
|---|---:|
| 已精读/已有独立笔记 | 8 |
| 已阅读/已有专题笔记 | 11 |
| 已初读/讨论过，待系统精读 | 12 |
| 待精读 | 101 |
| **论文/项目总计** | **132** |

另列 **1 项观点**，不混入论文阅读数量。

完整检索工作稿：[`physical-token-literature-audit-2026-09-19.md`](physical-token-literature-audit-2026-09-19.md)。其中每篇至少有“方法摘要 + 与本项目关系 + 核验边界 + 一手来源”的**检索笔记**；这不等于已经全文精读。

## 1. 状态定义

- **已精读/已有独立笔记**：已经围绕核心机制、训练/推理流程、证据与项目边界做过较深入阅读，并有独立 notes 文件。
- **已阅读/已有专题笔记**：围绕当前问题做过专题阅读，已有独立笔记，但仍可能需要补附录/代码。
- **已初读/讨论过，待系统精读**：已经讨论过主要思想，但还不能作为 related-work 最终表述依据。
- **待精读**：当前只有检索/摘要级 mini-note；正式写论文前必须继续读正文、实验、附录和代码。

## 2. 近期阅读顺序

### 09-25：GLOW 与 Real2sim2real

| 条目 | 类型与状态 | 借鉴重点 |
|---|---|---|
| [Knowin GLOW](../../notes/knowin-glow.md) | P132；企业技术报告，已专题阅读、未复现；补录已有 RSI 案例 | 执行回执、经验监督分流、记忆有效性 |
| [Real2sim2real——具身的 scaling 起点](../real2sim2real-scaling-perspective.md) | 观点；截图已梳理，作者与公开原文待核实；不计入论文数量 | 区分场景重建与动力学校准，明确 agent 的离线作用 |

[三项可执行候选实验](../glow-real2sim2real-experiments.md)：同容量实测后果监督、同预算记忆检索、响应校准。全部未执行；按假设、标签、对照、指标和停止条件展开。

### 09-22 项目相关增量

UniIntervene 为 P0 减干预强近邻，优先明确未来预测、时序价值与记忆恢复的既有边界；CLAP 为 P1 动作后果/跨本体接口参考。两项已核对方法、实验、相关附录与官方 README，未复现。保持[当前研究合同](../physical-experience-protocol-2026-09-22.md)，不新增完整世界模型或恢复大模型训练前置要求。

### 09-21 增量

ForceDelta-VLA 列为新增 P0 强近邻，先核验监督来源和时序/感知归因；RPent 列为 P1 系统专题，关联 P107 Harness VLA，不作为第二篇同名论文。两项均为专题阅读，未升级全文/代码精读。

### Wave 0 · 防撞优先（09-19 批次）

RLT → FLARE → Pri4R → AGRA → CometVLA → PAR → DyWA → TACO → RoboPack → MSDP → exUMI → Spline Policy → LeTO → V-GPS → FlowDAgger → DSRL → HPT → GeoAAC。

### Wave 1 · Physical representation / supervision

Manipulator RMA、FD-VLA、HapticVLA、DeCAL、PIN-WM、ContactNets、RoboPack、MuSe、UniTac-NV。

### Wave 2 · Learner / value / action selection

RECAP、V-GPS、Q-VGM、DSRL、FlowDAgger、LWD、IQL、CQL、Cal-QL、RLPD。

### Wave 3 · WAM / world-action interface

RepWAM、OA-WAM、RISE、Motus2、Riemann-1.0、WAM-RL、DINO-WM、V-JEPA 2、DyWA。

### Wave 4 · Execution / recovery / harness

SmoothRL、VLA-Corrector、BCP、GeoAAC、RL²-VLA、Zeva、Harness VLA、SHAPER、Zetta、ASPIRE、ENPIRE。

## 3. 每篇精读必须填满的 10 个问题

1. 它真正解决的 scientific problem 是什么？
2. 输入是什么，哪些是部署时可得、哪些是 privileged？
3. representation / action feature 从哪里取？
4. 训练目标和 loss 是什么，梯度更新哪些参数？
5. action / state / time 的定义是什么，是否区分 proposed 与 executed？
6. 它最强的 baseline 和关键 ablation 是什么？
7. 核心实验是否真的证明了它声称的 physical / universal / self-improving？
8. 与我们的 Physical Token 哪一部分重合？
9. 哪个点可以借，哪个点必须避免重复？
10. 读完后对我们的实验产生什么具体 action：baseline / ablation / metric / no-action？

## 4. 原始 125 项目录（09-19 快照）

### 动作侧表征与最邻近工作

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P001 | [RLT](https://arxiv.org/abs/2604.23073) | P0 | 已精读/已有独立笔记 | [独立笔记](../../notes/rlt.md) |
| P002 | [Pri4R](https://arxiv.org/abs/2603.01549) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P003 | [FLARE](https://proceedings.mlr.press/v305/zheng25a.html) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P004 | [AGRA](https://arxiv.org/abs/2606.12217) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P005 | [CometVLA](https://arxiv.org/abs/2608.30289) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P006 | [PAR](https://arxiv.org/abs/2508.09822) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P007 | [PhysGen](https://arxiv.org/abs/2603.00110) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P008 | [SA-VLA](https://arxiv.org/abs/2606.30113) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P009 | [ActionPiece](https://arxiv.org/abs/2609.18487) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P010 | [Spline Policy](https://arxiv.org/abs/2606.07386) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P011 | [PhysVLA](https://arxiv.org/abs/2606.13886) | P1 | 已阅读/已有专题笔记 | [独立笔记](../../notes/physvla.md) |
| P012 | [MCF-Proto](https://arxiv.org/abs/2605.11809) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P013 | [X-DiffVLA](https://arxiv.org/abs/2605.25044) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P014 | [DyWA](https://openaccess.thecvf.com/content/ICCV2025/html/Lyu_DyWA_Dynamics-adaptive_World_Action_Model_for_Generalizable_Non-prehensile_Manipulation_ICCV_2025_paper.html) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P015 | [GAP](https://arxiv.org/abs/2602.23814) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P016 | [VLA物理/空间复审](https://openaccess.thecvf.com/content/CVPR2026/html/Li_VLA_Models_Are_More_Generalizable_Than_You_Think_Revisiting_Physical_CVPR_2026_paper.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 动力学充分表示、历史辨识与表征理论

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P017 | [UP-OSI](https://faculty.cc.gatech.edu/~turk/paper_pages/2017_learning_universal_policy/index.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P018 | [RMA](https://www.roboticsproceedings.org/rss17/p011.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P019 | [Manipulator RMA](https://openaccess.thecvf.com/content/CVPR2024/html/Liang_Rapid_Motor_Adaptation_for_Robotic_Manipulator_Arms_CVPR_2024_paper.html) | P1 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P020 | [DeepMDP](https://proceedings.mlr.press/v97/gelada19a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P021 | [DBC](https://ai.meta.com/research/publications/learning-invariant-representations-for-reinforcement-learning-without-reconstruction/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P022 | [SPR](https://arxiv.org/abs/2007.05929) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P023 | [TACO](https://www.microsoft.com/en-us/research/publication/taco-temporal-latent-action-driven-contrastive-loss-for-visual-reinforcement-learning/?lang=ja) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P024 | [TD-MPC](https://proceedings.mlr.press/v162/hansen22a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P025 | [TD-MPC2](https://proceedings.iclr.cc/paper_files/paper/2024/hash/cf73d57b6dcda32b293df7c2d5341f49-Abstract-Conference.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P026 | [R3M](https://proceedings.mlr.press/v205/nair23a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P027 | [VIP](https://arxiv.org/abs/2210.00030) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P028 | [Offline meta-RL](https://proceedings.mlr.press/v162/pong22a.html) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P029 | [Situational dynamics](https://journals.sagepub.com/doi/abs/10.1177/02783649261431863) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 力触觉、接触与多模态物理监督

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P030 | [Making Sense](https://ieeexplore.ieee.org/document/9043710/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P031 | [FD-VLA](https://arxiv.org/abs/2602.02142) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P032 | [HapticVLA](https://arxiv.org/abs/2603.15257) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P033 | [MSDP](https://arxiv.org/abs/2511.14427) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P034 | [MuSe](https://arxiv.org/abs/2606.30988) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P035 | [DeCAL](https://arxiv.org/abs/2609.09119) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P036 | [exUMI](https://proceedings.mlr.press/v305/xu25e.html) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P037 | [TacX](https://proceedings.mlr.press/v305/higuera25a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P038 | [Sparsh](https://proceedings.mlr.press/v270/higuera25a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P039 | [UpViTaL](https://ieeexplore.ieee.org/document/11127230/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P040 | [RoboPack](https://www.roboticsproceedings.org/rss20/p130.html) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P041 | [See, feel, act](https://doi.org/10.1126/scirobotics.aav3123) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P042 | [Deep Haptic MPC](https://arxiv.org/abs/1709.09735) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P043 | [UniTac-NV](https://arxiv.org/abs/2506.19699) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 显式物理模型、可微约束与安全控制

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P044 | [PIN-WM](https://www.roboticsproceedings.org/rss21/p153.html) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P045 | [DeLaN](https://arxiv.org/abs/1907.04490) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P046 | [ContactNets](https://arxiv.org/abs/2009.11193) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P047 | [GNS](https://proceedings.mlr.press/v119/sanchez-gonzalez20a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P048 | [DPI-Net](https://arxiv.org/abs/1810.01566) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P049 | [RoboCraft](https://journals.sagepub.com/doi/10.1177/02783649231219020) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P050 | [SAM-RL](https://roboticsproceedings.org/rss19/p040.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P051 | [PROMPT](https://roboticsproceedings.org/rss17/p071.html) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P052 | [One-Shot Real-to-Sim](https://ieeexplore.ieee.org/document/10982102/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P053 | [PhysDreamer](https://physdreamer.github.io/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P054 | [PhysMani](https://arxiv.org/abs/2607.01938) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P055 | [LeTO](https://docs.lib.purdue.edu/iepubs/14/) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P056 | [DDAT](https://iconlab.negarmehr.com/DDAT/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P057 | [DPCC](https://arxiv.org/abs/2412.09342) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P058 | [MDOC](https://www.roboticsproceedings.org/rss22/p041.html) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P059 | [Learned CBF](https://arxiv.org/abs/2004.03315) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P060 | [Safe Learning review](https://www.annualreviews.org/content/journals/10.1146/annurev-control-042920-020211) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P061 | [Learning-Based MPC review](https://doi.org/10.1146/annurev-control-090419-075625) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P062 | [UMI-on-Air](https://arxiv.org/abs/2510.02614) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P063 | [HFVC Preconditions](https://proceedings.mlr.press/v205/liang23a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P064 | [Fill the Seam](https://ieeexplore.ieee.org/document/9812429/) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P065 | [Diffused Orientation Fields](https://doi.org/10.1126/scirobotics.aea1762) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P066 | [Prof. Robot](https://openaccess.thecvf.com/content/CVPR2025/html/Ruan_Prof._Robot_Differentiable_Robot_Rendering_Without_Static_and_Self-Collisions_CVPR_2025_paper.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 世界—动作模型与潜空间未来预测

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P067 | [RepWAM](https://arxiv.org/abs/2606.13674) | P1 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P068 | [OA-WAM](https://arxiv.org/abs/2605.06481) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P069 | [Riemann-1.0](https://arxiv.org/abs/2608.27033) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P070 | [WAM-RL](https://arxiv.org/abs/2606.17906) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P071 | [RISE](https://arxiv.org/abs/2602.11075) | P1 | 已精读/已有独立笔记 | [独立笔记](../../notes/rise.md) |
| P072 | [Motus2](https://arxiv.org/abs/2608.30237) | P1 | 已精读/已有独立笔记 | [独立笔记](../../notes/motus2.md) |
| P073 | [CauVA](https://www.roboticsproceedings.org/rss22/p016.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P074 | [DINO-WM](https://proceedings.mlr.press/v267/zhou25t.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P075 | [V-JEPA 2](https://arxiv.org/abs/2506.09985) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P076 | [DreamerV3](https://www.nature.com/articles/s41586-025-08744-2) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P077 | [Human-video structured WM](https://roboticsproceedings.org/rss19/p012.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P078 | [DiWA](https://proceedings.mlr.press/v305/chandra25a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P079 | [EgoWAM](https://arxiv.org/abs/2607.08436) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P080 | [GlanceWAM](https://arxiv.org/abs/2608.23927) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P081 | [Video2Act](https://arxiv.org/abs/2512.03044) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P082 | [PointWorld](https://point-world.github.io/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 离线／在线RL、价值引导与冻结策略适配

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P083 | [RECAP / π*0.6](https://arxiv.org/abs/2511.14759) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P084 | [LWD](https://arxiv.org/abs/2605.00416) | P1 | 已精读/已有独立笔记 | [独立笔记](../../notes/lwd.md) |
| P085 | [Q-VGM](https://arxiv.org/abs/2606.08015) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P086 | [V-GPS](https://proceedings.mlr.press/v270/nakamoto25a.html) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P087 | [RedFlow](https://arxiv.org/abs/2607.27782) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P088 | [DSRL](https://proceedings.mlr.press/v305/wagenmaker25a.html) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P089 | [FlowDAgger](https://arxiv.org/abs/2607.08877) | P0 | 已初读/讨论过，待系统精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P090 | [Policy Decorator](https://policydecorator.github.io/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P091 | [IQL](https://arxiv.org/abs/2110.06169) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P092 | [CQL](https://proceedings.neurips.cc/paper/2020/hash/0d2b2061826a5df3221116a5085a6052-Abstract.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P093 | [Cal-QL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/c44a04289beaf0a7d968a94066a1d696-Abstract-Conference.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P094 | [RLPD](https://proceedings.mlr.press/v202/ball23a.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P095 | [DPPO](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c0749c39aaff9e9e4c91f7118bf21b1e-Abstract-Conference.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P096 | [FQL](https://proceedings.mlr.press/v267/park25f.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P097 | [ConRFT](https://arxiv.org/abs/2502.05450) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P098 | [HIL-SERL](https://hil-serl.github.io/) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P099 | [D2PPO](https://arxiv.org/abs/2508.02644) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 执行时序、失败恢复与非参数自进化

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P100 | [SmoothRL](https://arxiv.org/abs/2608.29768) | P1 | 已精读/已有独立笔记 | [独立笔记](../../notes/smoothrl.md) |
| P101 | [VLA-Corrector](https://arxiv.org/abs/2607.01804) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P102 | [BCP](https://arxiv.org/abs/2608.03483) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P103 | [GeoAAC](https://arxiv.org/abs/2609.20776) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P104 | [RL²-VLA](https://arxiv.org/abs/2607.26991) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P105 | [FailSafe](https://arxiv.org/abs/2510.01642) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P106 | [Zeva](https://arxiv.org/abs/2608.30880) | P0 | 已精读/已有独立笔记 | [独立笔记](../../notes/zeva.md) |
| P107 | [Harness VLA](https://arxiv.org/abs/2607.08448) | P1 | 已阅读/已有专题笔记 | [独立笔记](../../notes/harness-vla.md) |
| P108 | [SHAPER](https://arxiv.org/abs/2608.11350) | P1 | 已精读/已有独立笔记 | [独立笔记](../../notes/shaper.md) |
| P109 | [ASPIRE](https://arxiv.org/abs/2607.00272) | P1 | 已阅读/已有专题笔记 | [独立笔记](../../notes/aspire.md) |
| P110 | [ENPIRE](https://arxiv.org/abs/2606.19980) | P1 | 已阅读/已有专题笔记 | [独立笔记](../../notes/enpire.md) |
| P111 | [Zetta ζ](https://arxiv.org/abs/2608.16590) | P1 | 已精读/已有独立笔记 | [独立笔记](../../notes/zetta.md) |
| P112 | [AGM](https://arxiv.org/abs/2608.29537) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P113 | [ForeAct](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_ForeAct_Steering_Your_VLA_with_Efficient_Visual_Foresight_Planning_CVPR_2026_paper.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P114 | [SEAM](https://ri.cuhk.edu.hk/en/research/projects/rethinking-intermediate-representation-for-vlm-based-robot-manipulation) | P2 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

### 通用动作头、动作tokenizer与跨本体底座

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---:|---|---|
| P115 | [π0](https://arxiv.org/abs/2410.24164) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P116 | [π0.5](https://arxiv.org/abs/2504.16054) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P117 | [OpenVLA](https://arxiv.org/abs/2406.09246) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P118 | [FAST](https://arxiv.org/abs/2501.09747) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P119 | [Diffusion Policy](https://journals.sagepub.com/doi/10.1177/02783649241273668) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P120 | [ACT](https://arxiv.org/abs/2304.13705) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P121 | [Octo](https://arxiv.org/abs/2405.12213) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P122 | [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P123 | [HPT](https://papers.nips.cc/paper_files/paper/2024/hash/e0f393e7980a24fd12fa6f15adfa25fb-Abstract-Conference.html) | P0 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P124 | [LAPA](https://proceedings.iclr.cc/paper_files/paper/2025/hash/45d74e190008c7bff2845ffc8e3facd3-Abstract-Conference.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |
| P125 | [VQ-BeT](https://proceedings.mlr.press/v235/lee24y.html) | P1 | 待精读 | [检索笔记](physical-token-literature-audit-2026-09-19.md) |

## 5. 阅读升级规则

- 从“待精读”升级到“初读”：必须读完正文并能画出方法图。
- 从“初读”升级到“已阅读”：必须能解释最关键 loss / data / inference contract，并完成项目重合判断。
- 从“已阅读”升级到“精读”：必须读实验与附录，核查至少一个关键实现或公开代码路径，并能写出 reviewer 可能质疑的点。
- 对 P0 最近邻，正式写论文前应额外完成 code / appendix audit；仅靠摘要不得形成 novelty claim。

## 5. 2026-09-21 新增专题

| ID | 工作 | 优先级 | 类型与状态 | 笔记 |
|---|---|---|---|---|
| P126 | [ForceDelta-VLA](https://arxiv.org/abs/2609.18242) | P0 | 论文；已阅读/已有专题笔记 | [专题笔记](../../notes/forcedelta-vla.md) |
| P127 | [RPent](https://github.com/RLinf/RPent) | P1 | 系统；已阅读/已有专题笔记 | [专题笔记](../../notes/rpent.md) |

增量说明：125 项历史检索稿保持原样；新增条目的方法、证据与边界记录在独立笔记及 JSON 总账。RPent 与 P107 Harness VLA 通过关联记录区分。

## 6. 2026-09-21 追加：恢复经验与物理判定

| ID | 工作 | 优先级 | 类型与状态 | 笔记 |
|---|---|---|---|---|
| P128 | [XPACE](https://arxiv.org/abs/2609.17372) | P1 | 论文；已阅读/已有专题笔记 | [专题笔记](../../notes/xpace.md) |
| P129 | [EmbodiedJev](https://github.com/FBddcz/embodied-jev) | P1 | 系统；已阅读/已有专题笔记 | [专题笔记](../../notes/embodied-jev.md) |

[关联RLT的候选实验](../xpace-jev-rlt-ideas.md)：先做可恢复性probe，再以表示×恢复数据选择的2×2实验分离收益。此为未实施提案。


## 7. 09-22 增量：UniIntervene 与 CLAP

| ID | 论文 | 优先级 | 阅读状态 | 笔记 |
|---|---|---|---|---|
| P130 | [UniIntervene](https://arxiv.org/html/2606.12372v1) | P0 | 已阅读/已有专题笔记；未复现 | [专题笔记](../../notes/uniintervene.md) |
| P131 | [CLAP](https://arxiv.org/html/2608.27406v1) | P1 | 已阅读/已有专题笔记；未复现 | [专题笔记](../../notes/clap.md) |

[对当前 Physical Token / RLT 的取舍](../uniintervene-clap-project-implications.md)：固定专家与 gate 的表示验证优先；完整视频模型、记忆扩张与学习门控分别作为后续变量。

## 8. 09-25 补录：企业系统与观点分开统计

| ID / 类型 | 标题 | 优先级与状态 | 入口 |
|---|---|---|---|
| P132 / 企业系统 | [GLOW: A Generative Learning Framework for General-Purpose Embodied Intelligence](https://knowinai.com/tech.html) | P1；官方技术页专题阅读，未复现 | [独立笔记](../../notes/knowin-glow.md) |
| 观点 / 不占论文编号 | Real2sim2real——具身的 scaling 起点 | 原文来源待核实；截图观点与本库分析分开 | [观点拆解](../real2sim2real-scaling-perspective.md) |

GLOW 此前已有 RSI 专区案例，本次只补齐主知识库入口与实验关系，不新增第二个同名系统。Real2sim2real 观点关联原目录 P050 SAM-RL 与 P052 One-Shot Real-to-Sim；本轮仅核对相关公开摘要/项目说明，未提升这两篇的历史阅读等级。

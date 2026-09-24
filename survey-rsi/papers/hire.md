[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# HiRE: Hindsight Reward Editing for Policy Finetuning

> **一句话：** 用成功与失败观测持续改写奖励，再在线微调策略。

**首次公开：** 2026-09-22　**采用版本：** arXiv v1　**核查日期：** 2026-09-24　**状态：** 预印本；方法及指定实验已核查，未复现。

**作者：** Niu, Haoyi；Han, Zhengtao；Ji, Yufeng；Li, Zhongyu；Sreenath, Koushil

[摘要与版本](https://arxiv.org/abs/2609.27068) · [全文 v1](https://arxiv.org/html/2609.27068v1) · [PDF](https://arxiv.org/pdf/2609.27068v1) · [作者项目](https://hire-project.github.io/)

**综述定位：** 核心策略改进 / 奖励自适应 / 在线RL / 真机与仿真

![HiRE 原文图](https://arxiv.org/html/2609.27068v1/visualization/reward_score_plot/segment_focused_viz.png)

*原文 v1 Figure 2：沿执行轨迹对照视觉相似度奖励和 HiRE 奖励，展示目标丢失与恢复时的反馈差异。这是机制可视化，不是系统架构图。 [原图](https://arxiv.org/html/2609.27068v1/visualization/reward_score_plot/segment_focused_viz.png)，版权归原作者。*

## 解决什么问题

 冻结视觉编码器的目标相似度奖励可能被“看起来接近目标”的失败轨迹利用，例如丢失物体后机械臂仍靠近终点。稀疏成功信号又难以支持高效在线微调。

## 核心方法

 保留成功与失败观测支持集，在冻结的 DINOv2/SigLIP 特征空间构造正负密度对比势函数，作为势能奖励塑形信号，与稀疏完成奖励一起训练策略。新执行结果持续编辑支持集，奖励编辑本身不需梯度；策略仍通过 DICE-RL 残差 actor/critic 进行训练。不能把“无梯度奖励编辑”写成“整个系统不训练”。

## 主要结果

 仿真覆盖 RoboMimic/MimicGen 四任务、三随机种子；ToolHang 中稀疏奖励基线几乎无法学习，HiRE 最终约 95%。真机为 I2RT YAM 六自由度机械臂、线性夹爪和两台 RealSense；瓶子任务基础策略使用 117 条示范，汉诺塔使用 50 条。先采 20 个 warm-up episode，此后交替采集和训练。瓶子任务每检查点 30 次，基础策略 **6/30→20/30**，60 和 70 个在线 episode 时均为 66.7%；汉诺塔每检查点 15 次，报告**峰值** 73.3%，应避免写成稳定最终成绩。主要在线训练使用一张 RTX 5090。

## 综述可借鉴之处

 奖励不仅是预先固定的裁判，也可随策略经验更新。适合连接“奖励可靠性”“失败样本价值”“策略—反馈共同适配”三个主题；与 No Free Checker 的验证器盲区、SRPO 的自参考奖励形成比较。

## 证据边界

 真机成功/失败标签由人提供，不能根据摘要称其完全没有人工反馈。支持集更新规则、表征与学习算法固定，没有改进规则递归增强。势能塑形的策略不变性有理论条件，不能推广为任意自适应奖励均安全；不同仿真消融还存在奖励尺度/回放配置差异。实时反馈更新和机器人参数学习有证据，跨部署长期保持尚未展示。

## 原文定位

 §§3–5，Figures 1–3，Table 2；Appendices A–C。 已核对原文方法、指定结果和样本口径；未复现代码。

**标签轴：** 更新对象：奖励支持集、残差策略/价值函数；反馈：成功/失败标签＋视觉表征；保留范围：在线多轮采集与更新；同任务；物理证据：四项仿真＋两项真机。

[证据对照](../evidence-map.md) · [综述提纲](../survey-outline.md) · [本轮记录](../daily/2026-09-24-follow-up.md)

[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# AD-WM: Action-Discriminative World Models for Counterfactual Model Predictive Control

> **一句话：** AD-WM 让潜在世界模型更能区分同一状态下的候选动作，从而改善反事实 MPC；它强化了预测到行动的桥梁，但训练完成后不再从部署经验更新。

短名：AD-WM　作者：Jiabin Qiu, Zixuan Chen, Hongye Cao, Jieqi Shi, Jing Huo, Yang Gao　首次发表：2026-09-24　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.30264](https://arxiv.org/abs/2609.30264)　项目页：[AD-WM](https://ad-wm.github.io/)　最后核查日期：2026-09-27

![AD-WM 原文 Figure 2](https://arxiv.org/html/2609.30264v1/ad-wm.png)

*图注：常规 JEPA 低预测误差可能掩盖动作差异；AD-WM 用 residual transition、inverse recovery 与归一化 action-recovery 约束保留反事实动作信息。来源：原文 Figure 2，arXiv v1。*

## 解决什么问题

MPC 需要从同一状态比较多条候选动作，但潜在世界模型通常只优化事实转移误差：即使预测值接近真实，也可能无法正确排序动作。论文问的是应优化什么表征和诊断指标，才能让预测真正服务闭环行动选择。

## 核心方法

AD-WM 在 joint-embedding 模型中预测 latent increment 而非绝对下一状态，并加入 inverse dynamics 和经归一化的 action-recovery / conditional mutual information 目标，迫使预测后表征保留动作信息。辅助头训练后丢弃，部署仍使用相同 CEM/MPC。作者另外提出 candidate action discriminability 与 elite regret，检查模型能否选出后验代价较低的候选，而不只比较 factual MSE。

## 主要结果

- **匹配仿真：** OGBench-Cube 在相同 LeWM 架构、训练和 CEM 预算下，五类 hard-start 平均成功率从 3.7±1.4% 到 52.0±3.1%；Original 从 73.3±2.5% 到 90.7±3.4%。跨五个环境的匹配复现中四个提高：Cube 73.3→90.7、Reacher 76.7→83.3、TwoRoom 90→98、Scene 35.5→39.5；PushT 94→92。Scene 的三种子配对检验 p=0.13，增益未解决。
- **诊断：** LeWM 的 factual MSE 最低却控制成功率最低；hard-start success 与负 elite regret 的相关为 0.810–0.863，说明候选选择质量比单纯预测误差更接近控制收益，但相关只基于固定候选 bank。
- **真机：** Franka 使用冻结 V-JEPA2 ViT-G、DROID 后训练且不使用实验室图像/示范。每模型 82 次：基础 pick-and-place 19/45→32/45，复杂物体 2/10→5/10，目标物体移动 14/27→21/27，完整 lift-and-place 9/27→17/27；安全停止记失败。训练用 4 张 A800，315 epochs×300 iterations，batch 8/GPU。

## 综述可借鉴之处

AD-WM 可支撑“世界模型不能只看视觉预测精度”的论点。综述中的 matched protocol 应固定编码器、数据、规划器、候选预算和执行栈，再把**事实预测、候选排序、elite regret、闭环成功和推理成本**分列。它也是世界模型作为自我改进支撑件的典型：能提高行动选择，不代表系统会从后续物理经验继续进化。

## 证据边界

部署期间不更新模型或策略，因此不是持久 RSI。真机由人工提供 grasp/move/place 图像子目标，使用单一场地、相机与 backbone，且模型试验按非随机块执行。诊断主要在 Cube；外部方法的训练和推理预算不同。Scene 增益的统计证据不足，真机复杂协议样本也较小。

## 原文定位

§III-A–E；§IV-A–E；Figures 2、4–5；Tables I–IV；§V 限制；采用 arXiv v1。全文方法、匹配仿真、诊断和 164 次总真机试验已核查；未复现。

标签：世界模型 / 离线数据 / 固定部署模型 / 自主规划 / Franka真机 / matched与非随机块 / 支撑组件 / 预测—行动桥梁。

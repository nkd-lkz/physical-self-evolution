[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# An Analysis of Streaming Deep Reinforcement Learning for Adaptive Continual Learning in Robotics

> **一句话：** 论文让预训练机器人策略只用最新一条 transition、无 replay 地持续更新；四足仿真能从突变中恢复，操作任务却出现峰值后衰退，直接展示了持久参数更新的潜力和稳定性上限。

短名：Streaming Deep RL for Robotics　作者：Teeratham Vitchutripop, Alyssa Quarles, Wenhe Zhang, Richard Xue, Daniel Rakita　首次发表：2026-09-23　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.28807](https://arxiv.org/abs/2609.28807)　代码：[tjvitchutripop/stream-rl-robotics](https://github.com/tjvitchutripop/stream-rl-robotics/)　最后核查日期：2026-09-27

![Streaming Deep RL 原文 Figure 1](https://arxiv.org/html/2609.28807v1/figures/overview.png)

*图注：预训练后，Stream-AC 在机器人、自身环境或目标发生突变时，以 batch size 1 的最新经验持续更新，不使用 replay buffer。来源：原文 Figure 1，arXiv v1。*

## 解决什么问题

大多数机器人 RL 依赖批量更新、经验回放或离线重训，难以逐步利用刚发生的部署经验。论文分析深度流式 RL 是否能把一个预训练策略持续适配到未见的本体、环境和目标突变，以及优化器和防塑性损失机制会怎样影响稳定性。

## 核心方法

作者先用并行 PPO 预训练策略，再用 Stream-AC 每步读取并立即丢弃最新 transition，以 batch size 1 的 TD 更新 actor–critic。比较 Adam、Overshooting-bounded Gradient Descent（ObGD）、AdaptiveObGD，以及 AdaptiveObGD 配 continual backpropagation（CBP）或 layer normalization（LN）。实验由熟悉条件的 50 万步 warm-start 和突变后的 150 万步组成；每 1 万步冻结参数、评测 50 episodes。

## 主要结果

- **四足：** ManiSkill3 AnymalC-Reach，5 种子。三种突变下，最佳流式方法的峰值成功率分别为：断腿 AdaptiveObGD 0.968、目标移动 AdaptiveObGD+LN 0.848、低摩擦 AdaptiveObGD+LN 0.676；预训练策略为 0.060/0/0。Batch PPO 的对应峰值为 0.412/0.060/0.004。均值成功率明显低于峰值，例如 AdaptiveObGD+LN 为 0.538/0.436/0.278。
- **操作：** Panda Push Cube 目标移动时，AdaptiveObGD+LN 峰值 0.784、全程均值 0.233，基线为 0；曲线峰值后下降到约 20%。Transport Box 关节受损时峰值 0.248、均值 0.122，预训练策略为 0.080，显示复杂任务恢复有限。
- **口径：** 成功率每次以 50 episodes 计算、训练中每 1 万步评测，全部训练 5 种子。作者还报告 successive difference 衡量波动；ObGD 往往峰值高但更不稳定。

## 综述可借鉴之处

这是“持续在线参数更新”的直接对照，适合与回放式、周期批次式和测试时上下文适应并列。最值得引用的不是“最高提高 90 点”，而是**峰值与全程均值分离**：改进器可能短暂找到好策略却无法保持。综述的多轮评价应至少同时报告峰值、面积/均值、末端表现、方差和旧任务保持。

## 证据边界

全部是带 dense reward 的状态输入仿真，没有相机/VLA或真机安全成本。每个实验只经历一次 M0→M1 突变；作者明确限制为 forward transfer，没有回测原 M0，因此不能证明跨任务抗遗忘。操作结果会随时间退化，且部分优化器经过较强超参调优。策略参数持续更新，但学习规则本身没有自我修改，不是递归改进器。

## 原文定位

§III-B–E；§IV-A–F；§V-A–D；§VI；Figures 1–3；Tables 1–3；采用 arXiv v1。全文方法、训练/评测步数、种子和主要表格已核查；未复现。

标签：策略参数 / dense reward与最新transition / 跨episode持久 / 全自动仿真 / ManiSkill3 / 固定外部成功指标 / 非递归 / 核心持续改进。

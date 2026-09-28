[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Streaming-WAM: Action-Conditioned World-Action Model for Asynchronous Robot Manipulation

> **一句话：** 用已经提交执行的动作前缀约束未来视频和后续动作生成，可在异步控制中显著缩短等待而保持成功率；训练完成后模型固定，因此是世界模型运行支撑，不是部署期学习。

短名：Streaming-WAM　作者：Xuyao Huang, Yixuan Wang, Zengyao Ye, Boyuan Zhao, Chenyang Yu, Haoran Wen, Zhijie Deng　首次发表：2026-09-24　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.28927](https://arxiv.org/abs/2609.28927)　代码：[SJTU-DENG-Lab/Streaming-WAM](https://github.com/SJTU-DENG-Lab/Streaming-WAM)　最后核查日期：2026-09-28

![Streaming-WAM 原文 Figure 2](https://arxiv.org/html/2609.28927v1/streaming-wam-method-slot.png)

*图注：已提交动作成为下一次更新的固定前缀，同时条件化未来视频与动作续写，使推理和执行重叠。来源：原文 Figure 2，arXiv v1。*

## 解决什么问题

世界动作模型在推理时生成未来视频，会让机器人在 action chunk 之间停等。直接异步预测又可能忽略推理期间已经排队执行的动作，导致预测场景与真实状态错位。

## 核心方法

模型从 one-step consistency-distilled Joint-WAM 初始化。第一阶段冻结 action expert，用示范中的已提交动作前缀训练 video expert；第二阶段冻结视频侧，以未来视觉特征监督 action expert 续写剩余动作，同时保留视频终点损失。运行时冷启动后，每执行 8 个动作发起一次更新；在真机 30 Hz 下形成约 267 ms 重叠窗口，作者报告所有更新都在窗口内完成。

## 主要结果

- 四套 LIBERO（各 10 任务、每任务 50 次）平均成功率 98.35%，相对 Fast-WAM 的 episode time 加速 2.93×；相对已蒸馏 Fast-WAM-Joint-CD 仍加速 1.46×。
- RoboTwin 2.0 的 50 任务、Clean/Random 各每任务 100 次中，Streaming-WAM 平均 91.74%，Fast-WAM-Joint 为 87.00%；RoboCasa 24 任务、每任务 50 次为 75.33%，与 X-WAM-CD 持平。
- 两个真机任务各采 50 条示范、每方法评测 30 次。Streaming-WAM 在 Stamp Paper 和 Block Manipulation 分别成功 27/30、28/30，和同步 Joint-WAM 各差 1 次；Stamp Paper 平均 episode time 从 90 s 降至 38 s。

## 综述可借鉴之处

它说明 Physical RSI 系统的世界模型不能只比较成功率或预测 MSE，还要报告推理是否阻塞执行、deadline miss 和完整 rollout 时间。可作为“世界模型支撑持续闭环”的效率基线，与真正部署后更新模型/策略的工作分列。

## 证据边界

训练数据为固定公开示范或新采真机示范，部署期间参数、损失和动作前缀机制不更新；异步上下文变化不是学习。跨 benchmark 的速度基线/backbone 并非完全相同，真机每任务 30 次且成功数差异很小。它不支持持久自我改进或改进器递归。

## 原文定位

§§3–4；Figures 1–6；Tables 1–4。采用 arXiv v1；全文训练阶段、评测分母、真机时延和消融已核查，未复现。

标签：世界动作模型 / 异步执行 / 固定权重 / 仿真与真机 / 运行效率 / 支撑组件 / 非RSI核心。

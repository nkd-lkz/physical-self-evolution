[首页](../README.md) / [主题导航](../topics.md) / [全部论文](../papers/README.md)

# MemBodied: Recurrent Associative Memory for Vision-Language-Action Models

> **一句话：** 固定容量的联想状态能改善同一 rollout 内的历史依赖决策，但作者的跨 episode 携带实验从 50.0% 降到 36.8%，这正好说明“有记忆”不等于持久自我改进。

短名：MemBodied　作者：Tej Deep Pala 等　首次发表：2026-09-23　采用版本：v1　发表状态：arXiv预印本

论文链接：[arXiv](https://arxiv.org/abs/2609.28256) · [HTML](https://arxiv.org/html/2609.28256v1)　项目/代码：[项目页](https://declare-lab.github.io/MemBodied) · [GitHub](https://github.com/declare-lab/MemBodied)　最后核查日期：2026-09-25

![MemBodied原文Figure 1](https://arxiv.org/html/2609.28256v1/membodied_architecture.svg)

*图注：原文 Figure 1（v1）。逐层联想矩阵在策略调用之间读写动作摘要与后续视觉后果，另用 episode 初始场景锚点提供固定参照。*

## 解决什么问题

部分机器人任务的当前图像存在状态别名：同一画面可能对应不同初始位置、已完成步骤或失败尝试。直接堆叠长视频成本高，作者希望给 VLA 一个固定容量、可在 episode 内递归更新的状态。

## 核心方法

每个 action-expert 层维护可读写的联想矩阵，用 gated-delta 更新把“交互/动作摘要＋随后视觉结果”写入状态；episode anchor 压缩首次观察，帮助回忆初始布局。新增约 40M 参数，占 π0 的 1.26%；NativeMEM 的比较实现约 415M、占 12.81%。主设置在每个 rollout 开始时清空联想状态和锚点。

RMBench 用 LoRA 训练 10,000 步、batch 8，序列长度按任务为 8/14/18。真机为两台 AgileX PiPER、顶视 Orbbec 和两台 D405 腕相机；每任务采 50 条示范，清洗后保留 41/50/49 条，并训练任务专用策略。

## 主要结果

RMBench 五个任务、每任务 50 次 rollout：无状态、四帧堆叠、普通递归、去锚点 MemBodied、完整 MemBodied 的均值分别为 6.4、14.8、16.8、37.6、50.0%。NativeMEM 为 38.4%，与 MemBodied 组合为 45.2%；不同任务没有一种方法全部占优。

三项真机任务每种策略各 20 次，完整成功才计分；无状态均值 3.33%，MemBodied 为 26.67%。LIBERO 四套共 40 任务、每任务 50 次，均值 95.1%，与 π0 已发表基线 94.2% 接近，Long 套件为 90.6% 对 85.2%；这不能单独证明完全可观测任务上的记忆增益。

附录的跨 episode 探索很关键：保持锚点仍每 episode 重置，只把联想状态跨 rollout 携带，五任务均值从 50.0% 降至 36.8%，其中 4/5 任务退化。A100 80GB、每策略 200 episodes 的模型侧统计中，NativeMEM 1593.7 ms/周期，MemBodied 129.2 ms，作者报告延迟低 91.9%；两者峰值显存 20.57/18.61 GiB。

## 综述可借鉴之处

这是区分“历史条件控制”和“持久学习”的好反例：任务内状态确实改变了正确分支决策，但未经训练的跨 episode 留存会污染后续任务。可放入记忆章节，并要求所有记忆型 Physical RSI 工作报告清空边界、跨实例迁移和负迁移。

## 证据边界

策略权重在部署时不更新，联想状态只为当前 rollout 设计；跨 episode 携带不是训练目标且效果更差。真机每任务仅 20 次、为任务专用策略。它证明 episode 内记忆有用，不证明跨任务持续积累或改进器递归。

## 原文定位

架构见 §3、Figure 1；RMBench/LIBERO/真机结果见 §§4–5、Tables 1–2、Figures 2–3；训练与真机预算见 Appendix B、C 和 Table 5；跨 episode 实验见 Appendix D.4、Table 6；效率见 Appendix B.7。全文 v1 的方法及上述表图已核查，未复现。

标签：联想记忆 / episode内 / 状态重置 / VLA / 真机 / 边界案例。

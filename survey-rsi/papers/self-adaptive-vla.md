[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Self-Adaptive VLA for Robust Robot Deployment

> **一句话：** 把前几次失败 rollout 压成 context token 并逐次相加，可在最多 6 次尝试内补偿硬件偏移；它是有明确重置边界的测试时上下文适应，不是部署期参数自更新。

短名：Self-Adaptive VLA　作者：Hongxin Zhang、Chunru Lin、Tsun-Hsuan Wang、Zhenjia Xu、Chuang Gan　首次发表：2026-09-24　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.30092](https://arxiv.org/abs/2609.30092)　项目链接：[作者项目页](https://icefoxzhx.github.io/self-adaptive-vla)　最后核查日期：2026-09-26

![Self-Adaptive VLA 原文 Figure 2](https://arxiv.org/html/2609.30092v1/method_v7.svg)

*图注：原文 Figure 2（v1）。训练时用已知注入偏移构造 context-conditioned expert data；测试时把多次 rollout 的 context token 求和，通过 AdaLN 调制基础策略。*

## 解决什么问题

制造误差、磨损和校准偏差会使 VLA 在新工作站反复以同样方式失败。重新采集专家数据或现场标定成本高；纯 memoryless 策略又无法利用前几次失败判断硬件偏移。

## 核心方法

作者在训练侧注入执行器 bias 或关节编码器 offset，让冻结基础策略产生次优 context rollout；再按已知偏移预补偿原专家动作，构造“失败上下文—正确补偿动作”配对。轻量 context encoder 把图像、本体状态和动作历史压缩成一个 token，通过 DiT 的 AdaLN 调制基础 VLA。测试时每次 rollout 单独编码，多次 token 直接求和，使策略逐次校正；生成 token 后不增加每步推理开销。

## 主要结果

四项 10–15 秒精细任务使用 Piper/Piper-X 双臂或 Marvin 双臂＋20-DoF Wuji Hand。每任务、每偏移类型评测 20 个独立未标定环境，每个环境最多 6 次尝试，尝试间完全复位。基础策略名义平均成功率 88.8%；执行器偏移下为 7.5%，单次上下文为 45.0%，最多 6 次 token ensemble 为 72.5%，按作者定义恢复名义性能的 80%；关节编码器偏移下分别为 5.0%、46.3%、75.0%，恢复 84%。

Transport Corn 在两类偏移下可恢复到 100%；Insert Tube 的名义值仅 75%，单次适应 20–25%，多次 ensemble 50%。Gated Memory Policy 在表中平均为 30.0%/41.3%，低于多次 ensemble 的 72.5%/75.0%。

## 综述可借鉴之处

这篇是划分“同实例多次尝试”和“持久学习”的好边界：策略确实使用自己的失败经验，性能也随尝试改善，但更新载体只是当前部署实例的上下文 token。它可与 Zeva-Ego、MemBodied 讨论 context 的重置协议，也能与参数型在线 RL 对照。

## 证据边界

post-training 依赖人为注入且已知的偏移以及原始专家数据；测试偏移来自预设分布。论文没有在现场修改模型权重，也没有证明 token 跨环境、跨任务或跨会话保留；每个 20-episode 设置中，最多 6 次尝试合并为一次 episode 成功，不能与单次成功率直接比较。属于任务/部署实例内适应，不是严格 RSI。

## 原文定位

全文方法与结果已读，未复现。数据构造与 encoder 见 §IV、Figures 2–3；任务、20 个环境和六次尝试协议见 §V-A；主结果 Table I、Figures 5–6；新工作站与消融见 Figures 7–9。

标签：上下文 token / 自身失败 rollout / 同部署实例最多六次 / 不更新权重 / 自动适应 / 多类真机 / episode 成功 / 边界案例。

# LEMCA: LLM-Guided Synthesis of Efficient Mode-Switching Control Architectures

作者：Arjun Krishna；Vincent Pacelli；Dinesh Jayaraman　|　arXiv v1：2026/09/18；作者页标注CoRL 2026

[论文](https://arxiv.org/abs/2609.21319) · [采用版本 v1 全文](https://arxiv.org/html/2609.21319v1) · [PDF](https://arxiv.org/pdf/2609.21319v1) · [作者项目页](https://lemca-robotics.github.io/) · [OpenReview入口](https://openreview.net/forum?id=802PZFmFGd)

**收录：**2026-09-22　**类别：**核心改进器 / 代码演化 / 控制架构 / 仿真　**阅读状态：**方法及指定实验/表格已核查；未复现。

![Figure 2：LEMCA系统图](https://arxiv.org/html/2609.21319v1/theme.svg)

*原文Figure 2：LLM在演化搜索中编辑模式、感知/计算配置和转移程序，控制器综合与评测结果回流到下一代。[原图](https://arxiv.org/html/2609.21319v1/theme.svg)，版权归原作者。*

**解决什么问题：**机器人的困难阶段需要高分辨率感知和大计算量，简单阶段却可能浪费资源；人工设计随状态切换资源的控制器代价高。LEMCA自动搜索“保持性能约束时资源最省”的控制架构。

**核心方法：**把模式切换控制器写成有限状态机程序：每种模式包含感知/计算配置、控制策略和监视器，另有模式转移逻辑。LLM对当前程序生成定向代码diff，验证代码可执行；遗传算法做可行性优先选择，Design Log压缩历代权衡。每个候选通过MSC-PPO或MPPI综合控制器，再以任务回报、资源成本和模式占用反馈下一代。

**主要结果：**覆盖point-to-disk、3个RF-DMC任务和clutter-nav。相对合适的单体控制器，绝大多数设置资源成本至少降低20%；clutter-nav报告约10倍成本降低。性能—资源误差带基于1000次rollout。手工模板上的BayesOpt可有小幅收益，但约需100次评估；消融显示GA框架关键，而Design Log的增益并不稳定。

**综述可借鉴之处：**这是“更新对象”不再只是权重或奖励，而是具身控制系统架构程序的明确例子。综述可以把它放在代码/架构演化分区，并用其约束优化、可执行验证、档案/日志和资源—性能Pareto前沿说明一个较完整的改进器闭环。

**证据边界：**全部在仿真或快速控制基准，尚无硬件部署。任务、传感器库、成本函数和性能阈值由人预先给出；RF-DMC每个设计评估约0.5 L40 GPU小时，候选需完整训练。它演化控制架构，但LLM/选择规则本身没有递归增强，不能据此声称改进器越改越强。

**原文定位：**§2–3；Figures 2、4–6；Appendix A/E。作者项目页提供任务说明、设计与视频。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-22.md)

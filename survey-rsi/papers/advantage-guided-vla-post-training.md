[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Dissecting Advantage-Guided Post-Training for Vision-Language-Action Policies

> **一句话：** 把优势估计、校准和加权分开验证，给离线 VLA 改进提供强基线。

**首次公开：** 2026-09-23　**采用版本：** arXiv v1　**核查日期：** 2026-09-24　**状态：** 预印本；方法及指定实验已核查，未复现。

**作者：** Cao, Jiahang；Zhao, Hanye；Lai, Hang；Zhang, Shenyu；Han, Xiaoshen；Li, Xinghang；Liu, Futeng；Peng, Wanli；Wang, Heyun；Wang, Yunhong；Li, Jason；Yu, Yong；Zhang, Weinan

[摘要与版本](https://arxiv.org/abs/2609.28161) · [全文 v1](https://arxiv.org/html/2609.28161v1) · [PDF](https://arxiv.org/pdf/2609.28161v1) · [作者项目](https://dissectvla.github.io/)

**综述定位：** 边界案例 / 离线后训练 / 优势估计 / 真机

![Advantage-guided VLA audit 原文图](https://arxiv.org/html/2609.28161v1/teaser-p6.svg)

*原文 v1 Figure 2：优势构造、分组校准、样本利用三个设计阶段；将离线诊断与真机后训练串联。 [原图](https://arxiv.org/html/2609.28161v1/teaser-p6.svg)，版权归原作者。*

## 解决什么问题

 VLA 后训练常把价值函数、优势归一化和数据筛选绑在一起，很难判断性能变化究竟来自哪个环节，尤其在数据来源混合、回报稀疏的长程操作中。

## 核心方法

 将流程拆成优势构造、分组校准、样本利用。比较 IQL/SARSA 等价值学习与 Q−V、n-step TD、Monte Carlo 优势；再比较全局归一化、数据源与状态价值分箱；最后在相同部署数据上比较连续加权、硬筛选和 DAgger 式全数据模仿。价值估计训练 10000 步、策略训练 4000 步，batch 均为 2048。

## 主要结果

 π0.5 在四项双臂真实操作任务上评测；每任务数据约为 40 小时专家示范、100 个自主 episode、100 个人工接管 episode。每设置每任务 **20 次**真实执行。连续加权的平均进展分/成功率为 **0.86/0.74**，基础 SFT 为 0.44/0.11，DAgger 为 0.71/0.45，硬筛选为 0.75/0.50；成功率相对 SFT 提高 **63 个百分点**。四任务加权成功率为 0.80、0.70、0.80、0.65，不与进展分混算。

## 综述可借鉴之处

 为“用部署经验改进 VLA”的综述章节提供拆解表和必要基线。可以说明反馈质量之外，优势怎么构造、跨数据源怎么校准、保留全部样本还是硬筛选，同样决定更新成效。

## 证据边界

 本文是固定离线数据上的后训练与诊断，不能说成多轮自主部署学习。阶段标注使用模型辅助流程，并非独立无误的真实奖励；四任务各 20 次的结论也不宜外推所有 VLA。作者未将 RECAP 作为直接对照，理由涉及其预训练优势条件；本文 Filter 不是完整 RECAP，不能由此下“优于 RECAP”的结论。

## 原文定位

 §§III–V，Figure 2、Figures 3–5；Tables I–II。 已核对原文方法、指定结果和样本口径；未复现代码。

**标签轴：** 更新对象：离线价值估计与 VLA 权重；反馈：自主/人工接管轨迹＋过程标注；保留范围：固定部署数据上的一批后训练；物理证据：四项双臂真机任务。

[证据对照](../evidence-map.md) · [综述提纲](../survey-outline.md) · [本轮记录](../daily/2026-09-24-follow-up.md)

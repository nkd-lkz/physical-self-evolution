[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# From Rollout to Reset: A Graph-Based Harness for Autonomous Long-Horizon Manipulation Evaluation

作者：Jiang, Jing；Yang, Yue；Jiang, Xinkai；Bertasius, Gedas；Szafir, Daniel J.；Lioutikov, Rudolf　|　arXiv所列日期：2026/09/16（采用版本见下方链接）

[论文](https://arxiv.org/abs/2609.19413) · [采用版本 v1 全文](https://arxiv.org/html/2609.19413v1) · [PDF](https://arxiv.org/pdf/2609.19413v1)

**收录：**2026-09-21　**类别：**闭环基础设施 / 自动复位 / 自主评价 / 真机　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 2：评分、规划复位与复位验证](https://arxiv.org/html/2609.19413v1/figures/framework_v4.png)

*原文Figure 2：评分、规划复位与复位验证。[原图](https://arxiv.org/html/2609.19413v1/figures/framework_v4.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

## 解决什么问题

长程任务可能在许多状态结束，如何避免每次评测都让人复位？

## 核心方法

把多视角RGB-D观测转换为场景图历史，LLM读取图来打分、组合已学习的原子复位技能，并检查复位是否真正完成。

## 主要结果

四项真机任务、共100个episode中，复位成功率76%，AutoEval为52%，运动规划复位为65%；评分准确率90%，复位验证准确率91%。操作员时间从手动88分钟降到24分钟，但平均循环时间由53秒增至121秒。

## 综述可借鉴之处

可放在物理RSI的运行成本章节：任务学习之外，复位、验收和人工介入决定能否长期采数据。人工工时和总循环时间需要分别报告。

## 证据边界

这是评价/复位自动化，没有报告机器人策略持续学习。仍需技能示范及每任务参考案例；Pot-Cook上复位48%，低于运动规划72%，平均优势并非任务通吃。

## 原文定位

§III–IV、Tables I–III、Conclusion。原文声明Figure 1–2含AI辅助绘制并经作者审核。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)


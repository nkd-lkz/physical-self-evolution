[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# No Free Checker: A Survey of Verifiers for Robot Policies

作者：Wan, Yang；Yue, Xihang；Liu, Zhirui；Chu, Ziyuan；Wang, Shuxun；Chen, Yuhan；Jiang, Xiaonan；Zhu, Xukun；Dong, Yubo；Zhu, Linchao　|　arXiv所列日期：2026/09/08（采用版本见下方链接）

[论文](https://arxiv.org/abs/2609.09250) · [采用版本 v1 全文](https://arxiv.org/html/2609.09250v1) · [PDF](https://arxiv.org/pdf/2609.09250v1)

**收录：**2026-09-21　**类别：**重点综述 / 验证器 / 奖励可靠性 / 参考文献入口　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 4：学习型验证器在评价、推理和策略更新中的作用](https://arxiv.org/html/2609.09250v1/scorers.png)

*原文Figure 4：学习型验证器在评价、推理和策略更新中的作用。[原图](https://arxiv.org/html/2609.09250v1/scorers.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

## 解决什么问题

评价或训练机器人时，什么样的验证器既便宜可用，又能真正反映任务表现？

## 核心方法

梳理约150项相关工作，按人类、规则/形式化、学习/预训练模型、模型内部信号划分判据来源，交叉讨论判据成本、时机、查询频率与可信度。

## 主要结果

提供验证器地图及Table 7的九项报告指标，包括独立rollout数、分类型误差、人类一致性、校准、跨形态转移，以及优化后误差和搜索诱发的假阳性。它是综述，没有新机器人策略增益实验。

## 综述可借鉴之处

应优先用于RSI的“谁判断改进有效”章节，并沿其参考文献继续补查验证器。区分与人工标签一致、能训练出好策略、抗奖励投机三种证据。

## 证据边界

“可用性与可信度权衡”是作者的综述观点，不能当作严格定理。Figure 1说明检索截止2026年7月初，不能因为9月上传就声称覆盖9月前沿。

## 原文定位

Introduction、§2–6、Tables 1、3、7；Figure 1图注的截止日期。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)


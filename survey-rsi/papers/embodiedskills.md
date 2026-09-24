[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# EmbodiedSkills: A Unified Framework for Orchestrating, Training, and Deploying VLA Agents

作者：Wang, Wei；Zhang, Wenqiao；Lin, Yutong；Yuan, Yuqian；Lin, Tianwei；Mao, Jinhao；Fan, Zhenxuan；Gao, Mingjian；Dai, Yang；Li, Wentong；Lv, Zheqi；Dong, Zheng；Niu, Yingjie；Zhu, Jiaqi；Xiao, Jun；Li, Chao；Zhuang, Yueting　|　arXiv所列日期：2026/09/01（采用版本见下方链接）

[论文](https://arxiv.org/abs/2609.01281) · [采用版本 v1 全文](https://arxiv.org/html/2609.01281v1) · [PDF](https://arxiv.org/pdf/2609.01281v1)

**收录：**2026-09-21　**类别：**边界案例 / 技能契约 / 验证与恢复 / 仿真　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 2：高层子目标与低层有界执行和验证](https://arxiv.org/html/2609.01281v1/model.png)

*原文Figure 2：高层子目标与低层有界执行和验证。[原图](https://arxiv.org/html/2609.01281v1/model.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

## 解决什么问题

如何保证高层提出的技能在当前状态可执行，并在执行后检查是否真正完成？

## 核心方法

统一技能接口将高层选择、前置条件验证、有界VLA动作、后验检查和恢复相连，结构化轨迹支持组件训练；运行框架与低层模型解耦。

## 主要结果

任务适应后的低层策略在50项RoboTwin任务平均86.20%，LIBERO四套97.40%；四项记忆任务仅12.5%。Table 5另报告移除验证等消融，应与低层性能表区分理解。

## 综述可借鉴之处

可借鉴“提议不等于执行许可”的技能契约和可审计轨迹设计，为RSI候选更新的验收接口提供工程思路。

## 证据边界

在线适应是可选能力描述，主分数不能证明自主自我进化。正文对Table 2参照模型出现与表列名称不一致的LingBot-VA描述，正式横向比较前需核对作者版本。

## 原文定位

§3、实验章节、Tables 2–5及摘要。不是已有EmbodiSkill的同名写法，按完整题名与arXiv ID单独保留。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)


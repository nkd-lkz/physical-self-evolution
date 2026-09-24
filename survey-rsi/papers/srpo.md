[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models

作者：Fei, Senyu；Wang, Siyin；Ji, Li；Li, Ao；Zhang, Shiduo；Liu, Liming；Hou, Jinlong；Gong, Jingjing；Zhao, Xianzhong；Qiu, Xipeng　|　arXiv所列日期：2025/11/19（采用版本见下方链接）

[论文](https://arxiv.org/abs/2511.15605) · [采用版本 v2 全文](https://arxiv.org/html/2511.15605v2) · [PDF](https://arxiv.org/pdf/2511.15605v2)

**收录：**2026-09-21　**类别：**核心策略改进 / 自参考奖励 / VLA-RL / 旧文补漏　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 2：成功参考、潜在世界表示和策略优化](https://arxiv.org/html/2511.15605v2/main3.png)

*原文Figure 2：成功参考、潜在世界表示和策略优化。[原图](https://arxiv.org/html/2511.15605v2/main3.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

## 解决什么问题

仅有成功/失败的稀疏奖励时，怎样利用失败轨迹中的部分进展？

## 核心方法

用当前rollout批次的成功轨迹作为参考，在冻结V-JEPA 2表示空间中计算失败轨迹接近成功轨迹的程度，形成过程奖励，再进行带KL约束的策略优化。

## 主要结果

LIBERO四套任务平均成功率：one-shot SFT为48.9%，离线SRPO为92.5%，在线SRPO为99.2%。后者比起点增加50.3个百分点。真机另用X-ARM 7的五项任务进行离线RL实验。

## 综述可借鉴之处

补齐“自身成功经验→过程反馈→新策略”的主线，可衔接IRR、RoboReward和世界模型奖励。参考池随rollout更新，是与固定奖励模型有别的设计。

## 证据边界

仍需终点成功信号识别参考轨迹；one-shot SFT和世界模型预训练有外部数据。真机实验是离线RL，不能写成真机自主在线进化；固定改进规则不构成强递归证据。

## 原文定位

§3–5、Table 1、Appendix F.2与G.1。属于2025年文献补漏，不是9月21日新发表。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)


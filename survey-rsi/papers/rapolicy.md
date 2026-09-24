[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Stable and Efficient Real-World Online VLA Post-Training via Asynchronous Replay-Anchored Policy Improvement

短名：RAPolicy　作者：Jiarui Yang, Jiajin Zhang, Bin Zhu, Jingjing Chen, Yu-Gang Jiang　首次发表：2026-09-19　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.22888](https://arxiv.org/abs/2609.22888)　项目链接：[作者项目页](https://flyfaerss.github.io/RAPolicy/)（arXiv列出；2026-09-23直开失败）　最后核查日期：2026-09-23

![RAPolicy框架图](https://arxiv.org/html/2609.22888v1/framework.png)

*图注：异步真实机器人rollout、replay-anchored chunk critic与单步flow actor的闭环；原始来源为论文Figure 2，arXiv v1。*

## 解决什么问题

 在线强化学习后训练VLA时，机器人采集慢、学习端易空等，且flow动作分布难以直接做稳定的off-policy更新。论文希望在真实机器人交互预算内持续提高既有VLA策略。

## 核心方法

 rollout与学习异步并行。critic对记录下来的行为动作块做IQL式in-sample目标，不用当前actor预测下一动作；actor重用数据中的高斯latent，以critic优势加权的似然更新单步flow策略。每组数据做20次critic和5次actor更新，critic先预热2560步。更新会写回策略参数，属于任务部署期的持久策略改进；采集过程允许人类接管。

## 主要结果

 在Franka Research 3、腕部与第三视角RGB、π0.5初始化上评估。四个单任务各用10条示范、无离线buffer初始化、在线训练约1–2小时；最终各20次评测的成功率为100%、95%、70%、80%，初始分别为5%、15%、0%、10%。五任务联合实验用每任务30条示范（150条），120分钟内从52%（26/50）升到88%（44/50），高于同协议HG-DAgger的70%；每任务10次最终评测。远端训练使用8张RTX 3090，其中1张服务rollout、7张训练；稀疏奖励为成功时10。

## 综述可借鉴之处

 这是“部署经验→参数更新→再次部署”的直接真机证据，可放在自我改进策略/VLA-RL主线。其异步采集、行为锚定critic和latent复用也说明Physical RSI需要同时设计数据管线与可稳定更新的策略接口。

## 证据边界

 任务和场景仍较专用，未测未知任务迁移、跨任务遗忘或改进器本身的递归增强；依赖人工接管。最终评测样本较小，部分强基线只在个别任务出现，多任务实验没有覆盖全部RL基线，因此不能把相对优势外推为通用结论。

## 原文定位

 arXiv v1 §III-A–D、§IV-A–D，Figures 2/4/5，Tables I/II。方法、实验预算和指定表图已读；未复现。

标签：策略参数 / 真实交互与人工接管 / 跨rollout持久更新 / 人在环 / 真机 / 稀疏成功奖励 / 核心自我改进。


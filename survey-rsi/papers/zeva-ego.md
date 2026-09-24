[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Zeva-Ego: Egocentric Mid-Training with In-Context Causal Learning for Robot Manipulation

短名：Zeva-Ego　作者：Bingjia Huang, Xin Ding, Fu Chen, Kun Li, Wei Sun, Hao Wu, Yunxin Liu, Ting Cao　首次发表：2026-09-21　采用版本：arXiv v2（2026-09-22）　发表状态：预印本

论文链接：https://arxiv.org/abs/2609.24411　项目：https://air-embodied-brain.github.io/Zeva-Ego　最后核查日期：2026-09-24

![Zeva-Ego总览](https://arxiv.org/html/2609.24411v2/zeva_ego_teaser.png)

*图注：Figure 1，egocentric mid-training、因果转移上下文和跨尝试记忆的整体流程；来源为arXiv v2。*

## 解决什么问题

 大规模第一视角视频缺少机器人动作标签，而冻结VLA在新任务部署中又难以从连续尝试的成败经验快速调整。论文同时研究如何把人类视频转成动作监督，以及如何在不更新参数时利用尝试历史。

## 核心方法

 Action-Centric Encoder（ACE）把第一视角视频的状态转移转换为动作监督，用于VLA中期训练。In-Context Causal Learning中的Causal Transition Encoder编码状态、动作与反馈；BIT在单次尝试内使用转移上下文，PIM按阶段匹配保留同一任务实例的先前尝试。上下文只注入action expert，基础参数在测试时冻结。

## 主要结果

 使用1万小时第一视角视频后，RoboTwin2.0平均成功率由63.8升至75.3，接近使用2000小时机器人示范的74.7，作者据此给出约4–5:1的经验换算观察。跨尝试实验从第1次58%升至第4次89%，过程中不更新参数。整体评测还覆盖RoboTwin2.0 50任务、LIBERO-PRO分布变化和ChemLab-Evo真机；真机三项原子任务各20个随机episode，Zeva-Ego平均85%，Zeva为83.3%，π0.5为73.3%。整体成绩同时受离线中训影响，不能全部归因于ICCL。

## 综述可借鉴之处

 是区分“任务内/同实例记忆”和“持久自我改进”的好案例，也给人类视频作为物理经验代理提供量化入口。建议在综述中将参数更新、上下文状态、保留跨度和清空条件分列，避免把四次尝试内上升直接称为持续RSI。

## 证据边界

 PIM跨的是同一任务实例的尝试，不清楚是否跨会话、任务或部署永久保存；没有参数更新，也没有改进器增强。真机只有三项原子任务，每项20次；58→89的跨尝试曲线不等同于大范围任务能力增长。

## 原文定位

 Figure 1；§§3–5；Tables 1–3；Appendix A.2–A.3；采用v2。项目页已打开，方法和指定实验已读，未复现。

标签：上下文状态 / 执行反馈 / 同任务跨尝试 / 自动推理 / 真机+仿真 / 作者自评 / 边界案例。


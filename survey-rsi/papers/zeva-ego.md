[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Zeva-Ego: Egocentric Mid-Training with In-Context Causal Learning for Robot Manipulation

短名：Zeva-Ego　作者：Bingjia Huang, Xin Ding, Fu Chen, Kun Li, Wei Sun, Hao Wu, Yunxin Liu, Ting Cao　首次发表：2026-09-21　采用版本：arXiv v2（2026-09-22）　发表状态：预印本

论文链接：https://arxiv.org/abs/2609.24411　项目：https://air-embodied-brain.github.io/Zeva-Ego　最后核查日期：2026-09-24

![Zeva-Ego总览](https://arxiv.org/html/2609.24411v2/zeva_ego_teaser.png)

*图注：Figure 1，egocentric mid-training、因果转移上下文和跨尝试记忆的整体流程；来源为arXiv v2。*

## 解决什么问题

 大规模第一视角视频缺少机器人动作标签，而冻结VLA在新任务部署中又难以从连续尝试的成败经验快速调整。论文同时研究如何把人类视频转成动作监督，以及如何在不更新参数时利用尝试历史。

## 核心方法

 Action-Centric Encoder（ACE）通过教师表征与视觉编码的两阶段对齐，把第一视角视频用于动作中期训练。In-Context Causal Learning 中的 Causal Transition Encoder 编码状态、执行动作与反馈；BIT 在一次尝试内使用转移，PIM 按阶段匹配同实例先前尝试。上下文只注入 action expert，部署参数冻结，但这一接口经过离线训练，并非任意冻结策略都可直接插入记忆。附录 A.3 的 effect 辅助目标采用视觉特征差分，不等同于直接监督测得接触力或物体动力学。

## 主要结果

 作者的数据规模对照中，1万小时 ego 视频对应 RoboTwin2.0 成功率 63.8→75.3，2000小时机器人数据为74.7；其4–5:1观察仅限该设置，不是通用数据兑换率。跨尝试报告第1次58%、第4次89%，不是四次累计“曾成功”率。真机三项原子任务每项20个随机 episode，整体均值85%，Zeva 83.3%、π0.5 73.3%；该整体差异不能全部归于 ICCL。中训和跨尝试实验的条件不同，不拼成同一改进曲线。

## 综述可借鉴之处

 是区分“任务内/同实例记忆”和“持久自我改进”的好案例，也给人类视频作为物理经验代理提供量化入口。建议在综述中将参数更新、上下文状态、保留跨度和清空条件分列，避免把四次尝试内上升直接称为持续RSI。

## 证据边界

 **v2 §4.3.2 明确：BIT 在新尝试清空，PIM 在新任务实例开始时清空。** 因而本版本并未展示跨独立实例永久累积的经验库；此前本卡的“不清楚是否清空”修订为明确的实例边界。§5.1.2 的跨尝试协议为每实例4次、各次恢复同一初态；不能当成独立新任务学习。

 **数字归属需保留歧义：**§5.4.1/Fig.11 将58→89曲线放在 RoboTwin 语境，§6结论却使用 real-world 措辞；本次不擅自统一为真机结果，待作者澄清/原始数据。方法无部署参数更新，也未证明改进器增强。记忆辅助头与动作接口经过离线训练，比较时需分离训练配方和检索本身的贡献。

## 对当前 RLT 研究的影响

这是“后果监督 + 记忆注入”的直接近邻。候选差异应落在 **视觉差分 vs 实测物理响应**、**同实例重试 vs 新实例/条件复用**及相同交互预算下的小型 learner 收益，不能只把模块改名为 Physical Token。见[四条线索对比](../discussions/physical-rsi-sept24.md)和[可执行实验](../experiments/rlt-contact-memory/README.md)。这些是本库提案，不是该论文的实验结论。

## 原文定位

 [arXiv v2 全文](https://arxiv.org/html/2609.24411v2)：Figure 1；§4.3.2（PIM清空）；§5.1.2（重试协议）；§5.4.1/Fig.11 与 §6（数字归属）；Tables 1–3；Appendix A.2–A.3（effect监督）。项目页已打开，方法和指定实验已读，未复现。2026-09-24同日追加勘误，不计新增论文。

标签：上下文状态 / 执行反馈 / 同任务跨尝试 / 自动推理 / 真机+仿真 / 作者自评 / 边界案例。

[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Learning from Mixed-Quality Deployment Experience for Robot Manipulation

> **一句话：** PACL 用预测式 action-chunk critic 给成功、部分进展和失败 rollout 分级，再训练条件扩散策略并在推理时筛选动作块，使固定部署数据变成可留存策略改进。

短名：PACL　作者：Yangang Ren、Yujie Yan、Zirui Li、Jiaming Guo、Di Zeng、Ji Tao、Lan Yu、Xuesong Tian、Chen Lv　首次发表：2026-09-24　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.29000](https://arxiv.org/abs/2609.29000)　最后核查日期：2026-09-26

![PACL 原文 Figure 1](https://arxiv.org/html/2609.29000v1/framework.png)

*图注：原文 Figure 1（v1）。chunk-level critic 用 TD 与未来潜变量预测学习质量；离散 Q 条件指导扩散 actor，部署时从多个动作块中选最高值者。*

## 解决什么问题

机器人部署后会自然积累成功、局部进展与失败轨迹。把它们一律当示范会复制坏动作；稀疏奖励和有限覆盖又让常规 offline RL 的值估计不稳定。论文限定一个实用场景：只使用自然产生的 rollout，不增加人工纠正或专门探索。

## 核心方法

PACL 从人类示范训练的 Diffusion Policy 出发。预测式 action-chunk critic 一方面做时序差分学习，另一方面预测未来视觉潜变量，以长时程表征补充稀疏奖励；估计的 chunk Q 被离散成质量条件，扩散 actor 因而可同时学习不同质量经验而不把它们等价处理。推理时生成多个候选 action chunk，由同一 critic 排序选择。

## 主要结果

作者在 Robomimic 的 Can、Transport、Square、ToolHang 和三项 Franka 真机任务 PickCup、StackCup、MoveSpoon 上评测；仿真每任务 250 次 rollout，真机每任务 25 次。统一从同一 Diffusion Policy 热启动。基线 DP 的七项成功率为 88/84/78.8/46.4/84/72/64，PACL 为 98.4/96/93.2/82.8/100/100/84；强基线 SSDF 为 98.4/92/88.4/81.2/100/96/80。

数据预算表显示基础策略使用 200 条轨迹；PACL 小/中/全量变体总计 350/500/700 条并后训练 50 epochs。Square 与 Transport 的 full 结果为 93.2%/96%。候选数消融并非单调：Transport 上 N=4/8/12/16 时为 89.2/83.2/86.8/80.4，说明 critic 选择和额外推理预算不能简单等价为性能提升。

## 综述可借鉴之处

PACL 是“混合质量自主部署经验怎样进入参数”的清晰案例，可与 BEE 的人工接管、HiRE 的成败支持集和 advantage-guided 后训练比较。综述应把经验来源、质量建模、更新时机和推理时筛选成本拆成不同列。

## 证据边界

这是固定数据上的离线/批次式 post-deployment learning，不是机器人边执行边持续更新；真机每任务仅 25 次评测。PACL 同时增加数据、critic、Q 条件 actor 和候选筛选，不能只凭总表把收益全部归因于未来潜变量预测。没有跨轮旧能力保持或改进器自身演化。

## 原文定位

全文方法与指定实验已读，未复现。框架见 §III、Figure 1；协议与主结果见 §IV、Table I；critic 与候选数消融见 Table II、Figures 3–5；数据预算见 Table III；限制见 §V 与附录。

标签：策略与 critic / 自主混合质量 rollout / 固定部署批次 / 参数留存 / 无新增人工纠正 / 仿真＋Franka 真机 / 环境成功 / 核心持久改进。

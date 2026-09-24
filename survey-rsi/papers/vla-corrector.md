[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies

短名：VLA-Corrector　作者：Chang Song, Bin Qian, Yan Feng, Zhijie Song　首次发表：2026-09-06　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.06508](https://arxiv.org/abs/2609.06508)　项目/代码：未核实到公开入口　最后核查日期：2026-09-23

![VLA-Corrector框架图](https://arxiv.org/html/2609.06508v1/VLA.drawio.png)

*图注：可观测验证器检测异常、触发stage prompt，再调用同一冻结VLA恢复；原始来源为论文Figure 1，arXiv v1。*

## 解决什么问题

 冻结VLA在长程任务中会把局部偏差累积成失败，而依赖特权状态的监控器难以部署。论文尝试只用实际可观测信号判断阶段和异常并发起恢复。

## 核心方法

 对连续8步的双目RGB、8维proprioception和7维已执行动作编码，GRU输出可观测验证结果；训练标签由离线特权规则教师给出。触发门控后，系统注入人工定义的阶段prompt，由同一冻结OpenPI π0.5策略继续执行。验证器训练使用120个episode的60/20/20划分，在CPU上30个epoch。

## 主要结果

 仿真每个条件1000个episode，LIBERO标准任务平均成功率从70.9%升至80.2%，特权版本为82.6%。真机三任务、每任务40次，刻意施加目标位移后总体成功率82.5%→88.3%，且没有用真机数据训练验证器。

## 综述可借鉴之处

 可放在失败检测—恢复—学习链条中，说明一个部署可见的验证器能提高任务韧性，也给“特权教师离线蒸馏、可观测监控在线运行”提供具体设计。

## 证据边界

 基础策略与验证器部署期参数不更新，提升来自任务内提示恢复，不会跨episode积累，因此属于ICL/闭环恢复边界案例而非持久RSI。阶段与prompt有人为定义，真机扰动也是刻意施加；没有证明长期未知故障覆盖。

## 原文定位

 arXiv v1 Problem/Method/Experimental/Results各节，Figure 1，Tables 1–3。方法、训练规模、仿真与真机统计已读；未复现。

标签：验证器与提示 / 可观测轨迹、特权教师 / 任务内恢复 / 固定策略 / 仿真与真机 / 边界案例。


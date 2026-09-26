[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# RoboRecover: Benchmarking Robot Policy Recovery under Execution Deviations

> **一句话：** RoboRecover 用 2,000 个执行偏差后的中间状态证明：初始状态成功率不能代表失败恢复能力，恢复、保持和学习收益必须分别评测。

短名：RoboRecover　作者：Yang Li、Chen Zhao、Zhuoran Wang、Jiankang Wang、Chao Shao、Yihan Lin、Haitao Shen、Jing Zhang　首次发表：2026-09-24　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.28952](https://arxiv.org/abs/2609.28952)　项目/代码：[作者仓库](https://github.com/RUCKBReasoning/RoboRecover)　最后核查日期：2026-09-26

![RoboRecover 原文 Figure 2](https://arxiv.org/html/2609.28952v1/bench.png)

*图注：原文 Figure 2（v1）。RoboTwin 与 LIBERO 各 1,000 个 scenario，按平台、任务、偏差来源、训练/测试划分和 source policy 展示覆盖。*

## 解决什么问题

大多数机器人 benchmark 从预设初态跑完整轨迹，只看最终成功。实际执行会因接触和错误动作进入偏离分布的中间状态；策略需要理解任务进度、修复对象关系并继续原目标。这个能力不能从常规初态成功率推断。

## 核心方法

RoboRecover 从真实策略轨迹中定位 deviation state，用动作前缀重放重建中间状态，然后在原任务目标下评测恢复。RoboTwin 与 LIBERO 各含 800 train / 200 test scenario；来源包括自然失败、动作扰动和人工构造。训练集还用于学习失败监测器，并比较直接继续、回滚、监测后回滚和 corrective action 等干预。

## 主要结果

总计 2,000 scenario。RoboTwin 里 LingBot-VA 初态 83.75%、恢复 59.5%；Fast-WAM 为 81%→49.33%。LIBERO 里 π0.5 为 94.17%→64.40%，UniFOLM 98.83%→48.0%，Cosmos 97.83%→52.1%，初态排名与恢复排名明显不同。

在 LIBERO/π0.5 干预表中，直接继续恢复率 64.4%；固定回滚 30 步为 74.0%，监测后回滚 77.0%；固定 corrective action 为 71.2%，监测后纠正 75.5%。监测器用 RoboTwin 720 个训练 deviation、约 32 万帧训练；平衡验证 80 个 deviation/8 千帧上 F1 为 85.36，自然频率验证 80 个 deviation/1.6 万帧上 F1 为 88.97，但假阳性率仍约 13%。

## 综述可借鉴之处

它为 Physical RSI 补充一个独立评价轴：能否从自己造成的异常状态恢复。综述应把“更新前后任务成功”“执行中恢复率”“恢复所需动作/回滚预算”分列；否则单一最终成功率会把恢复组件误写成长期能力增长。

## 证据边界

这是 benchmark 与干预研究，不是自我改进算法；没有真机，也没有跨 episode 参数/记忆留存。scenario 由已有轨迹与模拟重放构造，恢复分布仍受 source policy 和偏差生成方式影响。监测器与恢复器的收益不能直接当作 RSI 证据。

## 原文定位

全文方法和指定结果已读，未复现。任务定义 Figure 1；数据组成 Figure 2、Tables 2–3；策略比较 Table 4、Figures 4–5；干预 Table 1；监测器数据与指标见 §4.4 和附录。

标签：评测与恢复 / 执行偏差 / scenario 级 / 不更新被测策略 / 部分学习监测器 / 纯仿真 / 初态与恢复成功率 / 支撑组件。

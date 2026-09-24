[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# MEMOBench: A Process Level Memory Benchmark for Robotic Manipulation

作者：Haiyang Sun；Haoxiao Wang；Junming Chen；Weicheng Fang；Zihao Su；Jingkun Yi；Wenyou Yi；Hao Chen；Zhou Zhao　|　arXiv v1：2026/09/07

[论文](https://arxiv.org/abs/2609.07047) · [采用版本 v1 全文](https://arxiv.org/html/2609.07047v1) · [PDF](https://arxiv.org/pdf/2609.07047v1) · [代码与数据入口](https://github.com/Collab-Gen/MEMOBench)

**收录：**2026-09-22　**类别：**评价框架 / 跨时段记忆 / 过程指标 / 仿真 / 旧候选补全　**阅读状态：**方法及指定实验/表格已核查；未复现；公开代码仓库已打开。

![Figure 1：MEMOBench总览](https://arxiv.org/html/2609.07047v1/teaser.png)

*原文Figure 1：历史依赖任务、可执行记忆检查点和过程指标。[原图](https://arxiv.org/html/2609.07047v1/teaser.png)，版权归原作者。*

## 解决什么问题

只看最终任务成功无法判断机器人是忘了信息，还是记对了但感知/控制执行失败。MEMOBench把记忆过程拆成存储、更新和压缩三种操作，并在执行中检查。

## 核心方法

30个历史依赖LIBERO任务、1500条专家示范、84个检查点模板产生4200个实例。每个检查点同时有粗到细语言、模拟器谓词和操作标签；外部状态谓词形成MSR、MUR、MCR三项过程率，并可作为语义、对比或逐帧记忆对齐的训练监督。

## 主要结果

所有模型在30任务上各用50条示范训练、50次留出rollout评估，共1500次评测。最强显式记忆基线平均成功率仅31.9%。以π0.5、replan step 5为例，平均SR/MSR/MUR/MCR为30.4/54.9/13.5/4.2；加入真实记忆文本的oracle对应为51.9/64.0/52.9/56.8，说明更新和压缩是明显瓶颈。对代表性炉灶任务的150次rollout中仅10次成功，失败主要集中在状态更新后仍使用过期记忆。

## 综述可借鉴之处

可直接支撑RSI综述的“保留了什么、何时失效、最终成功是否掩盖内部失败”评测框架。它还提醒持续记忆不能只测写入，应单列过期事实更新与历史压缩，并用oracle分解记忆与执行上限。

## 证据边界

全为仿真；过程指标检查的是外部可执行谓词，不是直接读取模型内部记忆，仍可能受控制失败影响。检查点标签含人工判断，三名盲标者Fleiss κ为0.799。对齐实验只覆盖同一π0.5记忆模块主干，不能推出所有架构都会同样受益；它是诊断/监督基准，不是完整自我改进算法。

## 原文定位

§3–6；Figure 1；Tables 2–4；Limitations。仓库提供任务配置、检查点注释和评测脚本。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-22.md)


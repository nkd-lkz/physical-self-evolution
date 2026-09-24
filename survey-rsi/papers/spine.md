[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# SPINE: Bridging Cyber-Physical Gap with Agentic AI

短名：SPINE　作者：Minkyu Ham, Dongho Kim, Chan Lee, Min Jun Kim, Yixi Zhang, Jiayi Wang, Han Liu　首次发表：2026-06-29　采用版本：arXiv v2（2026-09-21）　发表状态：预印本

论文链接：https://arxiv.org/abs/2607.13049　项目：https://magics-lab.github.io/SPINE-web　最后核查日期：2026-09-24

![SPINE架构](https://arxiv.org/html/2607.13049v2/figures/spine_architecture.png)

*图注：Figure 2，机器人画像、分层诊断、修复/验证门与事件记忆构成的agentic操作闭环；来源为arXiv v2。*

## 解决什么问题

 通用编码代理不理解具体机器人配置、命令依赖和物理故障，容易把软件问题与硬件问题混淆。论文目标是让代理把系统恢复到可安全遥操作的状态，并减少人工排障时间。

## 核心方法

 SPINE运行于Claude Code。Profile Builder预先编译机器人配置、契约、命令DAG与就绪检查；Debugger执行observe–triage–repair–verify循环，调用四个只读诊断子代理。软件故障由代理修改，物理故障给出一次操作员动作，再通过backend closure gate验证；Incident Memory只保存经验证的修复记录。

## 主要结果

 在DOBOT X-Trainer和AgileX PiPER上植入12个软件、硬件及混合故障场景（7+5）。SPINE主实验每场景3次；人类基线分别7名和9名操作员，通用代理使用同一Claude Sonnet 5.0但不提供SPINE结构/画像。DOBOT故障解决分数0.76→1.00，平均时间14:51→10:20（约-30%）；PiPER为0.99→1.00、12:30→7:48（约-38%）。DOBOT消融中，无画像平均OSS 0.79、无硬件playbook为0.57，但每个消融每场景仅1次，属初步证据。

## 综述可借鉴之处

 可作为“harness与维护闭环”支撑案例，尤其适合讨论验证后写入记忆、软件/物理故障分流和人机权限边界。它提示Physical RSI不仅要改策略，还要先建立可诊断、可恢复、可验证的运行时。

## 证据边界

 物理修复仍由操作员执行；故障是人工植入，实验从预先建立的known-good画像出发。验收终点是“可遥操作就绪”，论文明确不是自主策略执行。Incident Memory虽持久，但本实验没有独立证明其让后续故障处理持续变强；因此是基础设施，不是核心RSI。

## 原文定位

 §§III–VI，Figures 2–3，Tables I–III；采用v2。项目页已打开，方法和指定实验已读，未复现。

标签：运行时与事件记忆 / 诊断反馈 / 跨事件可保存 / 人机协作 / 真机 / 作者自评 / 支撑组件。


[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning

> **一句话：** RACaP 在部署前演化可复用 Policy API、ReAct harness 与经验记忆，再冻结后执行；它把代码改进从任务现场移到受预算约束的 evolution stage。

短名：RACaP　作者：Zexi Li、Yehang Zhang、Haojian Huang、Bohan Zhou、Wenqian Li、Chenxu Wang、Yifan Chang、Yangkai Wei、Tianyi Zhang、Ying-Cong Chen、Kaiwen Zhou、Yinchuan Li、James Cheng　首次发表：2026-09-24　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.29394](https://arxiv.org/abs/2609.29394)　最后核查日期：2026-09-26

![RACaP 原文 Figure 1](https://arxiv.org/html/2609.29394v1/RACaP_Figure1_editable.png)

*图注：原文 Figure 1（v1）。阶段一由能力课程形成配对 rollout；阶段二按失败簇自主选目标，coding agent 修订 API、harness 与经验，champion 验证通过后再发布。*

## 解决什么问题

Code-as-Policy 在任务到来后现场生成和修复程序，延迟高，常把坐标和恢复逻辑写死，过去经验也难迁移。RACaP 试图先演化通用工具与运行结构，部署时只做视觉观测、推理和函数调用。

## 核心方法

演化阶段分两步：固定 capability curriculum 先产生成功/失败配对；随后系统聚类失败、选择薄弱能力、由 coding agent 提议对 typed Policy API、双层 ReAct harness 或长期经验记忆的修改，并用独立 rollout 与 champion 比较后接纳。部署时三类产物全部冻结；Full ReAct 分解任务，Transport ReAct 处理局部搬运，视觉报告闭合执行反馈。

## 主要结果

LIBERO-90 演化阶段二报告单种子 54.4%。在未见的 LIBERO-Pro 六个 split 上，每 split 10 任务×3 种子，共 180 episode：RACaP Phase 2 平均 45.0%，Phase 1 为 32.8%，CaP-X 13.3%，RATS-base 17.8%，RATS-90 8.3%；策略中位墙钟时间约 380 s，而 CaP-X 为 845 s。LIBERO-Long 10 任务×5 种子上 Phase 2 为 46%，Phase 1 为 32%。

阶段二开发使用 32 个 proposal、596 个模拟 episode。60 个配对的一次适应分析由 38.3%→48.3%，但 p=0.146。sealed robosuite 35 episode 中，冻结 RACaP Phase 2 为 17.1%，低于 CaP-X 25.7%；在 robosuite 上继续演化后 RACaP-RS 和 RATS-RS 均为 31.4%，说明迁移仍依赖新的 evolution budget。

## 综述可借鉴之处

RACaP 很适合“演化发生在哪里”的分类：修改对象不只是一段技能代码，而是 API、agent harness 和经验库；部署阶段却完全冻结。它也提供 proposal 数、模拟 episode、API 成本与时延，可用于综述的闭环预算表。

## 证据边界

实验均为 LIBERO/robosuite 仿真；主要 LIBERO-90 结果为单种子。Phase 2 的目标选择虽自动，但更新/验证规则本身固定，未证明改进器越改越强。部署期不继续学习；部分 baseline 数字来自原论文，任务与预算不完全统一。

## 原文定位

全文方法与指定实验已读，未复现。框架 Figure 1、§§3.1–3.4；冻结运行时 Figure 3；主结果 Tables 1–4；开发预算 Table 6；robosuite、一次适应和蒸馏见 §4 与附录。

标签：Policy API＋harness＋经验 / rollout 与视觉 critic / 部署前演化 / 冻结发布 / 自动候选＋champion 验证 / 纯仿真 / 成功率＋成本 / 核心可演化 harness、非递归改进器。

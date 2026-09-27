[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# AdaHVLA: Adaptive Harnesses for Long-Horizon Vision-Language-Action Execution

> **一句话：** AdaHVLA 不改 VLA 权重，而是依据机器人执行证据持续改写代码式协调策略，并用可回溯的 revision graph 保留候选、假设和结果；这是较直接的持久 harness 自我改进证据，但外层改写流程本身固定。

短名：AdaHVLA　作者：Junyi Tang, Jie Peng, Zezhen Ding, Yuan Shen, Tianlong Chen　首次发表：2026-09-24　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.29204](https://arxiv.org/abs/2609.29204)　代码：[Haaareally/AdaHVLA-Adaptive_Harness_VLA](https://github.com/Haaareally/AdaHVLA-Adaptive_Harness_VLA)　最后核查日期：2026-09-27

![AdaHVLA 原文 Figure 2](https://arxiv.org/html/2609.29204v1/overview.png)

*图注：AdaHVLA 的执行与改写闭环。分析、修订和行为评估代理分别处理证据、提出可检验修改并比较亲代/子代；revision graph 跨尝试保留分支。来源：原文 Figure 2，arXiv v1。*

## 解决什么问题

冻结 VLA 在局部控制上可用，却常在长时任务中丢失阶段状态、错误判断完成或恢复失败。固定 harness 能补上协调逻辑，但无法随机器人—执行器组合和新环境持续校正。论文研究的是：能否把执行轨迹变成可检验的代码修订，并在后续任务继续复用。

## 核心方法

系统把 harness 写成代码式 coordination policy。每次 episode 后，分析代理从指令、观察、动作和运行状态中归因失败并形成可证伪假设；修订代理据此修改源码；评估代理在新上下文中对亲代和子代的目标效应、总体行为与最终成功分别打分。候选 harness、证据、假设和观察效应写入 stateful revision graph，失败分支不被删除，后续任务可以回到早期候选继续改写。运行时推理代理、底层控制器和 VLA 参数保持不变。

## 主要结果

- **四足导航：** NaVILA-LH 含 50 个实例，10 个用于适应、40 个留出测试；每个适应模型从同一初始 harness 独立重启 3 次，每次最多评估候选 0–15。Single VLA 测试成功率为 2.5%，初始 harness 为 22.5%；六种适应模型的最终 harness 为 31.7%–57.5%，其中 GPT-5.6-sol Max 为 57.5%。测试结果不参与修订或选择。
- **机械臂操作：** VLA-Arena L1/L2 各 50 个实例，仍为 10/40 适应—测试划分。以 π0.5 为例，L1 从 Single VLA 20.0%、初始 harness 25.0% 提升到 55.8%；L2 从 6.7%、10.0% 提升到 38.3%。SmolVLA 与 OpenVLA-OFT 上也均有提升。
- **口径：** 表中均值来自 3 次运行；相当于 30 个适应或 120 个测试评估，不是独立任务数，也不是全部适应 rollout 预算。真机 Unitree Go2 只给出示例轨迹，没有量化成功率或独立分母。

## 综述可借鉴之处

这篇工作适合放在“技能、代码与 harness 演化”主线，并与只在当前调用中更新上下文的系统分开。它给出一个可操作的发布协议：修订必须绑定行为假设和后续证据，分支历史要可回滚，测试集不能反馈给改写器。综述比较 harness 工作时，应单列**改写对象、候选预算、选择证据、跨任务留存和底层模型是否冻结**。

## 证据边界

主要量化来自 Isaac Lab / Isaac Sim 和 RoboSuite / MuJoCo；真机只是定性轨迹。三次重启共享同一任务划分，不能当 120 个独立任务。代码协调策略和记忆会持久更新，但生成假设、修订、评估与候选选择的外层流程没有被自身修改，因此属于持久 harness 自我改进，而不是已证实的严格递归改进器。不同适应 LLM 的比较也没有隔离模型规模与能力。

## 原文定位

§III-A–E（执行、归因、修订、评估和 revision graph）；§IV-A–D（任务、平台与主结果）；§V-A–B（累计改进与消融）；Figures 2–5；Tables I–II；采用 arXiv v1。全文方法、表格、分母和限制已核查；未复现。

标签：harness代码 / 执行证据 / 跨episode与跨任务 / 多代理改写 / 仿真为主 / 留出测试 / 非递归外层 / 核心自我改进。

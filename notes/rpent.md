# RPent：把经验保存在系统中，如何与策略学习区分？

> 核验日期：2026-09-21；阅读等级：官方 README、Memory、Flash、RoboTwin 与榜单协议专题阅读。未运行代码或独立复现。用户附件是发现入口，下面事实以官方材料为准。

**RPent: Agentic Infrastructure for the Physical World** 是开源具身 Agent 基础设施；其首篇关联论文为已有条目 Harness VLA。此次新增的是系统笔记，不把它重复计作另一篇 Harness VLA 论文。[官方仓库](https://github.com/RLinf/RPent) · [Harness VLA](https://arxiv.org/abs/2607.08448)

## 1. 技术定位

RPent 将规划器、动作技能、环境接口和经验记忆连接起来。一次任务可以混合调用冻结 VLA 与解析工具，并根据观测组织执行。RoboTwin 文档中的动作模型是 LingBot-VLA；因此其成绩不能与本项目 π0.5/RLT 直接相减后解释为 harness 收益。[RoboTwin 官方文档](https://rpent.readthedocs.io/en/latest/rst_source/usage/robotwin.html)

| 组件 | 保存或处理什么 | 与本项目的关系（研究分析） |
|---|---|---|
| Planner | 子任务、工具选择、失败后下一步 | 任务级恢复，不等价于接触动力学表征 |
| VLA / primitive | 可调用的局部操作能力 | 可以承接未来训练完成的策略，但当前不需改基线 |
| Memory / recipe | 经验证的策略、阶段完成条件、历史工具顺序 | 经验写回的非参数形式 |
| 环境接口与反馈 | 当前观测、动作执行、原生成功条件 | 可借鉴日志与评估协议 |

官方 Memory 文档将经验分为 global、suite 与 task_only，并明确：**Evaluation 只读，Exploration 写入；目前 Exploration 仅支持 LIBERO。** 所以“框架面向持续进化”与“已证明 RoboTwin 在线持续学习”必须分开。[Memory 文档](https://rpent.readthedocs.io/en/latest/rst_source/development/memory.html)

## 2. Flash Mode 的实际边界

Flash 将成功轨迹整理成计划，借助当前视觉重新定位语义锚点，再把相对位移映射到当前场景。当前文档说明它用于 LIBERO 评估、不调用 LLM 做规划，不能与 exploration 同开；缺失计划或锚点文件会报错。因此不把附件所述“失败自动回到 Planner”视为已核验能力。[Flash 文档](https://rpent.readthedocs.io/en/latest/rst_source/usage/flash.html)

当前官方完整 800-case LIBERO-PRO 评测报告 Flash 581/800（72.63%）。其计时用每份最终计划对应的一条成功轨迹工具执行时间，而 Codex 用可得的 planner 运行记录；排除模型与服务启动。该统计不是严格同回合端到端计时，不据此外推统一加速倍数。附件中的另一组 200-case 数字没有在本轮锁定同一协议，不录入为当前比较结论。[Flash 评测口径](https://rpent.readthedocs.io/en/latest/rst_source/usage/flash.html)

## 3. RoboTwin 与榜单证据

官方 RoboTwin C2R 记录：GPT-5.5 / xhigh、LingBot-VLA，50 任务 × 5 回合，共 156/250 成功（62.4%），58 失败、36 超时。评测 seed 经专家执行筛选；记忆来自 clean 成功轨迹，迁移到 randomized 场景；当前几何必须重新定位。成功由原生 TASK_ENV.eval_success 判定，而非 planner 自报完成。[复现协议](https://rpent.readthedocs.io/en/latest/rst_source/usage/robotwin.html#reproducing-results)

LIBERO-PRO 的 Astra 741/800（92.63%）合并了 Long 与另外六个 suite 的两个评测批次，各自使用探索后冻结的记忆快照；不是全部 800 回合共享一份记忆，更不是测试时持续更新的学习曲线。[官方榜单与记忆说明](https://rpent.readthedocs.io/en/latest/rst_source/leaderboard/performance.html)

研究含义：同任务 clean→randomized 的策略复用与全新任务探索是不同能力；在文章中应分别定义任务身份、物体变化、初始状态变化和物理参数变化。

## 4. 对“自进化”的可检验拆分

以下为本项目建议，不是 RPent 已完成的实验。

| 维度 | 更新什么 | 最低证据要求 |
|---|---|---|
| 回合内适应 | 当前上下文或短期状态 | 同一回合内利用新反馈纠错，不能单独称跨回合成长 |
| 非参数经验积累 | 可持久化 memory / recipe | 相同冻结模型，积累前后对独立测试集的改善 |
| 参数学习 | actor / critic 或明确定义的 adapter | 等交互预算学习曲线，冻结更新组和旧任务保留 |
| 跨任务积累 | 可复用表示、技能或知识 | 按任务身份隔离；新任务学习更省样本，而非同任务换 seed |

本项目可以先证明参数学习这一层：学习具体接触任务的成功率如何随真实交互预算变化。第二层目标才是用已学经验降低新任务适应成本。持续增长不是必须每轮单调上升，应报告跨种子趋势与置信区间。

## 5. 如何避免 Agent 增益掩盖 Token 增益

先完成 RLT 与 Physical Token 的 policy-only 比较。若后续确实要引入 harness，再设置 2×2：RLT/改进表征 × 无记忆/同版本冻结记忆。固定基础模型、工具集合、任务语言、执行预算、历史长度和允许读取的传感器。

同一批探索数据生成 memory 或训练策略，账本分别记录环境交互量、人工干预、模型调用费用与训练量。评测期间冻结参数与 memory；禁止根据测试失败继续补 recipe 后仍沿用旧测试成绩。若研究目标就是测试时学习，应另设明确 adaptation stream 和不参与更新的 evaluation stream。

可以立即借鉴两项基础设施实践：每次执行记录 before→issued action→executed action→after→原生成功信号；每份经验保存来源任务、seed、版本和验证状态。这是后续可归因实验的准备，不需要先接入完整 planner。

## 6. 与 ForceDelta、RLT 的统一位置

| 工作 | 改善发生在哪里 | 主要反馈 | 对当前路线的用途 |
|---|---|---|---|
| ForceDelta-VLA | 离线学得的快速局部修正 | 实时力/状态；训练用教师预测差 | 强近邻与时序/感知对照 |
| RLT | 小型策略与价值网络在线更新 | 执行经验、任务回报、参考动作 | 当前在线学习 baseline |
| RPent / Harness VLA | 规划、工具调用、可复用经验 | 执行结果与记忆 | 系统层知识库；后续独立评估 |

**候选论文问题仍应聚焦：真实动作后果监督能否使紧凑表示更有利于有限预算在线适应？** RPent 提供的是经验如何进入系统的参照；证明物理表征有效仍需直接的同输入、同容量、同交互预算实验。

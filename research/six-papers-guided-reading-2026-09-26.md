# 六篇论文导读：从“自进化”到 RLT 接触实验

> 2026-09-26。核对公开论文/代码；这是**论文阅读与实验选择**，没有在 RLinf 训练或完成六篇复现。现有独立笔记保留： [Zeva](../notes/zeva.md)、[Harness VLA](../notes/harness-vla.md)、[SHAPER](../notes/shaper.md)、[ASPIRE](../notes/aspire.md)、[ENPIRE](../notes/enpire.md)、[Zetta](../notes/zetta.md)。下表的“适配”是对我们当前 RLT 目标的判断，不是论文作者的结论。

## 先带着一张图看六篇

每读一篇先问四件事：**改的是什么、反馈何时进入、失败回执来自哪里、是否真让下一次接触动作更好**。不要把“固定 VLA + 更强外部代理”的成功归到动作物理表征。

| 论文 | 一句话，用直白话说 | 更新的东西与反馈时间 | 对 RLT 的具体借鉴 | 本轮取舍 |
|---|---|---|---|---|
| [Zeva](https://arxiv.org/abs/2608.30880) v2 | 机器人记住“刚才**实际做了什么**、物体**真的如何变化**”，再用这段经验影响下一步 | 接触后果编码；BIT 在一次尝试内，PIM 在同一 episode 跨尝试；部署冻结参数 | 完成后的动作—响应记录、阶段检索、快记忆 + 慢 RL | **主精读，做最小实现**；原创已覆盖 in-context action-effect memory |
| [Harness VLA](https://arxiv.org/abs/2607.08448) v5 | 把 VLA 当成可重试的局部接触技能，由外层系统决定何时调用、如何重新摆位 | 任务 trace、全局成功/失败规则更新 planner memory；VLA 冻结 | 失败分期、技能 operating range、重试基线；论文使用 RLinf 发布的 π0.5 SFT 作 LIBERO primitive，不等于 RLT RL 算法 | 对照和系统层参考，不作为首轮表征改动 |
| [SHAPER](https://arxiv.org/abs/2608.11350) v2 | 通过 rollout 反思，修改技能说明与给代理看的历史组织方式 | 经评审的文本反馈修改 skill/harness，模型参数固定 | “哪些历史值得给策略看”及失败归因 | 文本诊断参考；难单独证明动作端物理增益 |
| [ASPIRE](https://arxiv.org/abs/2607.00272) v1 | 看执行细节找失败点，修复代码技能，验证后留在技能库 | 细粒度 trace → code-as-policy 修复 → 可复用 skill | 从回执中区分感知、接触、夹持、规划失误 | 启发实验日志；改动面偏大 |
| [ENPIRE](https://arxiv.org/abs/2606.19980) v2 | 把复位、运行、验收、查错、改代码连成可重复的真实机器人研究循环 | coding agent 修改训练 recipe/代码；验证后再迭代 | 可复现实验运行单、版本和停止条件 | 用于实验 harness，不是当前主要算法贡献 |
| [Zetta ζ](https://arxiv.org/abs/2608.16590) v1 | 执行中用快速异常检测器守护 VLA，出错就调用恢复技能，并验证后才升级技能 | 高频 critic/恢复 skill、rollout 候选、验证门控；底座冻结 | 独立的恢复控制对照与早期异常监测 | 第二阶段：恢复收益必须与记忆/表征收益拆开 |

## 推荐今天的阅读顺序（约 2.5 小时）

1. **30 分钟，扫六篇：**只看各自 Problem/Figure 1/Method 总图/主要消融，回答“在线究竟更新什么”。先把 Zeva 与 Zetta、Harness 的记忆边界分开。
2. **70 分钟，精读 Zeva v2 的 §III-C 至 III-F、§IV-D/IV-F：**画出 `(已执行动作, 前后观测) → CTE → (phase, effect) → BIT/PIM → prompt → 动作`。逐行标出“可在线读”的时间点和 episode 重置时机；用 [精读及 RLT 接口](zeva-rlt-implementation-2026-09-26.md)核对公开代码。
3. **25 分钟，看 Harness VLA + Zetta 的最强对照：**如果改善来自 re-stage、retry 或 runtime critic，表征主张不能成立。列出这三种行为有没有改动执行预算。
4. **25 分钟，先做可验证的接线试验：**运行 [时间隔离原型](prototypes/zeva_rlt_memory/README.md)；用一段本地 RLT rollout 检查数据字段和执行前/后分界。任何学习曲线须等可信 B0 恢复。

## 精读 Zeva 时写在纸上的问题

- 它的 `causal` 是否等于已经发现了真实摩擦系数？**不是**；现有证据是动作与观察后果的编码和功能相似检索。
- Policy 为什么会利用记忆？**因为离线先训练了 memory-conditioned policy**；部署冻结 ≠ 不需要训练记忆接口。
- PIM 是跨任务终生知识库吗？**原方法不是**：同一个 episode 跨 attempt 保留，换 episode 清空。跨任务替换是特设测试，若做长期知识库属于我们另外的研究假设。
- 效应监督的目标有没有塌缩风险？公开代码直接预测视觉差分的 MSE 只作诊断，真正优化包含 effect contrastive、action summary、alignment 和防塌缩项。不要把论文简化式直接复制成训练代码。
- 增益来自观测后果还是历史更多、参数更多、重试更多？在我们自己实验里要与等容量 history-only、随机记忆、phase-only、相同重试预算比较。

## 本轮决定

选择 **Zeva 的“已执行动作 → 实测后果 → 有界记忆”** 进行精读与原型开发。目标不是复现完整 Zeva，也不是直接把它的 prompt 塞入 RLT VLA；**第一轮先检验可靠的数据回执和检索是否成立**，再给冻结 VLA 外的小 actor/critic 训练一个可学习的记忆读出，仍沿用原 [loss-first 对照](flare-rlt-contact-experiments-2026-09-25.md)。如果 loss-first/B0 对照尚未可信，先不声称记忆提高了在线 RL 收敛。

## 来源与版本

- [Zeva v2](https://arxiv.org/html/2608.30880v2)；[Zeva 官方代码与复现说明](https://github.com/air-embodied-brain/Zeva)。
- [Harness VLA v5](https://arxiv.org/html/2607.08448v5)；[SHAPER](https://arxiv.org/abs/2608.11350)；[ASPIRE](https://arxiv.org/html/2607.00272v1)；[ENPIRE](https://arxiv.org/abs/2606.19980)；[Zetta ζ](https://arxiv.org/abs/2608.16590)。

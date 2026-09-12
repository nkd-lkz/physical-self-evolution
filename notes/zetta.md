# Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence

> 阅读日期：2026-09-12  
> 定位：Skill / Harness Evolution；Frozen Policy；Runtime Critic；Recovery Skill；Validation-Gated Self-Evolution

---

## 1. 一句话

Zetta 不更新基础 VLA 权重，而是在 VLA 外部持续演化一套 **runtime critic + recovery skill + tool harness**：执行中实时发现物理异常，失败后生成最小修复，并只有在历史回归和 held-out generalization 都通过后，才把新 critic / recovery 写入长期 skill memory。

它代表的是：

**Harness / Skill Evolution**，而不是 Policy Weight Evolution。

---

## 2. 它解决什么问题？

已有 embodied agent / harness 往往是：

```
固定 skill 执行完整 rollout
        ↓
episode 结束
        ↓
post-hoc reflection
```

问题是物理世界的异常发生得更快：

- grasp 已经松了；
- object drift；
- collision clearance 不够；
- contact 丢失；
- progress 停滞。

等 episode 结束才反思已经太晚。

Zetta 要解决：

> 如何让 frozen base policy 在执行过程中被一个可持续演化的闭环 Harness 实时治理，并把已验证的失败修复沉淀为可复用能力？

---

## 3. 三个时间尺度的闭环

### Loop 1 · Action-frequency Governance

Runtime critics 在动作频率附近持续检查 physical state。

例如：

- retained grasp?
- object drift?
- collision risk?
- stable placement?

一旦触发异常，立即调用 recovery skill。

这不是大 Agent 每一步重规划，而是把快速判断下沉到小型 code-based critic / skill。

### Loop 2 · Rollout-batch Candidate Optimization

失败 rollout 被：

1. 按最早 observable divergence 聚类；
2. 做 causal diagnosis；
3. 提出新的 critic / recovery candidate；
4. 尽量做 minimal repair，而不是重写整个系统。

### Loop 3 · Validation-Gated Skill Update

候选 skill 不能直接写入长期能力库。

只有同时通过：

- historical regression；
- held-out generalization；

才进入 versioned skill memory。

核心思想：

> **Experience → Proposal → Validation → Consolidation**

而不是：

> Experience → 直接永久记住。

---

## 4. “Aha Moment” 是什么？

Zetta 观察到能力提升经常不是平滑的。

早期多轮修复可能只有小收益；一旦找到真正决定成败的 physical variable / invariant，成功率会突然跳升。

例如某些任务中真正关键的不是“再规划一次”，而是：

- 持续检测 grasp retention；
- 保持 collision clearance；
- contact-aware approach；
- stable-contact / placement predicate。

这类变量一旦被 runtime critic 捕获，并配套 recovery skill，frozen VLA 的能力上限会被释放出来。

---

## 5. 为什么它能跨任务迁移？

Zetta 学到的不是一条 task-specific trajectory，而是更偏物理不变量的 skill：

- pregrasp / regrasp；
- stable placement；
- retained grasp；
- collision-aware approach；
- stable contact；
- object-relative geometry；
- progress predicates。

这些 skill 在相关任务之间可以 zero-shot transfer。

这对我们的“model-agnostic physical 外挂”想法非常重要：

> 真正可迁移的外挂，不应该绑定某个 VLA hidden token，而更可能绑定 **observable physical predicates + executed action + recovery interface**。

---

## 6. 主要结果

项目页报告：

- LIBERO-Pro Goal 平均成功率最高约 90.8%；
- RoboCasa 18-task 平均约 93.6%；
- 相对 frozen VLA 在部分设置有大幅绝对提升；
- Z-Infra 将 valid rollout throughput 提升约 20.6×；
- Agent inference speedup 约 11.1×；
- learned skills 能跨相关任务 zero-shot transfer。

最重要的证据不是单一数字，而是：

> **base VLA 权重保持冻结，能力仍能随着 self-exploration iteration 增长。**

---

## 7. 对当前项目最值得借的 4 点

### A. Physical 外挂可以是 Critic + Recovery，而不一定是新 Policy

```
Base Action Model
      ↓
Executed Action
      ↓
Physical State / Consequence
      ↓
Runtime Critic
      ↓
正常？ → 继续
异常？ → Recovery Skill
```

这比把 physics features 直接 concat 给 actor 更 model-agnostic。

### B. Failure 要定位“最早 observable divergence”

以后 Phase 1 failure profile 不只记 terminal failure，要尽量记录：

> 第一个能够观察到 policy 已经开始走坏的位置在哪里？

这能直接连接 D1 / D2 / runtime critic。

### C. 经验写回必须有 Validation Gate

未来无论是：

- replay；
- memory；
- recovery skill；
- distillation data；

都值得问：

> 这条经验真的值得长期保存吗？

### D. 区分 Policy Failure 与 Harness Failure

如果 base VLA 本来能成功，但因为：

- 没持续检查 grasp；
- 没及时 retry；
- 阶段切换错误；

那就不一定需要改 policy weights。

---

## 8. 对我们的创新边界

Zetta 已经非常明确地占据：

- frozen policy；
- runtime physical critic；
- recovery skills；
- failure-driven harness evolution；
- validation-gated skill consolidation。

所以如果我们以后做“model-agnostic physical外挂”，不能只讲：

> frozen VLA + physical critic + recovery。

需要证明我们的增量，例如：

- policy-level online learning；
- action-consequence representation；
- critic / recovery 可跨 Action Model；
- real + imagined physical experience 联合；
- experience selection / consolidation 更统一。

---

## 9. 今日讨论问题

1. 我们所谓 Physical Experience Layer，到底更应该像 RLT 的 actor-critic，还是像 Zetta 的 runtime critic + recovery harness？
2. 哪些 physical predicates 可以跨 task / action model 复用？
3. 经验是否应该先通过 validation gate，再进入 replay / memory / distillation？
4. 如何区分“base policy 真不会”与“base policy 会，但 Harness 没管理好执行”？

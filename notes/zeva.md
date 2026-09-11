# Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation

## 一句话

Zeva 不通过 RL 或微调更新权重，而是把机器人刚刚执行过的 **Action → State Change** 写成 Causal Interaction Memory，再通过 Context 影响冻结 policy 的后续动作。

它属于：

**Context Evolution**

而不是 Policy Evolution。

---

## 1. 它解决什么问题？

预训练 policy 在陌生物体、相机、本体或局部动力学条件下，会遇到 pretraining 无法覆盖的物理差异。

Zeva 的核心问题不是：

> 如何把 policy 权重再训练一遍？

而是：

> 能否让机器人从自己刚刚发生的 interaction 中临时学会“这个环境现在怎么运作”？

---

## 2. 核心表示：Action–Effect Transition

Zeva 更强调 transition，而不是单帧 state：

```
Before State
    +
Executed Action
    +
Observed State Change
    ↓
Causal Interaction Signal
```

这是对我们当前 Physical Experience 思路很重要的启发。

---

## 3. 双时间尺度 Memory

### Brief Interaction Trace

attempt 内的短期 interaction history。

### Persistent Interaction Memory

同一个 episode 内跨 attempt 积累的物理 interaction evidence。

因此可以简单理解为：

- BIT = within-attempt
- PIM = across-attempt

---

## 4. Memory 如何影响 Policy？

当前 phase → 检索相似历史 interaction → 形成 Causal Prompt → 注入冻结 policy。

所以：

```
Execute
↓
Observe Effect
↓
Store Action–Effect
↓
Retrieve Similar Experience
↓
Prompt Frozen Policy
↓
Better Next Action
```

---

## 5. 对当前项目的真正意义

Zeva 不意味着我们应该放弃 RLT。

更重要的是它提出了一个长期问题：

> 哪些 Physical Experience 应该先进入 Context，哪些才值得通过 RL 写进权重？

因此可形成：

**Fast Memory + Slow RL**

- 快速层：Zeva-style Context Adaptation
- 慢速层：RLT-style Policy Adaptation

---

## 6. 创新边界

如果后续我们做 Action Consequence Representation，就必须与 Zeva 正面对比：

- Zeva：action-effect memory → context
- 我们若做：action-effect → online critic / policy update

必须说明为什么要 weight update，以及它带来什么额外能力。

---

## 今日讨论问题

1. Physical Experience 的基本单位应该是 state，还是 transition？
2. 哪些信息值得“临时记住”，哪些应该“写进权重”？
3. Memory 与 RL 是否能形成互补的快慢时间尺度？

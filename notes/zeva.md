# Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation

> 阅读日期：2026-09-12（加深）  
> 定位：Context Evolution；In-Context Causal Learning；Frozen Policy；Action–Effect Memory

> **2026-09-26 校核：**以下“无需更新权重”只指**部署期**；CTE 和记忆条件动作策略曾在离线阶段训练。PIM 仅同一个 episode 跨 attempts 保留，跨任务长期库存储不是论文已实现机制。主文 v2 的 RoboCasa 76.8% 与公开 checkpoint 的固定无重试 78.0% 属不同评测合同；开放版 effect MSE 只记诊断，优化了对比及防塌缩等损失。具体代码路径与 RLT 对照参见 [Zeva 精读及最小接口](../research/zeva-rlt-implementation-2026-09-26.md)。

---

## 一句话

Zeva 在**部署时**不通过 RL 或微调更新权重，而是把机器人刚刚执行过的 **Executed Action → Observed State Change** 写成 Causal Interaction Memory，再通过 Context 影响已经经过离线记忆条件训练的 policy 的后续动作。

它属于：

**Context Evolution**

而不是 Policy Weight Evolution。

---

## 1. 它解决什么问题？

预训练 policy 在陌生物体、相机、本体或局部动力学条件下，会遇到 pretraining 无法覆盖的物理差异。

Zeva 的核心问题不是：

> 如何把 policy 权重再训练一遍？

而是：

> 能否让机器人从自己刚刚发生的 physical interaction 中临时学会“这个环境现在怎么运作”，并把这种经验马上用于下一次动作？

因此它强调：

```
Pretrained Policy
      ↓
Physical Interaction
      ↓
Action-Induced State Change
      ↓
Memory
      ↓
Better Next Decision
```

部署阶段 policy 参数保持冻结，在线更新的是 interaction memory。

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

可以抽象为：

\[
(s_t, a_t^{exec}, \Delta s_t)
\]

这对我们当前 Physical Experience 思路非常重要：

> 物理经验的核心单位可能不是“我现在是什么状态”，而是“我实际做了什么，这个动作造成了什么后果”。

---

## 3. Causal Interaction Extractor

Zeva 使用 Causal Transition Encoder，把：

- visual latent；
- action encoding；
- observed effect；

融合成 Causal Interaction State，再投影得到：

### Phase Token

描述当前任务阶段。

### Causal Interaction Signal

描述这个 action 实际造成的 state change / effect。

这里所谓 causal，更接近：

> **显式保留 intervention(action) 与 observed effect 的对应关系。**

不要把它误解成完整 Structural Causal Model。

---

## 4. 双时间尺度 Memory

### Brief Interaction Trace（BIT）

attempt 内的近期 interaction trace。

作用：
- 快速保留刚刚发生的 local dynamics；
- 让后续动作知道当前 attempt 已经做过什么、发生了什么。

### Persistent Interaction Memory（PIM）

同一个 episode 中跨 attempts 累积 physical interaction evidence。

作用：
- Attempt 1 失败；
- Attempt 2 又得到新的 effect；
- Attempt 3 可以检索之前失败经验并调整。

因此：

- BIT = within-attempt
- PIM = across-attempt

真实机器人 ablation 表明两层 memory 都重要；去掉其中任一层都会明显降低成功率。

---

## 5. Memory 如何影响 Policy？

当前 phase → 检索相似历史 interaction → 形成 Causal Prompt → 注入冻结 foundation policy。

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
Causal Prompt
↓
Frozen Policy
↓
Better Next Action
```

这里**部署时**没有 gradient update；policy 如何读取 prompt 已在离线训练中学过。

---

## 6. 为什么它可以叫“自进化”？

因为 performance 会随着 interaction experience 积累而提高，即使 policy weights 完全不变。

项目页展示：

### RoboCasa365

跨 repeated attempts 的 pooled cumulative success：

\[
26\% \rightarrow 73\%
\]

### ChemLab-Evo 真机

例如：

- Pick Up Test Tube：65% → 100%
- Place Beaker：25% → 70%
- Pour Water：30% → 80%

所以 Zeva 所谓 self-evolution 是：

> **Memory / Context Evolution**

而不是：

> policy parameter evolution。

---

## 7. Benchmark 结果

RoboCasa365-Atomic5：

- Zeva Avg. SR：76.8%
- Fast-WAM：72.4%

ChemLab-Evo 真机 Level-1：

- Zeva Avg. SR：83.3%

更重要的是 long-horizon process score 和 repeated-attempt improvement，而不只是单次 benchmark 数字。

---

## 8. Cross-Task Effect Retrieval：非常值得我们关注

Zeva 发现 interaction effect token 可以跨任务检索功能上相似的 physical effect，例如：

- container tilting；
- gripper closure；
- post-grasp lifting。

虽然：

- object 不一样；
- viewpoint 不一样；
- language instruction 不一样；

但 effect representation 仍能找到功能类似 transition。

这对我们“model-agnostic Physical Experience Layer”的启发很直接：

> 如果 representation 真正编码的是 action-induced effect，而不是 task appearance，它就有机会跨任务、甚至跨 action model 复用。

---

## 9. One-Shot Human Warm-Up

Zeva 还展示一个 human-guided demonstration 可以先写入 PIM。

之后 frozen policy 不更新权重，也能利用这条 interaction experience 改善 autonomous execution。

这说明 Memory 不一定只存机器人自己的 experience，也可以统一承载：

- self-exploration；
- human-guided interaction；
- demonstration-derived interaction effect。

---

## 10. 对当前项目的真正意义

Zeva 不意味着我们应该放弃 RLT。

更重要的是它提出一个长期问题：

> 哪些 Physical Experience 应该先进入 Context，哪些才值得通过 RL 写进权重？

因此可以形成：

**Fast Memory + Slow RL**

- 快速层：Zeva-style Context Adaptation
- 慢速层：RLT-style Policy Adaptation

长期还可以加第三层：

- Consolidation：把反复验证有效的经验写回 foundation policy。

---

## 11. 对我们的创新边界

如果后续我们做 Action Consequence Representation，就必须与 Zeva 正面对比：

- Zeva：action-effect → memory / context
- 我们若做：action-effect → critic / policy update

必须回答：

1. 为什么需要 weight update？
2. 哪些 information 仅靠 Context 不够？
3. weight update 是否带来跨 episode / task 更持久的能力？
4. 能否在不同 Action Model 间复用同一 effect representation？

---

## 12. 今日讨论问题

1. Physical Experience 的基本单位应该是 state，还是 transition？
2. 哪些信息值得“临时记住”，哪些应该“写进权重”？
3. Memory 与 RL 是否能形成互补的快慢时间尺度？
4. Zeva 的 cross-task effect retrieval 能否启发一个真正 model-agnostic physical representation？

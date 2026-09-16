# SHAPER: Self-Evolving Embodied Agents via Skill-Harness Evolution

> 阅读日期：2026-09-16  
> arXiv: 2608.11350 v2 · 2026-09-10  
> 定位：**Skill / Harness Evolution · Train-free / Non-parametric Self-Improvement**

---

## 1. 一句话

SHAPER 不更新 embodied foundation model 的参数，而是把 embodied agent 拆成：

```text
Frozen Planner M_theta
      +
Frozen Executor A_phi
      +
Reusable Skill s
      +
Context-Code Harness h
```

然后利用目标环境中的少量 rollout，把失败与成功压缩成 textual feedback，先优化 reusable skill，再优化 context-code harness。

因此它的“self-evolution”发生在 **model-external artifacts**，不是 neural weights。

---

## 2. 它到底更新什么？

SHAPER 固定：

- planner model weights；
- low-level executor / VLA weights；
- action interface；
- output parser。

只优化：

1. **Skill `s`**：给 planner 的持久化程序性指导，例如 scene inspection、task decomposition、subgoal selection、failure recovery、termination rule；
2. **Harness `h`**：context builder，决定哪些历史 observation、action、execution outcome 和 feedback 被保留，以及如何组织给 planner。

形式上：

```text
y_t ~ M_theta(g, o_t, s, h(tau_<t))
a_t = A_phi(y_t, o_t)
```

其中 `theta, phi` frozen，优化的是 `(s, h)`。

---

## 3. 核心方法：Rollout → Textual Gradient → Artifact Evolution

### 3.1 局部 round-level diagnosis

对每一步：

```text
before observation
+ planner output / subgoal
+ executed action
+ after observation
        ↓
      Judge
```

局部判断：

- subgoal 是否错误；
- 是否没有 progress；
- executor 是否与 planner command 不匹配；
- 是否出现重复 / stall。

关键点：不把整条长视频全部塞给 optimizer，而先做 action-effect 局部诊断。

### 3.2 Episode summarization

再把：

- round critiques；
- command / execution length / runtime error 等 metadata；
- terminal context；
- final reward / success；

压成 episode summary。

多个 episode summary + aggregate stats 构成论文所谓 **textual gradient** `Gamma(c)`。

它不是神经网络梯度，而是：

> 从 rollout 中提炼出的、能指导下一轮 skill / harness 修改的结构化反馈。

### 3.3 Two-stage evolution

SHAPER 不同时乱改两个 artifact，而是：

```text
Stage A
固定 seed harness
→ evolve skill
→ 选出 s*

Stage B
固定 evolved skill s*
→ evolve harness
→ 得到 h*
```

同一个 frozen foundation model 可以：

- interaction 时作为 planner；
- evolution 时换 optimizer prompt，作为 artifact optimizer。

生成的 harness code 先经过 sandbox validation；非法 import、文件 I/O、动态执行、超时等 candidate 直接拒绝。合法候选才进入 fixed validation set，用 beam search 保留 top-K。

---

## 4. VLABench 上到底学到了什么？

VLABench 中：

- frozen upper-level planner：Qwen3.6-27B；
- frozen executor：官方 VLABench pi0 VLA；
- planner 输出 textual subgoal；
- VLA 执行 low-level controls。

### Seed skill 的问题

原始 planner 容易：

- command 形式不符合 VLA actor 偏好的分布；
- partial success 后重复相同命令；
- 把本应由 VLA 解决的低层抓取几何也写进高层指令；
- 缺少显式 progress check。

### Evolved skill

演化后学到：

- short canonical commands；
- exact entity binding；
- one primitive per planner round；
- actor-aware command format；
- classify previous attempt as success / failure / partial / stalled；
- repeated no-progress 后改变 command；
- 根据 primitive 调整 execution-step budget。

所以这里的核心并不是“VLA 变强”，而是：

> **高层 planner 更懂 frozen executor 的 operating characteristics。**

---

## 5. Harness 到底学了什么？

原始 harness 倾向于：

- 保存大量完整 textual history；
- 只保留最近几张图；
- 把重复、无信息 view 和关键历史 evidence 同等对待。

最终 harness 改成：

- current observation 优先；
- compress old rounds；
- sparse evidence-aware visual memory；
- 保存 task-critical keyframes；
- deterministic RGB crops / overlays；
- 显式暴露 repeated command / stagnation / inverse-action cycles；
- structured context：当前 target、已有 evidence、ready state、information gap。

在 ESI-Bench 中尤其明显：早期关键视觉证据不再因 recency window 被丢掉。

---

## 6. 实验结果

### VLABench

作者构造 4 个 held-out split，共 800 个 evaluation episodes。

| 方法 | Overall success |
|---|---:|
| Direct VLA | 23.25% |
| SFT（same 15 train episodes） | 24.00% |
| Seed Agent | 28.25% |
| Skill Evolution | 33.50% |
| Harness Evolution | 30.50% |
| **SHAPER** | **34.50%** |

Full SHAPER 比 Seed Agent +6.25 pt，比 same-data SFT +10.50 pt。

更值得注意的是：distribution shift 下 improvement 更明显，说明 skill/harness artifact 能跨 target category / task form 复用。

### ESI-Bench

231-question subset：

- Seed Agent：32.5% micro / 31.2% macro；
- Skill Evolution：41.1% / 38.6%；
- **SHAPER：49.8% / 42.9%**。

Harness 对需要跨视角保留 evidence 的类别收益尤其明显，例如 reflection / grounding / spatial relation。

### Optimization cost

论文记录的 API-equivalent artifact evolution cost 约：

- VLABench：$2.25 / evolution run；
- ESI-Bench：$2.83 / evolution run。

这不包括 simulator / GPU infrastructure。

---

## 7. 论文边界

必须注意：

1. **没有更新 policy / VLA weights。** 这是 non-parametric evolution。
2. **没有真实机器人验证。** 论文实验是 VLABench 与 ESI-Bench。
3. **没有证明 cross-embodiment transfer。** 作者明确把它留作未来工作。
4. “self-evolving”表示 rollout 反馈持续修改 skill / harness，不等于开放世界无限 RSI。
5. VLABench 中 skill-only 已解释最大部分增益；skill 与 harness 的收益并非简单可加。

---

## 8. 与 Harness VLA 的区别

两篇都冻结 VLA，但关注点不同。

### Harness VLA

```text
Frozen VLA primitive
+ analytic primitives
+ memory-guided planner
→ 学习什么时候调用 / retry / re-stage
```

更强调：

> **VLA operating range + runtime orchestration。**

### SHAPER

```text
Frozen planner + frozen executor
        ↓
rollout diagnosis
        ↓
textual gradient
        ↓
evolve skill first
        ↓
evolve context-code harness
```

更强调：

> **如何系统地优化外部 agent artifacts。**

SHAPER 比 Harness VLA 更像一个“自动改 planner instructions + context builder 的优化算法”。

---

## 9. 对 Universal Physical Token 项目的真正可借鉴点

### 9.1 最值得借：把“模型问题”和“harness / execution 问题”彻底拆开

这和当前 hammer 调试高度相关。

我们已经观察到：同一个 Stage1 checkpoint 在 `H50/C10` 与 `H50/C50` 下行为可以显著不同。

这说明：

```text
policy / representation capability
!=
execution harness quality
```

因此在归因 Physical Token 收益之前，必须先固定：

- action chunk / horizon；
- TOPP / controller semantics；
- observation refresh；
- actual state / executed action contract；
- reward / transition timing。

这正好强化当前 **Gate 0 — Baseline Recovery**，而不是改变 B0/B1/B2 主线。

### 9.2 借 rollout-guided hierarchical diagnosis，不借完整 agent system

我们可以把 SHAPER 的：

```text
before → action → after
→ local diagnosis
→ episode summary
→ systematic failure pattern
```

用于 Research OS / failure analysis。

对 hammer 可形成一个物理版诊断模板：

```text
observation_t
+ reference / actor action
+ executed action
+ measured consequence
+ contact / slip / progress
        ↓
local failure card
        ↓
episode summary
```

这可以帮助判断 failure 属于：

- Stage1 task capability；
- execution semantics；
- observation / state；
- reward / transition；
- online actor / critic；
- 后续真正的 representation insufficiency。

但它只做 diagnosis，不进入第一版 Physical Token loss。

### 9.3 借 validation gate

SHAPER 的 harness candidate 不是生成后直接使用，而是：

```text
propose
→ sandbox validation
→ fixed validation set
→ top-K
```

对我们以后任何外部自适应模块都值得保留这个原则：

- adaptive chunk rule；
- recovery rule；
- failure memory；
- automated reward / diagnostic tool；

都不应“生成即上线”。

### 9.4 暂时不借：skill/harness evolution 本身

当前项目还在 Gate 0，下一科学问题仍是：

```text
B0 RL Token / matched readout
→ B1 + measured transition
→ B2 + valid physics
```

现在加入 LLM planner、memory、skill evolution 或 context-code generation，会引入新的强变量，破坏 Physical Token 的因果消融。

---

## 10. 当前项目动作

**分类：Add diagnosis / Frontier reference，不改变 mainline。**

当前不新增 SHAPER baseline。

真正值得立即落地的是：

> 在 hammer / RoboDojo 日志中进一步区分 **policy capability failure** 与 **execution-harness failure**，并把 `before → executed action → after → outcome` 做成结构化 episode diagnosis。

等 B0/B1/B2 稳定之后，再研究 Physical Token 是否能成为 Harness / Agent 的低层 physical-state interface。

---

## 11. 一个值得继续讨论的问题

> **如果同一个 frozen policy 因 execution harness 改变就能显著改善，那么 Physical Token 的实验如何证明自己学到的是“物理 grounding”，而不是仅仅补偿了一个不合理的 execution/context interface？**

这应该成为后续 B0/B1/B2 设计中的重要归因检查。

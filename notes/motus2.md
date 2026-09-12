# Motus2: A Self-Evolving General World Model for Dexterous Manipulation

> 阅读日期：2026-09-12  
> arXiv: 2608.30237v2  
> 定位：General World Model / Model-Based RL / Physical Experience / Memory / Tactile / Self-Evolution

---

## 1. 一句话

Motus2 把 **Policy（WAM）+ Simulator（AC-WM）+ Evaluator（Value Model）** 做成同一个共享参数 General World Model 的三个接口，再把三者串成：

```text
Generate Action
→ Predict Consequence
→ Evaluate Outcome
→ Update Policy
```

它想解决的不是“只会根据 observation 直接出 action”，而是让机器人知道：**做这个动作之后会发生什么、结果好不好，并把这种反馈重新写回策略。**

---

## 2. 它解决什么问题？

传统 imitation / VLA 的主要问题：

```text
Observation → Action
```

但是缺少：

```text
Action → Consequence → Value
```

因此：

- expert demonstrations 很贵；
- 失败轨迹通常被丢掉；
- policy 不知道动作是好是坏；
- 环境变化后，单纯 imitation 很难自我纠错；
- vision-only 对 slip / contact / grasp formation 等物理事件又存在 partial observability。

Motus2 的核心问题是：

> 能不能在同一个模型里统一 Action、World Simulation 和 Value Evaluation，并利用模型自己的 consequence prediction 与 value feedback 改善 action policy？

---

## 3. 核心创新 1：一个模型，三个接口

共享参数模型显式 factorize 为：

```text
Policy (WAM)
π(A | context)
        ↓
Simulator (AC-WM)
p(future | context, A)
        ↓
Evaluator (VM)
p(value | context, A, future)
```

它们不是三个完全独立的网络，而是同一视频-动作 backbone 的三种 conditional interfaces。

### 为什么重要？

World Model 不再只是“生成未来视频”。

真正服务决策的是：

```text
Action proposal
+
Action-conditioned future
+
Outcome value
```

---

## 4. 核心创新 2：Action-first 防止“偷看未来”

如果 Action prediction 能看到当前 action 之后的 future video，它可能通过 future 反推 action，训练时看似很强，但部署时未来根本不存在。

因此 Motus2 在 robot-domain mid/post-training 使用 action-first mask：

```text
A → Z → U
```

其中：

- A = action chunk
- Z = future visual latent
- U = value query

Action 看不到自己对应的 future video 和 value；future video 可以看 action；value 可以看 action + future。

这让：

```text
Action → Consequence → Evaluation
```

真正保持因果方向。

---

## 5. 核心创新 3：不同质量的数据，不做同一种监督

这是我认为对“自进化”最重要的一点。

### 成功 expert trajectory

可以监督：

```text
Policy + Simulator
```

因为动作本身是值得模仿的。

### Failure / suboptimal trajectory

不能直接 imitation，否则等于教 policy 重复失败动作。

因此只用于：

```text
Simulator
+
Evaluator
```

即：

> 失败数据不一定告诉机器人“应该做什么”，但非常适合告诉它“这样做会发生什么，以及这样好不好”。

这和我们当前的 Failure / Recovery Data 主线非常契合。

---

## 6. 核心创新 4：Self-Evolution = Planning + Policy Update

### A. Best-of-N Planning

推理阶段：

```text
Policy samples N candidate action chunks
        ↓
Simulator imagines N futures
        ↓
Value Model scores them
        ↓
execute argmax candidate
        ↓
observe real world again
```

这是 test-time planning，不改变 weights。

实验：

- Base：65.0%
- + Planning：67.5%

即 +2.5 points。

### B. MBRL Policy Optimization

Planning 只能从当前 proposal distribution 中选更好的动作，并不会让 proposal distribution 本身变强。

因此作者用 DiffusionNFT 把 evaluator score 转成 flow-matching policy update。

关键点：

- high-value candidates → policy 更靠近这些动作；
- low-value candidates → policy 远离这些动作；
- simulator / evaluator 固定；
- 只更新 action-related parameters。

实验：

- Base：65.0%
- + MBRL：72.5%
- + MBRL + Planning：75.0%

所以：

```text
Planning = 当场选得更好
MBRL = 以后生成得更好
```

---

## 7. Progress-Based Value Model

Value Model 学的是 task progress，而不是简单 success/failure。

成功 trajectory segment：正 progress target。

失败 / task-irrelevant segment：负 progress target。

因此 VM 可以用于：

- candidate ranking；
- 判断 progress；
- failure trajectory 分析；
- policy optimization feedback。

这个设计和我们后面可能做的：

```text
Value-Oriented Physics
Correction Benefit
Failure Onset Detection
```

有很强联系。

---

## 8. Memory：长期历史本身是状态

Motus2 比较：

- Sliding Window
- Global Autoregression
- Hybrid Memory

真实机器人 long-context probes 上：

- Hybrid Memory：25.0%
- Global Autoregression：57.5%

这说明目前简单保留完整历史反而明显更强；memory compression 还没有被优雅解决。

对我们最重要的启发：

> actual interaction history 可能本身就是 Physical State 的一部分。

这进一步支持 Phase 1 D1：先测 short history，再急着发明 Physical Token。

---

## 9. Tactile Expert：高频物理反馈不需要重跑完整 backbone

视觉无法完整判断：

- slip
- contact
- force evolution

Motus2 增加一个 lightweight tactile expert：

- 主 backbone 先把完整 action chunk denoise 到 intermediate state；
- reuse detached layer-wise KV cache；
- 每个短 sub-chunk 执行前，用最新 tactile window 做最后动作 refinement；
- 训练时附带 future-force prediction。

真实任务 ablation：

- without tactile：60.0%
- with tactile：72.5%

+12.5 points。

这和我们长期“慢大模型 + 快物理反馈模块”的分层思路非常接近。

---

## 10. 数据路线：Human Ego → Robot Domain

Motus2 使用约 130K raw hours egocentric corpus：

- monocular ego：扩大场景 / 物体 / 交互覆盖；
- stereo ego：补 depth cue 和 3D hand motion；
- >100h robot-domain mid-training + human-robot alignment：把人类经验 ground 到 robot action space。

五项真实任务中：

- Ego pretraining 后：51%
- Robot-domain mid-training 后：84%

提升 33 points。

说明人类数据可以 scale interaction priors，但仍然需要 robot-domain grounding。

---

## 11. 这篇论文中的“Self-Evolution”应该如何理解？

不要理解成：

> 机器人已经能在开放世界永久自主学习。

更准确：

> 在目标 robot post-training 阶段，用自身 policy 产生 candidates，用自身 world model 预测后果，用自身 value model 评估，再用这些 feedback 更新 action policy。

所以它属于：

```text
Model-Predicted Experience
        ↓
Self Evaluation
        ↓
Policy Evolution
```

目前仍是受控 post-training loop，而不是无限开放式 RSI。

---

## 12. 对当前项目最值得借的 6 点

### ① Failure Data 的用途分流

成功数据：可以 imitation。

失败数据：不要 imitation；更适合 dynamics / value / recovery supervision。

这可以直接加入我们未来统一 experience schema。

### ② Action Consequence 必须服务 Action Ranking

我们以后若做 Physical Consequence，不应该只证明 prediction loss 降了。

更强证据是：

> consequence prediction 是否让 candidate action ranking / correction 更准？

### ③ Value Model 可以成为 Failure Diagnosis 模块

Phase 1 可研究：

- value 是否能提前发现 progress plateau？
- failure onset 是否能被 value trajectory 定位？
- value 是否能估计 correction benefit？

### ④ 先测 History，再设计 Physical Token

Memory ablation 再次说明：

> 当前 observation 可能根本不是 Markov state。

先做 D1：current state vs actual proprio vs short history。

### ⑤ 慢 Backbone + 快 Physical Expert

Tactile expert 的设计很值得长期借：

```text
Large Backbone
→ reusable KV / intermediate action
→ small high-frequency physical expert
```

这可以推广到：

- tactile
- force
- execution residual
- contact corrector

### ⑥ World Model 与 RLT 可以是两条不同尺度

当前：

```text
RLT
真实 rollout → critic → lightweight actor
```

Motus2：

```text
Policy → imagined future → value → action policy update
```

未来真正值得问的是：

> Real Physical Experience 与 Imagined Experience 应该如何组合？

---

## 13. 与我们的主线位置

当前不要转向“复现 Motus2”。

Phase 0 仍然是：

```text
RoboTwin2 Multi-task RLT Benchmark
```

Motus2 更适合放在 Phase 2 / Phase 3：

```text
Phase 2
Physical Consequence / Value / History
        ↓
Phase 3
Predict → Evaluate → Improve
```

所以它对当前最有价值的是 **研究问题与实验设计**，而不是工程复现。

---

## 14. 一句总结

> **Motus2 真正的新意不是“VLA + 视频生成”本身，而是把动作生成、动作后果预测和结果评价做成同一个共享世界模型里的三个因果接口，再让失败数据、想象 rollout 和 value feedback 共同反过来优化动作策略。**

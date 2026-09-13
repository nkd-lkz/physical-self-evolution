# RISE: Self-Improving Robot Policy with Compositional World Model

> 阅读日期：2026-09-13  
> arXiv: 2602.11075 v2 · RSS 2026  
> 定位：World Model + Value + Imagination RL；Policy Evolution / Self-Improvement via imagined experience

---

## 1. 一句话

RISE 把真实机器人 RL 的“环境”换成一个 **Compositional World Model**：策略先提出 action chunk，Dynamics Model 预测多视角未来，Progress Value Model 给 imagined future 打分并形成 advantage，最后用这些 imagined rollout 反复更新 VLA policy。

核心闭环：

```text
Current Observation
      ↓
Policy proposes Action Chunk
      ↓
Controllable Dynamics Model
      ↓
Imagined Future Observations
      ↓
Progress Value Model
      ↓
Advantage
      ↓
Advantage-conditioned Policy Update
      ↓
Better Policy
      ↓
Next Imaginary Rollout
```

因此它不是“World Model 辅助规划”而已，而是把 World Model 当成 **RL training environment**。

---

## 2. 解决什么问题？

现实世界 on-policy RL 面临：

- robot interaction 串行、慢；
- hardware cost 高；
- reset / monitoring 麻烦；
- contact-rich 失败有安全风险；
- VLAs 在 expert manifold 外缺 recovery；
- 仅靠 offline data 又会有 distribution shift。

RISE 的核心问题：

> 能否用世界模型生成接近 on-policy 的 imagined interaction，让机器人策略在不反复真实试错的情况下继续自我改进？

---

## 3. Compositional World Model 为什么叫“Compositional”？

RISE 不用一个大模型同时完成全部 world modeling，而拆成两个最适合各自目标的模块。

### 3.1 Controllable Dynamics Model

输入：

- multi-view history `O_t`；
- candidate action chunk `a_t:t+H-1`。

输出：

- `H` 步未来多视角图像。

公式：

```text
future = D(history, action_chunk)
```

关键不只是“画面逼真”，而是 **action controllability**：不同动作必须真的导致不同、动作一致的未来。

RISE 从 Genie Envisioner 初始化，在大规模 action-labeled robot data 上进一步训练，并加入 Task-Centric Batching：同一 batch 少放不同 scene/task，多放同场景下不同动作，优先让模型学清楚“动作差异 → 后果差异”。

### 3.2 Progress Value Model

输入：

- observation / imagined observation；
- language instruction。

输出：

- 任务进展 value `V(o,l)`。

训练结合两个目标：

1. **Progress regression**：成功 demo 中用 `t/T` 建立粗粒度任务进度；
2. **TD learning**：加入 success + failure rollouts，让 value 对真实失败敏感，而不是只随着时间机械上升。

直觉：

> Progress loss 告诉模型“正常任务大概怎样前进”；TD loss 告诉模型“看起来时间继续走，但机器人其实可能已经失败”。

---

## 4. Advantage 怎么算？

对于当前状态 `o_t`，policy 生成一个 action chunk；Dynamics Model 预测未来：

```text
o_t → a_chunk → ô_{t+1}, ..., ô_{t+H}
```

Value Model 对未来每帧打分。

RISE 定义 chunk advantage：

```math
A(o_t,a_t,l)=\frac{1}{H}\sum_{k=1}^{H}V(\hat o_{t+k},l)-V(o_t,l)
```

所以它关心的不是：

> “最后是否成功？”

而是：

> “这个动作块让任务平均前进了多少？”

这给长程 / 精细操作提供比 terminal success 更密的学习信号，也避免要求 world model 一次预测完整任务直到终点。

---

## 5. Policy Warm-up：为什么先用真实数据？

在 imagination 自改进之前，policy 先用真实离线数据 warm-up：

- expert demonstrations；
- policy rollouts（success + failure）；
- human correction / DAgger data。

目的是把 policy 锚定到 **physically plausible behavior distribution**，避免世界模型里一开始就探索离谱 OOD actions。

训练成一个 advantage-conditioned policy：

```text
policy(action | observation, language, advantage_bin)
```

其中：

- expert / human correction → 直接标为 optimal advantage；
- rollout → 用 Value Model 评估得到 advantage。

---

## 6. Self-Improving Loop：真正怎么“自我改进”？

### Rollout Stage

1. 从真实 offline dataset 采一个 initial state；
2. 给 rollout policy 一个“最优 advantage” prompt；
3. policy 产生 action chunk；
4. dynamics model 预测未来多视角状态；
5. value model 计算实际 advantage；
6. imagined state 继续作为下一步 rollout input。

由于生成视频长期 rollout 会累积误差，论文把连续 imagined interaction 限制得较短，而不是无限往未来滚。

### Training Stage

保存 imagined tuple：

```text
(observation, imagined action, evaluated advantage)
```

行为 policy 在 advantage-conditioning 下学习这些数据：

- high-advantage action：值得保留 / 加强；
- low-advantage / failed action：作为低 advantage 行为，让 policy 知道什么不应该生成。

并混入 offline real data，避免 policy 在 imagination 中漂移或 catastrophic forgetting。

最终形成：

```text
Policy
→ Imagined Rollout
→ Value Evaluation
→ Advantage Label
→ Policy Training
→ EMA Rollout Policy Update
→ New Imagined Rollout
```

---

## 7. 它与 Motus2 的关键区别

两者都可以写成：

```text
Action → Predicted Consequence → Value → Policy Improvement
```

但侧重点不同。

### Motus2

更强调 General World Model 一体化：Policy / Simulator / Evaluator 共享体系，并支持 test-time Best-of-N Planning + MBRL。

### RISE

更强调：

> **World Model 直接替代 Physical Environment，成为大规模 Online RL 的 imaginary environment。**

核心目标是解决真实 on-policy RL 太贵、太慢、难 reset 的问题。

---

## 8. 它与 LWD / RLT 的关系

### RLT

```text
Real Physical Experience
→ lightweight actor-critic
→ Local Policy Adaptation
```

### LWD

```text
Fleet Real Experience
→ DIVL / QAM
→ Generalist Policy Evolution
```

### RISE

```text
Seed Real Experience
→ World Model
→ Massive Imagined Experience
→ Advantage-conditioned Policy Improvement
```

因此三者分别代表：

- RLT：局部真实在线适应；
- LWD：真实 fleet experience scaling；
- RISE：imagined experience scaling。

长期真正有意思的是 **Real + Imagined Experience** 如何互相校准。

---

## 9. 实验

三个真实双臂任务：

1. Dynamic Brick Sorting：运动传送带上动态抓取与颜色分类；
2. Backpack Packing：柔性背包 / 衣物 / 拉链；
3. Box Closing：双手折 flap 并将 tab 精确塞入。

成功率：

| 方法 | Brick Sorting | Backpack Packing | Box Closing |
|---|---:|---:|---:|
| π0.5 | 35% | 30% | 35% |
| RECAP | 50% | 40% | 60% |
| **RISE** | **85%** | **85%** | **95%** |

相对最强对照的绝对提升分别约：

- +35 pt；
- +45 pt；
- +35 pt。

---

## 10. 我认为最重要的创新点

### A. World Model 不再只是“规划辅助”，而是 Online RL Environment

这比单纯 Best-of-N 更进一步：imagined rollout 会持续扩展训练分布并真正改变 policy。

### B. Dynamics / Value 解耦

World Model 不必“一网打尽”。

- Dynamics：擅长预测动作后果；
- Value：擅长判断后果好不好。

这和我们当前 Physical Experience Layer 的思考高度一致。

### C. 中间 progress advantage

不要求预测完整任务终点，用短 action chunk 的 progress improvement 产生 dense learning signal。

### D. Imagined failures 也有学习价值

失败动作不需要真机一一执行；World Model 能制造 near-failure / failure consequence，再由 Value 标低 advantage，形成廉价负经验。

---

## 11. 对当前 Physical Self-Evolution 项目的启发

### 11.1 Action Consequence 必须服务 decision

如果未来做 Physical Consequence Representation，最终应证明：

```text
(s,a) → consequence
          ↓
        value
          ↓
  better action ranking / policy update
```

而不仅仅是 auxiliary prediction loss 更低。

### 11.2 Compositional 比“万能 Physical Token”更值得考虑

不一定一个 representation 同时承担全部能力。

可能拆为：

```text
Consequence Model
      +
Value / Progress Model
      +
Policy Adapter
```

各自使用最适合的 supervision。

### 11.3 Real / Imagined Experience 应严格区分

RISE 的核心依赖 world model fidelity。对我们的仓库长期可新增：

- real experience；
- imagined experience；
- source tag；
- confidence / model uncertainty；
- validation gate。

未来 imagined experience 不应直接与 real transition 等价对待。

### 11.4 Phase 0 仍不改变

当前仍优先：

- RoboTwin 2.0 / RLinf_support pinned RLT baseline；
- Stage 1 2k joint-full；
- Stage 2 C=10 real rollout；
- multi-task baseline。

RISE 暂时属于 **Phase 2/3 的高优先级 inspiration / stronger neighboring work**，不进入当前阻塞链。

---

## 12. 后续最值得讨论的问题

1. World Model 的 visual fidelity 与 decision utility 哪个更重要？
2. Imagined consequence 什么时候足够可信，可以作为 RL experience？
3. 是否应该给 imagined transition 加 uncertainty / validation gate？
4. Real failure experience 与 imagined counterfactual experience 如何分工？
5. RLT 的 real critic 和 RISE 的 world-model value 能否共享 / 蒸馏？
6. 我们的 physics sidecar 是否可用于训练 / 校准一个比纯视觉 world model 更可靠的 consequence/value teacher？

---

## 13. 最简总结

> RISE 的真正创新，不是“用了一个视频世界模型”，而是把 **可控 Dynamics Model + Progress Value Model** 组合成一个虚拟 RL 环境，在这个环境里持续生成 imagined on-policy rollouts，并把短时动作后果转成 advantage，反复训练 advantage-conditioned VLA policy。因此它把“自我改进”从昂贵的真实试错转移到了可扩展的 imagination space。
# LWD：Learning While Deploying — Fleet-Scale Reinforcement Learning for Generalist Robot Policies

> 阅读日期：2026-09-12  
> arXiv: 2605.00416  
> 定位：Foundation / Fleet Evolution；Offline-to-Online RL；Generalist VLA Post-training

---

## 1. 一句话

LWD 的核心不是“又一个机器人 RL 算法”，而是把真实部署本身变成训练数据来源：

```
Pretrained Generalist VLA
        ↓
Fleet Deployment
        ↓
Autonomous Rollouts + Human Interventions
        ↓
Shared Physical Experience
        ↓
Offline-to-Online RL
        ↓
Updated Generalist Policy
        ↓
Redeploy
```

也就是把 **Deploy → Experience → Learn → Redeploy** 真正做成一个 fleet-scale data flywheel。

---

## 2. 解决什么问题？

大规模 VLA 预训练带来广泛能力，但固定离线数据无法完全覆盖真实部署中的：

- distribution shift；
- long-tail failures；
- 新对象 / 新布局 / 新任务变化；
- multi-minute long-horizon error accumulation；
- human correction / intervention；
- 真实机器人执行中的 failure / recovery。

LWD 的问题定义是：

> 如何让一个已经预训练好的 generalist VLA，在真实部署过程中持续吸收多机器人、多任务的经验，并不断提升同一个共享策略？

---

## 3. 关键创新

### 3.1 Fleet-scale Learning While Deploying

不是单机器人 task-specific RL，而是：

- 16 台双臂机器人；
- 8 个真实任务；
- 多任务经验进入同一个 online replay；
- 中央 learner 更新一个 shared generalist policy；
- 新 checkpoint 周期性重新部署到 fleet。

最重要的系统思想：

> **一个机器人踩过的坑，应该变成整个 fleet 的经验。**

### 3.2 Offline → Online 使用统一 RL 目标

Stage 1 的 offline buffer 包含：

- expert demonstrations；
- historical policy rollouts（成功 + 失败）；
- play data（人为探索 failure modes）。

先训练 policy、critic 与 distributional value，再进入 online stage。

长程任务离线阶段使用更长的 n-step chunk TD 来加速稀疏 terminal reward 的传播；online 阶段则使用 1-step chunk-level TD。

Online 阶段：

- autonomous rollout；
- human intervention；
- 全部进入 online buffer；
- learner 使用 offline + online mixed replay，论文实现约 1:1。

### 3.3 DIVL：Distributional Implicit Value Learning

Fleet 数据高度 heterogeneous，同一相似状态可能因为未观测因素导致成功、失败或恢复。

DIVL 不只预测单一标量 V，而是学习 return distribution：

```
p(v | s)
```

然后用 quantile 作为 bootstrap。

作者还使用 adaptive τ：

- value distribution entropy 高 → 更保守；
- entropy 低 → 更 optimistic。

直观理解：

> **确定的时候敢乐观，不确定的时候保守。**

### 3.4 QAM：让 Q-gradient 更新 Flow-based VLA

π0.5 action expert 是 flow-based generator。

直接把 critic gradient 通过完整 flow / ODE solver 反传既贵又不稳定。

QAM：

1. Critic 在最终 action 给出 `∇a Q(s,a)`；
2. 通过 adjoint dynamics 把改进方向沿 flow trajectory 传播；
3. 把 trajectory-level optimization 转成 vector field 的 local regression targets；
4. 更新 action expert。

因此 LWD 不只是外挂 residual actor，而是试图把 reward / Q-value 真正写回 flow-matching VLA 的动作生成过程。

Online QAM 中：
- policy VLM backbone 冻结；
- action expert 更新；
- value / critic 继续适应 mixed replay。

---

## 4. 最重要实验结果

设置：

- 16 台 Agibot G1；
- 8 个真实任务；
- 4 个 grocery restocking；
- 4 个 3–5 分钟 long-horizon tasks；
- 30 Hz joint-position control；
- 每个 online experiment 4 小时 wall-clock；
- 约 60 robot-hours online data。

主要结果：

| 方法 | 8任务平均 |
|---|---:|
| SFT | 0.76 |
| RECAP | 0.85 |
| HG-DAgger | 0.85 |
| LWD Offline | 0.88 |
| **LWD Online** | **0.95** |

Long-horizon 平均：
- SFT：0.68
- HG-DAgger：0.73
- LWD Offline：0.79
- **LWD Online：0.91**

真正重要的是：

> 同一个 generalist policy 可以随着共享 fleet experience 持续提升，而不是每个任务单独训练一个 specialist。

---

## 5. 对“具身自进化”的启发

### 5.1 部署本身就是训练阶段

```
Deploy
→ Generate Experience
→ Evaluate
→ Learn
→ Redeploy
```

### 5.2 Physical Experience 是可积累资产

LWD 利用的不只是成功 demo，还包括：

- autonomous success；
- autonomous failure；
- play data；
- human intervention。

### 5.3 从 Local Adaptation 走向 Generalist Evolution

可以把我们当前路线理解成：

```
RLT
= Individual / Local Policy Adaptation

PLD
= Improved Experience → Foundation Consolidation

LWD
= Fleet / Generalist Policy Evolution
```

---

## 6. 最值得借到当前项目的 5 点

### A. 从 Phase 0 就统一 transition schema

不同 RoboTwin2 task 最好统一为：

```
(task_id,
 observation,
 executed_action_chunk,
 reward,
 done,
 success/failure,
 source=policy/human/recovery,
 checkpoint_version)
```

以后才可能 pooled replay。

### B. 不要只保存成功 demo

系统记录：

- success；
- failure；
- near-failure；
- recovery；
- intervention；
- terminal reason。

这直接支持 Phase 1 D4。

### C. Critic / Value 可以成为 Failure Diagnosis 工具

除 success rate 外，未来可以看：

> value 是否随 progress 上升？failure onset 前是否 plateau / drop？

### D. Offline → Online 尽量共用 learner / data contract

从现在开始让：

- offline demo；
- online rollout；
- human / scripted recovery

进入统一 transition interface。

### E. 把 Experience Selection 提前列为未来研究问题

LWD 是“经验汇聚”，但我们还可以继续问：

- 哪些 experience 值得 replay？
- failure / recovery 是否应更高优先级？
- 经验是否要先经过 validation gate？
- 多任务 pooled replay 是 transfer 还是 interference？

---

## 7. 现在不要照搬的部分

暂时不要直接复制：

- 16-robot fleet；
- full QAM；
- shared multi-task online learner；
- generalist action-expert online update。

当前项目最缺的仍然是：

1. RoboTwin2 Multi-task RLT baseline；
2. failure profile；
3. 明确真正 bottleneck。

所以 LWD 是 **Phase 3 / North-Star reference**，不是 Phase 0 替代路线。

---

## 8. 作者明确给出的未来方向

1. 当前 online update schedule 仍较直接；长期、大规模持续学习需要更高效稳定的 update strategy。
2. Long-horizon task 仍主要由单一短语言 instruction 驱动；未来需要更强 vision-language reasoning、task decomposition、closed-loop prompts 与 error recovery。
3. 当前没有显式建模 execution safety；未来需要 safety-aware learning / control。

---

## 9. 我们后续最值得追的 5 个问题

1. 哪些 deployment experience 值得进入长期 replay？
2. failure / recovery 是否应该比普通成功 rollout 更高优先级？
3. 一个任务的 value / correction / consequence 能否迁移到另一个任务？
4. 什么时候经验进入 Fast Memory，什么时候通过 RL 写入 policy？
5. 什么时候 specialist improvement 应 consolidation 回 generalist VLA？

---

## 10. 在我们的 Self-Evolution Map 中的位置

```
Zeva
Context Evolution
        ↓
RLT / SmoothRL
Local Policy Evolution
        ↓
PLD
Policy → Foundation Consolidation
        ↓
LWD
Fleet / Generalist Experience Flywheel
```

LWD 最重要的意义：

> **部署不是训练结束之后的终点，而可以成为持续产生 Physical Experience、更新 generalist policy 的下一阶段训练场。**

# Odyssey-3：Foundation World Model / Physical Agents

> 阅读日期：2026-09-16  
> 类型：公司官方研究博客 + 公众号转述  
> 项目关系：**World-model / representation frontier；当前不改变 Universal Physical Token 的 Gate 0 → B0 → B1 → B2。**

## 0. Source confidence

Odyssey 官方在 2026-09-15 发布了 `Introducing Odyssey-3: A General-Purpose Physical Intelligence`。官方页面明确描述：Odyssey-3 是一个 autoregressive diffusion transformer foundation world model，预训练在大规模世界视觉观测上，并通过不同任务的小型 action decoder / task policy 适配机器人、Humanoid、车辆、无人机和游戏。

本文公众号对公司背景、融资和“通用物理智能”叙事有大量扩展。项目知识库只记录官方技术页直接支持的结构和结果；融资、估值、团队规模等不是当前研究问题，不进入方法证据层。

---

## 1. 核心结构

官方描述的核心不是“一个模型直接输出所有本体动作”，而是：

```text
large pretrained world model
          ↓
shared internal representation
          ↓
small task / embodiment-specific action decoder
          ↓
robot / humanoid / car / drone / game controls
```

官方称：

- Odyssey-3 是 autoregressive diffusion transformer；
- 预训练学习物理、动力学、因果、人类行为等世界知识；
- 任务适配阶段用 physical-system observation + action experience；
- learned action decoder 把内部 representation 转成目标系统动作；
- 某些实验中保持 pretrained world-model backbone frozen，只训练相对小的下游 policy / action expert。

这个范式与当前项目的“共享 compact representation + lightweight adapter / learner”在抽象层面有相似性，但读出位置完全不同：

- Odyssey：**world-model backbone representation → action decoder**；
- 当前项目：**existing action-generation head → Physical Token readout → small online learner**。

所以它是强 related work，不是当前方法的直接替代。

---

## 2. 官方报告的机器人相关信号

官方称使用 tens of hours 的机器人 demonstration 后，可以控制多种 robot arms，并观察到训练示范中没有显式出现的 recovery，例如：

- missed grasp 后重新调整夹爪；
- 从不常见位置 / 姿态找回掉落物体。

这可以支持一个较谨慎的解释：

> broad pretraining representation 可能携带可被下游 action decoder 复用的空间、运动和 cause-effect prior。

但不能从这些 demo 直接推导：

- 模型已经显式学会 Newton / friction law；
- recovery 来自可辨识的物理参数；
- 跨机器人 transfer 已有严格统一 benchmark 证明。

官方也明确把跨不同 body / viewpoint / control 的稳定性列为仍需评估的问题。

---

## 3. 跨系统适配的官方例子

官方页面还报告：

- Humanoid：使用数十小时 teleoperation data，结合 Flexion 的 robot learning / control；
- Driving：20 小时 simulated driving data，world-model backbone frozen，small driving policy 输出 waypoints；
- Drone：数十小时模拟飞行数据，policy 从 recent camera history + motion state + high-level prompt 输出 waypoints；
- Game：冻结 pretrained world model，通过游戏录像 + keyboard/mouse control 训练策略。

其真正值得当前项目注意的不是具体 demo，而是同一个假设：

> **强 pretrained physical/world representation 能否让不同 embodiment 的 task-specific adaptation 变得更轻量？**

这与我们未来的 `Universal = shared token shape/objective + lightweight model/robot adapters` 是一个相邻问题。

---

## 4. 对 Universal Physical Token 最直接的三个启发

### 4.1 更加强化 `backbone tap vs action-head tap` 必须做

当前项目领导版假设 Physical Token 应优先从 action head pre-output feature 读取，因为它更接近动作生成。

Odyssey-3 则代表另一种强假设：

> **pretrained world-model backbone 本身可能已经承载大量可迁移的 physical / spatial / dynamics prior。**

因此我们不能默认 action-head tap 一定更好。

第一轮必须保留：

```text
Backbone feature readout
vs
Action-head feature readout
```

并在相同 token size / decoder capacity / dataset 下比较 transition prediction 与 online adaptation。

这是 Odyssey-3 对当前主线最直接、最有价值的压力测试。

### 4.2 “Universal”更应该定义成 adapter-efficient transfer，而不是同一个 action head 到处直接用

Odyssey-3 的跨系统故事并不是：

```text
one exact decoder → every embodiment
```

而是：

```text
shared foundation representation
+
small system-specific action component
```

这和我们现在对 Universal 的严格定义一致：

```text
shared token shape
+ shared physical objectives
+ lightweight model-family adapter
+ lightweight robot/control adapter
```

因此未来真正有意义的指标不只是 success，还应包括：

- 新 embodiment 所需可训练参数量；
- task-specific data amount；
- adaptation steps / interaction cost；
- token representation 是否需要重训；
- old embodiment retention。

### 4.3 recovery 只能作为 representation prior 的证据线索，不能直接变成“学会物理规律”的结论

Odyssey 的 recovery demo 很吸引人，但当前项目如果要声称 Physical Token 捕获了 physics，需要更严格：

```text
B0 matched readout
vs
B1 + measured transition
vs
B2 + valid physics
```

并报告 held-out transition / physical violation / online adaptation。

不能把 qualitative recovery video 当作 physics understanding 的替代证据。

---

## 5. PROWL / recursive self-improvement：长期相关，但现在后置

Odyssey 官方把 PROWL 描述成 world model 与 agent 的相互提升：

```text
agent explores world model
→ exposes simulator failures
→ improve world model
→ better simulator generates richer experience
→ improve agent
→ repeat
```

这和长期 `Real Experience + Imagined Experience` / recursive improvement 方向高度相关。

但它属于更远的 system-level self-evolution：

- 需要可信 world model；
- 需要 simulator validity / uncertainty；
- 需要 experience validation gate；
- 需要把真实和 imagined transition 分开追踪。

因此当前只保留为 North-Star related work，不进入第一轮 Physical Token 方法。

---

## 6. 对当前项目的实际动作

**不改变当前执行顺序。**

继续：

```text
Gate 0 trustworthy hammer/RLT baseline
→ B0 matched compact readout
→ backbone vs action-head tap
→ B1 measured transition grounding
→ B2 valid physics grounding
→ physical/contact shift
→ held-out model family / embodiment
```

Odyssey-3 主要增加两个未来问题：

1. action-head readout 是否真的比 strong backbone readout 更适合 physical adaptation？
2. 如果 representation 足够通用，新 embodiment 到底只需多小的 adapter / 数据预算？

这两个问题都可以纳入 Universal hypothesis 的后半程，而不影响当前 Gate 0。
# Universal Physical Token：领导约束后的研究主线

> 版本：2026-09-14  
> 状态：**当前项目主规范 / Source of Truth**  
> 说明：本页根据领导提供的两份 Physical Token PPT 整理。此前 Research OS 中更宽泛的“Physical Experience / Self-Evolution / 多阶段探索”只保留为历史与知识库背景，不再覆盖本页定义的主线。

---

## 0. 核心命题

当前项目要回答的不是“预训练 action model 有没有能力”，而是：

> **在不重新训练 action model 的前提下，能否用一个轻量、可复用的 Physical Token 接口，让机器人适应变化的接触动力学，并在在线交互中持续改进行为？**

核心思路：

```text
Frozen action model
      ↓
Action-head pre-output features
      +
Recent robot history
      +
Robot metadata / control convention
      ↓
Lightweight adapters + learned readout
      ↓
Fixed-size Physical Token z_t
      ↓
Small online learner
      ↓
Behavior adaptation
```

这里的重点是：**Physical Token 是 action-generation head 上的紧凑 readout，不是一个泛化到任意物理规律的“大而全世界模型”。**

---

## 1. Physical Token 放在哪里？

### 1.1 首选位置：Action Head

定义 action head 在最终动作投影之前的因果特征：

```text
F_t^head
```

Physical Token 的候选形式：

```text
z_t = E_phi(A_m(F_t^head), h_t, r)
```

其中：

- `F_t^head`：action head 的 pre-output / pre-projection 特征；
- `A_m`：不同 model family 的轻量 feature adapter；
- `h_t`：近期 robot state + actual/executed-action history；
- `r`：robot morphology、action convention、control metadata；
- `E_phi`：learned readout / learned queries；
- `z_t`：固定 `K × d` 形状的小型连续 latent，供后续在线 learner 使用。

### 1.2 不同 action model 的读出约定

- Regression / MLP：penultimate activations；
- Diffusion / Flow：固定采样时刻的中间特征，并显式包含 noise/time context；
- Autoregressive action model：使用当前可用的 causal states before logits，禁止读取未来示范动作；
- World model 只有在暴露明确 action-generation module 时才纳入这一接口。

### 1.3 必须做的对照

Action-head readout 是研究假设，不是默认真理。

因此必须比较：

```text
Backbone tap
vs.
Action-head tap
```

因为 action head 也可能在生成动作前丢掉部分物理信息。

---

## 2. “Universal” 到底是什么意思？

当前只能定义为：

> **共享 token shape + 共享 physical objectives + 每个 model family / robot 只使用轻量 adapter。**

不能提前宣称：

- 已经跨模型泛化；
- 已经跨本体泛化；
- 一个 token 可以直接无修改迁移所有 action model。

跨 head family 与跨 embodiment transfer 都必须通过 held-out 实验验证。

因此：

> **Universal 是 empirical hypothesis，不是现有结果。**

---

## 3. Physical Token 如何训练？

总目标：

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

### 3.1 L_ro：Readout / Reconstruction

作用：保留 action-head 中已有的任务与动作相关信息。

要求：

- reconstruction target 为 fixed / stop-gradient head features；
- reconstruction 不允许反向修改 base action model；
- token capacity 与 baseline 严格匹配。

### 3.2 L_dyn：Measured Transition Prediction

这是首个需要验证的“物理 grounding”。

使用 action-conditioned decoder：

```text
D(z_t, u_t, r) -> measured future physical state
```

其中 `u_t` 必须对应 **actual / executed action**，目标来自真实测得的后续状态，而不是模型计划动作或未来泄漏。

第一阶段优先预测：

- measured joint / end-effector motion；
- relative motion；
- action execution outcome；
- 其他可由当前 robot state 与可靠传感器直接得到的 transition quantity。

要求：

- validity mask；
- physical-unit normalization；
- terminal / reset 边界严格处理；
- 不跨 episode 做差分。

### 3.3 L_phys：Physics Constraints

第一版只使用**有可靠模型或测量依据**的约束。

优先：

1. **Kinematic consistency**

```text
L_kin = || v_EE - J(q) q_dot ||^2
```

要求所有量在同一 frame / convention 下。

2. **Actuator feasibility**

惩罚：

- joint limit violations；
- speed limit violations；
- 其他明确存在的 actuator/control constraints。

可选但不默认加入：

- contact / friction residual；
- rigid-body dynamics residual；
- force / torque consistency。

只有在对应的 sensing、model、calibration 都有效时，才能把这些项写入主实验。

---

## 4. Online Self-Improvement 的严格定义

当前项目里的 self-evolution / self-improvement 指：

> **冻结大 action model，通过 Physical Token + 小型在线 learner，在真实交互后持续改进行为。**

在线阶段默认：

- freeze base model；
- freeze action head；
- freeze token encoder / readout；
- update small actor / critic；
- learner 使用实际 executed actions 与 task rewards；
- physical regularization 作用在 predicted action outcomes 上。

Outcome decoder 的处理：

- 用 measured transitions 单独训练；
- actor optimization 时冻结 decoder weights；
- 但保留 decoder 对 action 的梯度，以便约束 action optimization；
- execution hard limits 与 learned physical regularization 分开实现。

若后续 consolidation 改变 token representation，旧 replay feature 需要重新编码，不能混用旧 token cache。

---

## 5. 第一组必须做的实验

领导给出的初始比较固定为：

```text
B0  RL Token / matched readout baseline
B1  B0 + transition loss
B2  B1 + physics loss
```

必须 matched：

- token size；
- policy / learner capacity；
- base action model；
- training data；
- online interaction budget；
- seed policy；
- task reward；
- control frequency / chunk convention。

主要指标：

- task success；
- physical violations；
- adaptation time / interaction cost；
- old-task retention；
- repeated seeds；
- uncertainty / confidence intervals。

优先实验顺序：

1. 先在已复现的 RL Token 任务上完成 B0/B1/B2；
2. 再引入明确的 physical shift / contact-dynamics shift；
3. Physical Token 在单模型/单本体成立后，再做 held-out model head family；
4. 最后做 held-out robot embodiment，检验 Universal hypothesis。

---

## 6. 当前已有结果如何解释？

现有 block assembly、drawer opening + placement 视频属于：

> **RL Token qualitative reproduction / baseline demonstrations**

它们不能被写成：

- Physical Token result；
- transition loss result；
- physics loss result；
- Universal transfer result。

Hammer 等已有工程资产可以继续用于：

- pipeline regression；
- physics field / transition logging；
- later controlled ablation；

但它们不自动定义当前主研究故事。

---

## 7. Streaming RL 的位置

早期路线中包含：

```text
SAC / replay -> Streaming Actor-Critic
batch≈1 / no replay / chunk-boundary update
```

但当前第一轮验证的主问题是：

> **Physical Token 的 transition / physics grounding 是否真的比 RL Token readout 带来稳定增益？**

因此当前不把 Streaming RL 与 Physical Token 同时作为首轮变量。

推荐顺序：

```text
先证明 Physical Token representation / online adaptation 增益
        ↓
再比较 replay learner vs streaming learner
        ↓
最后研究 uncertainty-aware update strength / safety fallback
```

Streaming RL 保留为后续 online-efficiency 方向，而不是第一组 Physical Token 实验的必要条件。

---

## 8. 当前不允许的过度叙事

除非有对应实验，否则公开仓库不写：

- “机器人已经学会物理规律”；
- “Universal Physical Token 已适配所有 action model”；
- “Physical Token 已经提升成功率”；
- “Contact / friction law 已被模型显式掌握”；
- “系统已经完成开放环境持续自进化”；
- “Streaming RL 一定优于 replay”。

当前准确表述应为：

> **我们提出并验证一个 action-head Physical Token 假设：通过 measured transition prediction 与有效 physics constraints 对 compact readout 进行 grounding，再让轻量在线 learner 在冻结 action model 的条件下适应变化的接触动力学。**

---

## 9. 当前执行顺序

```text
RLT reproduction / baseline audit
    ↓
Action-head extraction contract
    ↓
B0 matched RL Token / head-readout baseline
    ↓
B1 + measured transition prediction
    ↓
B2 + valid physics constraints
    ↓
Online actor-critic matched-budget comparison
    ↓
Physical shift / contact-dynamics shift
    ↓
Held-out model family
    ↓
Held-out embodiment
    ↓
Streaming RL / uncertainty-aware update（后续）
```

本页优先级高于此前由 Research OS 自动扩展出的四阶段 Physical Experience 路线。旧内容保留作历史记录与 related-work / idea pool，不再作为当前实验主规范。

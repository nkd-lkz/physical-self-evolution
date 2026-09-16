# Universal Physical Token：领导约束后的研究主线

> 版本：2026-09-16  
> 状态：**当前项目主规范 / Source of Truth**  
> 说明：本页根据领导提供的 Physical Token 方案与后续讨论持续维护。此前 Research OS 中更宽泛的“Physical Experience / Self-Evolution / Agent/Harness / 多阶段探索”只保留为历史与知识库背景，不再覆盖本页定义的主线。

---

## 0. 核心命题

当前项目要回答的不是“预训练 action model 有没有能力”，也不是“能否用更强通用模型做高层 planner”，而是：

> **在不重新训练 action model 的在线适应阶段，能否从 actor / action-generation head 提取一个轻量、可复用的通用 Physical Token，通过物理 grounding + 小型在线 learner，最终提升机器人在物理交互任务中的成功率？**

核心思路：

```text
Frozen action model / actor
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
Better physical adaptation / task success
```

这里的重点是：**Physical Token 是 actor / action-generation head 上的紧凑 readout，不是一个高层 planner，也不是一个泛化到任意物理规律的“大而全世界模型”。**

### 0.1 当前工程前置：Gate 0 — Baseline Recovery

领导定义的 B0/B1/B2 科学问题不变，但当前已有 hammer RLT 工程结果暴露出两个必须先解决的 baseline 问题：

1. **执行协议混杂**：已有 Stage1 使用 `H=50`；RoboTwin 原生 TOPP 下 `H50/C10` 与 `H50/C50` 会产生不同规划边界、物理时长和再观测分布，因此不能把历史 H50/C10 零成功直接解释成 Stage1 权重失效。
2. **Stage1 capability 风险**：协议对齐后的开发配对中已经出现 SFT20k 成功、旧 Stage1 2k 失败的场景；同时也存在二者都成功的正对照。因此旧 Stage1 不是完全不可用，但还不足以成为稳定 B0 reference。

因此当前执行顺序增加：

```text
Gate 0A  恢复可用 Stage1 reference
       ↓
Gate 0B  固定 execution / timing semantics
       ↓
Gate 0C  建立可信 B0 online baseline
       ↓
B1      + measured transition loss
       ↓
B2      + valid physics loss
```

当前 Stage1 recovery 方案：generic `pi05_base` + `rlt_alpha=1`，20k joint training，global batch64；checkpoint 按固定 seed 的 `H50/C50` 闭环能力曲线选择，不按最低训练 loss 选择。

**Gate 0 不是新的科研主张，只是为了让 B0/B1/B2 的比较可解释。**

### 0.2 领导最新边界：Planner / Harness 路线与本项目有本质区别

针对 GPT-6 Astra + π0.5、Harness VLA、SHAPER 等工作，领导明确要求：

> **这些工作主要是在看 planner / orchestration 怎么使用已有具身策略；本项目不是做 planner，而是从 actor 里提取通用 token，并用它提升最后的物理交互成功率。**

因此当前统一边界为：

```text
Astra / Harness / Agent route:
observation + history + candidate skill/action
        ↓
planner / reviewer / orchestration
        ↓
决定“调用谁、何时重试、是否修正”

Our route:
actor / action-generation features
        ↓
Universal Physical Token
        ↓
physical grounding + lightweight online learner
        ↓
提升 actor-side physical adaptation / final success
```

由此产生三条维护规则：

1. Astra / Harness / SHAPER 继续阅读，主要用于理解别人如何组织 planner、memory、retry、correction 与 execution harness；
2. 不把它们的 zero-shot reasoning、LLM planner、memory 或 skill evolution 直接并入第一阶段方法；
3. 如果借鉴其中的 failure diagnosis / operating-range / validation 思想，优先作为 **diagnostic / analysis tool**，不能替代 B0/B1/B2 的 actor-side representation 实验。

这条边界优先于任何由论文阅读衍生出的“把大模型 planner 接到当前系统里”的扩展想法。

---

## 1. Physical Token 放在哪里？

### 1.1 首选位置：Action Head / Actor Side

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

1. 先通过 Gate 0 得到可信 B0；
2. 在同一任务上完成 B0/B1/B2；
3. 再引入明确的 physical shift / contact-dynamics shift；
4. Physical Token 在单模型/单本体成立后，再做 held-out model head family；
5. 最后做 held-out robot embodiment，检验 Universal hypothesis。

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

旧 Stage2 C10 run 当前只作为工程闭环证据，不作为 B0 性能基线。

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
- “Streaming RL 一定优于 replay”；
- “旧 Stage2 零成功证明 RLT 缺 physics”；
- “Stage1 训练步数不足已经被证明是唯一根因”；
- “GPT-6 Astra / Harness planner 的结果直接验证了 Physical Token”；
- “本项目要通过增加大模型 planner 获得主要性能提升”。

当前准确表述应为：

> **我们提出并验证一个 actor-side action-head Physical Token 假设：通过 measured transition prediction 与有效 physics constraints 对 compact readout 进行 grounding，再让轻量在线 learner 在冻结 action model 的条件下适应变化的接触动力学，并以最终任务成功率验证其价值。**

---

## 9. 当前执行顺序

```text
Gate 0 · trustworthy RL Token baseline
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

Planner / Harness / general-model orchestration 始终保持在 Frontier / system-extension 层，除非后续单独立项，不进入上述首轮因果链。

本页优先级高于此前由 Research OS 自动扩展出的四阶段 Physical Experience 路线。旧内容保留作历史记录与 related-work / idea pool，不再作为当前实验主规范。

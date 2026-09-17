# Universal Physical Token：领导约束后的研究主线

> 版本：2026-09-17  
> 状态：**当前项目主规范 / Source of Truth**  
> 说明：本页根据领导提供的 Physical Token 方案、后续讨论与最新实验事实持续维护。此前 Research OS 中更宽泛的 Physical Experience / Self-Evolution / Agent/Harness / World Model 路线只保留为历史与知识库背景。

---

## 0. 核心命题

当前项目要回答的不是“预训练 action model 有没有能力”，也不是“能否用更强通用模型做高层 planner”，而是：

> **在不重新训练 action model 的在线适应阶段，能否从 actor / action-generation head 提取一个轻量、可复用的通用 Physical Token，通过 measured transition 与可靠 physics constraints 做 grounding，再由小型 online learner 提升机器人在物理交互任务中的适应效率与最终成功率？**

```text
Frozen action model / actor
      ↓
Action-generation / action-head features
      +
Recent measured robot history
      +
Actual / executed-action history
      +
Robot / control metadata
      ↓
Lightweight adapter + learned readout
      ↓
Fixed-size Physical Token z_t
      ↓
Small online actor / critic
      ↓
Better physical adaptation / task success
```

Physical Token 是 **actor-side compact interface**，不是高层 planner，也不是完整 world model。

---

## 0.1 当前工程前置：Gate 0 — Baseline Recovery / Validation

领导定义的 B0/B1/B2 科学问题不变，但正式消融前必须先得到可信 RLT baseline：

```text
Gate 0A  Recover & validate Stage1 reference
       ↓
Gate 0B  Fix execution / timing semantics
       ↓
Gate 0C  Establish trustworthy B0 online baseline
       ↓
B1      + measured transition grounding
       ↓
B2      + valid physics grounding
```

### 2026-09-17 最新 Stage1 证据

旧 clean50 `pi05_base + alpha1` 长程 Stage1 未完成原计划20k，最终停在约12.3k。统一 20-seed、`H50/C50 native_macro`、固定 prompt/action-sampling seed 的开发结果：

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

12k 只是当前 development candidate。曲线非单调、n=20有限且仍有10/20失败，因此不能宣布 Stage1 泛化已解决，也不能把训练量/数据量/联合损失写成唯一根因。

### 新 clean490 baseline recovery

clean500 全量质量审计后排除10条强动作轨迹异常，正式开发数据改为：

```text
clean490
├─ train450
└─ eval40
```

norm 只使用 train450。

下一轮 Stage1 仍保持论文/官方拓扑：generic `pi05_base + rlt_alpha=1`，H50、global64、dual-GPU，最新默认 max30k、warmup1k、每5k保存；正式GPU训练尚未启动。checkpoint 仍按闭环能力选择，不按最低 train loss。

Gate 0 是实验可解释性的前置，不改变 Physical Token 的科学主张。

---

## 0.2 Planner / Harness 与本项目的边界

针对 GPT-6 Astra + π0.5、Harness VLA、SHAPER 等工作，领导明确：

> **这些路线主要研究 planner / reviewer / orchestration 怎么使用已有具身策略；本项目不是做 planner，而是从 actor 里提取通用 token，并用它提升最后的物理交互成功率。**

因此：

```text
Astra / Harness route:
observation + history + candidate action
→ planner / reviewer
→ accept / retry / replan / correction

Our route:
action-generation features
→ Universal Physical Token
→ physical grounding
→ lightweight online learner
→ final physical-task success
```

Astra / Harness / SHAPER 可用于 failure diagnosis、operating-range 和 validation-gate 启发，但不进入第一轮 B0/B1/B2 方法变量。

---

## 1. Physical Token 放在哪里？

### 1.1 首选：Action Head / Action Expert

定义最终动作投影前的因果 feature：

```text
F_t^head
```

候选形式：

```text
z_t = E_phi(A_m(F_t^head), h_t, r)
```

其中：

- `F_t^head`：action-generation pre-output / pre-projection features；
- `A_m`：不同 model family 的轻量 adapter；
- `h_t`：recent measured state + actual/executed-action history；
- `r`：robot morphology / action convention / control metadata；
- `E_phi`：learned readout / learned queries；
- `z_t`：固定 `K × d` compact latent。

### 1.2 不同 action model 的 extraction contract

- Regression / MLP：penultimate activations；
- Diffusion / Flow：固定 sampling time 的中间 feature，并显式包含 noise/time context；
- Autoregressive：logits 前的 causal states；
- 禁止 future demonstrated actions / future observations leakage。

### 1.3 必须保留的对照

```text
Backbone tap
vs.
Action-head / Action-Expert tap
```

“离 action 更近就更懂物理”是研究假设，不是事实。

---

## 2. Universal 的严格定义

当前只允许定义为：

> **shared token shape + shared physical objectives + lightweight model/robot adapters**

不能提前宣称：

- 已经跨模型泛化；
- 已经跨本体泛化；
- 一个 token 无修改适配所有 action models。

Universal 是 empirical hypothesis，需要 held-out model family / task / embodiment 逐级验证。

---

## 3. Physical Token 如何训练？

总目标：

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

### 3.1 `L_ro` · Readout / Reconstruction

作用：保持 action-generation representation 中已有任务/动作信息。

要求：

- target 为 stop-gradient base feature；
- reconstruction 不更新 base action model；
- token/readout capacity 与 baseline matched。

### 3.2 `L_dyn` · Measured Transition Prediction

这是第一项真正需要验证的 physical grounding：

```text
D(z_t, u_t^exec, Δt, r) -> measured future physical outcome
```

#### 必须区分四类量

```text
reference / proposed action
actual executed action
command state
measured state
```

当前 Stage1 imitation dataset 的 state 仍保留原 command / drive-target 语义；B1 的 actual qpos / EEF / object consequence 必须显式从 sidecar / rollout measurement 读取，不能把 command target 改名成 measured state。

第一版优先 target：

- measured Δq / qdot；
- measured EE motion；
- relative robot-object motion；
- action execution discrepancy；
- 可靠的 action outcome / event。

要求：

- per-target validity mask；
- train-only normalization；
- terminal/reset边界隔离；
- 真实未来观测只能作label；
- target时间区间必须与实际执行的action sequence一致。

### 3.3 `L_phys` · Physics Constraints

第一版只使用有可靠定义、单位和模型依据的约束。

优先：

1. **Kinematic consistency**

```text
L_kin = ||v_EE - J(q) q_dot||²
```

或等价 FK consistency。

2. **Actuator / Controller feasibility**

- joint limit；
- speed limit；
- known action bounds；
- 其他明确 control constraints。

暂不默认加入：

- friction law residual；
- contact dynamics residual；
- full rigid-body dynamics；
- force/torque consistency。

只有 sensing、model、calibration 都有效时才加入。

---

## 3.4 2026-09-17 新增：Physics label validity 是方法合同的一部分

clean500 全量审计显示：

- 轨迹动作连续性可以合格；
- contact/impulse label 仍可能证据不足；
- `contact=0` 不一定等价于“没有几何接触/任务失败”。

因此所有物理监督必须支持：

```text
trajectory_valid
label_valid[k]
```

缺失/弱标签不能填0当真值。

这意味着：

- action learning 可以保留一条轨迹；
- contact-specific loss 可以对同一轨迹 mask；
- 其他可靠 transition targets 仍可使用。

这种 per-label validity 必须贯穿数据转换、loss、metric 与结果解释。

---

## 4. Online Self-Improvement 的严格定义

当前 self-improvement 指：

> **冻结大 action model，通过 Physical Token + 小型 online learner，利用真实交互持续改进行为。**

在线阶段默认：

- freeze base model；
- freeze action head；
- freeze token encoder / readout；
- update small actor / critic；
- learner 使用 actual executed action 与 task reward；
- replay 对齐真实执行后的 next state / terminal。

如果 outcome decoder 用于 actor regularization：

- decoder weights 在 actor update 时冻结；
- 保留 decoder 对 candidate action 的 gradient；
- decoder 自己用 measured transitions 单独更新；
- hard execution limits 由 controller / environment 独立保证。

如果后续 representation 本身更新，旧 replay token cache 需要重编码或版本化，不能混用。

---

## 5. 第一组必须做的实验

领导定义的主比较：

```text
B0  RL Token / matched readout baseline
B1  B0 + measured transition loss
B2  B1 + valid physics loss
```

为隔离 action-head tap 本身，还需要：

```text
B0-RLT   original / matched RL Token
B0-Head  same capacity, action-head tap, no physical grounding
B1       B0-Head + transition grounding
B2       B1 + valid physics grounding
```

必须 matched：

- token size / readout capacity；
- base model/reference；
- actor/critic；
- offline data；
- online interaction budget；
- reward；
- environment/action seeds；
- H/C/timing/execution semantics。

主要指标：

- task success；
- adaptation curve / interaction cost；
- physical violations；
- completion time；
- failure type；
- old-condition retention；
- repeated seeds / confidence intervals。

---

## 6. Representation evidence

除了最终 success，还需要证明 token 的信息确实变了：

- held-out transition prediction；
- action-conditioned consequence ranking；
- contact/slip event AUPRC（仅可靠标签）；
- failure-onset probe；
- base-policy operating-range probe；
- dynamics-shift probe。

真正的证据链应是：

```text
physical grounding
→ representation contains more decision-relevant consequence information
→ critic / action ranking improves
→ online adaptation improves
→ task success improves
```

辅助loss下降本身不能证明Physical Token有效。

---

## 7. Actor / Critic 怎么使用？

首轮完全沿用matched RLT接口，只替换 compact representation：

```text
Actor:
[z, proprio/history, reference chunk] → action

Critic:
[z, proprio/history, candidate action] → Q
```

这样 B0→B1→B2 的主要变化是 token supervision，而不是 RL algorithm。

后续再单独比较：

- actor + critic 都用 Physical Token；
- actor 用 RL Token、critic 用 Physical Token；
- actor 用 Physical Token、critic 用 RL Token。

Physical-aware critic 是有潜力的后续方向，但不应与第一轮表示实验同时改变。

---

## 8. 当前已有结果如何解释？

### 已有证据

- RL Token reproduction clips：只作 qualitative baseline；
- old Stage2 C10：只证明工程闭环；
- Stage1 6k–12k unified eval：证明部分 closed-loop capability；
- clean500→clean490：证明数据质量与物理标签有效性需要分层审计；
- new clean490 Stage1：CPU/data/config准备完成，GPU训练未启动。

### 当前没有的证据

- Physical Token 训练结果；
- B1/B2 success gain；
- physical-shift adaptation gain；
- cross-task/model/embodiment universality。

---

## 9. Streaming RL 的位置

首轮只回答 representation grounding：

```text
B0 → B1 → B2
```

之后再比较：

```text
Replay learner
vs.
Low-replay / Streaming learner
```

Streaming、no-replay、batch≈1、uncertainty-aware update 都是后续 online-efficiency 变量，不与第一轮 Physical Token 同时改变。

---

## 10. 当前执行顺序

```text
12k full-physics failure analysis
        ↓
clean490 Stage1 30k-max training
        ↓
5k...30k eval40 development curve
        ↓
independent final reference validation
        ↓
B0 trustworthy online RLT baseline
        ↓
B0-Head matched tap baseline
        ↓
B1 measured transition grounding
        ↓
B2 valid physics grounding
        ↓
controlled physical shift
        ↓
held-out task/model/embodiment
```

RoboDojo 作为第二平台继续按自身 Gate 推进，不阻塞当前 Hammer 核心假设验证。

---

## 11. 当前禁止的过度叙事

除非有对应实验，否则公开仓库不写：

- “机器人已经学会物理规律”；
- “Universal Physical Token 已适配所有 action model”；
- “Physical Token 已经提升成功率”；
- “Contact / friction law 已被模型显式掌握”；
- “clean500 500条全部是高质量示范”；
- “contact=0 就是无接触”；
- “12k显著优于其它Stage1 checkpoint”；
- “数据扩充已提高最终成功率”；
- “旧Stage2 success=0证明RLT缺physics”；
- “GPT-6 Astra / Harness planner 结果直接验证Physical Token”。

当前准确表述：

> **我们以 RLT 为 baseline，研究从 actor/action-generation pathway 提取的 compact representation 是否能通过真实 measured action consequence 与可靠 physics constraints 被 grounding，并在 matched lightweight online RL 中提高物理适应效率与最终任务成功率。当前仍在完成可信 baseline 和数据监督合同。**

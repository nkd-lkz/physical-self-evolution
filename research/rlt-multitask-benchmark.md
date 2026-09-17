# RL Token Baseline & Universal Physical Token Initial Validation

> 当前角色：**Baseline / Initial Validation Protocol**  
> 上位主线：[`physical-token-leadership-spec.md`](physical-token-leadership-spec.md)  
> 当前执行：**Gate 0 — Baseline Recovery / Validation**  
> 最新快照：[`progress-2026-09-17.md`](progress-2026-09-17.md)

---

## 0. 为什么现在还不能直接进入 B1 / B2？

RLT 是当前项目的核心技术 baseline。Physical Token 的科学增量只有在 reference、执行语义、数据质量和 Stage2 online baseline 都可信时才可解释。

当前需要控制四类混杂：

1. **H/C 与 TOPP execution semantics**；
2. **Stage1 reference capability**；
3. **离线示范轨迹和 physics label 的质量**；
4. **command state / proposed action 与 measured state / executed action 的语义区别**。

因此先完成 Gate 0，再进入 B1/B2。

---

## 1. Gate 0A · Stage1 reference capability

### 1.1 当前能力锚点

RoboTwin native TOPP 下：

- `H50/C50 native_macro`：当前已有 H50 reference 的能力锚点；
- `H50/C10`：会改变 TOPP 重规划边界、物理时长和再观测分布，只作为执行协议诊断；
- 论文式固定低层 `H10/C10`：需要单独控制接口/训练语义，不能只修改 YAML 数字冒充等价复现。

### 1.2 2026-09-17 统一 20-seed 结果

旧 clean50 `pi05_base + alpha1` Stage1 长 run 最终停止在约12.3k steps，没有完成原计划20k。已有完整 checkpoint 在统一协议下的开发结果为：

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

固定条件：

- same 20-seed development cohort；
- `H50/C50 native_macro`；
- same task prompt；
- fixed action-sampling seed。

解释边界：

- 12k 是当前 development candidate，不是 final reference；
- 曲线非单调；
- n=20 不足以证明统计稳定提升；
- 12k 仍有10/20失败；
- 当前 aggregate results 没有逐seed成功列表，不能分析哪些场景具体改善/退化；
- 历史8k 5/20使用不同prompt/noise，不与本轮7/20混算。

### 1.3 Failure-stage evidence

已准备对12k相同 cohort 做 full-physics video / chunk trace 补录，用于定位：

- grasp acquisition；
- grasp retention / slip；
- approach to block；
- contact / impact；
- terminal success。

该补录尚未正式执行；单环境采样与此前20环境批量评测的随机采样可能不同，因此不能用补录成功率覆盖原10/20结果。

---

## 2. Gate 0B · Data quality contract

### 2.1 clean500 全量审计

500条原始成功示范已完整导出，500个seed唯一。全量检查通过：

- 79,529 source frames；
- 318,116 four-camera RGB frames；
- 79,529 MP4 frames；
- finite numeric fields；
- temporal lengths / indices；
- main / physics command alignment；
- repository physics validator。

但识别出10条强动作轨迹异常，表现为关节目标分支跳变、TCP异常运动或异常初始绕转。原始证据保留，新训练候选排除。

正式候选：

> **clean490 = train450 + eval40**

- train450 = 70,640 training indices；
- eval40 = 6,238 development indices；
- norm只由train450计算。

`eval40`包含部分历史开发seed，因此不是论文最终独立test set。

### 2.2 Physics-label validity mask

另有10条动作轨迹连续，但contact/impulse证据偏弱。

规则：

- Stage1 action learning保留；
- contact/impulse auxiliary target mask掉；
- 不把“未记录非零冲量”当成可靠无接触负样本；
- 其他可信 measured outcome 继续使用。

因此后续 Physical Token 的 supervision contract 必须支持 **per-label validity mask**，而不是episode级“一刀切”。

---

## 3. 新 clean490 Stage1 recovery

### 3.1 当前准备状态

已完成CPU侧：

- train450 / eval40转换；
- train-only norm；
- data/split coverage checks；
- OpenPI loader batch check；
- Hydra train/eval dry-run；
- focused RLT tests。

正式 GPU training **尚未启动**。

### 3.2 最新默认训练计划

```text
generic pi05_base
+ rlt_alpha = 1
+ joint VLA task adaptation + RLT reconstruction
+ H = 50
+ global batch = 64
+ dual-GPU data parallel
+ warmup = 1k
+ max optimizer steps = 30k
+ checkpoint every 5k
```

开发评测 checkpoint：

```text
5k / 10k / 15k / 20k / 25k / 30k
```

用 eval40 closed-loop capability 选择，不按最低 train loss。

30k 是上限而非必须完成；连续多个 checkpoint 无改善或下降时可以提前停止。

### 3.3 最终 reference 门槛

- development-best checkpoint 在 eval40 上选定；
- 再使用封存 independent reset seeds；
- fixed environment + action seed；
- H50/C50 native_macro；
- 保存 episode-level success / completion / failure stage；
- 至少有一项可解释的多seed闭环能力证据。

只有之后才冻结正式 B0 reference。

---

## 4. Gate 0C · B0 Online Baseline

RLT 提供 compact readout + lightweight actor/critic 框架。B0 必须是一个可重复的 online baseline，而不是只证明代码能更新参数。

### 4.1 Baseline contract

固定：

- Stage1/reference checkpoint；
- H/C / execution mode；
- action parameterization；
- reward / terminal；
- actor / critic capacity；
- replay schema；
- warmup / update budget；
- seeds；
- action sampling RNG。

### 4.2 旧 Stage2 的地位

历史 C10 Stage2 已证明：

```text
rollout → replay → actor/critic update → weight sync → checkpoint
```

工程链可运行，但其 zero-reward / H50-C10 execution setting 不能继续承担当前 B0 性能结论。

新的 B0 优先在 H50/C50 native-macro 语义下重新建立，或将固定低层H10/C10独立立项。

---

## 5. RLT / RL Token 与 Physical Token 正式比较

Gate 0完成后，第一组实验固定为：

| ID | 方法 | 新增内容 | 目的 |
|---|---|---|---|
| Reference | frozen action model | no online learner | 基础能力 |
| B0-RLT | standard RL Token / matched compact readout | RLT reconstruction | online baseline |
| B0-Head | matched action-head readout | change tap only | 隔离readout位置 |
| B1 | B0-Head + measured transition | action consequence grounding | 测试transition增益 |
| B2 | B1 + valid physics constraints | kinematic / actuator consistency | 测试physics独立增益 |

所有组必须 matched：

- token shape / capacity；
- encoder/readout capacity；
- base action model；
- offline data；
- actor/critic；
- online interaction budget；
- reward；
- seeds；
- H/C/timing。

---

## 6. Action-head extraction contract

第一轮必须比较：

```text
Backbone tap
vs.
Action-head / Action-Expert pre-output tap
```

Action-head 更靠近动作生成是研究假设，不是默认真理。

不同model family需要固定 extraction convention：

- Regression / MLP：penultimate activations；
- Diffusion / Flow：固定sampling-time feature，并保留noise/time context；
- Autoregressive：logits前的causal states；
- 不允许future demonstrated action leakage。

---

## 7. B1 · Measured Transition Grounding

目标：让 compact token 对真实执行后的局部 action consequence 敏感。

```text
z_t = E(F_t^action, history_t, robot_meta)

D(z_t, u_t^exec, Δt, robot_meta)
    → measured future outcome
```

### 7.1 必须区分四类字段

```text
reference / proposed action
actual executed action
command state
measured state
```

当前 imitation dataset 的 state 是 command/drive-target 语义。B1 不得把它直接改名成 measured qpos。

### 7.2 第一版 targets

优先：

- Δ measured q；
- EE motion；
- relative object / EE motion；
- execution discrepancy；
- reliable event outcomes。

要求：

- per-target validity mask；
- terminal/reset隔离；
- train-only normalization；
- future真实观测只作为label；
- action sequence与实际执行区间严格对齐。

第一版不同时做full video world model。

---

## 8. B2 · Valid Physics Constraints

首版只使用可靠、可校验约束：

### Kinematic consistency

```text
L_kin = || v_EE - J(q) q_dot ||²
```

或等价的FK一致性形式。

### Actuator/controller feasibility

- joint limits；
- speed limits；
- known action bounds；
- 其他明确controller constraints。

### 后置

- friction residual；
- contact dynamics residual；
- force/torque consistency；
- full rigid-body dynamics。

只有 sensing / model / calibration 都可靠才启用。

---

## 9. Representation probes

除task success外，建议保持以下机制证据：

- transition prediction；
- action-sensitive consequence ranking；
- contact/slip AUPRC（有可靠标签时）；
- failure-onset probe；
- base-policy operating-range probe；
- physical-shift generalization。

这些 probes 解释“为什么有效”，但不替代最终 online-control 结果。

---

## 10. Actor / Critic 使用方式

第一阶段保持RLT matched：

```text
Actor:  [z, proprio/history, reference chunk] → action
Critic: [z, proprio/history, candidate action] → Q
```

B0/B1/B2 首轮只替换 `z` 的训练方式，避免同时改变RL算法。

后续再单独做：

| Actor | Critic | 目的 |
|---|---|---|
| RL Token | RL Token | baseline |
| Physical Token | Physical Token | full use |
| RL Token | Physical Token | physical-aware critic |
| Physical Token | RL Token | actor-only effect |

这组消融只有主实验成立后再做。

---

## 11. Physical Shift Protocol

在 nominal B0/B1/B2 稳定后，再测试明确单因素 shift：

- contact tolerance / geometry；
- actuator response / gain；
- execution delay / noise；
- mass / friction（仅在可准确控制、记录时）。

不要把 appearance shift 与 physical shift 混在第一轮。

---

## 12. Universal Hypothesis

只有当前 model/robot 上 B2 有稳定增量后才做：

1. held-out action-head family；
2. held-out task；
3. held-out embodiment。

Universal 当前仅表示：

- shared token shape；
- shared physical objectives；
- lightweight model/robot adapters。

不是已成立结论。

---

## 13. 当前完成标准

第一阶段论文级 claim 至少需要：

1. trustworthy Stage1 / B0；
2. clean data + label validity contract；
3. B0-RLT / B0-Head / B1 / B2 matched comparison；
4. backbone vs action-head tap；
5. held-out transition/consequence metrics；
6. online learning / adaptation curve；
7. physical violation metrics；
8. at least one controlled physical shift；
9. repeated seeds + confidence intervals；
10. deployable policy path without simulator-only privileged input。

当前最近的实际动作仍是：**完成12k failure-stage画像，启动clean490新Stage1，冻结可信reference，再重建B0。**

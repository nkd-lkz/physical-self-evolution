# RL Token Baseline & Universal Physical Token Initial Validation

> 当前角色：**Baseline / Initial Validation Protocol**  
> 上位主线：[`physical-token-leadership-spec.md`](physical-token-leadership-spec.md)

---

## 1. RLT / RL Token 现在是什么角色？

RLT 仍然是当前项目最重要的技术 baseline，但不再是最终研究故事。

它的作用是提供一个可比较的 compact readout + small online learner 框架，让我们严格回答：

> **在同样 token size、learner capacity、数据和交互预算下，transition grounding 与 physics grounding 是否真的优于普通 RL Token readout？**

因此当前第一组主比较固定为：

| ID | 方法 | 目的 |
|---|---|---|
| B0 | RL Token / matched head-readout baseline | baseline |
| B1 | B0 + measured transition loss | 检验 action-outcome grounding |
| B2 | B1 + valid physics loss | 检验 physics constraints 的独立贡献 |

---

## 2. 当前已有 qualitative baseline

现有演示：

- Block assembly：precision alignment / insertion；
- Drawer opening + block placement：multi-step manipulation with contact。

准确口径：

> **这些视频是 RL Token reproduction clips，只证明 baseline 行为可以运行；不是 Physical Token 结果，也不是比较实验。**

Hammer / RoboTwin 已有资产继续保留用于 pipeline、transition logging、physics label feasibility 和 regression，但不再决定上位研究叙事。

---

## 3. Baseline Contract

### 3.1 Base action model

记录：

- model family；
- checkpoint；
- action parameterization；
- action horizon / chunk；
- control frequency；
- frozen / trainable parameters。

### 3.2 Readout location

第一轮必须比较：

```text
Backbone tap
vs.
Action-head pre-output tap
```

因为 Physical Token 的核心假设是 action head 更接近动作生成与物理执行，但这一点必须实验验证。

### 3.3 Robot history

允许进入 token readout 的历史必须是部署时真实可得信息：

- current measured robot state；
- recent actual / executed actions；
- robot/control metadata；
- 必要的短历史。

禁止：

- future demonstrated actions；
- future states；
- rollout 后才知道的 label 直接作为当前 actor observation。

---

## 4. B0 · Matched RL Token / Head-Readout Baseline

B0 的目标不是追求最强性能，而是建立公平对照。

要求：

- token `K × d` 固定；
- readout capacity 固定；
- base model / action head frozen；
- online actor/critic capacity 固定；
- interaction budget 固定；
- reward 固定；
- seed policy 固定；
- action chunk / timing 固定。

如果原始 RL Token 读的是 backbone，而 Physical Token 读 action head，则必须增加 matched head-readout baseline，避免把“tap 位置变化”误当作“physics loss 收益”。

---

## 5. B1 · + Measured Transition Loss

action-conditioned decoder：

```text
D(z_t, u_t, r) -> measured future state
```

其中：

- `u_t` = actual / executed action；
- target = measured `t -> t+1` physical outcome；
- 用 validity mask 排除 invalid transition；
- terminal / reset 边界不跨 episode；
- physical-unit normalization 只使用 train split 统计量。

优先 target：

- Δq / qdot；
- EE motion；
- relative motion；
- action execution discrepancy；
- 其他可靠 measured transition quantity。

第一轮不要同时加入 world model、future video、force prediction、contact law 等额外变量。

---

## 6. B2 · + Valid Physics Loss

第一版只加入定义明确、部署/模型中可获得的约束。

### Kinematic consistency

```text
L_kin = ||v_EE - J(q) q_dot||²
```

要求：

- 同一 frame；
- 同一单位；
- Jacobian 与 q/qdot convention 一致。

### Actuator feasibility

记录并惩罚：

- joint-limit violation；
- speed-limit violation；
- 其他明确的 controller / actuator bounds。

### 暂不默认加入

- friction residual；
- contact dynamics residual；
- force / torque consistency；
- full rigid-body equation residual。

只有传感、模型和 calibration 都可靠时，才作为后续 B2+ 扩展。

---

## 7. Online Adaptation Protocol

在线学习阶段：

- base model frozen；
- action head frozen；
- token encoder/readout frozen；
- small actor/critic trainable；
- replay / transition 中记录 actual executed action；
- reward / terminal 与真实执行对齐。

如果使用 physical outcome decoder 约束 actor：

- decoder weights 在 actor update 时冻结；
- 允许 action gradient 穿过 decoder；
- decoder 本身用 measured transitions 在独立 step 更新；
- hard execution limits 仍由环境 / controller 独立保证。

---

## 8. Streaming RL 不是首轮变量

早期路线包含 Streaming Actor–Critic：batch≈1、no replay、chunk-boundary update。

现在第一组研究问题先固定为：

```text
B0 RL Token / head readout
vs.
B1 + transition loss
vs.
B2 + physics loss
```

在 Physical Token 的表示增益成立后，再比较：

```text
Replay learner
vs.
Streaming learner
```

这样才能区分：

- representation 改进；
- learner / replay 改进；
- 两者交互。

---

## 9. 指标

### 任务指标

- success rate；
- episode length / completion time；
- learning / adaptation curve。

### Physical metrics

- kinematic residual；
- joint-limit violation；
- speed-limit violation；
- action execution discrepancy；
- 若有可靠 contact sensing，再记录 contact-specific metrics。

### Adaptation metrics

- interaction steps to target performance；
- adaptation wall-clock；
- compute / memory cost；
- old-task retention。

### 统计

- matched seeds；
- repeated runs；
- confidence intervals；
- raw episode-level metrics；
- qualitative video 只作解释，不代替统计。

---

## 10. Physical Shift Protocol

先在 nominal setting 完成 B0/B1/B2，再测试明确 physical shift：

- contact geometry / tolerance；
- actuator response；
- execution delay / noise；
- mass / friction 等只有在 simulator / system 中能被准确控制和记录时才使用。

所有 shift parameter 必须写入 episode metadata。

不要把 appearance shift 与 physical shift 混在第一轮实验里。

---

## 11. Universal Hypothesis Test

只有 B2 在当前 action model / robot 上稳定成立后，才做：

### U1 · Held-out action-head family

例如从一种 action-generation family 迁到另一种 family；只允许 lightweight model adapter，保持 token shape 与 physical objectives 不变。

### U2 · Held-out embodiment

更换机器人后，只允许 lightweight robot / convention adapter；检查 token / objective 是否仍有效。

只有这些 held-out tests 支持后，才能把“Universal”从设计目标升级成实验结论。

---

## 12. 当前完成标准

第一阶段论文级 claim 至少需要：

1. B0/B1/B2 matched-budget 比较；
2. Action-head tap vs backbone tap；
3. transition prediction held-out 指标；
4. physical violation 指标；
5. online adaptation 指标；
6. old-task retention；
7. 至少一种明确 physical/contact shift；
8. repeated seeds + confidence intervals；
9. 不依赖 simulator-only privileged input 的部署路径。

跨 model / embodiment universality 是后续更强 claim，不是第一阶段必须完成的结果。

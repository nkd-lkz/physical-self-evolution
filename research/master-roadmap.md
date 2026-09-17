# Universal Physical Token：研究总路线

> 版本：2026-09-17  
> 当前状态：**领导主线不变；执行处于 Gate 0 — Baseline Recovery / Validation**  
> 主规范：[`physical-token-leadership-spec.md`](physical-token-leadership-spec.md)  
> 最新进展：[`progress-2026-09-17.md`](progress-2026-09-17.md)

---

## 0. 当前研究问题

当前项目严格收敛到：

> **Universal Physical Token for Robot Self-Evolution**

核心问题：

> **能否从已有 action model 的 actor / action-generation head 读出一个紧凑 token，并通过 measured transition prediction 与有效 physics constraints 对它进行 grounding，使冻结 action model 在变化的接触动力学下通过小型 online learner 更快、更可靠地适应？**

此前更宽泛的 Physical Experience / World Model / Harness / Fleet 路线继续保留在知识库作为 related work 与未来扩展，不覆盖当前领导定义的实验主线。

### Scope boundary

```text
Astra / Harness / Agent:
planner / reviewer / orchestration
→ 决定调用谁、何时重试、是否修正

Our project:
actor / action-generation features
→ Universal Physical Token
→ physical grounding
→ lightweight online adaptation
→ final physical-task success
```

当前第一篇工作不靠增加 LLM planner、memory 或 skill evolution 获得主要收益。

---

## 1. 当前执行门槛：Gate 0

在 B1 / B2 前先建立可信 RLT / RL Token baseline：

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

Gate 0 是因果归因的前置，不是新的算法主张。

### 1.1 2026-09-17 Stage1 证据

旧 clean50 `pi05_base + alpha1` 长程 Stage1 未完成原计划20k，最终停止在约12.3k。统一协议下已完成 6k/8k/10k/12k 的固定20-seed开发评测：

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

协议固定为 `H50/C50 native_macro`、相同 task prompt、相同 action-sampling seed 和同一 cohort。

当前结论：

- Stage1 已证明具备部分闭环任务能力；
- 12k 是当前 development candidate；
- 曲线非单调、样本量有限且12k仍有10/20失败；
- 不能宣布泛化问题解决，也不能把训练步数/数据量/联合loss写成唯一根因；
- 需要完整物理视频、failure-stage分析和独立最终seeds继续验证。

---

## 2. 数据基座：clean500 → clean490

### 2.1 全量审计

500条原始成功示范已经完整导出并完成全量CPU审计：

- 500 unique seeds；
- 79,529 raw/source frames；
- 318,116 four-camera RGB frames decoded；
- 79,529 MP4 frames decoded；
- 数值有限性、字段长度、图像尺寸、视频帧数与 transition 对齐通过；
- repository physics validator 对全部500条通过。

但审计识别出 **10条强动作轨迹异常**。这些原始文件继续保存为证据，但不进入新的动作监督数据。

因此正式候选数据为：

> **clean490 = train450 + eval40**

- train450：70,640 training indices；
- eval40：6,238 development-validation indices；
- norm stats 只使用 train450。

### 2.2 Physics label validity

另有10条动作轨迹本身连续，但 contact/impulse 标签证据偏弱。

原则：

```text
trajectory validity != per-physics-label validity
```

处理：

- Stage1 动作学习保留；
- contact/impulse auxiliary loss 使用 validity mask；
- 缺失/弱冲量标签不能填0解释成“无接触”；
- 其他可信 transition targets 可继续使用。

这个结论直接进入未来 B1/B2 的数据合同。

### 2.3 Command state 与 measured state 分离

当前 imitation dataset 的 state 仍沿用原 OpenPI/RoboTwin command/drive-target 语义。

未来 Physical Token B1 必须显式区分：

```text
reference / proposed action
actual executed action
command state
measured state
```

Measured transition 需要 actual qpos / EE / object consequence 等真实测量，不允许把 command target 静默当作真实物理状态。

---

## 3. 新 clean490 Stage1 baseline recovery

下一轮 Stage1 从 generic `pi05_base` 重新开始：

- joint VLA task adaptation + RLT reconstruction；
- `rlt_alpha=1`；
- H50；
- global batch64；
- dual-GPU data parallel；
- warmup1k；
- default maximum 30k optimizer steps；
- checkpoint every5k；
- `5k/10k/15k/20k/25k/30k` 使用 eval40 做开发选择。

当前数据转换、train-only norm、loader、Hydra dry-run 与 CPU regression 已完成；**GPU正式训练尚未启动**。

30k 是上限，不是必须跑满。选择依据仍然是 closed-loop capability，而不是最低训练 loss。

最终 reference 需要在 development-best checkpoint 确定后，用未参与开发的独立 reset seeds 重新评估。

---

## 4. 核心结构

```text
Frozen Backbone / Perception
          ↓
Frozen Action Head / Action Expert
          ↓
Pre-output action-generation features F_t^head
          +
Robot history h_t
(measured state + actual/executed actions)
          +
Robot metadata r
          ↓
Model adapter A_m + learned readout E_phi
          ↓
Physical Token z_t  (fixed K × d)
          ↓
Small online actor / critic
          ↓
Adapted action
```

核心假设不是“物理变量越多越好”，而是：

> **在固定容量下，action-side compact representation 经过真实 action consequence 与可靠 physics constraints grounding 后，是否更适合价值判断和在线适应。**

---

## 5. Physical Token 目标

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

### 5.1 `L_ro` · Readout / Reconstruction

- preserve stop-gradient action-generation features；
- 保持原任务/动作信息；
- 不修改 frozen action model。

### 5.2 `L_dyn` · Measured Transition Prediction

```text
D(z_t, u_t^exec, r) -> measured future physical outcome
```

第一版优先：

- actual joint / EE motion；
- relative robot-object motion；
- execution discrepancy；
- 可靠的事件/接触结果（仅在标签有效时）。

要求：

- actual/executed action；
- validity mask；
- terminal/reset隔离；
- train-only normalization；
- future真实结果只能作target，不能泄漏到当前actor输入。

### 5.3 `L_phys` · Valid Physics Constraints

第一版优先：

- kinematic consistency；
- joint limits；
- speed limits；
- 明确的 actuator / controller feasibility。

Contact、friction、force/torque、full rigid-body residual 只有 sensing/model/calibration 可靠后才进入。

**模拟器能导出字段，不等于该字段天然适合作为物理监督。**

---

## 6. 第一组正式实验

| ID | 方法 | 新增内容 | 回答的问题 |
|---|---|---|---|
| B0 | RL Token / matched head-readout baseline | compact readout | baseline |
| B1 | B0 + measured transition | real action-outcome grounding | transition grounding 是否带来增量？ |
| B2 | B1 + valid physics | kinematic/actuator constraints | physics constraints 是否有独立增量？ |

所有组必须 matched：

- base/reference checkpoint；
- token capacity；
- actor/critic capacity；
- deployment inputs；
- offline data；
- online interaction budget；
- reward；
- seeds；
- H/C/timing/execution semantics。

### 必须增加的 readout 对照

```text
Backbone tap
vs.
Action-head / Action-Expert tap
```

Action-head 更接近动作生成是研究假设，不是已知事实。

---

## 7. Online self-improvement

在线阶段默认：

- base model frozen；
- action head frozen；
- token encoder/readout frozen；
- small actor/critic trainable；
- learner 使用真实 executed actions 与 task rewards；
- replay 与 outcome target 对齐真实执行时间。

第一阶段 actor/critic 结构尽量沿用 matched RLT，先只更换表示，避免 learner 改动掩盖 representation 的贡献。

后续可以单列：

- actor-only token use；
- critic-only physical token；
- both actor/critic；
- Q-guided flow update；
- streaming / low-replay。

这些不是首轮 B1/B2 必须变量。

---

## 8. 指标与证据链

### 8.1 Representation evidence

- held-out transition prediction；
- contact/slip/event AUPRC（有可靠标签时）；
- failure-onset / operating-range probes；
- hidden dynamics parameter probe 仅作诊断，不直接输入主策略。

### 8.2 Decision evidence

- same-state candidate ranking；
- critic calibration / action discrimination；
- token usage ablation。

### 8.3 Online control evidence

- success rate；
- success-vs-interaction curve / AUC；
- interaction steps to target performance；
- completion time；
- physical violation metrics；
- failure taxonomy；
- old-condition retention。

主张需要形成：

```text
better representation
→ better action/value discrimination
→ better online adaptation
→ better task success
```

不能只靠 auxiliary loss 下降。

---

## 9. Physical shift 与 Universal test

只有 nominal B0/B1/B2 稳定后，才进入：

1. 同任务单因素 physical shift：mass / friction / delay / gain / contact tolerance；
2. appearance shift 单独报告，不与 dynamics shift 混合；
3. held-out task / head family；
4. held-out embodiment。

“Universal”当前只表示 shared token shape + shared objective + lightweight adapters，是待验证 hypothesis。

---

## 10. RoboDojo 的位置

RoboDojo 继续作为第二平台：

- D0–D2 complete；
- D4 CPU protocol complete；
- D3 B300 renderer pending；
- D5–D10 pending。

它不阻塞 Hammer 上的 Gate 0 与 Physical Token 核心假设验证。

---

## 11. Streaming / WAM / Agent 的触发条件

- **Streaming RL**：B0/B1/B2 表示问题先成立，再研究 replay efficiency；
- **Full WAM**：局部 consequence prediction 已证明长期规划确有价值后再启动；
- **Agent/Harness**：失败主要来自任务拆解/skill orchestration，而非局部物理执行时再考虑；
- **Foundation consolidation**：轻量适应已经持续产生稳定、高质量新经验后再考虑写回大模型。

这些不是当前必经路线。

---

## 12. 当前禁止的过度表述

当前不能写：

- “Physical Token 已提升成功率”；
- “机器人已经学会物理规律”；
- “12k显著优于其它checkpoint”；
- “clean500全部500条都适合训练”；
- “contact=0等于没有接触”；
- “数据扩充已带来最终性能提升”；
- “Universal已跨模型/跨本体成立”；
- “旧Stage2零成功证明RLT缺physics”。

当前最准确表述：

> **项目以 RLT 为 baseline，当前已建立部分可用的 Hammer Stage1 reference 能力曲线，并完成 clean500 全量质量审计与 clean490 数据准备。下一步先用 clean490 建立更可信 Stage1/B0；随后在 matched 条件下验证 action-side compact token 的 measured-transition / physics grounding 是否真正提高在线适应与最终任务成功率。**

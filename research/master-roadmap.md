# Universal Physical Token：研究总路线

> 版本：2026-09-18  
> 当前状态：**领导主线不变；执行处于 Gate 0 — trustworthy B0 diagnosis / recovery**  
> 主规范：[`physical-token-leadership-spec.md`](physical-token-leadership-spec.md)  
> 最新进展：[`progress-2026-09-18.md`](progress-2026-09-18.md)

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

在 B1 / B2 前必须先建立可信 RLT / RL Token baseline。当前已经从“Stage1能否完成任务”推进到“B0 online learner能否至少保持reference”的诊断阶段：

```text
Gate 0A  Validate Stage1 reference
       ↓
Gate 0B  Fix execution / timing semantics
       ↓
Gate 0C  Build B0 online baseline
       ↓
B0-Diag BC/reference/Q diagnosis  ← current
       ↓
trustworthy B0
       ↓
B1      + measured transition grounding
       ↓
B2      + valid physics grounding
```

Gate 0 仍然只是因果归因前置，不是新的算法主张。

### 1.1 旧 clean50 Stage1 证据

统一 20-seed、`H50/C50 native_macro` 协议下：

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

12k仍只是旧数据路线的development anchor。

### 1.2 新 train450 Stage1 证据

新clean490/train450 Stage1从generic `pi05_base`联合训练VLA+RLT，原计划30k，迁移前主动停止在约10823 steps，完整checkpoint为5k与10k。

10k checkpoint 在相同eval40 / H50-C50 / fixed prompt/action seed协议下做两次独立设备运行：

> **22/40 = 55% in both runs**

这支持当前开发协议上的聚合可复现性，但不能解释为80个独立seeds，也不能直接与旧12k的10/20做显著性结论。最终reference仍需失败阶段分析、matched-seed对照和独立seeds复核。

### 1.3 B0 Stage2 现状

使用旧clean50/12k frozen reference的首个H50/C50 Stage2 run已经停止。周期20-seed评测：

- 早期约45%；
- 后期约15%。

因此当前B0尚不可信。下一步不是继续加budget，而是BC-only/reference-consistency、actor deviation、reference dropout、BC/Q ratio、critic calibration与macro discount诊断。

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

新 Stage1 已经从 generic `pi05_base` 启动并产生可评测 checkpoint：

- joint VLA task adaptation + RLT reconstruction；
- `rlt_alpha=1`；
- H50；
- global batch64；
- dual-GPU data parallel；
- warmup1k；
- 原计划maximum30k；
- checkpoint every5k。

迁移前主动停止在约 **10823 / 30000**，因此不能写成30k完成。

当前完整保存点：

- 5k；
- 10k。

10k在eval40上两次均为22/40（55%）。这使10k成为当前新数据路线的development candidate，但最终reference仍需要：

1. 18个失败episode的failure-stage画像；
2. 5k/10k/旧12k同seed对照；
3. independent reset seeds复核；
4. paired video / episode-level evidence。

训练loss只作为健康度，不作为选模依据。

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

在线阶段的理想默认仍是：

- base model frozen；
- action head frozen；
- token encoder/readout frozen；
- small actor/critic trainable；
- learner 使用真实 executed actions 与 task rewards；
- replay / discount 与真实执行时间对齐。

但 2026-09-18 的首个 H50/C50 B0 Stage2 暴露了一个关键问题：

> **online parameter update ≠ policy improvement**

旧clean50/12k frozen reference 的 Stage2 周期成功率从约45%退化到约15%，因此已经停止。

当前必须先证明：

```text
actor ≈ reference under BC-only / anchoring
        ↓
Q signal is calibrated enough
        ↓
actor deviation is controlled
        ↓
online training preserves / improves success
```

下一轮B0诊断重点：

- BC-only / reference consistency；
- actor-reference action deviation；
- reference dropout；
- BC/Q weighting；
- critic calibration；
- macro execution duration / discount；
- checkpoint / actor takeover timing。

只有B0能够稳定保持或改善reference，才进入B1/B2。第一阶段仍尽量沿用matched RLT actor/critic，避免learner改动掩盖representation贡献。

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

RoboDojo继续作为第二平台，目前：

- D0–D5 infrastructure / native task gates 已完成；
- D6 real reference-only adapter pending；
- D7 multi-seed Dojo-Eval pending；
- D8 real transition alignment pending；
- online RLT 尚未开始。

科研任务候选：

- `plug_in_charger`：精密接触 / insertion；
- `push_T`：摩擦 / dynamics；
- `insert_key` / `insert_tubes`：后续扩展。

官方 ARX X5 π0.5 candidate 已确认存在，但在权重恢复、RGB/get_obs版本兼容和闭环能力验收完成前不能当作正式reference。

RoboDojo不阻塞Hammer上的B0诊断与Physical Token主实验。

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

> **项目以 RLT 为 baseline。当前新train450 Stage1 10k在eval40上两次均为22/40（55%），但旧clean50/12k上的首个B0 Stage2发生明显在线退化，因此主线已转入B0诊断。只有在BC/reference/Q与执行时间语义被证明可信后，才会进入B1 measured-transition与B2 physics-grounding实验。**

# Physical Self-Evolution

Living research website for **Universal Physical Token, robot self-improvement, VLA / action models, Online RL and embodied physical adaptation**.

## 分区入口与单向引用

| 区域 | 内容与入口 |
| :--- | :--- |
| **RLT / Universal Physical Token 项目** | [Research OS 网站](https://nkd-lkz.github.io/physical-self-evolution/)；`research/`、`notes/` 与根目录 `data/` 存放项目观点、方案和实验记录 |
| **具身 / 机器人 RSI 综述** | [独立文献库](survey-rsi/README.md)；仅公开论文、作者来源及综述分析 |

**公开论文可以从 RSI 文献库进入 RLT 项目；RLT 的研究观点、方案与进度不回流到综述区。** [文献引入与已迁回材料](research/survey-literature-intake.md)提供项目侧入口。同一公开仓库内的分区不是权限隔离，历史版本仍可访问。

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Physical RSI 资料核验与 RLT 实验入口 — 2026-09-30

- [新资料摄取与三步实验](research/physical-rsi-source-intake-2026-09-30.md)：核验 RPent、Astra 42 任务评测、Axis、Simate、RoboICL 与 IROS 相关原始论文；区分公开证据、团队自述和二次转述，将接触后果监督、经验检索、等预算 RL 分开设计。
- [Axis 仿真到真机回流与技能库](notes/axis-capability-library.md)：校正“零真机数据”和纯计算成本的口径；[Astra 笔记](notes/astra-robodojo.md)补入 42 任务论文；[RPent 笔记](notes/rpent.md)补入任务卡对照。

这些是论文/官网阅读与待验证实验，没有新增闭环提升或真机结果。Simate 官网当时标注 RoboDojo 评估进行中，媒体所称榜首未被当作已验证排名。

## RLT 近邻论文专题 — 2026-09-30

- [注意力可视化、ActGaze 近邻与经验条件视觉证据方案](research/literature/visual-evidence-rlt-2026-09-30.md)：区分热图、输入依赖与闭环控制；新增 FLARE 时序诊断、Zeva 90 条遗忘测试流和 Jev 6 次候选覆盖拟合。CPU 回归更新为 **196 / 206 / 206 passed**；没有新 GPU 作业或第四分支训练。

- [UniMPA：预期转移、历史可执行动作与 flow 生成](notes/unimpa.md)；[F4R：失败诊断、目标化仿真与再训练闭环](notes/f4r.md)。两项是项目研究所需的独立文献笔记，未复现代码或真机；与现有 [三分支前沿对照](research/literature/frontier-rlt-2026-09-30.md)衔接。

## Three-branch audit and research proposals — 2026-09-30

下午续作已完成：[99 次预定诊断＋12 次追加 CPU 拟合与人工接管入口](research/three-branch-audit-2026-09-30.md#下午续作预先固定实验矩阵与人工介入入口)。Zeva 支持度门控降低开发预测误差；Jev 排序随 BC／数据条件变化；FLARE 已补齐动作前缀敏感性和匹配 online 配置。原始统计与新结果图见[结构化记录](data/continuation-2026-09-30.json)。小模型矩阵约 31 分钟完成后已释放 GPU；不是 12 小时大训练，也不是 111 次机器人闭环。完整 Jev online 仍保留 12 小时空闲等待预算。

VR 单环境 `horizon=1` pilot 已准备，支持真实人工 transition、有限更新、BC 发布门槛和 optimizer/replay 恢复；未接入正式 64 环境，Windows/PICO 跨机器闭环待操作者验收。[启动指南](https://github.com/nkd-lkz/UPT_dev/blob/feature/rlt-pico-vr-intervention/experiments/maniskill_rlt/VR_ONLINE.zh-CN.md)。最新 CPU 套件：FLARE / Zeva / Jev 为 **195 / 203 / 205 passed**，各 1 skip、1 已知排除；VR **34 passed、2 skipped**。以下保留首轮结果，不与续作混算。

- [代码审查与 42 组小实验](research/three-branch-audit-2026-09-30.md)：FLARE 掩码梯度修复、Zeva 固定响应读取器、Jev 同幅度连续 residual 对照；含负结果、测试范围与结构化证据。
- [三个方案的原理、摘要与架构图](research/three-branch-research-plan-2026-09-30.md)：解释物理经验存在哪里、新反馈更新什么，以及通往真机持续学习的验收门槛。三张架构图和一张真实诊断图提供 SVG / PDF / PNG。
- [前沿邻近工作与创新边界](research/literature/frontier-rlt-2026-09-30.md)：覆盖至 09-30，包含 09-29 修订的 F4R、UniMPA、StateMem、Imagine-RL、RouteRLT 等；不以调研替代新颖性或能力证明。
- 三分支 CPU 回归分别为 **194 / 201 / 204 passed**；各通过单 rank 小模型 FSDP 更新与恢复。合计包含共用测试；这不是完整机器人在线训练验收。
- 仅小模型在物理 GPU 2 受限共存；GPU 0/1、baseline 与 VR 未改动。Jev 完整在线队列继续等待资源空闲。当前仍无新增闭环成功率、迁移或减少人工干预的证据。

## Earlier ManiSkill RLT snapshot — 2026-09-30

- [完整进度快照](research/progress-2026-09-30-maniskill-rlt.md)：汇总 baseline、FLARE 动作后果表征、Zeva 交互记忆、Jev 有限动作决策和 PICO VR 五条隔离代码线，并列出已验证证据与未完成 Gate。
- Baseline Stage 1 已完成 2000 step；固定 20 回合闭环评测为 **8/20（40%）**。正式 Stage 2 正在两张 L40 上运行；截至快照至少到 149/5000，前五次 256 环境评估约为 35.9%–42.2%，尚未形成最终结果。
- FLARE 启发的增量未来 latent 预测保留三初始化离线正向结果。最新 baseline / FLARE 各 100 轮在线对照均正常退出，但两组 10 次单环境评估全部失败；预测网络在更新，控制收益没有得到支持。
- Jev 启发分支新增最多 17 个 reference-relative 有限动作候选和本地选择器。229 项 CPU 回归通过，三 seed 合成诊断验证修正后的更新方式；GPU 只读预检通过，尚未执行 ManiSkill smoke。
- Zeva reader 的真实更新和负结果、Windows / PICO 本地调试及服务器 scripted takeover 证据继续保留；两者都没有新增能力结论。

上述内容属于 RLT / Physical Token 项目，不写入 `survey-rsi/`。训练 loss、短 smoke 和参数变化均不等价于任务成功率或自进化能力。

## Guided reading and prototype — 2026-09-26

- [六篇联合导读：Zeva / Harness VLA / SHAPER / ASPIRE / ENPIRE / Zetta](research/six-papers-guided-reading-2026-09-26.md)：按自进化发生的位置选择实验。
- [Zeva 精读及 RLT 最小实验方案](research/zeva-rlt-implementation-2026-09-26.md)：原论文与公开代码/权重的边界、等预算消融和停止条件。
- [Completed-transition memory prototype](research/prototypes/zeva_rlt_memory/README.md)：标准库实现与时间隔离检查；还未接入 RLinf 或训练策略。

## Project-relevant readings — 2026-09-22

- [UniIntervene](notes/uniintervene.md)：动作后果、时序价值与记忆恢复，是减少专家干预方向的 **P0 强近邻**；公开包目前提供离线流程，不含真机部署/HIL-SERL 集成。
- [CLAP](notes/clap.md)：跨本体动作接口与世界模型，是物理后果及 Universal 证据的 **P1 参考**；不直接加入当前高频控制链路。
- [与 Physical Token / RLT 的取舍](research/uniintervene-clap-project-implications.md)：只保留问题定义、可借鉴机制、已有创新边界与低成本验证启发。

两项均已核对方法、实验、相关附录与官方 README，未复现；阅读总账增至 **131 项**。不新增实验成绩，不改变当前基线恢复与固定专家/门控的研究合同。

## Reading and research update — 2026-09-25

- [Six concise paper notes](research/literature/reading-notes-2026-09-25.md): FLARE, Pri4R, AGRA, Spline Policy, CometVLA and PAR; existing entries promoted to an initial discussion, no reproduction claimed.
- [Chelsea Finn talk perspective](research/chelsea-finn-physical-rsi-talk-2026-09-25.md): distinguishes secondary talk coverage, PI primary RECAP / π0.7 evidence, and open verification questions.
- [FLARE-inspired RLT experiments](research/flare-rlt-contact-experiments-2026-09-25.md): matched future/outcome loss controls, separate candidate-action screening, intervention accounting and held-out-task transfer; all are proposals.
- [Reading ledger](research/literature/reading-ledger.md): 134 paper/project entries and 2 separately counted perspectives as of 2026-09-30.

## Discussion update — 2026-09-22

本轮把迁移恢复、RLT关键阶段与专家纠错、100/200步语义、TOPP恢复边界，以及“物理经验能否减少干预”的讨论整理为三个入口：

- [迁移后最简切入口](research/migration-recovery-2026-09-22.md)：恢复冻结train450/10k与匹配norm；旧日志/视频分析 → 最小干预闭环 → 缓存特征probe。当前迁移包缺权重与原始数据，不等于已恢复55%能力。
- [RLT干预机制与Hammer时间语义](research/rlt-intervention-2026-09-22.md)：base→actor与expert纠错分开；旧Stage2未启用Hammer专家；H50/C50下从名义100步起通常只剩两个actor chunk。TOPP仅是恢复专家的执行组件。
- [物理经验与干预研究合同](research/physical-experience-protocol-2026-09-22.md)：固定专家/门控先验证后果监督，之后单独比较预测式门控；无专家成功率、专家控制时长与吞吐率分别统计。

更新已同步到[网站研究假设池](https://nkd-lkz.github.io/physical-self-evolution/index.html#ideas)。本轮是代码/归档证据核查与实验设计，**没有新增GPU实验或已实现的Hammer干预功能**。现有RLT并非“只有语义监督”；研究增量是显式、可测的动作后果grounding。公开[脱敏核查摘要](data/recovery-audit-2026-09-22.json)保留来源哈希，内部原始日志留在本地。

## Latest experiment evidence — 2026-09-22

[Detailed update](research/progress-2026-09-22.md): the supplied evaluation-summary screenshot reports train450 Stage1 10k at **22/40 success (55%)**, with 18 failures, return 0.55, mean step reward ≈0.00287, and mean episode length 196.25/200. GPU6 matches the prior GPU7 aggregate result. This supplements the existing September 18 repeat-evaluation record; no new independent run or seed count is added without a distinct run ID.

The step-average reward is not the terminal success reward. W&B “0 media” does not establish that local videos are absent. Aggregate agreement does not establish per-seed trajectory agreement, superiority over old clean50/12k, or an RLT representation gain. The source is a user-supplied summary screenshot, not a new raw-log audit.

## Frontier update — 2026-09-21

- [XPACE](notes/xpace.md): recovery supervision, failure-data routing, and limitations of visual consistency.
- [EmbodiedJev](notes/embodied-jev.md): candidate decisions, physical verification, and calibration boundaries.
- [RLT research ideas](research/xpace-jev-rlt-ideas.md): operational recoverability definition, deployment-input probes, and a representation × recovery-data experiment. Proposal only; no new experiment results.

- [ForceDelta-VLA](notes/forcedelta-vla.md): teacher-defined force corrections, delay compensation, and the controls needed to distinguish representation gains from faster feedback. Distinct from FD-VLA.
- [RPent](notes/rpent.md): agent infrastructure, frozen evaluation memory, and the boundary between experience reuse and online policy learning. System entry linked to the existing Harness VLA paper.
- [Reading ledger](research/literature/reading-ledger.md): 131 literature/project entries, including the original 125-entry audit four September 21 additions and two September 22 additions. The additions are topical readings, not independent reproductions.

## Current research mainline — 2026-09-18

The project is aligned to the leadership-defined research proposal:

> **Universal Physical Token for Robot Self-Evolution**

Current question:

> Can we extract a compact, reusable representation from an existing actor / action-generation head, ground it with measured transition prediction and valid physical constraints, and use a small online learner to improve physical adaptation and final task success **without retraining the action model during online adaptation**?

### Scope boundary: actor-side token, not planner-side orchestration

- GPT-6 Astra / Harness-style systems are mainly **planner / reviewer / orchestration** approaches around an existing policy;
- this project is **not** trying to win by adding a stronger planner;
- the core object is an **actor-side universal compact token** extracted from the action model itself;
- planner/harness work remains Frontier reference for failure diagnosis, operating-range reasoning and validation-gated recovery.

```text
actor / action-generation features
        ↓
Universal Physical Token
        ↓
transition / physics grounding
        ↓
small online learner
        ↓
final physical-task success / adaptation gain
```

LLM planner, memory, zero-shot reasoning and skill-harness evolution are **not first-round B0/B1/B2 variables**.

Current source of truth:

- [`research/physical-token-leadership-spec.md`](research/physical-token-leadership-spec.md)
- [`research/master-roadmap.md`](research/master-roadmap.md)
- [`research/rlt-multitask-benchmark.md`](research/rlt-multitask-benchmark.md)
- [`research/progress-2026-09-30-maniskill-rlt.md`](research/progress-2026-09-30-maniskill-rlt.md) — current ManiSkill baseline, FLARE, Zeva, Jev and VR implementation evidence
- [`research/progress-2026-09-28-maniskill-rlt.md`](research/progress-2026-09-28-maniskill-rlt.md) — previous ManiSkill implementation snapshot
- [`research/progress-2026-09-22.md`](research/progress-2026-09-22.md) — latest evaluation evidence and counting boundaries
- [`research/progress-2026-09-18.md`](research/progress-2026-09-18.md) — detailed execution snapshot
- [`research/progress-2026-09-17.md`](research/progress-2026-09-17.md) — previous detailed snapshot
- [`research/robodojo-b300-log.md`](research/robodojo-b300-log.md) — second-platform bring-up / RLinf integration log
- [`research/robodojo-contact-task-reference-selection-2026-09-17.md`](research/robodojo-contact-task-reference-selection-2026-09-17.md) — contact-task and reference selection

## Current execution gate: small-resource recovery, then trustworthy online comparison

The immediate compute-limited entry is frozen-reference recovery, a validated minimal intervention loop, and cached-feature consequence probes. Offline representation research can proceed without a long RLT run. Formal B0/B1/B2 online claims still require a trustworthy matched learner; the earlier H50/C50 B0 Stage2 run was stopped after degradation:

```text
Recover / validate Stage1 reference
        ↓
Fix execution / timing semantics + validate intervention instrumentation
        ↓
B0 online baseline
        ↓
BC/reference/Q diagnosis  ← before restarting online comparison
        ↓
trustworthy B0
        ↓
B1 + measured transition loss
        ↓
B2 + valid physics loss
```

The current rule is simple: **do not interpret Stage2 parameter updates as algorithmic progress unless the trained actor at least preserves or improves the matched frozen reference.**

## Hammer Stage1 status

Two Stage1 lines are now tracked separately.

### Old clean50 reference line

The old clean50 `pi05_base + rlt_alpha=1` run stopped around 12.3k. On the unified 20-seed `H50/C50 native_macro` development cohort:

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

The old 12k remains a development reference anchor, not a final reference.

### New clean490 / train450 line

A fresh generic-`pi05_base` joint VLA+RLT Stage1 run was launched on train450 and later stopped for migration at about **10823 / 30000** steps. Complete 5k and 10k checkpoints were preserved.

The 10k checkpoint was evaluated twice under the same eval40 protocol on two allowed GPUs:

> **22 / 40 = 55% success in both runs**

The two runs also matched on aggregate return (~0.55) and mean episode length (~196.25). This supports aggregate reproducibility under the current development protocol, but it is **not** an independent 80-seed result and does not by itself prove that train450 is significantly better than the old clean50 line.

The next reference work is failure-stage review, matched-seed checkpoint comparison and independent-seed validation.

## Hammer clean500 → clean490

The data contract remains:

- 500 raw demonstrations preserved;
- 10 strong action-trajectory anomalies excluded from new supervision;
- **clean490 = train450 + eval40**;
- train450 provides 70,640 training indices;
- eval40 provides 6,238 development-validation indices;
- normalization uses train450 only;
- another 10 trajectories remain valid for action learning but have weak contact/impulse labels, so contact-specific auxiliary targets require a validity mask.

The dataset audit strengthens supervision quality, but does not itself prove better task success.

## New clean490 Stage1 — stopped after 10k checkpoint

The fresh clean490 Stage1 run used:

- generic `pi05_base`;
- joint VLA task adaptation + RLT reconstruction;
- `rlt_alpha=1`;
- H50;
- global batch64;
- dual-GPU data parallel;
- intended maximum 30k optimizer steps;
- checkpoint every5k.

It was actively stopped at about **10823 steps** for migration. This is not a completed 30k run.

Latest saved training-health values were approximately:

- total loss 0.05317;
- RLT loss 0.05236;
- VLA loss 0.000808.

Checkpoint choice remains based on closed-loop capability, not minimum training loss. The 10k checkpoint currently has the strongest new-line evidence: two eval40 runs at 22/40 each.

## B0 Stage2 — stopped after online degradation

The first new H50/C50 B0 Stage2 run used the old clean50/12k frozen reference.

Reference anchor:

> **10 / 20 = 50%** on the matched development cohort.

Stage2 used a direct normalized actor, 4 training environments, batch64, replay warmup and a 4:1 critic:actor update ratio. During periodic 20-seed evaluation:

- around rounds 200/300: ~45%;
- around rounds 800/900: ~15%.

The run was actively stopped around outer round 985. The low final critic / BC losses are **not** accepted as evidence that Q-values or the actor are correct.

Current interpretation:

> **This B0 configuration degrades the frozen reference and is therefore not yet a trustworthy online baseline.**

Next: BC-only / reference-consistency, action-deviation, reference-dropout, BC/Q-balance and critic-calibration diagnostics. No further budget is added to the same configuration until those checks are complete.

## RoboDojo second-platform status

RoboDojo status is unchanged from the latest 9/17 validation:

- D0–D5 complete at the infrastructure/native-task level;
- D6 real reference-only adapter pending;
- D7 multi-seed Dojo-Eval pending;
- D8 real transition alignment pending;
- online RLT not yet started.

Current task candidates remain:

- `plug_in_charger`: primary precision-contact candidate;
- `push_T`: friction / dynamics control;
- `insert_key` / `insert_tubes`: later contact-rich extensions;
- `stack_bowls`: engineering regression only.

The official ARX X5 π0.5 candidates still require version compatibility checks, model restoration and actual capability evaluation before they can serve as D6 references.

## Core architecture

```text
Frozen action model / actor
      ↓
Action-head pre-output features
      + robot history
      + robot metadata
      ↓
Lightweight model/robot adapters
      ↓
Fixed-size Physical Token z_t
      ↓
Small online actor / critic
      ↓
Behavior adaptation
```

Representation objective:

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

- `L_ro`: readout / reconstruction from stop-gradient action-head features;
- `L_dyn`: action-conditioned prediction of **measured** physical transitions using actual/executed actions;
- `L_phys`: valid physical constraints, starting from kinematic consistency and actuator feasibility.

Contact / friction / rigid-body / force targets are optional and require valid sensing, models, calibration and per-label validity masks.

## Initial Physical Token experiment

After B0 is trustworthy:

1. **B0 — RL Token / matched head-readout baseline**
2. **B1 — B0 + measured transition loss**
3. **B2 — B1 + valid physics loss**

Matched variables include token size, learner capacity, base model, data, online interaction budget, reward, seeds and action timing.

A critical data contract is explicit:

```text
reference / proposed action
actual executed action
command state
measured state
execution duration / executed length
optional physics label + validity mask
```

These must remain distinct.

## What “Universal” currently means

Universal is an **empirical hypothesis**, not a result:

- shared token shape;
- shared physical objectives;
- lightweight adapters for model families and embodiments.

Cross-model / cross-robot claims require held-out tests.

## Existing evidence

- Block-assembly and drawer-opening/placement clips remain **RL Token qualitative reproduction**, not Physical Token results.
- Old clean50 Stage1 provides a partial reference capability curve; 12k reached 10/20 on its 20-seed development cohort.
- New train450 Stage1 10k reached **22/40 twice** on eval40; this is development evidence, not a final independent comparison.
- The first H50/C50 B0 Stage2 run **degraded** from about 45% periodic success to about 15% and was stopped; this is evidence that the current online learner configuration is not yet trustworthy.
- clean490 strengthens data quality and label validity but does not itself prove task improvement.
- RoboDojo D3/D5 prove renderer + native-task infrastructure paths, not RLinf/RLT algorithm performance.
- **No validated online-RL gain and no Physical Token / physics-grounding gain exists yet.**

## Public repository policy

This is a **public, redacted research log**.

We publish scientific design, sanitized metrics, public SHAs / branches and research conclusions. We do not publish internal absolute paths, usernames, host/IP information, credentials, private dashboard identifiers or unnecessary infrastructure commands.

See [`research/knowledge-base-maintenance.md`](research/knowledge-base-maintenance.md).

## Repository structure

```text
.
├── index.html
├── reader.html
├── assets/
├── data/
├── notes/
├── archive/
└── research/
    ├── physical-token-leadership-spec.md
    ├── master-roadmap.md
    ├── rlt-multitask-benchmark.md
    ├── progress-2026-09-18.md
    ├── progress-2026-09-17.md
    ├── robodojo-b300-log.md
    ├── robodojo-contact-task-reference-selection-2026-09-17.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    └── reading-program.md
```

## Literature map & reading ledger

The Physical Token literature review is now maintained as a first-class research asset rather than an ad-hoc paper list:

- **Direction map / mental model:** [`research/literature/physical-token-direction-map.md`](research/literature/physical-token-direction-map.md)
- **125-paper master audit:** [`research/literature/physical-token-literature-audit-2026-09-19.md`](research/literature/physical-token-literature-audit-2026-09-19.md)
- **Read / unread / priority ledger:** [`research/literature/reading-ledger.md`](research/literature/reading-ledger.md)
- **Machine-readable ledger:** [`data/literature-reading-ledger.json`](data/literature-reading-ledger.json)
- **Deep-note index:** [`notes/README.md`](notes/README.md)

Every catalogued paper has at least a **search/abstract mini-note** containing method, project relevance, verification boundary and first-party source. A paper is marked “read” or “deep-read” only after actual method/experiment review; the remaining entries stay explicitly queued rather than being treated as understood.

Current reading priority is collision avoidance around **action-side representations, future/consequence supervision, hidden-dynamics adaptation, physical constraints, value guidance, WAM interfaces and cross-head transfer**.

## Knowledge-base rule

The Frontier Knowledge Base continues to track RISE, Motus2, LWD, RLT, SmoothRL, Zeva, Zetta, Astra/Harness and related work. They inform baselines and innovation boundaries, but do not override the leadership-defined actor-side Physical Token experimental contract.

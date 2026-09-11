# 面向物理交互的机器人自我改进：研究总路线

> 版本：2026-09-11  
> 当前状态：进入 **Phase 0 — RLT Multi-task Benchmark**  
> 用途：项目主线、实验协议、论文边界与滚动计划的统一文档。

---

## 0. 最新主线

项目不再按“Physical Token → Streaming → WAM”这种模块堆叠路线推进。

新的四阶段主线是：

| 阶段 | 目标 | 当前状态 |
|---|---|---|
| Phase 0 | RLT Multi-task Benchmark | **当前主阶段** |
| Phase 1 | Failure Diagnosis | Phase 0 稳定后启动 |
| Phase 2 | Physical Experience Representation | 只有诊断支持后启动 |
| Phase 3 | Self-Improvement Loop | 多任务与诊断稳定后启动 |

核心原则：

> **先把 RLT baseline 和 benchmark 基础设施做扎实，再让失败证据决定创新方向。**

RLT 是技术脚手架，不是最终研究叙事。

长期 Research Vision 仍然是：

**Physically Grounded Self-Improving Robot Policies**

---

## 1. Phase 0 — RLT Multi-task Benchmark

### 1.1 为什么现在先做这个？

当前最大风险不是“idea 不够多”，而是没有一个足够稳定、可重复、跨任务的 baseline bench。

如果 baseline 不清楚，后续任何收益都无法判断来自：

- 更好的 foundation policy；
- 不同 action parameterization；
- reward / termination 变化；
- 任务难度；
- 数据覆盖；
- privileged input；
- 真的算法创新。

因此 Phase 0 的任务是建立：

\`\`\`
Reference Policy
      ↓
RLT-π0.5-adapted
      ↓
Online Rollout
      ↓
Independent Evaluation
      ↓
Multi-task Comparison
\`\`\`

---

### 1.2 Hammer 是否走偏？

结论：

**没有白做，也不需要推倒；但它不再承担“唯一研究任务”的角色。**

Hammer 已经提供了大量可复用资产：

- RoboTwin 环境 bring-up；
- 三相机与 14D observation/action interface；
- 50 条成功 expert trajectories；
- LeRobot 数据转换；
- norm stats；
- π0.5 SFT checkpoints；
- physics sidecar；
- contact / grasp / geometry 等辅助信号；
- 训练 / 评估脚本和排错经验。

这些资产对 Phase 0 和 Phase 1 都有价值。

但 hammer 单任务有几个问题：

1. success 定义未必完整刻画“高质量物理交互”；
2. impact / tool use 只是物理交互的一种机制；
3. 单任务容易把工程特例误当成一般结论。

所以新的定位是：

> **Hammer = Task 0 / Pilot / Regression Task**

用于：
- Reference checkpoint 验收；
- RLT pipeline bring-up；
- 每次代码重构后的 regression；
- physics logging 验证。

但论文核心结论必须来自多任务。

---

### 1.3 第一批多任务应覆盖什么？

不追求任务数量，而追求物理机制差异。

推荐最小组合：

| Task | 机制 | 作用 |
|---|---|---|
| Hammer | tool / impact | 保留已有资产，验证 pipeline |
| Precision contact | local alignment / point contact | 验证小误差纠正 |
| Insertion / constrained contact | contact-rich / constraint | 验证精细约束、卡住与恢复 |

Task 1 / Task 2 的具体任务名以 RoboTwin2 当前可用环境、reward 和 success 定义审计为准，不因为名字听起来“精细”就自动进入正式实验。

---

### 1.4 Phase 0 完成标准

至少满足：

1. 三类物理机制任务；
2. 统一 task adapter；
3. 统一 observation/action contract；
4. 统一 reference evaluation；
5. 统一 online RL logger；
6. 固定 train / eval seeds；
7. 每个任务都有 reference 与 RLT learning curve；
8. episode-level raw metrics；
9. 失败视频；
10. checkpoint/config 可恢复；
11. action timing / executed action / replay transition 无未解释差异。

---

## 2. RLT Baseline Contract

我们使用 π0.5 与本地环境，因此必须把：

- **RLT-π0.5-adapted**
- **Local-Residual**

明确分开。

### RLT-π0.5-adapted

目标是尽量保留原论文：

- compact readout；
- reference-conditioned actor；
- action anchoring / regularization；
- reference dropout；
- chunk-level TD；
- off-policy replay。

只做基础模型与环境适配。

### Local-Residual

本地已有 residual actor、K=1 或历史切换逻辑。

它可以用于 bring-up / 实用对照，但不能无条件称作原论文 RLT。

### 必须核查

1. 基础模型 checkpoint 与 SFT 数据。
2. compact representation 从哪层取。
3. Stage 1 / Online 阶段哪些参数更新 / 冻结。
4. Actor 输出完整 chunk 还是 residual。
5. Critic input / target / TD backup。
6. 预测 H、执行 C、control frequency、policy decision frequency。
7. replay 存计划 action 还是真实 executed action。
8. reward / terminal / timeout。
9. policy switch / critical phase 逻辑。
10. train/eval seeds 与预算单位。

---

## 3. 当前已有资产：哪些继续用？

### 3.1 直接保留

- hammer environment；
- expert collector；
- 50 条成功 demo；
- LeRobot 数据；
- norm stats；
- π0.5 SFT checkpoints；
- physics sidecar；
- contact / grasp / geometry labels；
- evaluation / video / logging 脚本；
- 当前训练环境和 server / client 接口经验。

### 3.2 改造成共享基础设施

过去为 hammer 写死的内容，要逐步抽成：

- task adapter；
- observation mapper；
- action mapper；
- reward / success wrapper；
- episode logger；
- video recorder；
- seed manager；
- checkpoint evaluator；
- replay schema。

目标是：

> 新增一个 RoboTwin2 task，不再重新复制一套训练代码。

### 3.3 暂时不丢，但不作为主线

Physics sidecar 暂时不要删除。

它在 Phase 0 只负责：
- logging；
- failure taxonomy；
- representation probe；
- 后续 D1–D5 诊断。

只有 Phase 1 证明它有 decision-relevant 增量后，才进入 Phase 2 方法设计。

---

## 4. Phase 1 — Failure Diagnosis

Multi-task RLT baseline 稳定后，先做最便宜诊断。

### D1 · Input / History

比较：
- command target；
- + actual q；
- + short history。

问：缺的是“物理表示”，还是缺真实执行可观测性？

### D2 · Candidate Headroom

同状态执行：
- base action；
- 少量合法 correction candidates。

后续策略固定。

问：Reference 周围到底有没有可利用的改进空间？

### D3 · Supervision Purpose

控制 feature / data / capacity，比较：
- reconstruction；
- future latent；
- physical consequence；
- correction benefit。

问：physics 最适合进入 representation、value 还是 correction？

### D4 · Data Coverage

相同新增预算：
- 普通 expert；
- failure / near-failure / recovery。

问：收益来自算法，还是终于覆盖了失败附近？

### D5 · Execution Horizon

固定 C=1 / 5 / 10，记录：
- control frequency；
- VLA calls；
- actual executed action span。

问：真正瓶颈是不是 feedback 太慢？

---

## 5. Phase 2 — Physical Experience Representation

Phase 2 不是默认会发生。

只有 Phase 1 证据支持后，才选择 1–2 个方向：

### R0 · Action Consequence

研究：

\`\`\`
(state, action) → decision-relevant consequence
\`\`\`

例如：
- relative geometry change；
- contact event；
- object motion；
- slip / stuck；
- progress。

### R1 · Value-Oriented Physics

如果 candidate set 已有明显更优动作，则把 privileged physics 用于：
- critic teacher；
- candidate ranking；
- value distillation。

### R2 · Correction Benefit

如果 correction headroom 明显，但无效干预很多，则学习：
- 是否应该纠偏；
- 哪种 correction 值得执行。

### R3 · Execution History

如果 D1 表明 actual state / history 已解释大部分收益，则优先解决 observability。

---

## 6. Phase 3 — Self-Improvement Loop

先区分三种自我改进：

### Context Adaptation

参数不更新，只改变 Memory / Context。

代表：Zeva。

### Online Policy Adaptation

更新 lightweight actor / critic / readout。

代表：RLT / SmoothRL。

### Experience Consolidation

把验证过的新经验回写 foundation policy。

代表：PLD。

### 最小多轮协议

1. 冻结 task set / final test / 总交互预算。
2. Round 0 保存 base policy 与独立评估。
3. 每轮相同新增交互预算。
4. 记录 success / failure / recovery / intervention。
5. 更新后在未参与训练的 initial states 上评估。
6. 每轮回测旧任务 / 旧 dynamics。
7. 报告人工、数据、计算成本。

---

## 7. RoboDojo：B300 每日小任务

RoboDojo 当前不抢主线资源。

定位：

> **每天固定少量时间推进的第二实验平台 bring-up。**

### 目标顺序

1. 确认 B300 上 CUDA / PyTorch / simulator / rendering 兼容。
2. 安装官方依赖。
3. 跑官方最小 smoke。
4. 明确 observation / action contract。
5. 跑 Dojo-Eval。
6. 最后才讨论 Dojo-RL。

### 每日记录

每天只要求留下一个可检查产物，例如：
- 安装到哪一步；
- 哪个依赖不兼容；
- 完整错误日志；
- 修复方法；
- 官方示例是否成功；
- GPU / renderer / driver 状态。

避免“今天折腾了一下环境”这种不可复用记录。

---

## 8. 近期行动顺序

### P0

Hammer checkpoints：
- 5k / 10k / 15k / 20k；
- 同一开发 seeds；
- success / stage profile / video；
- 冻结共同 Reference。

### P0

RLT 原文 vs 本地代码差异审计。

输出：
- readout；
- actor；
- critic；
- H / C；
- replay；
- reward；
- switch；
- learner / rollout timing。

### P1

Hammer 上完成首个 RLT-π0.5-adapted baseline。

### P1

迁移 RoboTwin2，新增至少两个不同 contact mechanism 任务。

### Side Track

每天推进 RoboDojo on B300。

---

## 9. 每日论文阅读的角色

论文不是 roadmap。

每篇论文只回答：

1. 它解决什么？
2. 它的核心方法？
3. 最重要证据？
4. 它占掉我们哪块创新空间？
5. 它是否要求新增 baseline / ablation / diagnosis？
6. 如果不影响当前 Phase 0，就归档，不改变主线。

---

## 10. 长期 North Star

**Physical Experience Flywheel**

\`\`\`
Deploy
  ↓
Experience
  ↓
Evaluate
  ↓
Learn
  ↓
Redeploy
  ↓
Consolidate
  ↓
Share
\`\`\`

最终目标不是单个机器人不断重复踩坑，而是让一个本体自主纠错产生的经验，被后续任务、后续本体和下一代 foundation policy 复用。

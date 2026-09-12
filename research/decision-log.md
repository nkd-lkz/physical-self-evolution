# 科研决策日志

## 2026-09-12 · Paper-aligned Stage 1 口径纠正

**决定：**

第一条 hammer RLT 主线 Stage 1 从 **通用 π0.5 base** 开始，在目标任务 demonstrations 上联合完成：

- VLA task loss；
- RLT reconstruction loss。

本地沿用 RLinf 的 `rlt_alpha=1.0`。独立训练好的 20k task-SFT checkpoint 只保留为：

- standalone reference；
- post-SFT 工程兼容性/额外对照。

它不再作为 paper-aligned Stage 1 的必要初始化。

**原因：**

重新核对论文训练流程与本地代码梯度语义后，确认 `prefix_out.detach()` 使 RLT reconstruction 不回传 VLA；当 alpha>0 时 VLA 由 `vla_loss` 更新。本地 base-init 1-step smoke 已通过，支持进入 2,000-step joint-full。

---

## 2026-09-12 · Stage 2 正式口径固定为 C=10

**决定：**

- 正式 RLT Stage 2 action chunk 使用 `C=10`；
- π0.5 reference horizon 为 `H=50`；
- reference dropout 为 0.5；
- `C=1` 只用于 transition / 接线错误定位，不能称为论文设定复现。

当前本地 actor 仍是 `Local-Residual` 参数化，因此正式记录使用：

**RLT-π0.5 adapted / Local-Residual**。

**原因：**

mock 时序已经覆盖逐子步 reward/done、early done、actual executed length、terminal observation 与跨 chunk freeze；下一门槛是真实环境 C=10 rollout。

---

## 2026-09-12 · RoboTwin 2.0 版本顺序

**决定：**

1. 先在 **RoboTwin 2.0 / RLinf_support pinned path** 完成第一条 RLT Stage 1/2 baseline；
2. baseline 冻结后，再迁移到 RoboTwin 2.0 `main` bridge；
3. 不同时切换环境版本和算法复现，以免无法归因。

**原因：**

`RLinf_support` 是 RLinf 当前训练兼容路径，不应误写成“RoboTwin 1.0”。latest-main bridge 已完成 transition alignment，但尚无真实 learner update。

---

## 2026-09-12 · Reference 正式评估前固定双重随机性

**决定：**

当前 4-env checkpoint sweep 只用于开发期快筛。正式 reference/RLT 配对评估前必须同时固定：

- environment seed；
- action-sampling seed。

**原因：**

当前环境初态固定，但 π0.5 action generation 的 Gaussian noise 尚未使用固定 generator，因此 5k/10k/15k/20k 的 4-env 结果不能被解释为严格可重复的 checkpoint 排名。

---

## 2026-09-12 · Physics sidecar 暂不进入 baseline observation

**决定：**

已有 contact / impulse / actual state / object dynamics sidecar 继续作为：

- logging；
- failure analysis；
- future representation probe；
- future critic/reward/auxiliary target 候选。

第一条 RLT baseline 不把这些 simulator privileged labels 拼入 actor/policy observation。

**原因：**

先保持第一条 baseline 无 privileged information leakage，再由 Phase 1 诊断决定是否进入 Phase 2。

---

## 2026-09-11 · 四阶段主线

**决定：**

将科研主线改为：

1. Phase 0 — RLT Multi-task Benchmark
2. Phase 1 — Failure Diagnosis
3. Phase 2 — Physical Experience Representation
4. Phase 3 — Self-Improvement Loop

**原因：**

当前项目已经积累足够多的候选 idea，但缺少统一、跨任务、可归因的 baseline 基座。继续增加 Physical Token / WAM / Streaming 会扩大不可控变量。

---

## 2026-09-11 · Hammer 的重新定位

**决定：**

Hammer 不放弃，但从“主故事任务”调整为 **Pilot / Regression Task**。

**原因：**

- 已有工程与数据资产价值很高；
- 适合首个 RLT bring-up；
- 但单一 tool-impact 任务无法代表精细物理交互的一般结论。

---

## 2026-09-11 · RoboTwin2 / RoboDojo 分工

**决定：**

- RoboTwin2：当前主线，负责 Multi-task RLT benchmark 与算法开发。
- RoboDojo：B300 上每日小任务推进，先完成安装 / smoke / Dojo-Eval，不抢主线。

---

## 2026-09-11 · Research Story

**决定：** 不再以 RL Token / Physical Token 为上位故事。

**改为：** Physical Interaction + Self-Improvement。

---

## 2026-09-11 · Paper Reading Guardrail

新论文默认只进入知识库，不自动修改研究主线。

只有以下情况才改变主线：

1. 实验直接否定当前解释；
2. 强近邻已经覆盖核心 novelty；
3. 新工作提供更简单且更强 baseline；
4. 工程现实暴露当前问题定义错误。

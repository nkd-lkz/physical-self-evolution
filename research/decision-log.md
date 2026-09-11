# 科研决策日志

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

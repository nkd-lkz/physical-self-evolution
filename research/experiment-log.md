# 实验日志

## 2026-09-11 · 主线更新：进入 Phase 0

### 事实

- 现有 hammer 工程资产可用，但单任务不再作为项目唯一主线。
- π0.5 SFT 5k / 10k / 15k / 20k checkpoints 已生成。
- Reference checkpoint 尚未完成正式独立评估。
- RLT baseline 仍无正式可引用结果。
- RoboDojo 将作为 B300 上的每日小任务旁线推进。

### 解释

当前最缺的不是新 idea，而是：

1. 多任务 RLT baseline；
2. 统一 task / logger / evaluator；
3. 明确 RLT 原论文与本地实现差异；
4. 之后才能做 failure diagnosis。

### 下一步

1. Hammer checkpoints 统一 seeds 评估。
2. 冻结 Reference。
3. RLT 代码审计。
4. Hammer RLT baseline。
5. RoboTwin2 新增两个不同物理机制任务。
6. B300 上每天推进 RoboDojo 安装 / smoke。

---

## 2026-09-11 · 旧实验资产如何复用

### 保留

- hammer env / collector；
- 50 demos；
- LeRobot 数据；
- norm stats；
- π0.5 SFT；
- physics sidecar；
- contact / grasp / geometry labels；
- eval / logging / video scripts。

### 重新定位

- hammer：Pilot / Regression Task。
- physics sidecar：先做 logging / diagnosis，不直接变成 actor input。
- Physical Token：从“计划中的下一模块”降为 Phase 2 候选。

---

## 记录模板

### 日期 · 标题

**事实**

**证据**
- checkpoint:
- config:
- log:
- video:

**解释**

**影响哪个研究假设**

**下一步最便宜的证伪实验**

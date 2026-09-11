# RLT Multi-task Benchmark 执行文档

> 当前阶段：Phase 0  
> 目标：先建立稳定、可复现、可扩展的 RLT 多任务实验台，再开始方法创新。

---

## 1. 为什么不是直接继续 hammer？

Hammer 不丢弃，但降级为 **Task 0 / Pilot / Regression Task**。

已有资产很多：
- 环境已经打通；
- expert collector 可用；
- 50 条成功 demo；
- π0.5 SFT checkpoints 已有；
- physics sidecar 可用于诊断；
- logging / video / evaluation 经验已有。

这些资产最适合用来做：
1. Reference checkpoint 验收；
2. RLT pipeline bring-up；
3. 代码重构后的 regression；
4. 后续 D1–D5 诊断。

但单一 hammer 不能代表：
- precision contact；
- insertion；
- sustained contact；
- constraint-rich interaction。

因此多任务 benchmark 才是 Phase 0 的真正产物。

---

## 2. 第一批任务组合

### Task 0 · Hammer

机制：
- tool manipulation；
- impact；
- contact establishment。

作用：
- 复用已有资产；
- 建立第一个 Reference + RLT 完整闭环。

### Task 1 · Precision Contact

目标机制：
- local alignment；
- point contact；
- 小误差容忍度低。

具体任务名在 RoboTwin2 中以实际 reward / success / physics 审计后确定。

### Task 2 · Constrained Contact / Insertion

目标机制：
- insertion；
- friction；
- constraint；
- stuck / recovery。

同样先检查：
- collision geometry；
- penetration；
- artificial snap / attach；
- success tolerance；
- reward 是否作弊。

---

## 3. 统一 Benchmark Interface

希望最终抽象成：

\`\`\`
TaskAdapter
├── reset(seed)
├── get_observation()
├── map_policy_action()
├── step(action)
├── get_reward()
├── is_success()
├── is_terminal()
└── diagnostics()
\`\`\`

每个任务都输出统一日志：

\`\`\`
episode_id
seed
task
checkpoint
reference_action
actor_action
executed_action
reward
success
terminal_reason
eef_pose
q / qdot
contact
episode_length
inference_latency
chunk_length
video_path
\`\`\`

---

## 4. Reference Protocol

每个 task 都必须先有 Reference-only 结果。

### 开发阶段

固定一组 dev seeds，用于：
- checkpoint selection；
- pipeline debug；
- reward / success audit。

### 最终评估

使用独立 eval seeds。

不要：
- 一边训练；
- 一边根据 final test seeds 调 checkpoint。

### 最低记录

- success rate；
- episode length；
- completion time；
- earliest failure stage；
- video；
- terminal reason。

---

## 5. RLT Baseline Protocol

### Stage 1

记录：
- VLA checkpoint；
- hidden layer；
- readout architecture；
- reconstruction objective；
- 哪些参数 trainable。

### Stage 2

记录：
- actor architecture；
- critic architecture；
- actor parameterization：full chunk / residual；
- reference action input；
- BC / anchor weight；
- reference dropout；
- gamma；
- target update；
- replay size；
- batch size；
- update-to-data ratio；
- warmup data source。

### Timing

记录：
- VLA horizon H；
- RL chunk C；
- control Hz；
- policy decision Hz；
- inference latency；
- robot 在 inference 期间是否执行旧 action。

---

## 6. 完成标准

单个任务：
- Reference ≥ 3 independent eval runs；
- RLT ≥ 3 train seeds；
- 每个 seed 有 learning curve；
- checkpoint 可恢复；
- raw metrics 可导出；
- failure video 可回看。

Phase 0：
- 至少 3 类 interaction mechanism；
- 同一代码入口；
- 同一 metrics schema；
- 同一 seed policy；
- 同一预算定义；
- 无隐式 privileged information。

---

## 7. 当前本周动作

### A. Hammer

1. 评估 20k checkpoint 少量完整 episodes。
2. 若能正常 rollout，再比较 5k / 10k / 15k / 20k。
3. 冻结 Reference。
4. 跑 RLT-π0.5-adapted smoke。
5. 再扩到多 seed training。

### B. RLT Code Audit

逐项对照：
- paper；
- RLinf 实现；
- 本地实现。

输出差异表。

### C. RoboTwin2

先不大规模跑。

先完成：
1. 环境版本确认；
2. observation/action interface；
3. 选两个不同 contact mechanism 的候选任务；
4. success / reward / physics audit；
5. 做 task adapter。

---

## 8. 什么时候进入 Phase 1？

只有当下面成立：

- multi-task reference 稳定；
- RLT 能重复训练；
- evaluation pipeline 稳定；
- failure video / raw metrics 能分析；
- action timing / replay transition 已对齐。

然后才做 D1–D5。

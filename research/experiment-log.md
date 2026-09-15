# 实验日志

## 2026-09-15 · 日报快照：Stage1 运行中 + clean500 + RoboDojo D0–D4

### 事实

- 新的 `pi05_base + rlt_alpha=1 + 20k` hammer Stage1 已正式启动。13:29 UTC 快照为 `2459/20000`，`global_step_2000` 已保存；最近 `loss/rlt/vla/grad = 0.254/0.252/0.00251/1.27`，均为有限值。run 未结束，不能记为能力恢复完成。
- clean500 成功示范采集已启动。快照时有 160/500 条成功 raw trajectories，其中 110 条为 clean50 之外的新增成功轨迹。最终 HDF5 / physics sidecar / video 尚未达到 160 份，因此不能写成“160 条最终数据完成”。
- clean500 后处理已预先固定为 `train450/val50`，norm stats 只使用 train450。
- RoboDojo D0–D2 已完成：固定源码/子模块、约66GB assets、独立 Isaac runtime 与 Isaac/IsaacLab import 均通过。D1 doctor 为 13 PASS / 4 WARN / 0 FAIL，D2 doctor 为 14 PASS / 3 WARN / 0 FAIL。
- RoboDojo D4 已完成：XPolicyLab CPU WebSocket closed loop 完成 10 episodes × 20 action steps = 200 steps；ARX X5 joint action schema 为 14D float32，chunk length 2。
- RoboDojo D3 尚未执行，因此还没有 B300 headless RGB renderer/device 的实验结论；D5 原生任务、D6–D7 Dojo-Eval、D8–D9 Dojo-RL、D10 baseline 均未开始。
- 已发现 Isaac runtime 与 XPolicyLab policy 的 `websockets` 依赖冲突，目前采用独立 simulator / policy 环境；CPU bridge schema 4/4 tests 与 lint 检查通过，但尚未接真实 env。

### 解释

今天三条线都属于 **Gate 0 / infrastructure strengthening**：

1. Stage1 20k 用于恢复更可信的 RL Token / RLT reference；
2. clean500 用于降低 clean50 小数据重复和后期过拟合风险；
3. RoboDojo 用于建立第二平台的可复现实验基础。

它们都不能提前写成 Physical Token 的算法收益。

### 下一步

1. 保持 Stage1 20k 正常运行；结束后固定 seed + action seed 评测 `2k/4k/.../20k` 的 H50/C50 闭环能力。
2. clean500 收满 500 raw success 后做完整性校验，再做 CPU-only `train450/val50` 转换和 train450-only norm stats。
3. 等允许使用的 GPU 空闲后，RoboDojo 首先执行 D3 headless/RGB gate；通过后才跑 D5 原生 task，再进入 RLinf reference adapter。
4. B0 稳定前不启动 B1/B2 大消融。

详细记录：`research/progress-2026-09-15.md` 与 `research/robodojo-b300-log.md`。

---

## 2026-09-15 · Hammer RLT baseline recovery：先恢复可信 B0，再进入 Physical Token

### 事实

- 旧 hammer Stage1 `base-init + rlt_alpha=1 + 2k` 已完成工程训练，但训练预算明显低于 standalone task-SFT20k：2k/global batch32 vs 20k/global batch64，样本槽位约相差 20×。
- 离线动作误差检查显示旧 Stage1 的动作 MAE 约高于 SFT20k 4–5×；这支持“旧 Stage1 任务能力不足风险”，但尚不能把训练步数定义为唯一根因。
- H/C 执行协议是另一个独立混杂变量：已有 H50 checkpoint 在 RoboTwin 原生整段 TOPP 下用 H50/C50 能成功；此前 H50/C10 会改变 TOPP 规划边界、物理时长和再观测分布，因此旧 C10 结果不能直接代表 Stage1 权重失效。
- 固定 H50/C50 开发配对中，目前有一个 seed 两者都失败、一个 seed 为旧 Stage1 失败而 SFT20k 成功；另有一个额外正对照 seed 两者都成功。其余配对未完成的 seed 不计入结果。
- 官方 expert 已在一个验证场景中完成任务，并沿 native→adapter 链路产生正 reward / success / terminated；因此目前没有证据支持“任务永远无法产生正奖励”。
- 新 Stage1 决策为：从通用 `pi05_base` 开始，`rlt_alpha=1`，联合 VLA task adaptation + RLT reconstruction，20,000 optimizer steps，2-GPU data parallel，global batch64、micro batch2、每 rank gradient accumulation16、warmup1000、每2000步保存。
- `SFT20k + alpha0 + 2k` 暂缓，保留为后续保能力 / 初始化方式对照。

### 解释

当前是领导版主线中的 **Gate 0 — Baseline Recovery**。需要严格区分 execution protocol 与 Stage1 capability；只有 B0 可解释后，B1 transition grounding / B2 physics grounding 才有因果意义。

### 下一步

1. 完成新的 `base + alpha1 + 20k` Stage1 joint training。
2. 对 `2k/4k/.../20k` checkpoints 做固定 environment seed + action seed 的 H50/C50 闭环评测。
3. 不按 train loss 最低选权重；按 success、completion time、failure stage 和配对稳定性选 Stage1 checkpoint。
4. 冻结 Stage1 reference 后重新设计 Stage2 B0；旧 C10 Stage2 只保留为工程闭环证据。
5. B0 稳定后再进入 B1 `+ measured transition` 与 B2 `+ valid physics`。

---

## 2026-09-14 · 领导方案约束后的科研主线修正

### 事实

- 领导提供的 Physical Token 方案把研究问题明确收敛为：从现有 action-generation head 读取 compact token，用 measured transition prediction 与有效 physics constraints 进行 grounding，再通过小型 online learner 在冻结 action model 的条件下适应变化的接触动力学。
- Physical Token 第一版输入侧包含 action-head pre-output features、recent measured robot state、actual/executed-action history 与 robot/control metadata。
- 当前“Universal”只定义为 shared token shape + shared physical objectives + lightweight model/robot adapters；跨 model family / embodiment 仍是待验证假设。
- 第一组正式比较固定为：B0 RL Token / matched head-readout baseline；B1 + measured transition loss；B2 + valid physics loss。
- 首轮 physics loss 只优先使用 kinematic consistency 与 actuator feasibility；contact/friction/force/rigid-body residual 只有 sensing、model、calibration 有效时才加入。
- 在线阶段默认 freeze base model、action head 与 token encoder/readout，只更新 small actor/critic。
- Streaming RL 保留为后续 online-efficiency 方向，不与首轮 Physical Token 表示变量同时改变。
- 现有 block assembly、drawer opening + placement 视频只记为 RL Token qualitative reproduction，不记作 Physical Token result。

### 解释

此前 Research OS 中的四阶段路线和大量 related-work synthesis 继续保留为历史探索、related work 与未来扩展，不再自动决定当前实验。当前 Source of Truth 是 `research/physical-token-leadership-spec.md`。

---

## 2026-09-12 · RLT Phase 0 关键推进

### 事实

- Hammer task-SFT checkpoint 快筛已完成：5k/10k/15k/20k 为 1/4、0/4、2/4、2/4；早期只固定环境 reset seed，因此仅用于开发期快筛。
- RLT Stage 1 paper-aligned base-init 1-step smoke 已通过；post-SFT warm-start loader 问题已修复，但不作为主线初始化。
- Stage2 C=10 的 transition/replay/update 工程链路已完成相关 mock 与真实 rollout 验证；2026-09-15 起 H50/C10 不再作为 Stage1 capability 锚点。
- RoboTwin 2.0 main bridge 已完成 transition alignment，但 learner migration 仍后置。

---

## 2026-09-11 · 历史探索：进入 Phase 0

此前将主线组织为 RLT Multi-task Benchmark → Failure Diagnosis → Physical Experience → Self-Improvement。该结构保留用于历史追溯；2026-09-14 起被领导版 Universal Physical Token 研究合同取代。

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

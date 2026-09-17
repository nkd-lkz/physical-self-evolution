# 实验日志

## 2026-09-17 · Stage1 固定20-seed能力曲线 + clean500全量审计 + clean490准备

### 事实

- 旧 clean50 `pi05_base + rlt_alpha=1` 长程 Stage1 最终停止在约 12.3k steps，没有完成原计划 20k；6k/8k/10k/12k 是本轮可完整验收的主要 checkpoint。
- 在统一 20-seed 开发 cohort、固定 `H50/C50 native_macro`、固定 training prompt 与 action-sampling seed 下，四个 checkpoint 均正常结束：6k `8/20=40%`、8k `7/20=35%`、10k `8/20=40%`、12k `10/20=50%`。
- 12k 是当前开发集上最高的 reference 候选，但曲线非单调、样本量有限且仍有 10/20 失败，不能宣布 Stage1 泛化问题已经解决，也不能把训练量/数据量/联合 loss 写成唯一根因。
- 历史 8k 的 `5/20` 使用不同 prompt/noise 协议，继续保留为历史记录，不与本轮 `7/20` 混算。
- 12k 同 cohort 的 full-physics video / chunk trace 入口已经准备并完成 CPU/dry-run 检查，但正式录像尚未执行；若单环境补录得到不同成功率，必须与原20环境聚合评测分开报告。
- clean500 已完整导出 500 条 raw/main/physics/video 数据，episode 连续、500 个 seed 唯一。全量数值、四相机 RGB、MP4 和 transition 对齐审计未发现结构性错误，repository physics validator 对 500 条均通过。
- 审计识别出 10 条强动作轨迹异常，主要表现为非初始关节目标分支跳变或异常初始绕转。原始文件保留，但从新 Stage1 动作监督和 train/eval candidate 中排除，形成 clean490。
- 另有 10 条动作轨迹连续但 contact/impulse 证据偏弱；这些轨迹保留用于 Stage1 动作学习，但 contact/impulse-specific auxiliary supervision 必须使用 validity mask，不能把缺失冲量当作“无接触/失败”真值。
- clean490 已固定为 `train450/eval40`：train450=70,640 indexes，eval40=6,238 indexes。norm stats 只由 train450 重新计算；eval40 是开发验证集，不是最终独立测试集。
- 新 clean490 Stage1 的数据转换、train-only norm、OpenPI loader、Hydra train/eval dry-run 与 focused CPU tests 已完成。最新默认训练计划为 generic `pi05_base + alpha1 + H50`、global batch64、dual-GPU、最多30k optimizer steps、warmup1k、每5k保存；正式 GPU run 尚未启动。

### 解释

今天把 Gate 0 从“长训练是否能救旧 Stage1”推进到了更可解释的状态：

1. 旧 Stage1 已证明具备部分闭环能力，但 12k 只是一项开发候选；
2. 数据规模扩张本身不能替代质量审计，正式训练集必须使用 clean490；
3. `contact=0` 与“没有真实接触”不是同义词，后续物理监督必须按标签有效性 mask；
4. 新一轮 Stage1 使用更多、质量更可控的数据重新建立 reference，但在结果出来前不能把数据扩充写成性能提升。

### 影响哪个研究假设

- 支持继续把 Hammer 作为 Gate 0 / representation-supervision feasibility 平台；
- 强化 B1 的数据合同：必须区分 proposed/reference action、actual executed action、command state 和 measured state；
- 强化 B2 的监督合同：物理标签按字段使用 validity mask，缺失/弱标签不能补零；
- 仍没有 Physical Token 的正式算法收益证据。

### 下一步最便宜的证伪实验

1. 先完成 12k full-physics failure-stage 画像，判断 10/20 失败主要集中在哪个阶段。
2. 启动 clean490 Stage1，按 `5k/10k/15k/20k/25k/30k` 做统一 eval40 能力曲线；连续多个 checkpoint 不改善时允许提前停。
3. 选择 development-best checkpoint 后，使用独立封存 reset seeds 做最终 reference 验证。
4. 只有 reference 与 B0 可解释后，再实现 B1/B2。

详细记录：`research/progress-2026-09-17.md`。

---

## 2026-09-15 · 日报快照：Stage1 运行中 + clean500 + RoboDojo D0–D4【历史快照】

### 事实

- 新的 `pi05_base + rlt_alpha=1 + 20k` hammer Stage1 已正式启动。13:29 UTC 快照为 `2459/20000`，`global_step_2000` 已保存；最近 `loss/rlt/vla/grad = 0.254/0.252/0.00251/1.27`，均为有限值。该 run 后续在约12.3k停止，因此本条只保留为历史运行快照。
- clean500 成功示范采集已启动。快照时有 160/500 条成功 raw trajectories，其中 110 条为 clean50 之外的新增成功轨迹。2026-09-17 已完成全500导出与审计，本条只保留为历史快照。
- 当时预先规划为 `train450/val50`；该决策已被 2026-09-17 clean490 审计后的 `train450/eval40` 正式划分取代。
- RoboDojo D0–D2 已完成：固定源码/子模块、约66GB assets、独立 Isaac runtime 与 Isaac/IsaacLab import 均通过。D1 doctor 为 13 PASS / 4 WARN / 0 FAIL，D2 doctor 为 14 PASS / 3 WARN / 0 FAIL。
- RoboDojo D4 已完成：XPolicyLab CPU WebSocket closed loop 完成 10 episodes × 20 action steps = 200 steps；ARX X5 joint action schema 为 14D float32，chunk length 2。
- RoboDojo D3 尚未执行，因此还没有 B300 headless RGB renderer/device 的实验结论；D5 原生任务、D6–D7 Dojo-Eval、D8–D9 Dojo-RL、D10 baseline 均未开始。

### 解释

该日三条线均属于 Gate 0 / infrastructure strengthening，不是 Physical Token 算法收益。

---

## 2026-09-15 · Hammer RLT baseline recovery：先恢复可信 B0，再进入 Physical Token

### 事实

- 旧 hammer Stage1 `base-init + rlt_alpha=1 + 2k` 已完成工程训练，但训练预算明显低于 standalone task-SFT20k：2k/global batch32 vs 20k/global batch64，样本槽位约相差 20×。
- 离线动作误差检查显示旧 Stage1 的动作 MAE 约高于 SFT20k 4–5×；这支持“旧 Stage1 任务能力不足风险”，但尚不能把训练步数定义为唯一根因。
- H/C 执行协议是另一个独立混杂变量：已有 H50 checkpoint 在 RoboTwin 原生整段 TOPP 下用 H50/C50 能成功；此前 H50/C10 会改变 TOPP 规划边界、物理时长和再观测分布，因此旧 C10 结果不能直接代表 Stage1 权重失效。
- 固定 H50/C50 开发配对中，当时已有一个 seed 两者都失败、一个 seed 为旧 Stage1 失败而 SFT20k 成功；另有一个额外正对照 seed 两者都成功。
- 官方 expert 已在一个验证场景中完成任务，并沿 native→adapter 链路产生正 reward / success / terminated；因此没有证据支持“任务永远无法产生正奖励”。
- 当时决策为：从通用 `pi05_base` 开始，`rlt_alpha=1`，联合 VLA task adaptation + RLT reconstruction，20,000 optimizer steps，2-GPU data parallel，global batch64、micro batch2、每 rank gradient accumulation16、warmup1000、每2000步保存。该 run 后续未完成20k，2026-09-17 已转向 clean490 新数据方案。

### 解释

该阶段定义了领导版主线中的 **Gate 0 — Baseline Recovery**。只有 B0 可解释后，B1 transition grounding / B2 physics grounding 才有因果意义。

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

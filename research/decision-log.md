# 科研决策日志

## 2026-09-15 · clean500 固定 train450 / val50，norm 只用 train450

**决定：**

Hammer 成功示范扩充到 500 条后，正式数据处理固定为：

- 500 条成功 raw trajectories 全量完成并先做完整性验收；
- 再固定拆分 `train450 / val50`；
- norm stats **只使用 train450** 计算；
- val50 不参与 norm 统计，也不参与训练期 checkpoint selection 的数据拟合。

**原因：**

当前 clean50 数据量小、重复采样高。扩充数据的目的之一是降低小数据重复和过拟合风险，因此必须提前冻结 train/val 与 norm 口径，避免后续根据结果调整划分造成泄漏。

---

## 2026-09-15 · RoboDojo 按 D0–D10 Gate 严格推进，D3 renderer 未通过前不跳到真实任务

**决定：**

RoboDojo 当前采用分层验收：

- D0–D2：源码/资产/runtime；
- D3：B300 headless app + RGB renderer；
- D4：XPolicyLab CPU protocol；
- D5：官方原生 task episode；
- D6–D7：RLinf reference / Dojo-Eval；
- D8–D9：training bridge / RLT L0；
- D10：完整 baseline。

截至当前：D0–D2 与 D4 已完成，D3 尚未执行。

**原因：**

Isaac Python import 成功不能替代真实 renderer/device 验收，XPolicyLab CPU closed loop 也不能替代 Dojo-Eval。保持 gate 分离可以避免把“环境能启动”“policy 协议能通信”“RLinf 已接入”“online RL 已跑通”混成一个结论。

---

## 2026-09-15 · RoboDojo simulator 与 policy runtime 继续隔离依赖

**决定：**

RoboDojo/Isaac simulator runtime 与 XPolicyLab policy runtime 保持独立 Python 环境；后续 RLinf integration 优先复用跨进程 bridge，而不是把所有依赖强行合并。

**原因：**

已观察到 Isaac runtime 与 XPolicyLab 对 `websockets` 的版本要求冲突。分离环境已完成 CPU protocol 验证，同时避免污染 hammer 训练环境。

---

## 2026-09-15 · 在 B0/B1/B2 之前增加 Gate 0：Baseline Recovery

**决定：**

领导定义的 Universal Physical Token 主问题不变，但实验顺序增加一个明确前置门槛：

```text
Gate 0A  恢复可用 Stage1 reference
Gate 0B  固定 RoboTwin execution / timing semantics
Gate 0C  建立可信 B0 online baseline
        ↓
B1 + measured transition
        ↓
B2 + valid physics
```

**原因：**

旧 Stage2 的零成功不能直接解释为“缺 physics”。当前已经确认 execution protocol 与 Stage1 capability 都可能影响结果；如果 B0 reference / online baseline 本身不稳定，B1/B2 的收益无法归因。

---

## 2026-09-15 · H50/C50 是当前 RoboTwin Stage1 能力锚点；H50/C10 只保留为历史诊断

**决定：**

- 当前已有 Stage1 checkpoint 使用 `H=50`；
- 在 RoboTwin 原生 TOPP 执行中，用 `H50/C50` 作为 reference 能力锚点；
- 旧 `H50/C10` 结果继续保留为工程与执行协议诊断，不作为 Stage1 能力公平结论；
- 后续论文式 `C=10` 必须单独设计并验证其控制/transition 语义，不能仅改推理字段后宣称与原论文等价。

**原因：**

每 10 个目标重新进入 TOPP 会改变规划边界、物理时长、再观测频率和状态分布。已经观察到同一 H50 policy 在 C10 与 C50 下行为明显不同。

---

## 2026-09-15 · Stage1 恢复优先采用 base + alpha1 + 20k joint training

**决定：**

当前优先运行：

- generic `pi05_base` initialization；
- `rlt_alpha=1`；
- joint VLA task adaptation + RLT reconstruction；
- 20,000 optimizer steps；
- 2-GPU data parallel；
- global batch64 / micro batch2；
- warmup1000；
- every 2000 steps save checkpoint。

`SFT20k + alpha0 + 2k` 暂缓，保留为后续保能力 / 初始化方式对照。

**原因：**

这一路径保留论文/官方的 base-init joint-training topology，同时把旧 2k Stage1 明显较小的训练预算补足。现有证据支持“旧 Stage1 存在能力不足风险”，但并未证明训练步数是唯一根因，因此新 20k run 被定义为 baseline recovery experiment，而不是“已知修复”。

---

## 2026-09-15 · Stage1 checkpoint 不能按最低训练 loss 选择

**决定：**

新 Stage1 以 `2k/4k/.../20k` 保存，并使用固定 environment seed + action seed 的 `H50/C50` 闭环能力曲线选择 checkpoint。

选择指标优先：

- success；
- completion time / episode length；
- failure stage；
- 与 SFT20k 的 paired behavior；
- 多 seed 稳定性。

训练 loss 只作为优化健康度，不作为最终选模标准。

**原因：**

当前 clean50 数据规模较小，20k×64 对应约 1.28M 样本槽位，存在高重复与后期过拟合风险；更低的 imitation / reconstruction loss 不等价于更好的闭环操作能力。

---

## 2026-09-14 · 领导约束后：主线改为 Universal Physical Token

**决定：**

从今天起，当前项目的上位研究主线固定为：

> **Universal Physical Token for Robot Self-Evolution**

核心目标是：

> 从已有 action-generation head 读出 compact token，通过 measured transition prediction 与有效 physics constraints 做 grounding，再用小型在线 learner 在冻结 action model 的前提下适应变化的接触动力学。

此前 Research OS 自动扩展出的“RLT Multi-task Benchmark → Failure Diagnosis → Physical Experience → Self-Improvement”四阶段路线不删除，但降级为**历史探索框架**，不再覆盖领导定义的主规范。

---

## 2026-09-14 · Physical Token 固定在 action-head readout

第一版 Physical Token 优先从 action head 的 pre-output / pre-projection features 读取，并显式融合 recent measured robot state、actual/executed-action history 与 robot/control metadata。必须保留 Action-head tap vs Backbone tap 作为关键对照。

---

## 2026-09-14 · Universal 是 empirical hypothesis，不是现有结果

当前“Universal”只允许表示 shared token shape、shared physical objectives 与 lightweight model-family / robot adapters；跨模型/跨本体必须通过 held-out 实验后再升级为结果。

---

## 2026-09-14 · Physical objective 首轮固定为 reconstruction + transition + valid physics

第一版：

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

`L_phys` 第一版优先 kinematic consistency + actuator feasibility；contact/friction/rigid-body/force-torque 只有 sensing、model、calibration 有效时才加入。

---

## 2026-09-14 · 首轮主实验固定为 B0/B1/B2，Streaming RL 后置

1. B0：RL Token / matched head-readout baseline；
2. B1：B0 + measured transition loss；
3. B2：B1 + valid physics loss。

表示变量与 learner 变量不同时改变。

---

## 2026-09-14 · Online self-improvement 的参数冻结边界

在线阶段默认 freeze base model、action head、token encoder/readout；只更新 small actor/critic。Outcome decoder 用 measured transitions 单独训练。

---

## 2026-09-14 · 现有视频只记为 RL Token qualitative baseline

现有 block assembly、drawer opening + placement 视频只作为 RL Token reproduction / qualitative baseline demonstrations。

---

## 2026-09-12 · Paper-aligned Stage 1 口径纠正

第一条 hammer RLT 主线 Stage 1 从通用 π0.5 base 开始，在目标任务 demonstrations 上联合完成 VLA task loss + RLT reconstruction；独立 20k task-SFT 保留为 standalone reference / post-SFT 对照。

---

## 2026-09-12 · Stage 2 正式口径固定为 C=10【历史工程口径，2026-09-15 增加执行协议限定】

RLT 论文 actor chunk 使用 `C=10`，但在 RoboTwin TOPP 语义下，`H50/C10` 不能直接作为已有 H50 Stage1 checkpoint 的公平能力锚点；论文式 C10 必须单独建立与验证控制/transition适配。

---

## 2026-09-12 · RoboTwin 2.0 版本顺序

先在 RoboTwin 2.0 / RLinf_support pinned path 完成第一条可信 baseline，再迁移 RoboTwin 2.0 main bridge；不同时切换环境版本和算法复现。

---

## 2026-09-12 · Reference 正式评估前固定双重随机性

正式 reference/RLT 配对评估前同时固定 environment seed 与 action-sampling seed。

---

## 2026-09-12 · Physics sidecar 暂不进入 baseline observation

已有 privileged sidecar 继续作为 logging、failure analysis、future representation probe 与 critic/reward/auxiliary target 候选；不直接拼进第一条 baseline policy observation。

---

## 2026-09-11 · 四阶段主线【已被 2026-09-14 主线取代】

该结构保留用于历史追溯，但不再是当前实验 Source of Truth。

---

## 2026-09-11 · Hammer 的重新定位

Hammer 当前定位为 pipeline regression、transition/physics logging 与 controlled ablation 资产，不定义 Universal Physical Token 的上位故事。

---

## 2026-09-11 · RoboTwin2 / RoboDojo 分工

RoboTwin / 现有 RL Token infrastructure 是当前 baseline 与 Physical Token 验证平台；RoboDojo 是独立支线，按自身 Gate 验收。

---

## 2026-09-11 · Paper Reading Guardrail

新论文默认只进入知识库，不自动修改研究主线；如果与领导主实验冲突，先完成领导定义的实验合同，再作为 baseline / ablation / discussion。

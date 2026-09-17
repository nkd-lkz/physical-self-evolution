# 科研决策日志

## 2026-09-17 · clean500 全量审计后正式收敛为 clean490 / train450 / eval40

**决定：**

- 500 条原始轨迹全部保留作审计证据；
- 10 条强动作轨迹异常从新 Stage1 动作监督和 train/eval candidate 中排除，不删除原始文件；
- 不为凑齐“500 条干净数据”继续补采，正式候选集使用 **clean490**；
- clean490 固定为 `train450 / eval40`；
- norm stats 只使用 train450；
- eval40 只用于开发 checkpoint selection，不能称为最终独立测试集。

**原因：**

全量审计说明“文件导出成功”与“动作轨迹适合监督”是不同层级。当前490条已经能形成稳定开发划分；继续补采会同时引入新的采集成本与分布变量。2026-09-15 的 `train450/val50` 只是采集未完成时的预案，从本条起被正式取代。

---

## 2026-09-17 · Contact / impulse 弱标签保留轨迹，但必须按标签 mask

**决定：**

10 条动作轨迹连续、抓取和末端几何可接受，但非零 contact/impulse 证据偏弱。它们：

- 保留用于 Stage1 VLA/RLT 动作学习；
- contact/impulse-specific auxiliary target 使用 validity mask；
- 不作为可靠的“没有接触 / 任务失败”负样本；
- 其他可靠 measured-transition 字段继续使用。

**原因：**

sidecar 中的非零冲量事件与任务几何接触/成功并非同一语义。缺失标签填零会把“未记录/弱证据”错误解释为真实负样本，直接污染后续 Physical Token 的物理监督。

---

## 2026-09-17 · 12k 是当前 Stage1 开发候选，不是最终 reference

**决定：**

统一 20-seed、`H50/C50 native_macro`、固定 prompt 与 action-sampling seed 下：

- 6k：8/20（40%）
- 8k：7/20（35%）
- 10k：8/20（40%）
- 12k：10/20（50%）

当前把 12k 作为 **development candidate**，继续做 full-physics failure-stage 分析与独立 seed 复核，不直接冻结为最终 reference。

**原因：**

曲线非单调，20 个开发 seeds 统计能力有限，而且 12k 仍有 10/20 失败。现有结果足以证明 Stage1 有部分闭环能力，但不足以证明泛化问题解决，也不足以把训练步数、数据规模或联合 loss 定成唯一根因。

---

## 2026-09-17 · 新 clean490 Stage1 默认 30k / 每5k保存，正式 GPU 训练尚未启动

**决定：**

下一轮 Stage1 baseline recovery 使用：

- generic `pi05_base`；
- `rlt_alpha=1`；
- H50；
- global batch64；
- dual-GPU data parallel；
- warmup1k；
- 默认最多 **30k optimizer steps**；
- 每 5k 保存 checkpoint；
- `5k/10k/15k/20k/25k/30k` 使用 eval40 做开发闭环选择。

30k 是训练上限，不是必须跑满；连续 checkpoint 无改善/下降时可以提前停止。CPU data/norm/loader/dry-run 已通过，但正式 GPU run 尚未启动。

**原因：**

旧 clean50 20k 会造成约162个等效 frame-level 遍历；新 train450 的30k约27个量级，不能把两者简单视为同一过拟合风险。训练步数仍然不能替代闭环验证。

---

## 2026-09-17 · B1 数据合同显式区分 command 与 measured execution

**决定：**

B1 measured-transition grounding 必须在 schema 中区分：

```text
reference / proposed action
actual executed action
command state
measured state
```

当前 Stage1 imitation dataset 的 `state` 继续保持已有 command/drive-target 语义；未来 B1 的 actual qpos / EEF / object consequence 必须来自 sidecar 或真实 rollout measurement，不能静默替换字段含义。

**原因：**

Physical Token 的科学问题是 action consequence grounding。如果用命令目标冒充实际状态，模型可能只学习控制器/命令映射，而不是执行后的物理后果。

---

## 2026-09-16 · 领导明确：Astra / Harness 属于 planner 侧参考，本项目坚持 actor-side Universal Physical Token

**决定：**

针对 GPT-6 Astra + π0.5 等近期工作，领导明确：

- 这些路线主要研究 **planner / reviewer / orchestration 如何使用已有具身策略**；
- 本项目与其有本质区别：**从 actor / action-generation head 内部提取通用 compact token**；
- token 需要通过 transition / physics grounding 获得对真实物理执行有用的表示；
- 最终评价不是 planner reasoning 是否更强，而是 **在 matched 条件下，是否提高最终物理交互任务成功率与在线适应能力**。

因此后续处理 Astra、Harness VLA、SHAPER 等工作时：

1. 继续阅读“别人怎么用 planner / harness”；
2. 可借 failure diagnosis、operating-range、validation gate 等分析思想；
3. 不把 LLM planner、memory、skill evolution 或 zero-shot reasoning 直接并入 B0/B1/B2；
4. 不把 planner-side 提升当成 Physical Token 的直接证据。

---

## 2026-09-15 · clean500 固定 train450 / val50【历史预案，已被 2026-09-17 取代】

当时在数据采集未完成时预先计划 `train450/val50`、norm 仅使用 train450。全量审计后发现10条强轨迹异常，因此正式方案更新为 clean490 `train450/eval40`。本条只保留历史决策轨迹。

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

领导定义的 Universal Physical Token 主问题不变，但实验顺序增加明确前置门槛：

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

旧 Stage2 的零成功不能直接解释为“缺 physics”。execution protocol 与 Stage1 capability 都可能影响结果；如果 B0 reference / online baseline 不稳定，B1/B2 的收益无法归因。

---

## 2026-09-15 · H50/C50 是当前 RoboTwin Stage1 能力锚点；H50/C10 只保留为历史诊断

- 当前已有 Stage1 checkpoint 使用 `H=50`；
- RoboTwin 原生 TOPP 下以 `H50/C50` 作为 reference 能力锚点；
- `H50/C10` 保留为执行协议诊断；
- 论文式 C10 必须单独建立控制/transition 适配。

---

## 2026-09-15 · Stage1 recovery 优先 base + alpha1 joint training【后续由 clean490 新方案继续】

该决策保留论文/官方 base-init joint topology。旧 clean50 长 run 后续停止于约12.3k；2026-09-17 起以 clean490 新数据和30k上限继续同一 baseline-recovery 思路。

---

## 2026-09-15 · Stage1 checkpoint 不能按最低训练 loss 选择

新 Stage1 必须使用固定环境/action seed 的 H50/C50 闭环能力选择 checkpoint，优先看 success、completion time、failure stage、paired behavior 与多 seed 稳定性。

---

## 2026-09-14 · 领导约束后：主线改为 Universal Physical Token

**决定：**

> **Universal Physical Token for Robot Self-Evolution**

核心目标：从已有 action-generation head 读出 compact token，通过 measured transition prediction 与有效 physics constraints 做 grounding，再用小型 online learner 在冻结 action model 的前提下适应变化的接触动力学。

---

## 2026-09-14 · Physical Token 固定在 action-head readout

第一版 Physical Token 优先从 action head 的 pre-output / pre-projection features 读取，并显式融合 recent measured robot state、actual/executed-action history 与 robot/control metadata。必须保留 Action-head tap vs Backbone tap 作为关键对照。

---

## 2026-09-14 · Universal 是 empirical hypothesis，不是现有结果

当前“Universal”只允许表示 shared token shape、shared physical objectives 与 lightweight model-family / robot adapters；跨模型/跨本体必须通过 held-out 实验后再升级为结果。

---

## 2026-09-14 · Physical objective 首轮固定为 reconstruction + transition + valid physics

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

Hammer RLT Stage 1 从通用 π0.5 base 开始，在目标任务 demonstrations 上联合完成 VLA task loss + RLT reconstruction；独立 task-SFT 保留为 standalone reference / post-SFT 对照。

---

## 2026-09-12 · Stage 2 C=10【历史工程口径】

RLT 论文 actor chunk 使用 `C=10`，但 RoboTwin TOPP 语义下 `H50/C10` 不能直接作为已有 H50 checkpoint 的公平能力锚点；论文式 C10 必须单独建立与验证控制/transition 适配。

---

## 2026-09-12 · Reference 正式评估前固定双重随机性

正式 reference/RLT 配对评估前同时固定 environment seed 与 action-sampling seed。

---

## 2026-09-12 · Physics sidecar 暂不进入 baseline observation

已有 privileged sidecar 继续作为 logging、failure analysis、representation probe 与 critic/reward/auxiliary target 候选；不直接拼进第一条 baseline policy observation。

---

## 2026-09-11 · 四阶段主线【已被 2026-09-14 主线取代】

该结构保留用于历史追溯，但不再是当前实验 Source of Truth。

---

## 2026-09-11 · Hammer 的重新定位

Hammer 当前定位为 pipeline regression、transition/physics logging 与 controlled ablation 资产，不定义 Universal Physical Token 的上位故事。

---

## 2026-09-11 · Paper Reading Guardrail

新论文默认只进入知识库，不自动修改研究主线；如果与领导主实验冲突，先完成领导定义的实验合同，再作为 baseline / ablation / discussion。

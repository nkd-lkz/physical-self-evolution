# 科研决策日志

## 2026-09-14 · 领导约束后：主线改为 Universal Physical Token

**决定：**

从今天起，当前项目的上位研究主线固定为：

> **Universal Physical Token for Robot Self-Evolution**

核心目标是：

> 从已有 action-generation head 读出 compact token，通过 measured transition prediction 与有效 physics constraints 做 grounding，再用小型在线 learner 在冻结 action model 的前提下适应变化的接触动力学。

此前 Research OS 自动扩展出的“RLT Multi-task Benchmark → Failure Diagnosis → Physical Experience → Self-Improvement”四阶段路线不删除，但降级为**历史探索框架**，不再覆盖领导定义的主规范。

**原因：**

领导最新 PPT 已把研究对象、表示位置、physical objectives、online update contract 和首轮消融写得更具体。后续仓库与网站优先按该定义维护，不再让宽泛的 AI 辅助 brainstorming 反向决定科研问题。

---

## 2026-09-14 · Physical Token 固定在 action-head readout

**决定：**

第一版 Physical Token 优先从 action head 的 pre-output / pre-projection features 读取，并显式融合：

- recent measured robot state；
- actual / executed-action history；
- robot morphology / control convention metadata。

通过 lightweight model adapter + learned readout 输出固定形状 `K × d` token。

必须保留：

> **Action-head tap vs Backbone tap**

作为关键对照。

**原因：**

“Action head 更接近物理动作生成”是研究假设，不是默认事实；action head 也可能丢失部分物理信息，因此必须实验验证 tap location 本身的贡献。

---

## 2026-09-14 · Universal 是 empirical hypothesis，不是现有结果

**决定：**

当前“Universal”只允许表示：

- shared token shape；
- shared physical objectives；
- lightweight model-family / robot adapters。

只有当前 model/robot 上成立后，才能进入 held-out head family 与 held-out embodiment 测试。

**禁止提前表述：**“已经适配所有 action model / 本体”。

---

## 2026-09-14 · Physical objective 首轮固定为 reconstruction + transition + valid physics

**决定：**

第一版目标：

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

其中：

- `L_ro`：stop-gradient action-head feature reconstruction；
- `L_dyn`：基于 actual/executed action 的 measured transition prediction；
- `L_phys`：优先 kinematic consistency + actuator feasibility。

Contact / friction / rigid-body / force-torque 项只有 sensing、model、calibration 有效时才加入。

**原因：**

避免把“模拟器里能导出的物理量”直接等价成“可信的物理监督”。首轮只使用定义明确、量纲与 frame 可核对的物理约束。

---

## 2026-09-14 · 首轮主实验固定为 B0/B1/B2，Streaming RL 后置

**决定：**

首轮正式比较固定为：

1. `B0`：RL Token / matched head-readout baseline；
2. `B1`：B0 + measured transition loss；
3. `B2`：B1 + valid physics loss。

严格 matched：token size、learner capacity、base model、data、interaction budget、reward、seed、chunk/timing。

Streaming Actor–Critic、batch≈1、no replay、uncertainty-aware update 等保留为后续 online-efficiency 方向，不与首轮 Physical Token 表示变量同时改变。

**原因：**

如果同时改 representation 和 learner，很难判断收益来自 Physical Token 还是 Streaming RL。

---

## 2026-09-14 · Online self-improvement 的参数冻结边界

**决定：**

在线阶段默认：

- freeze base model；
- freeze action head；
- freeze token encoder/readout；
- update small actor/critic；
- 使用 actual executed actions 与 task rewards；
- outcome decoder 用 measured transitions 单独训练；
- actor update 时 decoder weights frozen，但保留 action gradient。

**原因：**

项目要验证的是“轻量接口吸收物理变化”，而不是通过重新训练大 action model 获得提升。

---

## 2026-09-14 · 现有视频只记为 RL Token qualitative baseline

**决定：**

现有 block assembly、drawer opening + placement 视频，只记录为：

> **RL Token reproduction / qualitative baseline demonstrations**

禁止把它们写成 Physical Token / transition loss / physics loss / Universal 的实验结果。

---

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

先保持第一条 baseline 无 privileged information leakage。2026-09-14 之后，哪些字段能进入 `L_dyn/L_phys` 由领导版 Physical Token spec 的“measured / valid / calibrated”规则决定，而不是自动加入。

---

## 2026-09-11 · 四阶段主线【已被 2026-09-14 主线取代】

**历史决定：**

1. Phase 0 — RLT Multi-task Benchmark
2. Phase 1 — Failure Diagnosis
3. Phase 2 — Physical Experience Representation
4. Phase 3 — Self-Improvement Loop

**当前状态：**

该结构保留用于追溯此前探索，但不再是当前实验 Source of Truth。

---

## 2026-09-11 · Hammer 的重新定位

**决定：**

Hammer 不放弃，但从“主故事任务”调整为 **Pilot / Regression Task**。

当前进一步定位为：pipeline regression、transition/physics logging 与 controlled ablation 资产，不定义 Universal Physical Token 的上位故事。

---

## 2026-09-11 · RoboTwin2 / RoboDojo 分工

**决定：**

- RoboTwin / 现有 RL Token infrastructure：当前 baseline 与 Physical Token 验证平台；
- RoboDojo：B300 上的独立支线，仍须实测后才形成兼容性结论。

---

## 2026-09-11 · Research Story【已被 2026-09-14 具体化】

此前写为 Physical Interaction + Self-Improvement。

当前已收敛成：

> **Universal Physical Token：action-head compact readout + physical grounding + lightweight online adaptation。**

---

## 2026-09-11 · Paper Reading Guardrail

新论文默认只进入知识库，不自动修改研究主线。

当前新增规则：

> 如果论文观点与领导定义的主实验冲突，先按领导实验合同完成可验证结果，再把论文作为 baseline / ablation / discussion。

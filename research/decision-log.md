# 科研决策日志

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

## 2026-09-12 · Stage 2 正式口径固定为 C=10【历史工程口径，2026-09-15 增加执行协议限定】

**历史决定：**

- RLT 论文 actor chunk 使用 `C=10`；
- π0.5 reference horizon 为 `H=50`；
- reference dropout 为 0.5。

**当前限定：**

在 RoboTwin TOPP 语义下，`H50/C10` 不能再直接作为 Stage1 reference 能力的公平锚点；论文式 C10 必须单独建立与验证控制/transition 适配。

---

## 2026-09-12 · RoboTwin 2.0 版本顺序

**决定：**

1. 先在 **RoboTwin 2.0 / RLinf_support pinned path** 完成第一条可信 baseline；
2. baseline 冻结后，再迁移到 RoboTwin 2.0 `main` bridge；
3. 不同时切换环境版本和算法复现，以免无法归因。

---

## 2026-09-12 · Reference 正式评估前固定双重随机性

**决定：**

正式 reference/RLT 配对评估前必须同时固定：

- environment seed；
- action-sampling seed。

---

## 2026-09-12 · Physics sidecar 暂不进入 baseline observation

**决定：**

已有 contact / impulse / actual state / object dynamics sidecar 继续作为：

- logging；
- failure analysis；
- future representation probe；
- future critic/reward/auxiliary target 候选。

第一条 baseline 不把这些 simulator privileged labels 拼入 actor/policy observation。

---

## 2026-09-11 · 四阶段主线【已被 2026-09-14 主线取代】

该结构保留用于历史追溯，但不再是当前实验 Source of Truth。

---

## 2026-09-11 · Hammer 的重新定位

Hammer 当前定位为：pipeline regression、transition/physics logging 与 controlled ablation 资产，不定义 Universal Physical Token 的上位故事。

---

## 2026-09-11 · RoboTwin2 / RoboDojo 分工

- RoboTwin / 现有 RL Token infrastructure：当前 baseline 与 Physical Token 验证平台；
- RoboDojo：B300 上的独立支线，仍须实测后才形成兼容性结论。

---

## 2026-09-11 · Paper Reading Guardrail

新论文默认只进入知识库，不自动修改研究主线。

如果论文观点与领导定义的主实验冲突，先按领导实验合同完成可验证结果，再把论文作为 baseline / ablation / discussion。

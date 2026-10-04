# 证据与实验总日志

这里汇总已测结果、数据出处和结论范围。10-04 完成昨晚训练核查及四组冻结复评。当前尚未观察到记忆的控制收益。逐日条目保留原日期；旧条目的“正在运行”不是实时状态。

<a id="evidence-summary"></a>
## 已有证据支持到哪里

| 记录 | 已记录结果 | 来源与边界 |
|---|---|---|
| 09-30 ManiSkill Stage 1 reference | 固定 20 回合，8/20 成功 | [09-30 日报](progress-2026-09-30-maniskill-rlt.md)；不是 IM-RLT 结果，不与旧 Hammer 任务合并 |
| Zeva 配对执行诊断，10-03 汇总复核 | 无历史 MSE 1.8211e-4；原 attention 1.8143e-4；固定响应公式 7.3889e-5 | [证据清单](papers/interaction-memory-2026-10-03/evidence_manifest.json)；相同开发数据的预测对照，不是成功率 |
| 09-30 后续支持度门控诊断 | 六个初始化的总体 MSE 2.4417e-5；late MSE 1.6588e-5，固定公式 late 为 1.6571e-5 | [结构化续作记录](../data/continuation-2026-09-30.json)；数据参与方法选择，不能宣称在新条件上泛化；late 部分并未优于固定公式 |
| 既有 12 小时 memory run，10-03 汇总复核 | 516 outer steps；四条固定轨迹，最佳 2/4、后期 1/4 | [论文开发证据说明](papers/interaction-memory-2026-10-03/paper_en.html)；always-on 控制，缺少匹配无记忆长跑，不支持收益归因 |
| 10-01 合成延迟反馈诊断 | 最新版本 324 条方法×条件×seed 记录 | [证据门槛记录](../data/evidence-gates-2026-10-01.json)；复用配对随机流，不是 324 次独立机器人实验 |
| 10-03 双卡匹配启动 | zero／response 各完成两轮 smoke、28/28 Q-head 张量变化及两个保存点，随后开始正式训练 | [当日启动记录](progress-2026-10-03.md#matched-launch)；单 seed、8 个固定评估初态，无 expert、无 Stage 1B；不是收敛或方法有效性结论 |
| 10-04 第 275 轮模型复评 | 零 context 16/64；响应 15/64；响应关闭历史 18/64；reference 19/64 | [逐回合数据](../data/zeva-frozen-eval-2026-10-04.json)、[日报](progress-2026-10-04.md)；单训练 seed，未见记忆收益 |
| 当前方法的正式控制、纠错与迁移 | **待测** | 未完成新 Stage 1B 的匹配控制实验，不能宣称干预减少或持续自进化 |

原始 manifest、预测输出、夜间日志等部分材料未公开；[公开证据清单](papers/interaction-memory-2026-10-03/evidence_manifest.json)保留代码 revision、指标和 SHA-256。读者可核对公开摘要，但仅凭哈希不能独立复算。论文报告的作者结果、代码入口存在、CPU／GPU smoke 通过，分别属于外部报告、工程证据和链路验证，不自动成为算法有效性的证据。

<a id="dated-records"></a>
## 按原日期保留的记录

下列 10-03 写作条目记的是初稿第一版（25 篇文献、当时七个仓库），随后已更新为 v2（26 篇文献）和十个仓库的核查；详见[当日日报](progress-2026-10-03.md)和[当前仓库审计](literature/rlt-simulation-baselines-2026-10-03.md)。保留旧条目用于还原顺序，不把它们当作并列的最新总览。


## 2026-10-04 · 训练核查与冻结复评

昨晚两组达到 8 小时预算。299 / 309 轮完整记录，共同第 275 轮均为 3/8。随后冻结模型，四组各评估 64 回合。响应组没有增加成功数；只有 26/64 初态进入 actor 阶段。下一步先检查 baseline 的模仿误差与 Q 目标。[完整证据、tmux 清理与工程修复](progress-2026-10-04.md)。

## 2026-10-03 16:42 · Zeva 同容量对照进入双卡训练

固定 `91f7bdfa`，GPU 0 为零 context，GPU 1 为历史固定响应。两组短程更新、评估、保存及权重变化核验通过，随后从头启动相同预算的正式训练。首次 FSDP 失败与重启日志分开；新结果不并入固定论文 v2。[配置、边界与运行快照入口](progress-2026-10-03.md#matched-launch)。

## 2026-10-03 · 论文初稿、证据复核与 baseline 调研

完成英文交互记忆论文、中文执行指南、框架图、25 篇文献与拟议实验矩阵；复核既有 Zeva 响应预测和夜间运行，不新增 GPU 训练或独立评估。七个 RLT 实现核查后，优先对 AlphaBrain／LIBERO 做成品复评与两阶段重训验收；RLT_a 公开 92% 属作者结果，不是本项目复现。Stage 1B 与新记忆结构后移到 baseline 验收之后。

[完整日报与论文下载](progress-2026-10-03.md) · [baseline 核查](literature/rlt-simulation-baselines-2026-10-03.md)。以下旧作业“正在运行”的说法保留当时日期，本轮未重新确认运行状态。

---

## 2026-09-30 晚间 · Jev GPU pilot 完成，四条探索线边界更新

Jev 启发分支 `d3618b18` 在物理 GPU 2 完成 2-step smoke 和独立 20-step ManiSkill pilot，均正常退出。pilot 使用 2 个训练环境、4 个固定评估环境和 500 控制步上限，共完成 320 次 actor/critic 更新；outer step 4/9/14/19 的固定评估 `success_once` 均为 0.5，并保存 checkpoint 与 4 个视频。工程链路已覆盖 rollout、真实执行动作 replay、FSDP 更新、评估与保存。

能力结论仍为负向或未决：reference probability 约 0.901，learner batch 的 greedy/target non-reference fraction 全程为 0。即选择器没有表现出采用原子修正的证据，50% 不能归因为 Jev 式有限候选。下一轮先做 matched reference-only control，并检查 Q 排序、BC/reference prior 和数据支持，不直接延长训练。脱敏结果见[结构化记录](../data/jev-atomic-pilot-2026-09-30.json)。

同日晚间只读快照显示 baseline Stage 2 至少到 274/5000、`rlt/update_step` 超过 96,000，仍在 GPU 0/1 运行且人工干预率为 0。FLARE 的最新动作时序诊断、Zeva 的自适应旧经验清理和 VR 单环境 HIL pilot 均已提交，但没有新增匹配闭环收益或真人跨机器干预结果。四个开发分支与 baseline 继续隔离。

---

## 2026-09-30 下午 · 99 次预定诊断、12 次追加拟合与 HIL pilot

三条研究分支完成缓存／小模型续作，不改动 GPU 0/1 上正式 baseline；GPU 2 只共存约 574 MiB 的小模型进程，预定矩阵约 31 分钟完成。Zeva 将经验响应先验与支持度门控修正组合，6 种子总体预测 MSE 为 `2.4417e-5`，但物理条件突变与闭环仍待检验。Jev 的连续 residual 在 BC=70、参考动作替换 25% 时反胜有限候选，保留全部 36 次比较，不能宣称离散普遍更优。FLARE 的动作置零／打乱损害预测、逆序影响很小，尚无时序因果能力结论。

新增 FLARE matched pilot 已通过配置一致性与路径检查；VR `run_rlt_vr_hil_pilot.sh` 准备了一个 Windows/PICO 环境到 GPU 2 的单步 learner、有限更新、BC 发布门槛和完整恢复。两者没有新完整在线验收，不能代替正式 64 环境训练。本阶段 Jev 队列仍在等待 GPU 2，随后已于晚间完成，结果见本日志首条。代码、统计、论文邻近工作和可编辑图见[续作审查](three-branch-audit-2026-09-30.md)；本条不修改 RSI 综述区。

---

## 2026-09-30 · Stage 1 eval20、Stage 2 baseline、FLARE 对照与 Jev 分支

ManiSkill Stage 1 step 2000 的固定 20 回合闭环评测已经正常结束：`eval/success_once=0.4`、`return=0.4`、mean episode length `335.25`，即 8/20 成功。该点估计建立了当前 Stage 1 reference，但不能单独证明训练充分收敛、没有过拟合或 RL token 已学到物理规律。

正式 baseline Stage 2 已在 GPU 0/1 上运行，配置为 64 个训练环境、256 个固定评估环境和 5000 global step，自动 expert 关闭。截至快照至少到 `149/5000`、`rlt/update_step=46400`；global step 24/49/74/99/124 的评估成功率分别约为 37.89%/36.33%/40.23%/35.94%/42.19%。这是单个在途 run 的周期结果，不是五个独立实验，也不是最终 checkpoint。

FLARE 启发分支完成 baseline / sidecar 各 100 global step 的中等 smoke。两组均 exit 0，并各进行 200 次 actor/critic 更新；每 10 step 的 10 次单环境评估全部为 0 成功。训练中的 baseline 1 次、FLARE 2 次成功都发生在第 0 步、`actor_switch_rate=0` 的 VLA reference 阶段，不能归因于新 actor 或 sidecar。FLARE 的 54 个在线张量有 50 个变化，未来预测 loss 前 10/后 10 轮均值约 0.217/0.146，只能证明更新链路，不证明控制收益。下一轮需统一 `use_orig_params` 并延长可验证的 BC 热身。

新增 Jev 启发的 `research/rlt-jev-atomic-decisions` 分支（`020e0cf6`）。它不调用 Jev API，也不使用模拟器候选预演；在冻结 VLA reference 周围构造最多 17 个受限关节 chunk，由本地选择器决策，连续 critic 仍用实际执行动作训练。229 项 CPU 回归通过；合成诊断发现并修正 selector 饱和问题。该阶段 GPU 2 只读 `--check` 已通过、真实 smoke 尚未执行；晚间的后续提交与 pilot 结果见本日志首条。

五条线的提交、指标、边界和下一步 Gate 见[09-30 完整快照](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/progress-2026-09-30-maniskill-rlt.md)。本次不修改 RSI 综述区；Zeva 与 VR 没有新增能力结论。

---

## 2026-09-28 · ManiSkill RLT baseline、FLARE、Zeva 与 PICO VR 进展

新的 ManiSkill `PegInsertionSide` 实验线已形成四个隔离分支。Baseline Stage 1 从 step 750 保留 optimizer 状态恢复，并完成 `2000/2000`；最终权重已导出。20 个固定 reset 的闭环评测首次因缺少 `policy_setup` 在动作转换前失败，该次不计 episode；修复为 Panda joint-action pass-through 后，重跑已进入 rollout 与完整视频录制，最终成功率仍待任务结束。

FLARE 启发分支用真实未来观测的冻结 RLT latent 监督动作条件化预测。直接回归未来 latent 弱于状态保持；增量预测在固定 split、三个初始化和 horizon 1/5/10 上均得到更低 cosine error，且真实 Stage 2 smoke / resume 的参数更新审计通过。它仍未证明在线成功率、收敛或迁移收益。

Zeva 启发分支已修复 FSDP 下 memory reader 未进入 critic optimizer 的问题，真实 smoke 与续跑中 `17/17` reader 张量更新。成功示范和隐藏动力学诊断均未显示 learned reader 的稳定优势；固定历史响应公式明显更准，说明信息存在而读取方式仍是瓶颈。这一结果按负结果保留。

PICO VR 分支已达到 Windows 本地仿真与手柄调试，并完成 GPU 2 单环境 learner 的 40-transition scripted smoke、33 次 actor/critic 更新及 checkpoint 恢复。真实 PICO 跨机器上传与在线更新尚未整链验收，不能把 scripted takeover 计为人工干预结果。

四条线的具体提交、数值、解释边界和下一步 Gate 见[09-28 完整快照](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/progress-2026-09-28-maniskill-rlt.md)。本次不修改 RSI 综述区，也不把短 smoke 解释为算法有效。

---

## 2026-09-22 · 迁移核查与干预讨论整理（无新增GPU运行）

归档元数据确认train450/eval40无seed交叉，最后Stage1日志为10823；迁移包缺历史权重和原始数据。旧12k物理诊断20回合与新10k eval40严格区分。旧Stage2配置expert=null、请求/干预摘要为0，尚无Hammer专家纠错闭环。

新增[恢复入口](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/migration-recovery-2026-09-22.md)、[干预与时间语义](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/rlt-intervention-2026-09-22.md)、[物理经验研究合同](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/physical-experience-protocol-2026-09-22.md)及脱敏核查摘要。此项是资料核查与实验提案，不计作新训练、评测或Physical Token收益。以下早先入库的截图证据继续保留。

---

## 2026-09-22 · train450 Stage1 10k评测摘要补充（不新增独立样本）

### 事实与来源

- 用户提供的摘要截图报告：GPU6评测22/40成功（55%）、18/40失败；return=0.55，按步平均reward约0.00287，mean episode length=196.25，预算上限200步。
- 截图报告与此前GPU7聚合结果完全一致，W&B已同步但显示“0 media”。本轮未直接读取原始评测日志、逐seed轨迹或本地视频。
- 仓库09-18已记录同一train450 Stage1 10k、eval40双设备复测与相同聚合指标；本次未提供独立run ID，因此只补充证据与解释，不默认为第三次运行。入库日期不是新增评测执行日期。

### 解释边界

- reward约0.00287为按步平均值，不是任务成功时奖励幅度；return=0.55与成功时reward=1的稀疏设置相容。
- 平均196.25接近200步上限，需分别查看成功/失败长度、timeout数量与真实执行时长；不能由总体均值推断全部成功很慢或全部失败超时。
- 聚合一致支持当前固定seed/协议下的聚合复现，不证明逐seed/逐轨迹一致；重复cohort不合并为80个独立seed。
- W&B“0 media”不代表本地没有视频；本地存在性与可播放性尚待核对。
- 55%与旧clean50/12k的50%来自不同cohort，不直接宣称提升；reference闭环结果也不单独证明RLT latent收益。

### 下一步（待执行）

对齐run/config/checkpoint/norm版本 → 核对逐seed成败与终止原因 → 复盘18个失败 → 做同cohort checkpoint比较；训练规模及表征归因仍需匹配训练因素。完整说明：[09-22进展补充](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/progress-2026-09-22.md)。

---

## 2026-09-18 · train450 Stage1 10k复测 + B0 Stage2退化诊断

### 事实

- 新 clean490/train450 Stage1 在迁移前主动停止于约 10823/30000 steps；完整保存点为 5k 和 10k，不得写成“30k完成”。
- step10k 在完全一致的 `H50/C50 native_macro + eval40 + fixed prompt/action seed` 协议下完成两次独立设备运行，均为 `22/40=55%`，return≈0.55，mean episode length≈196.25，eval正常退出。
- 两次聚合一致只证明当前开发协议下的 aggregate reproducibility；使用的是同一40个seeds，不能当成80个独立样本。
- eval40 与 train450 seeds 不重叠，但其中19个seed已用于旧development comparison，因此不能与旧clean50/12k的10/20直接宣称显著提升。
- 旧 clean50/12k frozen reference 的 H50/C50 Stage2 周期评测从约45%下降到约15%，约985外层round后主动停止；最新完整checkpoint约900 round。
- Stage2最后critic loss≈0.0206、BC loss≈0.00306，但这不能证明Q准确或actor闭环安全。当前证据只是：该B0配置相对reference明显退化。
- RoboDojo本日状态保持D0–D5工程验收通过，D6真实reference与online RL仍待完成。

### 解释

今天最重要的结论不是“55%更强”，而是把两个问题进一步拆开：

1. 新train450 Stage1 10k具有比旧line更好的开发候选证据，但仍需matched-seed与independent-seed验证；
2. 旧B0 Stage2说明“online更新已经发生”远远不够，actor必须至少保持reference，否则不能作为Physical Token的公平baseline。

### 下一步

1. 复盘10k eval40的18个失败episode，并做5k/10k/旧12k同seed对照；
2. 运行BC-only/reference-consistency诊断；
3. 统计actor-reference action deviation，消融reference dropout与BC/Q配比；
4. 审计critic calibration和macro discount的真实时间语义；
5. 可信B0重建完成前，不进入B1/B2。

---

## 2026-09-17 · RoboDojo D3/D5 真实验证完成

### 事实

- 在显式共享 GPU 授权下，RoboDojo D3 B300 headless RGB renderer gate 已完成。最终通过的最小 USD 场景产生 `240×320×3 uint8` RGB，像素动态范围约 `85–247`，并完成人工可见性检查。此前黑图 run 保留为失败证据，不计作 D3 成功。
- D5 原生 `stack_bowls / ARX X5 / joint` 单环境、单 episode 已完成。运行到原生 800-action 上限，三路 camera 各产生 801 帧 `640×480 @ 25 FPS` 视频并通过解码 / 人工首帧检查。
- D5 使用 debug / near-zero action policy，因此 `success=0`、`score=0` 只说明该 debug policy 没完成任务，**不能解释为环境、VLA 或 RLT 性能失败**。
- D5 调试过程中补齐了隔离 runtime 中的 GLU/OpenGL、IsaacLab task runtime、ARX X5 planner 配置、B300 `sm_103` 对应的隔离 NVRTC 12.9 编译路径以及录像 ffmpeg PATH；Hammer venv / model / Torch / NumPy 未修改。
- 历史 doctor 的 import 检查存在 host-specific 假阳性风险：`conda run ... python -` + stdin 在本机可能 exit 0 但未执行 marker。本轮改用 direct `python -c` / import 作为真实 runtime 证据。
- ARX X5 原生 state 契约进一步明确：arm joint state 来自实际 `joint_pos`，gripper scalar 来自 previous control 的 command-derived state；14D proprio 不能整体称为 measured state。
- 一次 RoboDojo policy target 会在内部生成插值 / hold 控制项，因此一次 policy action 不是一个 physics tick。未来 RLT `C`、discount、early termination 和 measured transition 必须按真实 executed duration 定义。
- CPU bridge schema / transition contract 预验收合计 24/24 tests passed，其中 20/20 mock transitions 通过；这些仍不是 D8 真实 transition 验收。

### 解释

RoboDojo 已从“安装 / CPU protocol”推进到 **真实 renderer + 原生 task episode**。当前可以把 D3、D5 标为完成，但 Dojo-Eval / Dojo-RL 仍未完成。

这次最有研究价值的不是 debug policy 的成功率，而是跨平台数据契约进一步被具体化：

```text
fixed-size state vector
≠ all-measured physical state

policy action
≠ one physics tick
```

这会直接约束后续 Universal Physical Token 的 B1 measured-transition 定义。

### 下一步

1. D6：确定与 ARX X5 / target task 匹配的 checkpoint、processor、norm，先做 reference-only adapter。
2. D7：固定 seeds 做 Dojo-Eval，保存 raw reward / success / action trace / video。
3. D7 通过后进入 D8：single-env、`C=1`、20 条真实 `(s,a,r,s')` transition 对齐；显式记录 terminal observation 与 executed duration。
4. D8 通过后才接 replay / actor / critic 做 D9 RLT L0 smoke。

详细记录：`research/robodojo-b300-log.md`。

---

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

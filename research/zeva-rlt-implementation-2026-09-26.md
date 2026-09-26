# Zeva 精读及 RLT 最小可实验接口

> 2026-09-26 · 基于 [论文 v2](https://arxiv.org/html/2608.30880v2)、公开 [代码/复现说明](https://github.com/air-embodied-brain/Zeva)、[现有 RLT 合同](physical-experience-protocol-2026-09-22.md)。**仅完成代码审阅、原型和单元检查，尚无 RLinf 接入或效果结果。** 本文的 RLT 扩展都是待验证假设；原论文不是 RLT 在线 RL 方法。

## 直白解释

机器人碰物体后，先把**实际执行的前缀**、接触前后可观察变化和任务阶段存成一条经验；下次面临类似阶段时快速拿出来参考。原 Zeva 的两种记忆分别管当前这次尝试与同一 episode 中的前几次尝试，而权重不在部署时更新。我们要试的是：把这种快记忆作为小型 RLT learner 的**新增输入**，看相同交互预算下它能否更快学会接触动作。

## 原论文机制与训练边界

1. CTE 将观测、多步**已执行**动作和状态变化融合为 interaction state，产生 `phase p_t` 与 `effect e_t`；主文用 effect、任务对比、阶段单调目标训练。只看当前照片不足以得出“动作造成了什么变化”。
2. BIT 是本次 attempt 的短轨迹；PIM 用 `(phase,effect)` 整理同一 episode 中跨 attempts 的完整转移，按阶段检索，存储和读取有界。重置一个 attempt 清 BIT；进入新 episode 两者均清。
3. 检索到的 prompt 进入**已经在离线阶段受过记忆条件训练**的 action policy。离线先训练 CTE、再训练 memory-conditioned flow policy；部署才冻结所有网络，仅更新上下文。把 PIM 接到一张从未见过记忆输入的现成 RLT actor 后面，不可能凭接口自动获益。
4. 论文跨任务 effect 实验是**将相似记录人为替换进策略**、比较成功率；这不是已经实现跨任务持久经验库的证明。

### 论文与开放代码需要对齐的细节

| 项目 | 论文陈述 | 发布代码/复现合同 | 对我们的含义 |
|---|---|---|---|
| CTE | `L_effect + L_task + L_phase` 为主；预示用前后状态差监督 | `cosmos_framework/model/zeva/cte_losses.py` 中 effect 对比学习、action summary、pre/post 对齐与防塌缩项参与优化；`effect_visual` MSE **只记录诊断**，原因是零变化基线会使回归塌缩 | 实施 motion Huber 时必须记录非零后果子集和 no-change 分层，不能只看平均 loss |
| 表示规模 | 论文定义功能性 phase/effect，不应推为普适 token 维度 | `causal_transition_encoder.py` 默认 phase/effect 各 128，hidden 256、4 步 transition、4 个 transition 的 effect 窗口（合 16 controls）；具体是该实现配置 | RLT 可从低维可观测响应先起步，维度只是工程选项 |
| 记忆 | BIT 一次尝试，PIM 同 episode 跨尝试 | `persistent_interaction_memory.py` 默认 capacity 64、top-k 4；以 phase 检索，以 phase/effect 合并 | 先不合并，保留每条真实执行 provenance；消融后再压缩 |
| 公布基准 | 主文 RoboCasa365-Atomic5 76.8% | `docs/reproduce.md` 给发布 checkpoint 固定 5×50、无重试、执行 chunk 32，195/250=78.0%；README 说明发布权重采用成功轨迹训练且这一基准**没有跨尝试自进化** | 两个数字来自不同评测条件，不能将 78% 作为跨尝试 PIM 的证据 |
| 跨尝试 | 论文另报告累计改善/消融 | `attempt_protocol.py` 重试方案预测 32、执行 16、同 seed/session 跨 attempt，最多 300 controls；与无重试基准不同 | 同预算比较 retry 数和实际 env steps；不要混用协议 |

公开仓库代码当前审阅点对应 checkout `17ca9fa`；重新下载的版本应重新核查。论文描述与发布 checkpoint 的训练/评测合同存在范围差异，不能假定完整主文结果可由这一份发布权重原样复现。

## 在 RLT 上先做什么：P0 到 P3

**P0：恢复可信起点。** 按 [已有恢复门槛](migration-recovery-2026-09-22.md)确保 Stage1/Stage2、执行 chunk、专家干预日志、计时对齐可复查。历史 Hammer 运行缺完整专家纠错证据；此前日志不能充当干预减少的基线。

**P1：不训练的回执与记忆原型。** RLinf rollout 记录 `session_id,task_id,seed,controller_version,attempt_id,t_decision,obs_t,z_RLT,phase_t,a_ref,a_proposed,a_executed_prefix,t_observed,Δq,Δobject,contact_event,valid_mask,source,expert_request,expert_executed`；只有实际执行后可写 `Δ`。执行前 query 只读当前 phase 与过去已完成记录；从模拟器真值构造后验标签时要明确标记 privileged，只用于训练或评测，不进 actor 在线观测。原型在 [`prototypes/zeva_rlt_memory`](prototypes/zeva_rlt_memory/README.md)。

**P2：等容量低成本表示与记忆读出。** 先沿既有 loss-first 获得部署可用 `z=f(z_RLT,h_t)`，`D(z,a_exec,Δt)` 预测实测 motion/contact（仅有效标签）；新方法加入 `m_t = Read(BIT_t, PIM_t, phase_t)`，小 actor/critic 的训练输入由 `z_t` 改为 `[z_t, m_t]`，容量对齐的对照也加同参数读出。实际训练须让 learner 在训练 rollout/replay 中看到相同记忆构造规则；推理阶段不能新增它从未学过的通道。建议最初 **detach VLA/RLT token**、只训练 `f/D` 和小 learner；critic 可用 memory-conditioned Q，但尚不能据此说 actor 的探索已减少随机性。

**P3：有了校准再比较两种使用方式。** A: 记忆只进入 actor/critic 特征，测在线样本效率；B: 已校准 `D` 给原 RLT actor 附近少数候选动作打风险/进展分，只在可信分布内排序，超界回退原安全控制。B 改变动作选择，必须另设相同 M 次候选、相同计算和执行时间预算；第一轮不把 A/B 混在一个表中。

## 最小矩阵与停止条件

| 组别 | 仅变化 | 用来排除 |
|---|---|---|
| B0 | 原始可信 RLT | 基座与训练退化 |
| H | 等历史长度、等维数、同读出 MLP；无实测后果 | 历史/参数更多 |
| L | P2 的实测后果 loss，无记忆 | loss-first 已解释收益 |
| M | L + 正确 BIT/PIM，learner 训练时也读记忆 | 记忆增益 |
| M-shuffle | M，但同预算打乱同阶段内 action→outcome 配对 | 记忆真实物理对应关系是否必要 |
| M-phase | 只以阶段/当前状态检索，不带 action-effect | 阶段语义已解释收益 |

**先挑一项可复位的 contact-rich RLT 任务，两个训练任务与第三个留出任务属于后续门槛。** 优先画在同样 `env steps / accepted control steps / expert control seconds` 上的 success、首次成功交互数及达到预注册成功率的交互数；另列壁钟时间、失败/接触类别、每个 episode 的 attempt 次数、数据有效率。任务/随机种子/专家门控和干预规则全部配对，不允许为了某组提高重试上限。先用少量 rollout 验证时间与标签，再按预先固定预算做多 seed 比较；pilot 数字不应写成显著结果。

**立即停止的情况：** `a_proposed` 被误当 `a_executed`、写记忆时未来观测泄漏、跨 episode 混存、控制版本发生变化但读旧记忆、B0 比 frozen reference 退化而无法解释，或者 L/H 已解释 M 全部改进。若 M 仅在同一任务 retry 有收益，结论应限定为 episode 内适应；要声称跨任务迁移，另做显式可验证的跨任务检索库并预注册负迁移对照。

## 当前代码状态与接入位置

[`memory.py`](prototypes/zeva_rlt_memory/memory.py) 只实现 episode/attempt 生命周期、**完成后写入**、phase 检索、容量限制和数据来源字段；[`test_memory.py`](prototypes/zeva_rlt_memory/test_memory.py) 检查未来泄漏、attempt 复位、episode 隔离和检索。它没有神经 CTE、没有梯度/critic、没有 RLinf 运行，也不声称能复现 Zeva。RLinf 接线应在执行器回执处调用 `write_completed`，在 `actor.act` 前调用 `read`；这两个时间点必须通过 rollout 轨迹审计，不能凭接口名假定正确。

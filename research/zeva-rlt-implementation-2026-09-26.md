# Zeva–RLT：交互经验学习、双时间尺度记忆与迁移

> 2026-10-03 执行顺序补充：先按[仿真 baseline 核查](literature/rlt-simulation-baselines-2026-10-03.md)验收两阶段训练与评估，再实施下述 Stage 1b 和双时间尺度记忆方案。研究目标与对照保留；[当日日报与论文初稿](progress-2026-10-03.md)汇总最新进度。本轮未新增训练结果。

> **2026-10-03 研究方向更新**：保留 Zeva 的交互提取和长短期记忆；Stage 1 学会压缩执行经验，Stage 2 用经验条件加快小网络 RL，并检验迁移。固定响应公式保留为基线和辅助监督，不能成为方法终点。以下新增部分是用户确认的研究目标及待实施方案，不是新增实验成绩。旧版原型和实验边界在后半页保留；最新已记录开发证据见首页。

## 10-03：当前研究问题与贡献边界

**能否把成功、失败和人工纠正产生的动作—后果记录，编码为可检索、可更新的经验，使冻结 VLA 的小 actor/critic 减少接触操作中的重新试错，并在新条件与相关任务中复用？**

Stage 1 学习的是如何理解交互；记忆保存当前环境已发生的证据；Stage 2 学习如何利用证据完成任务。普通 RL 已经用失败 transition 更新参数，我们要额外检验：同一个失败能否在梯度更新之外，及时成为下一次决策可读取的证据。

| 机制 | 保存什么 | 影响控制的路径 |
|---|---|---|
| Replay | 训练用 transition | 梯度更新参数 |
| 短期记忆 | 有顺序的近期动作及后果 | 识别接触阶段、执行迟滞和局部响应 |
| 长期记忆 | 带适用条件、来源、版本的交互证据 | 后续尝试中检索与复用 |
| 学到的 encoder | 从交互提取有效信息的规则 | 将新记录变成可用于控制的条件 |

经典近邻：[RMA](../notes/rma.md) 已有历史→适应 latent；[PEARL](../notes/pearl.md) 已有概率 context→actor/critic。最新近邻 [eRLT](../notes/erlt.md) 已有动作相关表征和 critic 路由更新。因此贡献不是新增一个 token，而是**后果监督、可持续读取的经验、低成本 RL 是否共同改善控制与迁移**。[RLT 后续工作图谱](literature/rlt-followups.md)持续记录这些边界。

## 10-03：第一版接口与严格时间边界

保留当前 `z_RLT` 与 VLA reference，新增互补经验条件 `c_t`。第一版只条件化小 actor/critic，之后再单独测试改变 action expert 是否值得成本。

```text
执行前：c_t = Reader(z_t, q_t, ShortMemory_t, LongMemory_t)
控制：  a_t = Actor(z_t, q_t, reference_t, c_t)
执行后：e_(t+1) = E_int(z_t, q_t, a_exec_t, z_(t+1), q_(t+1), dt, mask)
写入：  e_(t+1) 只供 t+1 及以后的决策读取
```

`a_exec_t` 是实际执行前缀；被取消的 chunk 后缀、没有执行的候选、插值前 command 与实际控制命令必须区分。记录 chunk 内逐步时间、控制来源与 mask，不把多种控制来源混成一条无标记样本。

经验记录至少含：`episode_id, attempt_id, physical_instance_id, task_id, timestamps, z_pre/post, q_pre/post, a_reference, a_command, a_executed, duration, valid_mask, control_source, outcome_source, termination_reason, controller_version, encoder_version`。可观测的相对几何/视觉特征与不可部署的仿真真值分字段存储。reward 与接触事件分开：失败不等于碰撞，正常接触不统一记负面标签。

## 10-03：Stage 1b 学会压缩并使用经验

工程上先在既有 Stage 1 后增加轻量 Stage 1b：验证现有 step 2000 checkpoint 的版本与特征合同后，缓存冻结 VLA 特征，训练 `E_int + ShortEncoder + Reader + D`。原始 RLT 的训练配置可包含 VLA 动作损失，不能把既有 Stage 1 描述成始终冻结；本提案明确冻结的是这次新增 Stage 1b 的 backbone。

核心目标是**已有记忆条件下，对下一次交互后果的预测**：

```text
c_t = Reader(current_state, completed_history_before_t)
predicted_delta = D(z_t, q_t, c_t, a_exec_t, dt)
L_effect = masked_Huber(predicted_delta, measured_delta)
```

当前实际动作是离线预测器的条件，当前真实后果是标签；两者都不能提前写进 `c_t`。仅把本次后果编码再重建本次后果，可以作压缩辅助任务，不能独立证明能帮助下一次决策。

可执行初版：逐 transition 的两层 MLP→128 维经验（工程起点，不是物理定义）；短序列用小型因果 Transformer/GRU；长期保存带 key 的记录，先 top-k 检索与单层 attention 读取，不急于复杂合并；输出128维条件与原 token 并列输入 actor/critic。历史长度、k、容量由固定开发集选取，所有对照匹配参数、上下文和候选预算。

标签优先级：实测关节变化→可取得的末端/物体相对运动→冻结视觉特征变化→可靠接触事件。仿真接触/冲量可作为训练标签；真机只有跟踪误差时称“响应异常”，不伪造力觉。Huber 的小误差为二次项、大误差为线性项，阈值依各目标归一化设定；缺失标签使用掩码并先排除 NaN。事件标签另用分类损失，不拿连续 Huber 强行统一。

执行有效的成功、失败、纠正记录都可参与后果学习。BC 只使用有依据的有效示范/纠正，不把失败轨迹整体当专家目标。轨迹、物理实例和目标条件整体分割，避免相邻帧或同实例历史泄漏到测试。

## 10-03：Stage 2 先固定编码，再分别测参数学习与记忆适应

第一版冻结经验 encoder/reader，更新小 actor/critic；记忆内容按真实回执更新。需要时保留原始证据，以后更换 encoder 时重编码；不能让不同版本的 latent 静默混读。

**额外工程门槛：off-policy replay 的 context 必须匹配采集时刻。** 存储执行前 `c_t` 与其版本，或存储足够的历史快照以因果重建；TD 的下一状态条件使用该转移完成后当时可用的记忆。不能用训练时已经塞满未来经验的当前大库，去重新给旧 transition 查询 context。target 中的 next-memory 更新和终止语义也要明确。

先分两类评估：

| 协议 | 哪些可变 | 用来回答 |
|---|---|---|
| 参数冻结的记忆适应 | encoder/actor/critic 冻结；记忆按时间写入 | 同一物理实例跨尝试的即时经验是否有效 |
| 记忆条件化在线 RL | 固定 encoder；actor/critic 按同预算更新 | 经验是否减少重新学习所需的交互 |

完整方法不止固定公式，但开发按增量验收：零 context→同容量原始历史→固定响应统计→后果预训练的短期条件→短期＋跨尝试长期经验。加入动作预测监督（eRLT 启发）与仅 critic 训练 context（PEARL 启发）对照，判断新监督是否有独立价值。再做打乱 action–effect 配对、无 phase、长期库清空/随机/错误条件检索，避免把任务 ID 或更多输入当成物理收益。

## 10-03：持久化、迁移与成本核算

原 Zeva 的 PIM 在同 episode 的多次 attempt 之间保留；默认跨 episode 清空。我们的第一版沿用该范围。若要跨 episode/跨任务复用，显式声明是项目扩展，新增 scoped store，至少隔离机器人、本体坐标系、控制器版本、物理实例和许可数据来源；不直接改旧原型的清空合同。

长期记录保存“情境＋动作＋后果＋有效性”，而非上次成功的固定关节角。先同实例多次尝试，再同任务新动力学条件，最后相关源任务→目标留出任务。目标评估比较空库、相关源库、不匹配源库；源库在评估前冻结。允许的目标内适应记忆另存一份并重置，禁止不同测试 seed 互相传经验。检索坐标、单位、控制频率不匹配时先拒读，不假设跨本体通用。

报告达到预注册成功率所需的 **环境交互数、墙钟时间、人工纠正分钟数**，并报独立固定初态成功率、记忆查询/写入 p50/p95 时延、控制超时率、旧任务保持及负迁移。目标成功率未达到时按预算截尾记录，不能只统计成功方法。预测误差下降但控制无收益也必须保留。

成本分成：离线数据采集、Stage 1b GPU 时间、在线采集/更新、记忆读写、复位和人工协助。可分别按秒、GPU小时、人工分钟计算 `每目标摊销成本(N)=共享前置成本/N+平均目标适应成本`；不同单位不直接相加。只有在 N 个独立目标上实际复用后，才报告摊销优势。记忆可能降低每秒吞吐但减少总交互，也可能完全无净收益。

开发顺序：①时序数据与回放审计；②Stage 1b 后果预训练；③短期条件接入 learner；④同实例跨尝试长期记忆；⑤冻结适应与迁移评测；⑥再单独研究 action expert 条件化、在线 encoder 更新和过期经验处理。两卡分工先用于采集/固定评估与轻量训练，之后跑匹配在线对照；这是计划，不是当前GPU占用声明。

用户给出的 `openpi/pi0.py:776/790`、`modules/rlt_token_transformer.py:355` 是其本地分支定位，本会话未访问对应训练机器，行号不能视为本次代码审计结果。动手前绑定 commit，确认 detach、噪声动作输入和部署特征一致性；不能把 SFT 时含真实示范的 action-expert hidden state 直接当在线可用条件。

---

## 09-26 历史方案与已审阅原型

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

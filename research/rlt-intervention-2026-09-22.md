# RLT 的关键阶段、仿真专家干预与 Hammer 时间语义

> 2026-09-22 讨论与代码核查；没有新增训练结果。本文区分原论文、RLinf 官方示例、迁移快照和拟议实现。<br>
> 配套：[小算力恢复入口](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/migration-recovery-2026-09-22.md) · [物理经验与干预研究合同](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/physical-experience-protocol-2026-09-22.md)

## 1. 先回答：之前 Stage2 下降时，启动人工接管了吗？

**保存的 Hammer 运行没有启用实际专家纠错。** 退化的 Stage2 使用旧 clean50/12k reference，周期评测约从45%降到15%，不能归到新 train450/10k 模型上。保存的 resolved config 为 `expert_model: null`；末次日志摘要的 `intervention_requested_rate`、`intervention_rate`、`human_mask_ratio` 均为0。结合环境实现，可以判断这条运行没有建立可工作的 Hammer 干预闭环；单独看到“0”本身并不能证明策略不需要帮助。

已存在的是 reference→actor 的阶段切换，以及可以复用的通用 route/replay/BC 基础。Hammer 尚缺失败/停滞检测、从当前状态恢复的专家，以及按回合的干预事件和控制时长统计。**不能把“actor 接管”记成人类/专家纠正。** 证据来源见[脱敏迁移核查](https://github.com/nkd-lkz/physical-self-evolution/blob/main/data/recovery-audit-2026-09-22.json)。

## 2. 三个不同的决策

| 决策 | 控制流 / 作用 | 要回答的问题 |
|---|---|---|
| 关键阶段切换 | base VLA → RL actor | 哪段任务值得交给 RL 优化？ |
| 纠错干预 | 当前策略 → human / expert | 当前执行是否需要外部帮助，帮助是否有效？ |
| 成功、失败、终止与奖励 | episode / transition 的结果 | 本次尝试完成了吗，是否还能继续？ |

精密接触阶段可以尚未出错；失败也可能在关键阶段之前发生。这三者需要独立记录和比较。

原论文在训练中由操作员选择把 base VLA 控制交给 RL 的时刻，聚焦高精度困难段；操作员还可通过遥操作覆盖 actor。论文提出用切换标签进行短暂微调，让 VLA 在测试时预测交接时机。关键阶段评测从部分完成的任务状态开始，全任务评测则包括前面的 VLA 执行。因此它不是一套无监督发现所有任务关键时刻的通用触发器。[RLT 原论文，§V 与 §VI](https://arxiv.org/html/2604.23073v2)

## 3. RLinf 如何在 ManiSkill 中模拟干预？

### 3.1 任务状态机决定“何时”

官方 joint-control 示例使用侧向插销任务 `PegInsertionSideWideClearance-v1`。自动阶段门控检查抓持、接近孔口和未成功等条件，产生 `rlt_switch_flags`。达到更靠近插入区域的监测窗口后，再检查停滞，产生 `intervene_flag`。这属于利用任务几何信息的仿真门控，不是人工实时操纵，也不是已学成的跨任务风险预测器。

停滞示例检查以下任一改善：沿孔轴的推进、横向对齐误差下降、`x - weight × yz_distance` 综合分数提升。当前默认阈值分别是0.003、0.0015、0.002，连续3个无足够改善的 chunk 后请求专家。实现还包括初次初始化、有效区域和抓持条件；进展相对保存的 best-progress 统计判断，不应简化成任意相邻帧差分。`stalled_progress` 路线触发后保持接管，直到成功、离开有效阶段或回合重置等条件清除状态，并非纠正一个动作就必然归还 actor。[固定版本环境代码](https://github.com/RLinf/RLinf/blob/b023deb7e90ceadfe18e0a528e862e3c630f7e0a/rlinf/envs/sim/maniskill/maniskill_rlt_env.py#L345)

### 3.2 额外的 SFT 模型决定“做什么”

`rollout.expert_model` 是额外加载的 OpenPI SFT policy，通过 `predict_action_batch` 生成纠正动作；`use_rlt: False`。它不是 TOPP，也不是另一个小型 RL actor。环境提出请求后，route 还要检查 warmup readiness、训练模式与模型可用性，才替换整个 action chunk。[专家预测代码](https://github.com/RLinf/RLinf/blob/b023deb7e90ceadfe18e0a528e862e3c630f7e0a/rlinf/algorithms/rlt/expert.py)、[route](https://github.com/RLinf/RLinf/blob/b023deb7e90ceadfe18e0a528e862e3c630f7e0a/rlinf/algorithms/rlt/route.py#L148)

官方文档称此功能默认关闭，但此次核查的 AC 示例 YAML 中 train 为 `True`、eval 为 `False`，expert 路径仍是待填写的占位符。**以固定 commit 的最终 resolved config、模型加载和实际执行日志为准。** 打开 YAML 开关不等于已经拥有可用专家。[官方说明](https://rlinf.readthedocs.io/zh-cn/latest/rst_source/examples/embodied/rlt.html)、[核查版本的 AC 配置](https://github.com/RLinf/RLinf/blob/b023deb7e90ceadfe18e0a528e862e3c630f7e0a/examples/embodiment/config/maniskill_rlt_stage2_ac_mlp.yaml)

### 3.3 专家动作如何参与学习？

route 保存实际发送给环境的动作，标记干预，把相应 `ref_chunk` 内容替换为专家动作，并将该 chunk 的 `actor_switch` 置为 false。普通样本的 BC 目标是 VLA reference；干预样本改用纠正动作，critic 则学习实际动作造成的 transition。名为 human 的 mask 在仿真里也可能代表模型专家，不能把它直接解释为真实人类工时。[route 源码](https://github.com/RLinf/RLinf/blob/b023deb7e90ceadfe18e0a528e862e3c630f7e0a/rlinf/algorithms/rlt/route.py#L178)

对于本项目的后果研究，应额外保留原始 reference、actor proposed action、expert action 和实际执行前缀，不能只有被覆盖后的 BC target。否则无法区分“学生本来会怎么做”与“专家实际做了什么”。

官方 route 明确要求 `mode == "train"` 才执行 expert；默认 eval 测 base+actor 的无专家能力。将 `env.eval.expert_takeover.enable` 改为 true 并不足以做辅助评测。需单独实现不更新参数、不污染训练 replay 的 assisted-eval 入口，不能直接拿训练模式冒充评测。[route 条件](https://github.com/RLinf/RLinf/blob/b023deb7e90ceadfe18e0a528e862e3c630f7e0a/rlinf/algorithms/rlt/route.py#L184)

## 4. “强 SFT 专家”的数据从哪里来，要重新训练吗？

若已有与任务、机器人、动作变换和 norm 匹配的可用 SFT checkpoint，可以直接加载；如果没有，就需要额外训练或换用其他专家。示例路径的 `more_steps` 只是命名，不能作为更强、更会恢复的证据。

官方提供400条成功示范的数据入口；采集流程用 ManiSkill motion-planning solver 生成轨迹，将位置控制动作转换为增量位置动作，回放成功后才保存。它不是“覆盖 actor 各类失败状态的恢复数据集”。[官方数据与采集说明](https://rlinf.readthedocs.io/zh-cn/latest/rst_source/examples/embodied/rlt.html)

因此应把两个能力分别验收：

- 从任务初态完成任务的成功率。
- 从学生实际遇到的失败/偏离状态出发，在指定剩余预算内恢复的成功率。

只做更多成功轨迹 SFT 不保证第二项。必要时需要补充失败状态纠正示范、经验证的脚本恢复，或由规划器产生的恢复数据。记录其生成、筛选和训练成本。

## 5. 既然专家更强，为何还要 RL？

专家可以提供纠错、学习信号与探索边界；RL 的研究价值可能是减少依赖、优化完成速度或适应新的动力学条件。这些都是需要比较的收益，不是因为名称叫 RL 就自动成立。

若专家本身便宜、可靠、速度足够且能覆盖部署条件，直接使用专家就是必须保留的强基线。应至少比较 frozen reference、expert-only、同纠正数据的 BC/DAgger 类方法和 RLT+同一专家。仿真脚本常使用部署时不可得的物体真值，因此还要分别报告 privileged oracle 与可部署策略的输入权限。冻结大模型只省去其梯度更新，不会自动消除 VLA 前向推理成本。

## 6. Hammer 的 H50/C50、100步与200步

以下是**迁移前旧 clean50/12k Stage2 实际运行配置**，不是所有 RLT/RoboTwin 任务的默认值。

| 名称 | 本运行数值 | 定义 |
|---|---:|---|
| Reference horizon H | 50 | VLA 一次预测的目标动作序列长度 |
| Execution chunk C | 50 | 一次送入 native macro 执行的目标点数；actor 对应50×14维动作 |
| `actor_start_step` | 100 | 已累计发出的名义目标点数达到100后，允许后续 chunk 使用 actor |
| `max_episode_steps` | 200 | RLinf 外层回合名义步预算 |
| `task_config.step_lim` | 200 | 本次显式覆盖的 RoboTwin 原生任务限制 |
| `max_steps_per_rollout_epoch` | 200 | 每轮 rollout 采样/flush 预算；语义与回合上限不同，数值恰好相同 |
| `warmup_post_collect_updates` | 2000 | 本运行 actor 上线前的 learner warmup 更新门槛；不是2000个环境步 |

`RoboTwinEnv.step()` 在 native macro 返回后执行 `_elapsed_steps += actions.shape[1]`，再检查切换和截断。因此当 C=50、回合未提前结束且 warmup 已通过时：

| 第几次 chunk | 进入时累计名义步 | 控制者 | 返回后累计名义步 |
|---|---:|---|---:|
| 1 | 0 | reference | 50 |
| 2 | 50 | reference | 100 |
| 3 | 100 | actor | 150 |
| 4 | 150 | actor | 200，预算耗尽 |

`latch_until_done` 使进入后的阶段保持到回合结束。warmup 尚未通过时，达到100也继续走 reference。这里的“100步接管”是**从第3个 chunk 开始允许 actor 控制**，不是先让 actor 执行100步，更不是训练到100次梯度更新才纠错。

### 6.1 不等于200次物理仿真或200次闭环观测

native TOPP 会把50个目标点进行时间参数化与内部控制执行。当前调用只向外返回 chunk 结束后的观测，没有向策略提供50个中间时刻的真实反馈。外层名义计数按发出的整 chunk 增加，即使内部成功早停，也可能计入完整50。因此需要分别记录：

1. 名义 waypoint / action 步数。
2. 策略 chunk 调用数与观测边界。
3. 实际 physics ticks、执行前缀与模拟秒数。
4. 推理、规划、执行、重置组成的墙钟时间。

旧12k物理诊断的20回合各观察到4次策略 chunk；非提前结束的 macro 曾观察到500 physics ticks、约2模拟秒。这是特定执行路径的实测，**不能把“50步=2秒”推广成通用换算**。新10k截图的平均长度196.25也不等于196.25秒或196.25次纠正机会。

### 6.2 为什么选100和200，而不是其他数字？

200沿用本地评测/预算协议；native Hammer 的任务配置原有400限制，本运行由 reset 适配层覆盖成200。100是保守地让 reference 先做前两个 macro 的工程切分；它不检测是否已经抓住、是否靠近敲击目标，也没有证据表明100是最优关键阶段。这里的理由是保持既有实验协议可比较，不是物理定律或论文规定。

可以把切换点100、50、全任务 actor，以及预算200/400作为**后续单独消融**；每次需重测同协议 reference，并报告实际阶段和执行时长。改变 C 会改变 TOPP 分段、状态分布和再观测频率，不能当作只改一个计数器的无害操作。

在当前200/C50/从100开始的设置下，actor 通常只剩两个 chunk。若照搬 ManiSkill“连续3个无进展 chunk 才接管”，很可能回合已结束还没有纠正机会，初始化还可能增加等待。Hammer 应先审计检测→请求→执行的延迟与剩余预算，再决定阈值和监测频率。

### 6.3 本地可复核代码位置

公开仓库保存脱敏结论与摘要哈希，不发布内部机器目录。以下为迁移源码树内的相对定位：

| 源码/配置 | 核查点 |
|---|---|
| `rlinf/envs/robotwin/robotwin_env.py` | `_update_rlt_switch()`、`step()` 的名义计数与截断 |
| `robotwin/envs/vector_env.py` | `SubEnv.reset()` 在 task setup 后覆盖 `step_lim` |
| `envs/_base_task.py`、`envs/beat_block_hammer.py` | TOPP 执行、原生任务与 `play_once()` |
| 旧 clean50/12k Stage2 的 `tensorboard/config.yaml` | H/C50、start100、三处200、warmup2000、expert=null |
| 同一运行的 `wandb-summary.json` | 实际请求、干预和 human mask 指标均为0 |

## 7. 可以用 RoboTwin + TOPP 实现纠错吗？

**可以把它作为低算力专家的组成部分，但 TOPP 本身不决定如何纠错。** TOPP 负责在已有路径上按速度/加速度等约束安排执行时间。拟议专家仍需：

```text
当前观测/状态 + 任务目标
          ↓
失败/阶段识别 → 选择恢复子目标
          ↓
IK / 路径规划 → TOPP 时间参数化
          ↓
从当前状态执行 → 检查恢复/失败 → 归还控制或终止
```

Hammer `play_once()` 组织抓取、抬起和朝目标放置/敲击的示范流程，不能仅因它从初态成功，就在任意失败时重新调用整套脚本。旧示范动作也不能不做状态对齐直接拼接。

第一版建议只验证一种恢复：**锤子仍被稳定持有、末端/敲击点偏离但尚有剩余预算**。从该真实状态重规划对齐和敲击；掉锤重抓作为后续独立恢复类型。若当前模拟器无法安全恢复完整分支状态，就先使用真实继续执行的接管案例，不伪造反事实成功率。

验收要求是从学生诱发的偏离状态恢复、无隐藏 reset、动作规范化只转换一次、实际动作与时长可追踪、terminal/next observation 正确，并能区分专家失败和学生失败。第二份 SFT 大模型可省去，但脚本专家的开发、规划与数据生成成本仍需计入。

## 8. 每个任务都要手写规则吗，有没有通用一些的？

| 方案 | 可复用部分 | 仍需要的任务信息 / 验证 |
|---|---|---|
| 几何阶段与进展规则 | 状态机、计时器、路由和日志 | 抓取/插入/敲击目标与阈值；作为透明基线 |
| 从交接标签学 phase classifier | 分类器结构与训练流程 | 哪些阶段交给 RL 的示例与跨任务校准 |
| 学失败风险 / 后果预测 | action-conditioned history encoder | 任务结果定义、有效标签、预测校准 |
| 不确定性 / novelty gate | 统一表示与预算管理 | 不熟悉不等于危险，低置信度不等于专家能救 |
| 预期专家收益减去成本 | 决策接口 | 学生与专家在同状态的条件能力、剩余时间和成本 |

统一框架可以减少逐任务手写规则，但不能消除任务目标、专家可恢复范围与传感器语义。先用 Hammer 规则建立可核验基线，再测试 learned gate 在未见物理条件和第二个任务中的迁移。

减少干预本身已有明确近邻：[ThriftyDAgger](https://arxiv.org/abs/2109.08273)研究预算下的 novelty/risk 门控，[LazyDAgger](https://arxiv.org/abs/2104.00053)研究切换负担。因此本项目若要形成研究增量，应证明**执行后果监督带来的物理表征在同等输入和预算下有额外决策价值**；不能只以“用网络替代手写规则”作为创新。

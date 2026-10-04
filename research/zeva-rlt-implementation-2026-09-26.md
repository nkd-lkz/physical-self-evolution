# 当前方案：让 RLT 读取已完成的交互经验

这份说明回答三个问题：我们改什么，已经测到什么，下一步测什么。**更新于 2026-10-04。当前还没有证据证明记忆提高了控制成功率。** 文件名保留原日期，旧链接继续可用。

[交互式讲解与结果](../index.html#understand) · [实验总日志](experiment-log.md) · [今日核查](progress-2026-10-04.md) · [固定论文 v2](papers/interaction-memory-2026-10-03/index.html)

<a id="reading-order"></a>
## 先用三句话讲清楚

冻结的 VLA 根据当前观测生成 reference 动作。我们让小 actor／critic 同时读取过去命令及其真实响应。我们要检验：这些额外信息能否减少重复试错，并减少达到相同成功率所需的纠错。

这是研究目标。昨晚只测试了现有的固定响应统计，没有测试经验预训练或纠错节省。

| 问题 | 唯一维护入口 |
|---|---|
| 现在研究什么？ | 本页：当前方法和执行顺序。 |
| 实际测到了什么？ | [实验总日志](experiment-log.md)：结果、数据和局限。 |
| 论文写成什么样？ | [论文 v2](papers/interaction-memory-2026-10-03/index.html)：10-03 的固定版本。 |
| 别人做过什么？ | [后续工作](literature/rlt-followups.md)、[开源 baseline 核查](literature/rlt-simulation-baselines-2026-10-03.md)：作者结果不算本地复现。 |

<a id="problem"></a>
## 为什么需要交互经验

图像不能保证说明当前执行条件。同一个命令可能产生不同的关节位移。过去的命令和响应，可能补充这个信息。

但 RL 本来就在利用旧数据。新增方法必须与原有机制分开。

| 机制 | 怎样使用旧数据 | 怎样验证 |
|---|---|---|
| replay | 采样旧 transition，更新网络参数 | 这是 baseline 已有的能力。 |
| 决策记忆 | 把历史作为当前 actor／critic 的输入 | 匹配训练；冻结参数后比较有／无历史。 |
| 经验迁移 | 把源条件的经验带到目标条件 | 比较空库、相关源库、不匹配源库。 |

“物理交互经验”指实际命令和真实后果。“物理规律”在当前阶段最多指局部响应关系。我们尚未证明通用摩擦、刚度、接触定律或持续自主能力增长。

<a id="implementation"></a>
## 一次动作怎样变成下一次可用的经验

先读取过去，再执行动作。当前动作的后果只能在执行完成后写入。

| 顺序 | 系统做什么 | 信息来自哪里 |
|---|---|---|
| 1 | 冻结 VLA 生成当前特征和 reference | 当前图像、任务、本体观测 |
| 2 | reader 生成 64 维经验条件 `c_t` | 此前已完成的命令—响应记录 |
| 3 | 小 actor 生成动作，critic 评估动作 | 当前特征、reference、经验条件 |
| 4 | 环境 gate 选择 reference 或 actor | 当前操作阶段；本轮无 expert |
| 5 | 环境执行实际命令，collector 写入后果 | 实际执行前缀和真实后继 |
| 6 | 下一次决策读取历史；训练器采样 replay | 前者改变输入，后者更新参数 |

可点击的流程图见[首页讲解](../index.html#understand)。失败记录可以用于 TD 和后果预测；失败动作不能自动成为正确的 BC 标签。padding 和无效 terminal 数据必须在非线性计算前屏蔽。reset 后首帧不能冒充上个回合的后继。

### 哪些模块已经存在

下面区分已有代码和待验证设计。两者不能混写为实验结果。

| 模块 | 已实现 | 尚未完成 |
|---|---|---|
| Stage 1 | 冻结 VLA／RL token checkpoint | 不能据此声称 token 已学到物理规律。 |
| 交互记录 | 9 维起始关节、10×8 维命令、9 维变化、10 位有效性、2 个结束标志，共 110 维 | 视觉后果、接触语义与来源版本等扩展。 |
| 历史存储 | 4 条近期记录、容量 32 的 archive、检索 4 条 | 跨条件长期记忆收益。 |
| 固定响应 reader | 七个响应斜率和七个支持度，补齐为 64 维；无可训练参数 | 明确的控制收益。 |
| attention reader | 64 维条件；critic TD 更新 reader；actor 读取 detach 的条件 | 更可靠的经验监督。本轮未训练此 reader。 |
| Stage 2 | 在线更新小 actor／critic、评估、保存 | 稳定收敛、纠错节省与迁移。 |

历史关节值来自环境原始记录。actor 的本体输入经过 VLA 数据变换。两者不能直接混用尺度。响应统计描述局部控制响应，不直接测量接触力或刚度。

### 下一版想学习什么

拟议 Stage 1B 使用真实时序轨迹，学习一个 64 维经验条件。小预测头根据当前状态、已执行动作和经验条件，预测 10 个控制 tick 后的变化。

首版用平方误差监督归一化关节变化和冻结后继视觉 latent。Stage 2 首轮冻结经验 encoder／reader，只训练小 actor／critic。之后再单独测试在线更新经验编码器。

| 约束 | 原因 |
|---|---|
| 按轨迹或实例划分数据 | 避免相邻帧泄漏。 |
| 只用实际执行前缀和真实后继 | 候选动作和 reset 画面不是真实后果。 |
| replay 保存当时的历史快照或因果索引 | 训练不能读取未来经验。 |
| 比较无动作、无历史和固定响应模型 | 排除场景或时间相关性。 |
| 最后比较相同预算下的实际成功率 | 预测更准不等于控制更好。 |

Stage 1B、action-expert 约束、跨任务记忆尚未完成。FLARE 是后果表征监督的参考；RMA、PEARL 是执行条件推断的近邻。新颖性需逐项比较，见[文献图谱](literature/rlt-followups.md)。

## 昨晚实验回答了什么

两组使用同容量头部、相同初始化规则和相同预算上限。区别是决策输入中的历史条件。代码固定为 `91f7bdfa`，两组均在 8 小时上限退出。

| 项目 | 零 context | 固定响应 |
|---|---:|---:|
| 完整记录的训练轮数 | 299 | 309 |
| actor 实际更新次数 | 6954 | 5851 |
| 最后 checkpoint | 275 | 300 |
| 共同第 250 轮评估 | 4/8 | 4/8 |
| 共同第 275 轮评估 | 3/8 | 3/8 |

**当前结论：尚未观察到固定响应的明确控制优势。** 更新和保存链路已跑通。共同保存点的成功数相同。这不能证明记忆有效，也不能证明记忆无效。

每次只有八个评估 lane，且只有一个训练 seed。相同轮数不等于相同 replay 数量或梯度更新次数。两组最后评估的轮次不同，不能直接比较 37.5% 与 50%。[完整数据](../data/zeva-matched-results-2026-10-04.json)保留全部周期结果。

<a id="next-experiments"></a>
## 保存模型的复评结果与下一步

共同第 275 轮的四组冻结评估已经完成。模型权重不变，同 seed 的初始观测指纹一致。

| 评估组 | 权重与输入 | 要回答的问题 |
|---|---|---|
| 零 context | 零 context 训练所得；条件为零 | 无历史训练后怎样？ |
| 固定响应 | 响应训练所得；读取历史 | 历史组怎样？ |
| 响应模型关闭历史 | 同一响应权重；条件为零 | 同一模型是否依赖历史？ |
| reference-only | 全程执行冻结 VLA reference | 小 actor 改善还是退化？ |

每组完成四个评估 seed，每个 16 个 lane，共 64 回合。零 context 为 16/64，固定响应为 15/64，响应模型关闭历史为 18/64，reference-only 为 19/64。[逐回合数据](../data/zeva-frozen-eval-2026-10-04.json)保留了全部结果。新 seed 不代表未见物理条件。关闭历史改变了输入分布；它不是重新训练的无记忆组，也不是跨重试的 retain／clear。

只有 26/64 回合到达 actor 接管阶段。其余 38 回合在 reference 阶段失败。响应模型的动作依赖历史，但没有带来额外成功。该结果来自一个训练 seed，不能证明记忆普遍有害。

**现在先诊断 baseline。** 在相同 gate 状态测 actor／reference 动作误差和 Q 排序，再用同数据、同初始化、同更新数比较 BC-only 与 Q+BC。之后回到在线匹配训练。今天的 64 回合作为开发数据；最终验收使用预先封存的新初态。

| 观察 | 后续动作 |
|---|---|
| 动作几乎不随历史变化 | 检查输入尺度、梯度和训练信号。 |
| 动作变化，但控制无收益 | 检查历史是否包含有用的执行条件。 |
| 小 actor 均弱于 reference | 先修复 baseline 学习流程。 |
| 控制收益可复现 | 再加入近期历史、attention、Stage 1B 和更多训练 seed。 |

### 怎样检验减少纠错

当前评估没有在线 expert，不能回答纠错节省。之后先验证固定 expert 能从 learner 的偏离状态恢复，并交还控制权。仿真不必先接 VR。

| 方法 | 无在线纠错 | 有限预算 expert 纠错 |
|---|---|---|
| 无记忆 RLT | 自主学习基线 | 纠错基线 |
| 记忆 RLT | 自主学习对照 | 检验纠错成本 |

四组共享初始 demonstrations、expert、gate、接管时长上限和预算上限。不强行匹配实际干预次数，因为它是待测结果。报告无辅助成功率、环境控制步、训练时间、接管次数和 expert 控制时长。

随后冻结参数，比较同一实例重试时保留／清空记忆。再测试条件变化和源库迁移，单列源数据成本。逐次尝试成功率是主指标；累计成功率是补充。真机与真人时间成本另行验证。

<a id="versions"></a>
## 版本与阅读规则

论文 v2 保留 10-03 的 16 页英文稿，尚未纳入昨晚结果和新评估。本说明采用 STE 的短句、统一术语和明确操作原则；中文不是 STE 标准认证文本。[写作规则与官方来源](knowledge-base-maintenance.md#clear-writing)说明具体做法。

每轮实验固定代码。开发和新 campaign 前检查官方 RLinf。10-04 main 仍为 `c70606f`，replay PR [#1623](https://github.com/RLinf/RLinf/pull/1623) 仍开放。昨晚已确认 replay 索引与保存文件不一致；新评估只加载模型权重。

AlphaBrain／LIBERO 保留为备用 baseline。本轮不并行切换框架。FLARE、Jev 保留历史记录。[决策日志](decision-log.md)说明路线变化。本页维护现行方案，日报记录事实，论文按版本发布。

### English explanation

The frozen VLA describes the current scene and generates reference actions. Past commands and measured responses can provide additional information about execution conditions. We give this information to a small actor and critic. We test whether it improves control with the same training budget. Later, we will test correction costs and transfer. The current pilot does not establish these benefits. A frozen evaluation gave 16 successes in 64 episodes without context and 15 with response memory. The reference succeeded in 19 episodes. We will first diagnose imitation error and Q-guided action changes.

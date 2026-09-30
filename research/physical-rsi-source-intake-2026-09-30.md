# 2026-09-30 新资料摄取：把 Physical RSI 落到 RLT 的可检验增量

> 项目侧研究备忘；原始论文/官方项目与媒体转述分开。**没有新增 RLT 训练结果或论文新颖性结论。** 既有基线、失败结果和计算限制以 [09-30 审计](three-branch-audit-2026-09-30.md)、[进度快照](progress-2026-09-30-maniskill-rlt.md)为准。

## 先给这批材料分层

| 材料与一手入口 | 可用于论证什么 | 不可推断什么 |
|---|---|---|
| [RPent 官方仓库](https://github.com/RLinf/RPent)、[Memory](https://rpent.readthedocs.io/en/latest/rst_source/development/memory.html)、[Flash](https://rpent.readthedocs.io/en/latest/rst_source/usage/flash.html)；[已存笔记](../notes/rpent.md) | 冻结 VLA 的任务规划、受验证记忆、执行接口与成功检查是系统级改进；Flash 的具体范围须按文档。 | LIBERO-PRO 成绩不等于在线改进 RLT actor，也不能与 RoboDojo 或 ManiSkill 成绩直比。报道列出的全部设备与仿真器不一定已经接入官方发布版本。 |
| [RoboProbe 原始论文](https://arxiv.org/abs/2609.24170)；[Astra 笔记](../notes/astra-robodojo.md) | 42 个 RoboDojo 任务、作者报告 Astra 22.48% 成功率、28.97 Score；语义/开放任务与精密、动态、双臂控制能力显著不均衡。扰动案例可观察到回合内反馈修正。 | 一次轨迹自我修正不等于跨回合经验积累；真实硬件诊断不能当正式真机可靠性结果。 |
| [Axis 官方博客](https://axisrobotics.ai/blogs/blog/beyond-more-tasks-axis-is-building-a-composable-library-of-robotic-capabilities)；[项目笔记](../notes/axis-capability-library.md) | 仿真策略 → 少量真实成功 rollouts → 联合训练；代理模型筛数据；有适用范围的 expert 能被组合。 | 标题“零真机数据”不描述后续真机回流；22%→52% 是自述且缺可复算协议；$5–10 是纯计算成本。 |
| [Simate 官方主页](https://mate-robot.cn/home/)、[Sinfra](https://mate-robot.cn/research/sinfra/) | 任务定义、实验版本、证据、仿真与部署反馈串联，是研究流程设计的参考。 | 截至核查，官网写 **Sipai RoboDojo evaluation in progress**；未核实媒体所称榜首、超过 Astra 或 AutoResearch 导致榜首。官网 Sinfra 的若干曲线/比较标成 illustrative，不是公开基准证据。 |
| [RoboICL 论文](https://arxiv.org/abs/2609.34261) 与 [代码](https://github.com/Mosi-AI/RoboICL) | 区分演示上下文和自身交互记忆，用固定锚点与最近反馈组成有界历史；论文报告 30 任务及开发任务的 Jev 门控调用节省。 | 它是冻结 LLM 的上下文方法；与 RLT 的参数学习、接触规律或 Jev 候选 actor 不是同一个机制。与 RoboProbe 单样本无总体收益也不矛盾：输入格式、任务集合、历史组织和预算不同。 |
| [HKU MMLab PhysicalRSI 1.0](https://mmlab.hk/research/PhysicalRSI)；[项目笔记](../notes/physicalrsi-mmlab.md) | 固定基模可通过生成、环境评测和继承 harness 候选改进程序技能；折衣服回撤等案例展示了持久程序与回合内重新测量。 | 排名、样本与成本须按其发布页口径；程序更新不直接证明物理规律、RLT 低层表征或 RL 收敛改善。部分随机场景显著退化，技能有效范围值得单独评估。 |
| [LITHE 原始预印本](https://arxiv.org/abs/2603.07442)、[KineFuse 原始预印本](https://arxiv.org/abs/2607.14842) | 前者提出快控制/慢规划频率隔离；后者在指尖遮挡下用本体、力矩、接触与视觉联合估计。 | IROS 产业文章对会议“共识”和具体产品性能的归纳不可作为论文结论；这些系统不直接验证目前 RLT 的视觉输入能感知摩擦力。 |

用户附带的三篇整理文本分别偏向数字 Agent 的 RSI 分类、Chelsea Finn 演讲的二次整理和一场 Astra 圆桌的转述。[Chelsea Finn 已有项目笔记](chelsea-finn-physical-rsi-talk-2026-09-25.md)单独记录可追溯的 PI 官方来源。另附截图提出“通用 recipe 还没有，关键是自动数据回流”的采访观点；它提醒我们记录新经验怎样进入下一轮训练，但不是一个已验证的算法。材料提供提问框架：**更新对象、更新时机、反馈从何而来、谁验证改进**；圆桌中的个别百分比、真实物理参数估计案例及行业观点没有逐一找到原始轨迹和评测协议，不录入本项目事实库。没有复制长篇原文。

## 对自己的问题重新定义

**物理属性**是质量、摩擦、柔顺、接触刚度等潜在因素；**物理规律**是关于系统怎样演化的约束；**交互经验**是本体/视觉观测和实际执行动作之间可追溯的状态变化及成功/失败。当前 RLT 若没有力/触觉或可辨识性实验，单靠视觉和关节位移不能给 latent 命名为“摩擦系数”。优先学**条件动作后果/响应及其不确定性**，再验证物性变化下的保持与迁移。[现有研究合同](physical-experience-protocol-2026-09-22.md)已限制模拟器真值仅作训练标签/评测，不在部署输入泄漏。

“自进化”也要说明哪里在更新：一次执行中的上下文/短历史、任务间的有证据记忆、RLT 小 actor/critic 参数、或开发者的实验配置。它们可以并存，但论文主要 claim 不宜同时压在四处。本文暂选**执行后果监督改善紧凑 actor 表征，从而让固定预算在线 RL 更快、更稳**；经验证的接触记忆为第二阶段，研究 harness 自动化只是实验管理，均独立消融。

## 三个小实验，各自有可否证结果

| 顺序与目标 | 最小实现与对照 | 判据与停止条件 |
|---|---|---|
| **E0：实测后果对 latent 是否有用？** | 基于可部署历史 + 实际执行的 action prefix + Δt，预测有效的 measured Δq、目标相对位移和接触/滑移事件；Huber 与带 validity mask 的事件损失。对照静止/状态历史、RLT prefix、同容量 head-only、head+后果。按 episode/物理条件切分；VLA 冻结。 | 留出条件的后果误差、事件校准改善才进入在线阶段；若简单 state/history 或 head-only 一样好，收缩“物理 token”主张。低训练 loss 不算任务能力。 |
| **E1：经验筛选或检索能否帮助下一次？** | 使用同一批**已经结束**的 episodes 建轻量 transition 库（条件、执行前缀、实测结果、有效性、版本）；对照无库、等容量最近短历史、随机/错误检索、同样条数的成功优先和接触覆盖筛选。训练流写入，评测只读。复杂检索网络须对比 Zeva 固定响应公式。 | 独立 episode 的成功率/校准/样本效率/延迟；如果只在相同 seed/布局受益，或简单公式更好，不叫跨任务记忆。之前 Zeva reader 的负结果仍保留；同日追加支持度门控改善开发集预测误差，尚无新的闭环控制收益，见[续作记录](three-branch-audit-2026-09-30.md#下午续作预先固定实验矩阵与人工介入入口)。 |
| **E2：固定干预预算下更快学会？** | 先验收 baseline Stage 2 与固定专家/路由；相同 VLA、奖励、chunk 时序、探索/训练步数、专家规则。B0 原 RLT、匹配容量 head-only、后果 grounding，物理约束最后单独加。Jev 有限候选与同幅度连续 residual 另开对照，绝不同时改 gate。 | 无专家成功率–交互数曲线、达到预定阈值步数、专家实际控制秒数与次数、wall-clock、旧任务遗忘；若仅 loss 改善、只靠更多专家时间或没有可信 baseline，停止成果宣称。 |

*标签/信息边界：* `y` 只能在 `a_exec` 真正执行之后采集；未执行的候选不可用另一个动作的后果标注。仿真接触标志要做有效性掩码，时长按实际前缀；真实场景没有力传感器时只写“视觉/运动后果”，不写“已测接触力”。未来加注意力图，可以先可视化关联失误，不直接把注意力热图视作因果解释或将离线目标框泄漏到测试输入。

## 下次组会可做的决定

1. 先锁定 `PegInsertionSide` 的基线与实际训练/评测种子、动作时间戳及专家计费。当前 Stage 1 固定 20 回合为 8/20；Stage 2 尚无最终结论，FLARE 100-step smoke 双方都失败；见 [真实审计](three-branch-audit-2026-09-30.md)。
2. 本轮只选择 **E0 后果监督** 与 **E1 简单响应检索** 其中一个作为独立机制 pilot。优先 E0，因为与论文主张和现有代码线最近；E1 不应与 E0 同时上生产训练。
3. 列出一个留出物理条件和第二个接触任务，预先定义独立 episode、失败类型、数据量与训练费用。没有至少一个新条件/新任务的独立测试，就只写“任务内适应”。

资料吸收的核心不是再拼“VLM + harness + memory + RL”总系统，而是锁定一条受实测交互反馈改变的接口，并让实验回答**改变的是表示、数据选择、记忆，还是更强基础模型本身**。

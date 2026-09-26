<p align="center"><img src="assets/cover.svg" alt="Physical AI · Self-Improvement · Research Library" width="100%"></p>

# 具身 / 机器人 RSI 研究库

面向综述写作，按 **问题 → 方法 → 结果 → 引用价值 → 证据边界** 阅读论文。持续区分任务内适应、可留存的自我改进，以及改进器自身的递归增强。

<!-- stats:start -->
**46 篇阅读卡片** · **141 项原报告条目** · **69 项待核查** · **85 条引文线索**
<!-- stats:end -->

**最近更新：2026-09-26** · [当日增量调研](daily/2026-09-26.md) · [9月25日调研](daily/2026-09-25.md) · [9月24日专题与实验提案](daily/2026-09-24-physical-rsi-cases.md) · [历史日志](daily/)

## 新增专题：从 Physical RSI 线索到 RLT 可执行实验

**[先读综合分析](discussions/physical-rsi-sept24.md)**：Simate、Skild、Zeva-Ego，以及附件补充的 GLOW，分别更新研究流程、策略、上下文或经验链路，不能用同一种“RSI”结论概括。

| 需要的产物 | 入口 |
| :--- | :--- |
| 和同事解释四条路线、证据与取舍 | [综合分析](discussions/physical-rsi-sept24.md) · [3项企业案例](cases/README.md) · [Zeva-Ego勘误](papers/zeva-ego.md) |
| 整理“物理直觉、成长、经验沉淀”的研究动机 | [研究随想与可证伪假设](discussions/physical-experience-theses.md) |
| 本周开始做数据、loss-first与记忆对照 | **[RLT实验方案](experiments/rlt-contact-memory/README.md)** · [接入合同/日志校验](experiments/rlt-contact-memory/implementation.md) |
| 安排Jev、注意力、TTA、Astra/harness的角色 | [后续组件与最小实验](discussions/optional-components.md) |

当前建议：**可靠执行回执 → 离线后果 probe → 匹配的在线 loss 对照 → 有重置边界的经验库**。新增内容均为来源核查或待实施提案，没有新机器人训练结果；企业案例与论文卡片分开计数。

## 从这里开始

| 我想做什么 | 阅读入口 |
| :--- | :--- |
| 找某个方向的相关工作 | **[按主题浏览](topics.md)** — 策略、世界模型、技能、记忆、持续学习等 10 个入口 |
| 判断一篇工作究竟证明了什么 | **[证据对照](evidence-map.md)** — 更新对象、保留范围、物理证据、关键限制 |
| 开始组织综述章节 | **[综述提纲与分类轴](survey-outline.md)** — 章节问题、已有支撑和还缺的证据 |
| 搜题名、短名或 arXiv ID | **[全部阅读卡片](papers/README.md)** · **[原报告 141 项](baseline.md)** |
| 接着读下一批论文 | **[候选队列](candidates.md)** · **[引文溯源](references.md)** |
| 导入文献管理器或 LaTeX | **[BibTeX](references.bib)** — 阅读卡片对应的 arXiv 元数据 |

## 本轮先读这三篇

| 工作 | 为什么值得读 | 放到综述哪里 |
| :--- | :--- | :--- |
| **[KnowBody](papers/know-your-body.md)** | 冻结VLM，把身体关系与任务知识做成验证后发布的跨episode更新；固定预算真机为12/16，对照4/16 | 非参数持久改进、body model、发布门控 |
| **[RACaP](papers/racap.md)** | 同时演化Policy API、ReAct harness与经验记忆；部署前后边界清楚，并报告proposal、episode、时延和成本 | 代码/harness演化、改进预算、非递归边界 |
| **[Uncertainty-Gated Exploration](papers/uncertainty-gated-exploration.md)** | 门控探索减少单任务坍缩，但没有任何方案超过行为克隆起点；汇总成功率会掩盖遗忘 | 在线VLA-RL、保持—可塑性、负结果 |

本轮另收录 [PACL](papers/pacl.md)、[Self-Adaptive VLA](papers/self-adaptive-vla.md)、[WAA](papers/world-action-agent.md)、[RoboRecover](papers/roborecover.md) 与 [world-model benchmark综述](papers/world-model-benchmarks-survey.md)。其中 Self-Adaptive VLA 是实例内上下文适应，RoboRecover 是评价基础设施；两者不因“自适应/恢复”措辞被升级为持久 RSI。全部结果均为作者报告，未复现。

## 按综述主线浏览

| 能力更新 | 反馈与运行条件 | 评价与组织 |
| :--- | :--- | :--- |
| [策略 / VLA-RL](topics.md#policy) | [奖励 / 验证 / 安全](topics.md#feedback) | [持续与部署学习](topics.md#continual) |
| [世界模型](topics.md#world) | [复位 / 恢复 / 采集](topics.md#infrastructure) | [自动研究与改进器](topics.md#improvers) |
| [技能 / 代码 / harness](topics.md#skills) | [课程 / 任务 / 环境](topics.md#curriculum) | [综述 / 评价方法](topics.md#surveys) |
| [记忆 / 上下文](topics.md#memory) | | |

## 阅读时保留的三个区别

- **任务内适应**：重试、重规划或上下文更新帮助当前任务；需要说明重置边界。
- **持久自我改进**：自身执行反馈形成可留存更新，并评估后续能力；不等于完全无人参与。
- **改进器递归增强**：生成、选择或执行更新的机制本身被修改，且后续改进能力得到验证。标题出现 RSI 不足以证明这一点。

[RegenHarness](papers/regenharness.md) 当前展示的是执行案例与版本化修订协议；[LEMCA](papers/lemca.md) 演化的是控制架构。两者都不应只凭“harness / 演化 / 改进器”用词升级为严格递归实证。

<details>
<summary><strong>证据、来源与维护</strong></summary>

- 正式卡片：方法及指定实验/表格已核查，均未复现；原图注明版本和图号。
- 原报告条目：保留公开题名和链接，未逐项重新核查，不与新增卡片混算。
- 候选与引文：不等于全文已读；只读摘要时不填猜测结果。
- [来源与 awesome 入口](sources.md) · [阅读模板](templates/paper.md) · [维护规范](MAINTENANCE.md)
- [结构化目录](data/catalog.json) · [去重基线](data/baseline.json) · [候选数据](data/candidates.json) · [引文数据](data/reference-frontier.json)
- 修改数据后运行 `python survey-rsi/scripts/build_index.py`；首页正文、论文卡片与历史日志保留人工编辑。

</details>

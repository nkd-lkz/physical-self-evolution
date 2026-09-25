<p align="center"><img src="assets/cover.svg" alt="Physical AI · Self-Improvement · Research Library" width="100%"></p>

# 具身 / 机器人 RSI 研究库

面向综述写作，按 **问题 → 方法 → 结果 → 引用价值 → 证据边界** 阅读论文。持续区分任务内适应、可留存的自我改进，以及改进器自身的递归增强。

<!-- stats:start -->
**38 篇阅读卡片** · **141 项原报告条目** · **60 项待核查** · **80 条引文线索**
<!-- stats:end -->

**最近更新：2026-09-25** · [当日增量调研](daily/2026-09-25.md) · [9月24日专题与实验提案](daily/2026-09-24-physical-rsi-cases.md) · [历史日志](daily/)

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
| **[InternW0](papers/internw0.md)** | 联合视频—动作世界模型兼顾7,233.5小时预训练、接触后训练和60.73 ms动作关键路径；但部署权重固定 | 世界模型—策略协同、支撑组件、延迟口径 |
| **[MemBodied](papers/membodied.md)** | episode内联想记忆均值50.0%；跨episode携带降到36.8%，直接揭示记忆持久化的负迁移风险 | 记忆边界、重置协议、任务内适应 |
| **[X2Real](papers/x2real.md)** | 44任务、ID/OOD、DAG过程分和8任务sim-real对照，为“越部署越强”提供更细评测维度 | 评价框架、自动采集、sim-real证据 |

本轮另有 **[The Gaussian Is Enough](papers/gaussian-is-enough.md)** 的负结果：在超过10万次仿真和1250次真机rollout的匹配比较中，复杂先验没有稳定优于高斯，编码器更新的影响更大。四项均为9月22–23日预印本，由9月24日候选池升级为全文核查卡片，未复现。

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

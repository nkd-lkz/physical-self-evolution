# Physical Self-Evolution · RLT 研究工作台

这个仓库记录基于 RLT 的交互记忆研究：利用已完成的命令—响应经验，检验能否加快学习并减少纠错需求。**截至 2026-10-03，尚未证明新方法带来控制、收敛、干预节省或迁移收益。**

**从[研究首页](https://nkd-lkz.github.io/physical-self-evolution/index.html)开始阅读。** 不需要依次翻完所有日报和旧方案。

| 阅读顺序 | 文档 | 它负责回答什么 |
|---|---|---|
| 1 | [当前研究方案与下一步实验](research/zeva-rlt-implementation-2026-09-26.md) | 现行问题、已有实现、拟议方法、baseline 与纠错对照 |
| 2 | [证据与实验总日志](research/experiment-log.md) | 测到了什么、数据在哪里、哪些结论还不能成立 |
| 3 | [英文论文 v2 与中文指南](https://nkd-lkz.github.io/physical-self-evolution/research/papers/interaction-memory-2026-10-03/index.html) | 2026-10-03 固定版本初稿；尚未完整纳入最新纠错预算协议 |
| 4 | [RLT 后续工作图谱](research/literature/rlt-followups.md) / [仿真 baseline 审计](research/literature/rlt-simulation-baselines-2026-10-03.md) | 外部论文与代码来源；作者结果不等于本地复现 |

当前方案只由第 1 项维护。实验事实看对应原始记录与公开摘要；论文是版本快照；日报和旧路线说明形成过程。**文件名日期、内容日期、整理日期与实验日期是不同概念**，页面不会再把一次 Git 编辑自动当作新研究进展。

仓库保留的原始数据哈希用于定位证据，不代表原始数据已公开，也不代表独立复现通过。文献的阅读／核验状态沿用原有阅读总账，本次整理没有将所有论文升级为“已核实”。

- `research/`：当前方案、证据总日志、版本化论文、历史研究记录。
- `notes/`：外部论文与项目笔记。
- `data/`：当前摘要、进度记录、文档用途登记与自动索引。
- `research/archive/`：明确标记的旧快照；其他旧记录保持原链接，在阅读器中标记历史用途。
- `survey-rsi/`：独立 RSI 综述域，本次整理未修改。

[旧 README 快照](research/archive/project-readme-before-2026-10-03.md) · [决策日志](research/decision-log.md) · [资料维护规范](research/knowledge-base-maintenance.md)

维护后运行：

```bash
python research/scripts/test_site_index.py
python research/scripts/build_site_index.py
python research/scripts/build_site_index.py --check
python survey-rsi/scripts/check_boundary.py
```

官方 RLinf main 与相关 PR 在研究开发、开始新实验前核查；固定每轮实验代码版本。此项是工作规范，不是已经启用的后台监控服务。

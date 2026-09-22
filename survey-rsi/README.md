# 具身 / 机器人 RSI 综述调研

按论文题名检索，优先说明**问题 → 方法 → 结果 → 综述用途**，附原图和证据边界。本目录用于综述资料积累；仓库其他目录继续服务Physical Token实验项目。

**最近更新：2026-09-22** · [今天的增量](daily/2026-09-22.md) · [候选文献](candidates.md) · [调研模板](templates/paper.md) · [来源与引文追踪](sources.md)

## 阅读卡片

15篇已读方法和指定实验/表格的卡片，均未复现。下表可直接按题名、短名或标签搜索。

| 工作 | 综述定位 | 阅读入口 |
|---|---|---|
| FAN | 核心持续改进 / VLA持续学习 / 动作归一化 / 真机 | [固定模板卡片](papers/fan.md) · [原文](https://arxiv.org/abs/2609.21358) |
| Compositional Continual World Models | 评价框架 / 世界模型 / 持续学习 / 仿真 | [固定模板卡片](papers/compositional-continual-world-models.md) · [原文](https://arxiv.org/abs/2609.22055) |
| LEMCA | 核心改进器 / 代码演化 / 控制架构 / 仿真 | [固定模板卡片](papers/lemca.md) · [原文](https://arxiv.org/abs/2609.21319) |
| AgenticRL | 核心策略改进 / 奖励代码自精炼 / 仿真到真机 / 版本修订 | [固定模板卡片](papers/agenticrl.md) · [原文](https://arxiv.org/abs/2606.03963) |
| MEMOBench | 评价框架 / 跨时段记忆 / 过程指标 / 仿真 | [固定模板卡片](papers/memobench.md) · [原文](https://arxiv.org/abs/2609.07047) |
| Learning and Transferring Closed-Loop Robot Software | 核心自我改进 / 代码演化 / 跨任务迁移 / 仿真 | [固定模板卡片](papers/learning-transferring-robot-software.md) · [原文](https://arxiv.org/abs/2609.19906) |
| MessyMem | 核心持续改进 / 持久记忆 / 移动操作 / 仿真与真机 | [固定模板卡片](papers/messymem.md) · [原文](https://arxiv.org/abs/2609.15976) |
| SRPO | 核心策略改进 / 自参考奖励 / VLA-RL / 旧文补漏 | [固定模板卡片](papers/srpo.md) · [原文](https://arxiv.org/abs/2511.15605) |
| HALTER | 闭环基础设施 / 自动复位 / 自主评价 / 真机 | [固定模板卡片](papers/halter.md) · [原文](https://arxiv.org/abs/2609.19413) |
| No Free Checker | 重点综述 / 验证器 / 奖励可靠性 / 参考文献入口 | [固定模板卡片](papers/no-free-checker.md) · [原文](https://arxiv.org/abs/2609.09250) |
| World Models: Plausible → Controllable → Actionable | 重点综述 / 世界模型 / 闭环效用 / 参考文献入口 | [固定模板卡片](papers/world-models-actionable-survey.md) · [原文](https://arxiv.org/abs/2609.16697) |
| Embodied-BenchForge | 评价基础设施 / 基准生成 / 验证修复 / 仿真 | [固定模板卡片](papers/embodied-benchforge.md) · [原文](https://arxiv.org/abs/2609.13082) |
| SafeMem | 边界案例 / 图记忆 / 风险验证 / 仿真与真机 | [固定模板卡片](papers/safemem.md) · [原文](https://arxiv.org/abs/2609.08444) |
| Show-Harness | 边界案例 / 语义动作接口 / harness / 真机 | [固定模板卡片](papers/show-harness.md) · [原文](https://arxiv.org/abs/2609.10522) |
| EmbodiedSkills | 边界案例 / 技能契约 / 验证与恢复 / 仿真 | [固定模板卡片](papers/embodiedskills.md) · [原文](https://arxiv.org/abs/2609.01281) |

## 去重与后续更新

- [原报告去重基线](data/baseline.json)：141个既有条目，只保存公开题名和来源；旧报告内容不视为本轮再次核查。
- [新增文献结构化目录](data/catalog.json)：15篇卡片的版本、标签和阅读状态。
- [候选目录](candidates.md)：35项仅摘要核查，未与正式卡片混算。
- [引文追踪队列](data/reference-frontier.json)：52项尚未独立全文验证的引文线索，继续回原文。
- [每日维护规范](MAINTENANCE.md)：去重、检索、原图、证据核查和提交要求。

每天分别记录新收录、旧文补漏、版本修订和待核查项。计划运行区间为2026-09-21至2026-09-30；是否完成以daily日志与Git提交为准。不要求每天凑数，也不把“harness”“闭环”“自进化”等题名用词当成RSI实证。

## 用于综述组织的标签

更新对象（策略/世界模型/奖励/记忆/技能/代码/数据/课程/改进器）；反馈来源；保留范围（任务内/跨任务/跨部署）；人工参与；仿真或真机；验收独立性；资源预算；证据强度；综述用途（核心机制/支撑组件/边界/综述/观点）。不同轴分别标记，不用一个等级替代所有判断。

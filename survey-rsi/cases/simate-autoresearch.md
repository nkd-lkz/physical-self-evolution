[案例目录](README.md) · [横向分析](../discussions/physical-rsi-sept24.md)

# Simate AutoResearch：研究流程自动化与榜单结果的证据边界

**类型：** 企业系统与官方产品页面。**核查：** 2026-09-24。**状态：** 官方页面及榜单公开数据已核查，未使用平台、未复现。

## 解决什么问题

本文仅以[官方首页](https://mate-robot.cn/home/)、[Sinfra](https://mate-robot.cn/research/sinfra/)与[RoboScientist Gallery](https://mate-robot.cn/research/RoboScientist/gallery/)为证据，关注研究配置、实验执行和评测记录如何衔接。这属于研发流程问题，不能直接等同机器人在真实任务中自主学习。

## 一手来源能确认什么

- [Simate 官网](https://mate-robot.cn/home/)目前使用 **Sinfra / Sipai / RoboScientist** 的产品分工；AutoResearch 是发现线索时的名称；其与公开产品的版本对应未核实，不另计为已确认的独立系统。
- [RoboDojo 官方榜单](https://robodojo-benchmark.com/leaderboard)本次快照的仿真榜：Simate-beta **Score 33.95、成功率 27.96%**；GPT-6-Astra 为 **28.97、22.48%**。分数与成功率是两个指标。原始发布页数据和官方域名前端公开数据一致，榜单会更新。
- [Sinfra 页面](https://mate-robot.cn/research/sinfra/)展示任务、模型版本、验证和部署记录的衔接；若干训练曲线、配置比较和 Agent 交互明确标为 **illustrative**，不能用作真实实验改进曲线。
- [RoboScientist 公开 Gallery](https://mate-robot.cn/research/RoboScientist/gallery/)并非只有空页面：其公开 CDN 索引与 v3 snapshot 含 **16 个研究节点、25 个 run、1 份报告**，有选择/否决记录及指标字段。这支持存在可检查的研究记录结构；它与本次榜单提交的版本对应、自动修改代码的完整轨迹和独立复现仍未核实，不把 Gallery 指标直接当作 RoboDojo 总榜成绩。
- “免费”公开表述可明确对应部分公开数据集访问；页面另有企业访问申请。免费内测范围、算力额度与期限没有核实成统一开放条款；公开页面不等于代码和模型开源。

## 可以支持与仍缺什么

官方榜单支持该提交在该快照下的评测排名。**它没有单独证明排名提升由 AutoResearch 导致，更没有证明研究改进器已经递归增强。**“全球首个”“完全超越”“已证明强 RSI”都不作为本库事实标签。

需要继续核查的证据是：初始系统、每轮具体改动、人工选择与纠正记录、全部失败尝试、固定外部评测、累计预算，以及相同预算的固定研究流程对照。评测过程是否反复被用于调参，也应说明。

## 来源定位

1. [官方首页](https://mate-robot.cn/home/)：Platform + Model + Scientist 与闭环分工。
2. [官方 Sinfra](https://mate-robot.cn/research/sinfra/)：Agent、Training Insights、Experiment Comparison、访问入口。
3. [官方 Sipai](https://mate-robot.cn/research/sipai/)：配置与训练系统介绍。
4. [官方实验展示入口](https://mate-robot.cn/research/RoboScientist/gallery/)及[公开索引](https://mate-robot.cn/research/RoboScientist/gallery/cdn/index.json)：已读取索引所指向的公开 snapshot；producer/部分操作归属为空，已有图谱与指标不能替代完整自动研究归因。未转载原始记录中出现的个人路径。
5. [RoboDojo 官方榜单](https://robodojo-benchmark.com/leaderboard)：仿真榜快照，访问 2026-09-24。

**标签轴：** 研究流程 / 实验反馈 / 人在环 / 企业系统 / 排名可核查、递归归因待验证。

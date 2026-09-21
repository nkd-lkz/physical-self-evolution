# 每日检索与证据维护

本目录服务具身/机器人RSI综述，范围覆盖策略、世界模型、记忆、技能、代码/harness、数据/课程、评价/复位和改进器；与仓库的Physical Token实验主线分别维护。

## 一个运行周期

1. 读取本目录README、data/baseline.json、data/catalog.json、data/candidates.json及最近daily日志。不要凭对话记忆判断去重。
2. 检索arXiv cs.RO/cs.AI/cs.LG、OpenReview和正式会议论文集、作者项目/代码、可信研究机构原文；发现新综述需抽查其直接引用的核心相关文献，继续滚雪球检索。
3. 并行覆盖策略/RL、世界模型、技能/harness、记忆/持续学习、验证/复位/安全、环境生成、自动研究等主题。awesome仅作线索入口，每篇回原始来源核实。
4. 按DOI、无版本arXiv ID、完整题名、作者与项目链接合并预印本/会议版本；同缩写不自动合并。已有条目更新版本、数字或勘误，只计修订。旧文首次补入标“旧文补漏”，不冒充当天新发表。
5. 先筛摘要，优先读最相关的全文方法/实验并写固定模板；目标每天补3–8篇高相关卡片，但不为数量降低标准。摘要级线索仅进候选队列；无新增时如实记零。
6. 核实方法图号、样本量、基线、物理平台、指标定义、人工参与及留存范围。没有完整来源不补写内容。预印本/行业观点/企业案例分别标注。
7. 原图优先嵌入作者页面链接，附图号、版本、来源；若下载再发布，遵循原始许可。论文自身采用AI插图时照实标注，不以图精美代替证据。未公开小组截图与聊天不上传。
8. 将正式卡片写入papers/，更新catalog、候选和README，写daily/YYYY-MM-DD.md；日志列新增、补漏、修订、待查、实际搜索覆盖和失败来源。保留旧日志；检索日期和论文日期分开。
9. 提交仅本目录（可维护根README的本目录入口），不得改变实验记录、研究主线或网站状态。提交前读取最新HEAD，用非强制快进更新；有冲突则基于最新内容合并。
10. 给用户简报与当天GitHub直达链接，说明最值得读的3项和证据警戒点。自动化失败时报告，不能声称已提交。

## 判定标签

- 核心自我改进：来自自身执行的反馈形成可保留更新，并评测更新后的能力。
- 持续改进：跨任务/部署累积记忆或技能且有对照证据；仍不自动等同强RSI。
- 严格递归候选：改进器、更新策略或学习规则自身被修改，并在后续轮次检验改进能力；不能仅凭题名认定。
- 支撑组件：奖励、验证、复位、生成任务、世界模型等；不把组件结果夸成完整系统。
- 边界案例：任务内重试、固定harness、离线微调、上下文适应。
- 观点：区分作者主张和整理者推论；无完整正文的小红书/公众号不收录内容。

## 搜索式示例

(robot OR embodied OR physical) AND (self-improvement OR self-evolving OR recursive OR autonomous learning)

(robot OR VLA) AND (deployment learning OR lifelong OR continual OR online reinforcement learning)

(robot OR embodied) AND (coding agent OR harness evolution OR skill discovery OR persistent memory)

(robot OR embodied) AND (verifier OR reward hacking OR reset OR failure recovery OR automatic curriculum)

每轮记录实际运行的搜索与覆盖；关键词搜索无效时转官方列表、API或原始文献引文，不能用不相关搜索结果证明“没有新论文”。

# 每日检索与证据维护

本目录服务具身/机器人RSI综述，范围覆盖策略、世界模型、记忆、技能、代码/harness、数据/课程、评价/复位和改进器。全部输入遵循[公开文献范围与来源边界](SCOPE.md)。

## 一个运行周期

1. 读取本目录AGENTS、SCOPE、README、data/baseline.json、data/catalog.json、data/candidates.json及最近daily日志。不要凭对话记忆判断去重。不要读取仓库其他项目材料或项目聊天来寻找选题、补写结论或评价创新性。
2. 检索arXiv cs.RO/cs.AI/cs.LG、OpenReview和正式会议论文集、作者项目/代码、可信研究机构原文；发现新综述需抽查其直接引用的核心相关文献，继续滚雪球检索。
3. 并行覆盖策略/RL、世界模型、技能/harness、记忆/持续学习、验证/复位/安全、环境生成、自动研究等主题。awesome仅作线索入口，每篇回原始来源核实。
4. 按DOI、无版本arXiv ID、完整题名、作者与项目链接合并预印本/会议版本；同缩写不自动合并。已有条目更新版本、数字或勘误，只计修订。旧文首次补入标“旧文补漏”，不冒充当天新发表。
5. 先筛摘要，优先读最相关的全文方法/实验并写固定模板；目标每天补3–8篇高相关卡片，但不为数量降低标准。摘要级线索仅进候选队列；无新增时如实记零。
6. 核实方法图号、样本量、基线、物理平台、指标定义、人工参与及留存范围。没有完整来源不补写内容。预印本/行业观点/企业案例分别标注。
7. 原图优先嵌入作者页面链接，附图号、版本、来源；若下载再发布，遵循原始许可。论文自身采用AI插图时照实标注，不以图精美代替证据。未公开小组截图与聊天不上传。
8. 将正式卡片写入papers/，更新catalog、候选和README，写daily/YYYY-MM-DD.md；日志列新增、补漏、修订、待查、实际搜索覆盖和失败来源。保留旧日志；检索日期和论文日期分开。
9. 提交仅本目录，不维护根README，不读写其他项目记录或网站。先运行 `python survey-rsi/scripts/check_boundary.py`，再人工核对新增内容是否完全来自公开来源，综述推论是否可追溯；不得添加项目回链。提交前读取最新HEAD，用非强制快进更新；有冲突则基于最新内容合并。
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


## 导航与同日追加维护（2026-09-24 起）

- `README.md` 是精简入口，保留人工编辑正文；统计区由脚本更新，不再把所有论文堆成首页长表。
- `data/catalog.json`、`data/candidates.json`、`data/reference-frontier.json` 为索引数据；`data/navigation.json` 管理主题与卡片路径，同篇可多主题。
- 新卡片写完后运行 `python survey-rsi/scripts/build_index.py`（仓库根目录）。脚本更新 `papers/README.md`、`topics.md`、`baseline.md`、`candidates.md`、`references.md`、`references.bib` 和首页统计区，不改卡片正文或日志。
- 新卡片的文件名加入 `data/navigation.json` 中恰当主题；若有新的综述发现，再人工更新 `evidence-map.md`、`survey-outline.md` 和首页推荐阅读，避免长期停留在旧批次。
- 同一天已有日志时，保留它并写 `daily/YYYY-MM-DD-follow-up.md`；如仍有后续轮次可使用有含义的后缀。日报分别统计“本轮增量”和“当前累计”，不要将早间成果再次计新。
- 编辑派生索引时，先把改动反映到数据或生成脚本，避免下一轮生成覆盖人工内容；历史阅读卡片和日志不做批量事实重写。
- `references.bib` 只导出有作者元数据的正式卡片，按所读 arXiv 记录生成，不猜测会议接收状态；原报告和候选不自动导入为已核查引用。

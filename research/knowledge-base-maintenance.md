# Knowledge Base Maintenance Protocol

## 目标

这个仓库同时承担两种职责：

1. **Project OS**：监督当前科研主线、实验进度、失败诊断和下一步。
2. **Frontier Knowledge Base**：积累具身自进化相关论文、项目、观点、方法边界和可借鉴点。

两者必须分开，否则会出现“今天看到一篇新论文，明天科研主线就被带跑”的问题。

---

## 1. 三层结构

### Layer A · Project Mainline

只记录：
- 当前 Phase；
- 实验事实；
- checkpoint / config / result；
- failure profile；
- 下一步；
- 决策变更。

只有实验或强近邻证据可以修改。

### Layer B · Frontier Knowledge

记录：
- 论文；
- 项目；
- 开源系统；
- 研究者观点；
- 行业系统；
- benchmark；
- tool / harness / runtime。

可以持续扩张，不要求每条都进入当前实验。

### Layer C · Historical Archive

历史版本只读保留。

任何大重构都不能把以前的知识直接删掉：
- 原 HTML snapshot；
- 旧 roadmap；
- 旧 paper notes；
- 被降级的 hypothesis。

---

## 2. 每日输入如何进入网站（2026-09-30 更新）

**统一入口是 [科研工作台](../index.html)。** 目录用于保存源文件，浏览、检索、汇报从首页开始；不再为每次调研新建一份互相竞争的总览。

| 输入 | 维护位置 | 首页呈现 |
| --- | --- | --- |
| 真实开发进度 | `data/experiments.json` 记录日期、标题、结果摘要；可显式填写 `path` 指向已有日报 | 每日科研进度，按日期折叠、搜索、筛选 |
| 最新实验状态 / 下一步 | `data/current-status.json` 的 `as_of / metrics / timeline / plan` | 当前证据快照与下一步；这是最近记录，不是实时 GPU 监控 |
| 详细实验证据 | 优先更新当天 `research/progress-YYYY-MM-DD*.md` 或既有专题；总日志保留研究时间线 | 自动进入资料库，日报链接与进度联动 |
| 论文 / 开源项目 / 调研 | 优先更新同主题 `notes/` 或 `research/literature/` 笔记；阅读状态沿用现有论文卡与总账 | 自动索引；按资料类型、主题和关键词查找 |
| 当前 idea / 重点阅读 | `data/research-hub.json`，只放少量精选卡与原始笔记路径 | 实验与 idea、重点调研；写清实现、对照和判定 |
| 原始随想 / 路线变化 | `research/perspectives-and-theses.md`、`decision-log.md` | 首页研究脉络入口与资料检索 |

一次普通更新的流程：

1. 核验来源或真实实验记录，更新已有主题笔记 / 当日日报。没有新结果就如实写“待运行 / 待核验”，不生成虚构进度。
2. 只有实验状态变化时更新 `current-status.json`；只有实际开发事件写 `experiments.json`。旧快照保留，后续结果追加，不把历史阶段误称当前状态。
3. 新论文按原有元数据方式更新阅读总账与论文卡。只有改变当下选择的文献才加入精选；普通新增资料自动收录即可。
4. 执行 `python research/scripts/build_site_index.py`，生成 `data/knowledge-index.json`。该文件是衍生索引，不手工编辑；合并修改后再次生成。部署会自动重建，避免漏收录。
5. 检查本地链接、JSON 和首页搜索；提交前执行既有边界检查。发布后确认首页可访问。

索引只扫描项目 `research/`、`notes/` 的 Markdown 与根目录项目元数据；不读 `survey-rsi/`。资料记录日期来自文件日期 / Git 修改日期，不冒充论文发表日期。未建立独立笔记的总账条目保留“阅读清单”标签；“有笔记”也不等于已复现。

页面组织：研究总览 → 每日科研进度 → 实验与 idea → 调研与阅读库。原详细笔记路径不变；旧首页结构保存在 [09-30 改版前快照](../archive/research-os-before-hub-2026-09-30.html)，仅用于追溯，当前状态以首页数据为准。

---

## 3. Public Repository Redaction Policy

本仓库是公开科研记录，只发布**脱敏后的科研证据与结论**。

### 可以公开

- 算法流程、实验设计和研究判断；
- 公开代码仓库 commit / branch 名称；
- 非敏感 checkpoint 版本名或 step；
- loss、success rate、episode length、transition count 等实验指标；
- 已公开论文 / 项目链接；
- 不暴露内部基础设施的复现实验摘要；
- 经脱敏后的失败原因与修复结论。

### 默认不公开

- 内部服务器绝对路径；
- 用户名、主机名、IP、账号、token、credential；
- 其他用户的进程名 / PID / GPU 占用细节；
- 私有 W&B / 内网 dashboard 标识；
- 可暴露机器结构、内部挂载点或权限信息的完整启动命令；
- 未确认可公开的数据 / checkpoint 下载地址。

### 写法原则

原始实验日志是最终证据，但公开仓库只保留足以支持科研结论的脱敏摘要。例如：

- 写“共享 GPU 导致资源竞争，launcher 已加入显式 shared-GPU 开关”；
- 不写其他用户用户名、PID 和内部进程路径。

- 写“Stage1 checkpoint 完整加载 667 base + 62 RLT tensors”；
- 不写私有绝对文件路径。

如需完整原始证据，应保存在私有实验存储或内部日志系统，而不是公开 GitHub。

---

## 4. 新论文最小 schema

每条至少记录：

- Title
- Year
- Category
- Layer
- What is updated?
- What feedback is used?
- Timescale
- Core mechanism
- Main evidence
- What can we borrow?
- Boundary / what it does NOT solve
- Relevance to our current Phase
- URL
- Read status

---

## 5. 论文什么时候进入主线？

只有以下情况：

1. 它给出必须补的 stronger baseline；
2. 它已经覆盖我们原本想宣称的 novelty；
3. 它暴露出当前实验设计不公平；
4. 它与我们的 failure profile 高度吻合；
5. 它给出一个更便宜、可证伪的解释。

否则：
- 归档；
- 留在 frontier；
- 不改本周计划。

---

## 6. 网站应该回答的五个问题

打开网站后，应该能快速回答：

1. **我现在科研做到哪里？**
2. **今天最应该做什么？**
3. **为什么做这一步？**
4. **别人围绕这个问题已经做了什么？**
5. **如果当前假设失败，我有哪些证据支持的备选方向？**

如果网站只能回答论文列表，说明 Project OS 太弱。

如果网站只能回答下一步实验，说明 Knowledge Base 太弱。

---

## 7. 每周维护动作

每周做一次：

### Project Review
- 哪些事实新增？
- 哪些假设被削弱？
- 哪个 task / pipeline 变稳定？
- 下周最小实验是什么？

### Frontier Review
- 新增哪些工作？
- 哪条路线突然变密？
- 哪些工作改变 innovation boundary？
- 哪篇必须精读？

### Archive
- 保存重要版本；
- 不覆盖旧 snapshot；
- 记录路线转向原因。

---

## 8. 长期目标

让这个网站逐步变成：

**Embodied Self-Evolution Research OS**

同时是：
- 实验监督台；
- 研究决策记忆；
- 论文地图；
- 灵感库；
- 失败案例库；
- 自己未来写论文时的 related-work 索引。

它应该成为科研的“第一入口”，但不是封闭世界。前沿仍然需要持续搜索、阅读、核验，再把新知识吸收到这里。


## 9. RSI 综述与项目区隔离（2026-09-26）

本协议的 Frontier Knowledge 是项目侧知识库，允许包含项目用途和研究推论；独立的 `survey-rsi/` 仅维护公开文献和可溯源综述分析。不能把项目笔记、实验进展、个人随想或内部上下文作为综述的来源，也不能将项目提案改写成“综述启发”后移回。

RLT 任务可以读取综述公开文献并在本区记录项目用途，见[单向文献引入](survey-literature-intake.md)。综述任务不读取本协议所在的项目资料、不改网站或根目录数据。公开发表的 RLT 相关论文可以按原始文献独立收录，不与本项目混淆。

跨区迁移需要用户明确指令；普通每日任务不能顺带迁移。目录划分与自动检查只减少内容串写，不能给公开仓库提供保密权限，也不能抹除旧 Git 历史。

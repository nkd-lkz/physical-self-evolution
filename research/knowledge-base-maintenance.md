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

## 2. 每日输入如何进入网站

用户每天可能提供三类内容：

### A. 实验进度

进入：
- data/experiments.json
- research/experiment-log.md
- 必要时 research/decision-log.md
- 首页 Current Project State

### B. 新论文 / 新项目

先进入：
- data/frontier.json
- research/frontier-landscape.md
- 若精读，再进入 data/papers.json 与 notes/

### C. 随想 / 观点 / 组会

进入：
- research/perspectives-and-theses.md
- Idea Pool
- 只有形成明确研究决策时才进入 decision-log

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

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

## 3. 新论文最小 schema

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

## 4. 论文什么时候进入主线？

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

## 5. 网站应该回答的五个问题

打开网站后，应该能快速回答：

1. **我现在科研做到哪里？**
2. **今天最应该做什么？**
3. **为什么做这一步？**
4. **别人围绕这个问题已经做了什么？**
5. **如果当前假设失败，我有哪些证据支持的备选方向？**

如果网站只能回答论文列表，说明 Project OS 太弱。

如果网站只能回答下一步实验，说明 Knowledge Base 太弱。

---

## 6. 每周维护动作

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

## 7. 长期目标

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

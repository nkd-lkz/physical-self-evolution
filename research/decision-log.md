# 科研决策日志

## 2026-09-11 · Research Story

**决定：** 不再以 RL Token / Physical Token 为上位故事。

**改为：** Physical Interaction + Self-Improvement。

**原因：**
- RLT 是很好的技术起点，但不是长期科学问题本身。
- representation、critic、data、history、execution 都可能是真正瓶颈。
- 研究方法必须允许实验推翻最初假设。

---

## 2026-09-11 · Baseline First

**决定：** 在创新前先完成多任务 RLT research bench。

**原因：**
- 没有稳定 baseline，后续任何模块收益都不可归因。
- RoboTwin2 / RoboDojo 将承担长期多任务对照平台。

---

## 2026-09-11 · Paper Reading Guardrail

**决定：** 新论文默认只进入知识库，不自动修改研究主线。

**只有以下情况才改变主线：**
1. 实验结果直接否定当前解释；
2. 强近邻工作已经覆盖核心 novelty；
3. 新工作提供一个更简单且更强的 baseline；
4. 工程现实暴露出当前问题定义错误。

# Harness VLA：Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

> 阅读状态：**专题阅读完成**  
> 定位：Planner / Harness self-improvement，不是 actor-side Physical Token。

## 1. 一句话

Harness VLA 将 frozen VLA 降级为一个局部 contact-rich manipulation primitive，由 Agent Planner、解析 primitive 和 memory 负责 staging、调用、重试和恢复。

## 2. 核心结构

```text
Task + RGB-D + state
        ↓
Agentic Planner
   ↙             ↘
analytic skill    VLA primitive
   ↘             ↙
   physical world
        ↓
new observation / memory
```

VLA 不再独自承担长程规划、空间搬运、失败恢复和接触动作全部责任。

## 3. 最值得记的概念：Operating Range

关键不是简单问“VLA 会不会做”，而是：

> **VLA 在什么状态分布、姿态、距离、任务阶段下可靠？**

系统通过 restage / move / retry 把机器人重新带回 VLA 的有效工作区间。

这给 Physical Token 一个非常有价值的 probe：

```text
z_phys → P(base policy remains valid)
z_phys → P(failure onset)
```

## 4. Memory

Task-specific memory 保存成功的 primitive sequence；global memory 存储可复用 failure / recovery heuristic。

这属于：

> Context / Harness Evolution

而不是 policy weight evolution。

## 5. 与我们的项目边界

Harness VLA 主要回答：

> “怎么更可靠地使用一个已有策略？”

Physical Token 想回答：

> “动作生成内部是否存在可被物理后果 grounding 的 compact state，并能帮助底层决策？”

因此 Harness 的 planner / memory 不应进入第一轮 matched representation experiment。

## 6. 可借鉴

- operating-range probe；
- failure-stage taxonomy；
- restaging / retry 作为 execution baseline；
- 区分 primitive failure 与 orchestration failure。

## 7. Source

- arXiv: https://arxiv.org/abs/2607.08448

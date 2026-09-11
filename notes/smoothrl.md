# SmoothRL: Online Reinforcement Learning During Asynchronous Execution

## 一句话

SmoothRL 解决的是：

> 当机器人执行动作的同时，VLA 在后台计算下一 action chunk 时，生成出来的完整 chunk 并不会全部真正执行，Online RL 应该怎样只对真实执行过的动作负责？

---

## 1. 与 RLT 的关系

RLT 的 RL abstraction 更接近：

```
state
↓
generate RL chunk
↓
execute chunk
↓
next state
```

因此当前 transition 里的 action 可以直接当作作用于环境的 action。

SmoothRL 面对的 deployment timing 是：

```
robot executes old chunk
        ||
policy infers new chunk
```

于是：

**generated chunk ≠ executed chunk**

---

## 2. 三个区域

异步下一个新 chunk 可划分为：

- Committed：新 chunk 计算期间，对应时段已经由旧 chunk 执行；
- Execution：当前新 chunk 真正送到机器人；
- Discarded：下一 chunk 到来后被覆盖，永远没有执行。

---

## 3. RL 为什么会出问题？

Reward 是真实执行动作产生的。

如果仍对整条 generated chunk 传 value gradient，就会把 credit / blame 分配给根本没执行过的动作。

因此 SmoothRL 的核心：

**Critic 条件化真实作用过的序列；Actor gradient 只通过 Execution Region。**

---

## 4. 对当前项目的意义

这篇论文不意味着我们现在必须做 async。

正确顺序是：

1. 先把 RLT synchronous / sequential baseline 定义清楚；
2. 记录完整 inference latency、control frequency、chunk timing；
3. 只有当 latency / motion continuity 真成为瓶颈时，再研究 async；
4. 一旦 async，必须把 generated action / executed action / replay transition 严格对齐。

---

## 5. 与 RTC 的区别

- RTC：解决异步 action chunks 如何连续地生成 / 拼接。
- SmoothRL：解决异步执行下 RL 的 credit assignment。

二者是互补，不是替代。

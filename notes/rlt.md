# RL Token: Bootstrapping Online RL with Vision-Language-Action Models

## 一句话

冻结大型 VLA，提取紧凑 RL Token / representation，并训练轻量 actor–critic，在 VLA 已有策略附近做样本高效 Online RL。

它是当前项目的 **技术脚手架和主 baseline**，不是最终 research story。

---

## 1. 两阶段

### Stage 1

VLA hidden states → compact RL representation。

通过轻量 encoder / decoder 让一个小 representation 保留对控制有用的信息。

### Stage 2

冻结 VLA / feature model，只训练轻量 actor / critic。

Actor 条件包括：
- compact representation；
- proprio；
- VLA reference action chunk。

---

## 2. Reference Action

RLT 不是让 RL 从整个连续动作空间从零探索。

它让 actor 看到 VLA reference，并在其附近优化。

核心直觉：

**Foundation Policy 提供 Prior，Online RL 做 Local Refinement。**

---

## 3. Action Chunk

原论文以 action chunk 作为 RL decision unit。

这同时解决两件事：
- 缩短 sparse reward credit-assignment horizon；
- 不需要以机器人控制频率查询大型 VLA。

---

## 4. 为什么是当前 baseline？

它天然适合我们的目标：
- 保留预训练 VLA 先验；
- Online update 只作用于小网络；
- 适合精细操作的局部适应；
- 可以比较 representation / critic / data / execution 的贡献。

---

## 5. 当前本地实现必须特别注意

我们使用 π0.5，而原论文是不同基础模型。

本地可能存在：
- residual actor；
- K=1；
- 不同的 switch；
- 不同的 execution chunk。

所以以后必须写：

**RLT-π0.5-adapted**

并明确与 **Local-Residual** 分开。

---

## 6. 当前最重要的问题

RLT 在我们的任务中失败时，不能直接说“它不懂物理”。

必须先判断：
1. observation 不足？
2. candidate action 无 improvement headroom？
3. critic 不会排名？
4. failure data 不够？
5. chunk 太长 / feedback 太慢？

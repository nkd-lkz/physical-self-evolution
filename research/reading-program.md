# 每日论文阅读计划：让前沿知识服务于科研主线

> 原则：每天读论文是为了提高研究判断力，不是为了每天改一次方向。

---

## 1. 每篇论文固定回答 7 个问题

1. 这篇论文真正解决的 failure mode 是什么？
2. 它更新的是 weights、memory、skill、harness、world model 还是 execution schedule？
3. 它利用什么 feedback？
4. 改进发生在哪个时间尺度？
5. 最强证据是什么？
6. 它占掉了我们哪块 innovation space？
7. 对当前项目要做什么？

合法的“项目动作”只有：

- Add baseline
- Add ablation
- Add diagnosis
- Archive / no action

---

## 2. 第一轮阅读顺序

### Track A · Baseline / Online RL / Execution

1. RLT
2. SERL
3. SmoothRL
4. Q-VGM
5. PLD

目的：
- 先理解 Online RL 最基本的系统条件；
- 再理解 VLA / flow policy / async execution 的特殊性；
- 最后理解 RL 经验如何回写 foundation model。

---

### Track B · Physical Experience

6. V-GPS
7. Rapid Motor Adaptation for Manipulator Arms
8. Pri4R
9. PHR-VLA
10. FD-VLA
11. MSDP
12. HapticVLA
13. SR-WM

目的：

比较 Physics 到底应该进入：

- history；
- representation；
- critic/value；
- privileged teacher；
- world model。

---

### Track C · Failure / Recovery

14. FailSafe
15. RedFlow
16. RL²-VLA
17. VLA-Corrector
18. BCP

目的：

回答：
- 哪些失败应该纠正？
- correction target 从哪里来？
- 什么时候应该 replanning？
- 什么时候应该缩短 chunk？
- 是否需要更新权重？

---

### Track D · Context / Harness / Agent Evolution

19. Zeva
20. Harness VLA
21. SHAPER
22. ASPIRE
23. Zetta
24. ENPIRE
25. Learning While Deploying

目的：

理解：
- 不更新权重的 self-improvement；
- skill / harness evolution；
- validation-gated memory；
- agentic policy improvement；
- fleet experience scaling。

---

## 3. 当前 Phase 0 的“阅读优先级”

虽然知识库会越来越大，但当前项目最值得精读：

### 一级

- RLT
- SERL
- RoboTwin2
- SmoothRL

### 二级

- Q-VGM
- V-GPS
- VLA-Corrector
- BCP

### 三级

- Pri4R
- Zeva
- RedFlow
- Harness VLA
- Zetta

### 长期

- PLD
- Learning While Deploying
- ENPIRE
- SHAPER
- ASPIRE

---

## 4. 每日群里分享模板

### Paper

标题 + 链接

### One Sentence

这篇论文真正解决什么？

### Mechanism

最多 3 条。

### Evidence

最关键实验结果。

### Boundary

它没解决什么？

### Our Project

- Add baseline？
- Add diagnosis？
- Add ablation？
- Archive？

### One Discussion Question

只留 1 个真正值得讨论的问题。

---

## 5. 每周复盘

每周不要问：

> 我看了多少篇？

问：

1. 哪个旧假设被削弱？
2. 哪个 baseline 必须补？
3. 哪个 failure mode 变得更清楚？
4. 有哪些 idea 应该明确不做？
5. 下周最便宜的证伪实验是什么？

---

## 6. 网站维护规则

新增论文先进入 Knowledge Base。

只有满足以下任一条件，才写进 Project Mainline：

1. 实验直接支持 / 否定某假设；
2. 强近邻已经覆盖核心 novelty；
3. 新论文给出更简单强 baseline；
4. 新论文暴露当前实验设计不公平；
5. 工程现实表明原问题定义错误。

这样知识可以无限扩张，但主线不会无限发散。

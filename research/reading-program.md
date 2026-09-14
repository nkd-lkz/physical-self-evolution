# 每日论文阅读计划：围绕 Universal Physical Token 服务当前科研主线

> 原则：论文用于找 baseline、边界和实现方法，不再用来每天扩展新的上位研究故事。  
> 当前 Source of Truth：`research/physical-token-leadership-spec.md`。

---

## 1. 每篇论文固定回答 7 个问题

1. 它是否与 **action-head / compact readout** 直接相关？
2. 它如何表示 **action → measured consequence**？
3. 它用了什么 physics / dynamics supervision，是否真的可测、可校准？
4. 它如何做 online adaptation，哪些参数被冻结？
5. 它最强的 matched baseline / ablation 是什么？
6. 它占掉了 Physical Token 的哪块 innovation space？
7. 对当前 B0/B1/B2 实验要做什么？

合法的“项目动作”优先只有：

- Add baseline
- Add ablation
- Add implementation detail
- Add metric
- Archive / no action

除非领导重新定义问题，否则论文不直接改上位主线。

---

## 2. 当前第一优先阅读 Track

### Track A · Compact Readout / Online RL

1. RLT
2. SERL
3. Q-VGM
4. SmoothRL

重点看：

- compact representation 从哪里读？
- actor / critic 看什么？
- online phase 冻结什么？
- actual executed action 如何进 replay / critic？
- learner 预算如何匹配？

当前用途：服务 B0 与 Online Adaptation Protocol。

---

### Track B · Transition / Physical Representation

1. Rapid Motor Adaptation for Manipulator Arms
2. Pri4R
3. FD-VLA
4. HapticVLA
5. MSDP
6. PHR-VLA

重点看：

- history / dynamics / future outcome supervision；
- privileged target 如何避免部署泄漏；
- physical variable 的单位、frame、mask、normalization；
- representation 改进是否最终帮助 control / critic。

当前用途：服务 B1 / B2 target 选择。

---

### Track C · Action Consequence / World Model

1. RISE
2. Motus2
3. SR-WM
4. V-GPS

重点看：

- Action→Consequence 如何定义；
- consequence 是否真正服务 decision；
- value / ranking 与 auxiliary prediction 的区别；
- 哪些机制可以压缩成轻量 Physical Token，而不必引入完整 World Model。

当前用途：related work / target design，不把 Full World Model 引入首轮 B0/B1/B2。

---

### Track D · Online Efficiency / Streaming（后置）

1. SmoothRL
2. Streaming RL / batch-to-streaming continuous control
3. adaptive chunk / continuation / replanning work

只有 B1/B2 证明 Physical Token 有价值后，再重点研究：

- replay vs no-replay；
- batch size≈1；
- chunk-boundary update；
- uncertainty-aware update strength；
- safety fallback。

---

### Track E · Self-Evolution Systems（知识库）

- Zeva
- Zetta
- Harness VLA
- LWD
- ENPIRE
- SHAPER
- ASPIRE

用途：长期理解 memory / harness / fleet / agentic evolution。

当前不把这些模块加入首轮 Physical Token 方法。

---

## 3. 当前精读优先级

### 一级：直接影响近期代码与实验

- RLT
- action-head / feature readout 相关工作
- Rapid Motor Adaptation
- Pri4R
- FD-VLA
- HapticVLA

### 二级：帮助定义 consequence / value 边界

- RISE
- Motus2
- V-GPS
- SR-WM
- Q-VGM

### 三级：Physical Token 成立后再深入

- SmoothRL
- Streaming RL
- BCP / VLA-Corrector

### 长期知识库

- Zeva / Zetta
- LWD
- Harness VLA
- ENPIRE / SHAPER / ASPIRE

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

### Physical Token Relevance

只回答以下之一：

- 对 B0 baseline 有帮助？
- 对 B1 transition target 有帮助？
- 对 B2 physics loss 有帮助？
- 对 online learner / metric 有帮助？
- 只是长期 related work？

### Boundary

它没有解决什么？尤其检查是否真的支持“物理规律 / universal / self-evolution”这类强表述。

### One Discussion Question

只留 1 个真正值得影响实验设计的问题。

---

## 5. 每周复盘

每周只围绕当前研究合同问：

1. Action-head tap 假设变强还是变弱？
2. B1 应预测哪些 measured transitions？
3. B2 哪些 physical constraints 真正可靠？
4. 有没有 stronger matched baseline 必须加入？
5. 哪些变量应该明确后置，避免首轮实验耦合？
6. 下周最便宜的 B0/B1/B2 证伪实验是什么？

---

## 6. 网站维护规则

新论文默认进入 Knowledge Base。

只有当它满足以下情况，才允许修改 Physical Token 主实验：

1. 已经覆盖 B0/B1/B2 的核心 novelty；
2. 证明 action-head tap / transition loss / physics loss 的设计不公平；
3. 给出必须补的 stronger baseline；
4. 给出更简单、更可测的 physical objective；
5. 实验事实直接否定当前领导方案中的某个假设。

否则：归档、引用、用于讨论，但不改当前 Source of Truth。

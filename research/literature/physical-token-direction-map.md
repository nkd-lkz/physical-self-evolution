# Physical Token Research Direction Map

> 日期：2026-09-19  
> 用途：在逐篇精读之前，先建立“这个领域有哪些路线、哪些已经有人做、我们的空间在哪里”的心智地图。  
> 完整125项：[`physical-token-literature-audit-2026-09-19.md`](physical-token-literature-audit-2026-09-19.md)  
> 阅读状态：[`reading-ledger.md`](reading-ledger.md)

## 1. 研究对象先拆清楚

“Physical Token”容易混淆成至少五种不同东西：

1. **Action token / action tokenizer**：描述动作本身；
2. **Dynamics context latent**：描述当前系统/物体如何响应动作；
3. **Future consequence latent**：压缩候选动作会造成的后果；
4. **Constraint / feasibility latent**：描述动作是否物理可行；
5. **Value / failure latent**：描述动作对任务是否有利、是否会失败。

当前最值得验证的是 2–4 的组合，而不是把任意 action token 改名为 Physical Token。

---

## 2. 八条主要文献路线

### A. Action-side representation / compact readout

代表：RLT、FLARE、AGRA、CometVLA、PAR、Spline Policy、SA-VLA。

已经有人做到：

- compact token/readout；
- future latent 对齐；
- action prior token；
- physical token 命名；
- 多种 action representation / tokenizer。

因此我们的增量不能只是：

> “从 action head 取一个 token。”

需要证明：

> action-side feature 在相同 history / data / capacity 下，是否额外保留真实 interaction response，并能迁移到新的 physical condition / head。

### B. Hidden dynamics / history adaptation

代表：UP-OSI、RMA、Manipulator RMA、TACO、TD-MPC/TD-MPC2、DyWA。

已经有人做到：

- 从短 history 隐式辨识 mass / friction / disturbance；
- 学 task-relevant latent dynamics；
- action-conditioned future representation。

必须做的强 baseline：

> **history-only dynamics encoder**

如果它已经解释全部收益，action-head hypothesis 就被削弱。

### C. Force / tactile / multisensory representation

代表：Making Sense、FD-VLA、HapticVLA、MSDP、RoboPack、exUMI、MuSe、DeCAL。

已经有人做到：

- force/tactile teacher；
- multisensory latent；
- 推理时去 privileged sensor；
- actor/critic 非对称读取；
- action-aware tactile representation。

因此不能把“加 contact / force 标签”本身当创新。

更有价值的问题：

> simulator / sensor physics 是否能监督一个 **deployable action-side latent**，并在 sensor 缺失或 dynamics shift 时仍有用？

### D. Analytic physics / constraints / safe control

代表：PIN-WM、ContactNets、LeTO、DDAT、DPCC、CBF 类方法、PhysVLA。

已经有人做到：

- known dynamics prior；
- contact models；
- trajectory constraints；
- runtime action correction；
- safe control。

这里必须区分：

```text
Known physics
FK / limits / robot model
→ analytic module 更合理

Unknown effective physics
friction / compliance / delay / slip
→ learned residual representation 更有意义
```

### E. World / World-Action Models

代表：RepWAM、OA-WAM、Riemann-1.0、RISE、Motus2、DINO-WM、WAM-RL。

已经有人做到：

- action-conditioned future prediction；
- world + action joint latent；
- future → value → policy improvement；
- policy / simulator / evaluator 共享模型。

Physical Token 如果支持 WAM，应把自己定义为：

> **control-facing physical interface**

而不是另造一个更小 world model。

### F. Value / Offline / Online RL

代表：RECAP、LWD、V-GPS、Q-VGM、DSRL、FlowDAgger、IQL/CQL/Cal-QL/RLPD。

关键认识：

> Physical Token 不应和 RLT online actor-critic 绑定。

它可以被：

- action ranking；
- value critic；
- offline advantage learning；
- latent steering；
- online RL；

消费。

更干净的第一步甚至可能是：

> 固定候选动作，只比较 RL Token vs Physical Token 的 action ranking / value calibration。

### G. Execution / failure / recovery / harness

代表：SmoothRL、VLA-Corrector、BCP、GeoAAC、Zeva、Harness VLA、SHAPER、Zetta。

这些工作提醒：

- proposed action ≠ executed action；
- generated chunk ≠ executed chunk；
- retry / replan / chunk 改变本身就会提高成功率；
- context/memory/harness 可以在不改 policy 的情况下变强。

因此首轮 Physical Token 实验必须控制 execution harness，避免把执行系统收益误写成 representation 收益。

### H. Cross-head / cross-embodiment foundations

代表：π0/π0.5、OpenVLA、FAST、Diffusion Policy、ACT、Octo、HPT、X-DiffVLA。

Universal 必须分层定义：

1. 同一种 head 的多个任务；
2. 不同 head 但同机器人；
3. 不同 head + 不同机器人；
4. held-out head / embodiment 少样本或零样本迁移。

“分别训练后都能跑”只能证明兼容，不能证明 universal transfer。

---

## 3. 当前最重要的防撞论文

第一梯队必须优先精读：

- RLT
- FLARE
- Pri4R
- AGRA
- CometVLA
- PAR
- DyWA
- TACO
- RoboPack
- MSDP
- exUMI
- Spline Policy
- LeTO
- V-GPS
- FlowDAgger
- DSRL
- HPT
- GeoAAC

这些论文分别覆盖了 compact token、future supervision、action alignment、physical token命名、hidden dynamics、multisensory representation、constraint layer、value guidance、latent steering 和跨模型接口。

---

## 4. 当前仍值得验证的三个核心 hypothesis

### H1 · Action-side physical sufficiency

在相同 history / proprio / capacity / supervision 下：

```text
action-head feature
vs
backbone feature
vs
history-only feature
vs
action-only feature
```

哪一个更能预测真实 executed-action consequence？

### H2 · Decision relevance

更低的 transition error 不够。

需要继续验证：

```text
better physical representation
→ better candidate ranking / failure prediction / value calibration
→ better control
```

### H3 · Transferability

如果 token 真的是“physical interface”，它应该在：

- new mass / friction / controller delay；
- new task；
- new action head；
- new embodiment；

中的至少一个维度，比普通 feature 更容易适配。

---

## 5. 当前建议的三个实验故事

### Story A · Representation-first

核心问题：

> Action generation feature 是否能形成对真实 interaction consequence 更充分的 compact latent？

优点：最干净、最适合先探索。

### Story B · Physical Critic

冻结 policy / candidate set：

```text
z_phys + candidate action → value / failure / consequence
```

先证明动作评价更好，不让 online RL 收敛问题绑架 representation。

### Story C · WAM-compatible interface

验证同一 physical objective 能否应用于：

- flow action head；
- autoregressive action head；
- WAM action module。

只有前两个故事成立后，再认真主张 Universal。

---

## 6. 和同事分工

### 你负责

- 文献全景与创新边界；
- action-head / physical representation 方案；
- supervision / loss / baseline matrix；
- 每篇 paper note；
- 形成可证伪的 2–3 套方案。

### 真机同事优先确认

- actual q / qdot；
- gripper actual state；
- EEF / object state 的可获得性；
- F/T / tactile；
- timestamps；
- actual applied command；
- controller frequency / delay；
- contact / failure label 可靠性。

真正的方法设计应由**真机可获得的数据合同**反推，而不是从 simulator 能导出什么反推。

---

## 7. 研究判断的更新规则

一篇新论文只有在以下情况才改变方案：

1. 已经覆盖我们准备宣称的 novelty；
2. 给出更简单的强 baseline；
3. 证明 action-head hypothesis 不合理；
4. 暴露 privileged leakage / execution mismatch；
5. 给出可复现、可测量的更优 physical objective。

其他论文继续进入知识库，不每天改变故事。

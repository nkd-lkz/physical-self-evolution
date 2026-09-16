# GPT-6 Astra × RoboDojo：Direct / π0.5 Hybrid / In-Context Adaptation

> 阅读日期：2026-09-16  
> 类型：技术报告 + RoboDojo 相关公众号转述 / 行业解读  
> 项目关系：**Planner / Harness frontier reference；不改变 Gate 0 → B0 → B1 → B2 主线。**

## 0. 领导讨论后的最终定位

领导对这类工作的态度已经明确：

> **主要看别人怎么用 Astra；不要把 Astra 的 planner / zero-shot reasoning 直接拉进当前方法。**

本项目与 Astra-Hybrid 的本质区别是：

```text
Astra Hybrid:
planner / reviewer
    ↓
审核、接受或修正已有 policy proposal

Universal Physical Token:
actor / action-generation head
    ↓
提取通用 compact token
    ↓
transition / physics grounding
    ↓
small online learner
    ↓
最终物理任务成功率提升
```

所以后续阅读 Astra / Harness VLA / SHAPER 的目标主要是：

- 看 planner 如何使用已有 VLA；
- 看 failure / recovery / execution history 如何组织；
- 看什么时候高层 reasoning 有帮助，什么时候物理执行仍是瓶颈。

但当前不把：

- LLM planner；
- zero-shot reasoning；
- memory；
- skill evolution；
- planner-side correction；

并入第一阶段 B0/B1/B2。

---

## 1. 先分清证据等级

今天四篇公众号/材料中，有三篇围绕 GPT-6 Astra 机器人控制：

1. **`GPT 6 Astra as an Embodied Policy` 技术报告与公开代码**：当前最强的一手来源。公开仓库给出了 RoboDojo 10-task subset 的 paired cases、代码、结果与视频。
2. **“重磅发现：GPT-6 Astra实现具身智能突破……”**：二手行业解读。其技术部分大体转述上述报告，但“架构层降维打击”“中国防卫战”等属于评论性表述，不作为科研证据。
3. **“RoboDojo官方实测GPT-6 Astra……”**：二手转述另一组更大规模 RoboDojo Astra 评测。本文记录其中与项目相关的现象，但在锁定该官方报告的一手 URL / artifact 之前，不把文中全部数字升级成已独立核验的 benchmark fact。

因此，本页把“可由公开技术报告直接核验的事实”和“公众号转述但值得跟踪的现象”分开。

---

## 2. 已核验：π0.5 + GPT-6 Astra Hybrid

公开技术报告比较两种闭环控制：

```text
Direct:
RGB + proprio + instruction + history
        ↓
GPT-6 Astra
        ↓
1–5 步 bounded EEF action

Hybrid:
RGB + proprio + instruction
        ↓
π0.5 → 50-step candidate joint trajectory
        ↓
GPT-6 Astra review + execution history
        ↓
accept 1–15 student steps
        OR
bounded 1–5 step EEF correction
        ↓
新观测，再决策
```

RoboDojo 10-task subset、每任务 5 个 paired cases 中：

- `π0.5 + Astra`：48% success，mean Score 62.60；
- `Astra Direct`：26% success，mean Score 37.81；
- Astra 只替换了 14.4% 的 executed control steps，85.6% 仍执行 π0.5 proposal；
- 公开报告还指出 Hybrid 的 recorded token 量比 Direct 少约 44.8%；
- 官方模型的对比数值是对公开 per-task aggregate 的重加权，不是全部同 seed 重新运行，因此不能把它们当严格 paired rerun。

这组结果支持一个清晰分工：

> **general model 更擅长 semantic / goal / progress / anomaly reasoning；task-adapted VLA 提供更成熟的连续动作与物体交互先验。**

但它不证明“LLM + VLA”在所有任务上都优于 Direct。RoboLab 的 10-task zero-shot subset 中，Astra Direct 为 49/50（98%），Hybrid 为 46/50（92%），π0.5 为 18/50（36%）。报告自身给出的边界是：**student action prior 是否适配当前任务很关键**。

---

## 3. 最值得观察的行为机制

### 3.1 Sparse intervention / targeted correction

Hybrid 并不是每一步都由 Astra 重写动作；大部分时间沿用 VLA，只在 observed execution failure 或 next-intent misalignment 时接管。

这说明一种系统范式：

```text
strong prior
    +
small fraction of targeted corrections
```

**但对当前项目，它只是 planner-side / harness-side 参考，不是 Physical Token 的直接实现。**

如果后续要研究 intervention gating，应作为 B0/B1/B2 之后独立的系统变量。

### 3.2 Outcome review 与 next-intent review 分离

技术报告中的 gate 明确分成两个问题：

1. **Last chunk execution outcome**：比较 before / after RGB、measured state、executed gripper command 和 history，判断 progress / failure / uncertainty / recovery；
2. **Next proposal intent**：当前 student chunk 是否仍在追求正确 subgoal、对象、位置、顺序和 grasp/release phase。

这套拆法可以借到**诊断工具**：

```text
before state
+ proposed action
+ actual executed action
+ after state / consequence
→ execution-status card
→ next-intent card
```

但诊断工具不等于方法本体。当前 actor-side Universal Physical Token 仍以 compact representation + physical grounding 为主。

### 3.3 “动作目标”不等于“物理结果”

报告反复强调：

- gripper closed command 不是 grasp success；
- EEF target 不是实际到达；
- FK trajectory 不是 contact/world simulation；
- 模型必须在下一轮通过 RGB + measured state 检查真实结果。

这直接支持当前 Physical Token 的 `actual/executed action → measured consequence` 设计，而不是只学习 policy command。

### 3.4 Chunk-boundary feedback 仍太慢

Hybrid 即使加入强 reasoning，仍有典型失败：chunk 内发生 slip / collision，但 Astra 要等动作片段结束才能看到下一次观测。

因此：

> **强语义 reasoning 不能替代高频 physical feedback。**

这和项目里的 H/C、TOPP、executed-action timing，以及未来 SmoothRL / adaptive execution 方向一致；但这些仍然要在 Gate 0/B0 之后单变量验证。

---

## 4. 公众号转述的大规模 Astra 评测：值得跟踪，但不改项目方法

公众号称另一组 RoboDojo 报告对 GPT-6 Astra 做了更大规模评测，并转述了两个现象：

### 4.1 语义强、精密接触弱

报道将 Astra 的能力地图描述成：

- open / semantic / spatial tasks 较强；
- precision、contact、long-horizon 显著较弱；
- 真机安全性尤其暴露问题。

这和 Hybrid 报告的总体方向一致：**知道目标、识别异常、重新规划**与**稳定抓取、摩擦/碰撞控制、连续接触**仍是不同能力层。

这类现象对当前项目主要提供**问题背景**：物理交互仍是瓶颈；不是告诉我们去做更强 planner。

### 4.2 交互后的 adaptation 值得观察

公众号还转述了坐标反转、镜像视图、屏蔽相机等扰动下，模型会根据“预期动作 vs 实际反馈”的差异调整后续控制。

如果一手报告后续确认，这一点与当前项目的：

```text
command / expected effect
        ↓
actual measured outcome
        ↓
representation / learner adapts
```

有概念上的相邻性。

但仍需保持边界：Astra 的 adaptation 发生在 general-model context/reasoning 层；本项目要验证的是 **actor-side token 是否能吸收并利用这种物理差异**。

另外，**“in-context demonstration 没帮助”不能被外推成“clean500 数据扩充没价值”**。前者是 general model context；后者是 task policy / representation 的 offline training data scaling。

---

## 5. 对 Universal Physical Token 的可借鉴点：只保留 actor-side 相关部分

### Borrow A：Expected vs Actual Transition Mismatch

一个有意义的 Physical Token 应该能描述：

```text
intended / commanded motion
vs
actual executed motion / object consequence
```

这强化 B1 的 measured transition target 设计。

### Borrow B：Failure / Operating-Range Probe 仅作为表示诊断

可在 representation evaluation 中增加：

```text
z_rl or z_physical
    ↓
P(failure onset)
P(base action still valid)
P(local correction may be needed)
```

其用途是回答“这个 token 有没有捕获与最终成功相关的物理状态”，而不是把 planner intervention 作为方法本身。

### Borrow C：Safety Hard Constraint 与 Learned Physics 分开

未来任何 online adaptation / correction 都必须保留：

- joint/action bounds；
- controller feasibility；
- explicit safety filters；
- validation / abort conditions。

这些不能交给 planner reasoning 或 learned physical regularization 替代。

### Borrow D：Base Actor Capability 必须先验收

Hybrid 是否受益强烈依赖 student policy 是否适配任务。这与当前 hammer Gate 0 一致：

> **先证明 frozen actor/reference 有可用闭环能力，再讨论 token / online learner 的增益。**

---

## 6. 当前项目动作

**不改主线，不引入 Astra planner。**

仍然是：

```text
Gate 0 trustworthy actor / baseline
→ B0 matched compact readout
→ B1 + measured transition grounding
→ B2 + valid physics grounding
→ final task success / adaptation gain
```

Astra 相关工作当前只保留：

1. planner / harness frontier observation；
2. failure diagnosis 语言与案例；
3. expected-vs-actual transition mismatch 的启发；
4. future operating-range probe。

RoboDojo 平台线仍按 D3 → D5 → D6/D7 → D8/D9 → D10 的 gate 走，不因为 Astra 报告看起来很强就跳过本地 renderer、native task、schema 与 reference adapter 验收。

---

## 7. Source guardrail

以下内容不进入科研事实层：

- “64% 性能差距 = 架构层降维打击”等媒体化评价；
- “中国必须如何打防卫战”等产业/政策观点；
- 未有一手公开材料支撑的模型参数量、训练 GPU 数、训练数据小时数、资金投入等数字。

这些可以保留为行业观点，但不能作为 Universal Physical Token 的方法动机或实验结论。

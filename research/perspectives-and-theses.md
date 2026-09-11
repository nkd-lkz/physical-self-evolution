# 观点与研究框架：具身 RSI、Physical AI 与分层自进化

> 这部分收录“行业 / 研究者观点 + 我们自己的综合框架”。  
> 它们用于建立长期问题意识，不当作项目实验事实，也不直接改变 Phase 0 主线。

---

## 1. 从“及格”到“可用”

一个很重要的判断是：

> 今天具身模型最大的差距，不一定是“完全不会”，而是从 50–60 分到 99%+ 可靠部署之间的鸿沟。

少量示范、基础 VLA、强视觉语言模型已经可以让机器人：
- 看懂任务；
- 完成粗粒度抓放；
- 在陌生场景获得初始泛化。

但真正部署要求：
- 稳定；
- 能识别自己做错；
- 失败后能恢复；
- 能把失败经验留下；
- 下一次明显变好。

所以“自进化”最关键的价值不是炫技式自动写代码，而是：

> **把失败和真实执行后果变成下一轮能力。**

---

## 2. SeeAct / 具身 RSI 观点：三套基础系统

从此前整理的访谈观点，可以把具身 RSI 抽象成：

### World Engine

负责产生经验：
- 真机；
- simulation；
- world model；
- real-to-sim / sim-to-real。

核心不是具体形式，而是：

> 能否低成本、可扩展地产生大量有价值 rollout？

### Evaluator / Reward Model

负责判断经验：
- 是否成功；
- 进展到哪里；
- 从哪一步开始失败；
- 哪个 correction 更好；
- 是否值得写入长期记忆 / 数据库。

### RL / Policy Base

负责把经验变成能力：
- Online RL；
- residual adaptation；
- VLA fine-tuning；
- distillation；
- skill consolidation。

一句话：

> **World Engine 产生经验，Evaluator 判断经验，Learning System 把经验变能力。**

---

## 3. 能力拓展自顶向下，能力增强自底向上

### Top-down Capability Expansion

上层 Agent 面对更复杂任务：

\`\`\`
Long-horizon Task
↓
Task Decomposition
↓
发现现有 Skill 不够
↓
提出新的学习需求
\`\`\`

### Bottom-up Capability Improvement

底层：
- 自主探索；
- 收集 failure / recovery；
- reward；
- RL / skill learning；
- 验证；
- 能力升级。

然后：

\`\`\`
更强 Skill
↓
上层可以少拆任务
↓
解决更长程问题
\`\`\`

这是一个循环，而不是 Agent 和 VLA 二选一。

---

## 4. 为什么 Harness 不会因为 Foundation Model 变强就消失？

机器人和软件 Agent 最大区别：

> 软件失败通常可以 Undo；物理失败会改变世界。

所以机器人 Harness 至少需要管理：

- Tool
- Skill
- State
- Memory
- Permission
- Verification
- Recovery
- Safety
- Compute
- Communication
- Controller handoff

模型越强，Harness 可能更薄，但不会归零。

---

## 5. 一个重要的系统分层

长期机器人系统可能是：

\`\`\`
General Foundation Model / Agent
语言 · 常识 · 规划 · Code · Reflection
        ↓
Memory / ICL
环境适应 · 历史 · interaction memory
        ↓
Harness / Runtime
Tool · Skill · State · Verifier · Recovery · Safety
        ↓
VLA / WAM / RL Policy
快速 sensorimotor control · contact-rich manipulation
        ↓
Controller / Hardware
IK · WBC · Force Control · Collision · 毫秒级闭环
\`\`\`

这个图不是当前项目架构，而是知识地图。

---

## 6. Agent、VLA、WAM、RL 谁会赢？

更合理的问题不是“谁替代谁”，而是：

> 不同时间尺度需要什么智能？

### Agent / System 2

擅长：
- 任务理解；
- 规划；
- 长上下文；
- code；
- reflection；
- tool selection。

### VLA / System 1

擅长：
- 快速；
- 连续；
- 局部；
- 高维 sensorimotor control。

### WAM / World Model

擅长：
- Action → future consequence；
- dynamics；
- planning prior；
- counterfactual evaluation。

### RL

擅长：
- 从真实 reward / failure / feedback 中把“哪种做法更好”写回策略。

因此更像：

> **Agent 负责想，Harness 负责组织，ICL 负责快速适应，WAM 负责理解后果，VLA 负责做，RL 负责让它越做越好。**

---

## 7. 四种“自进化”必须分开

### Level 1 · Context Evolution

参数不变。

通过：
- ICL；
- memory；
- history；
- causal interaction。

代表：
- Zeva。

### Level 2 · Skill / Harness Evolution

模型参数可以不变。

更新：
- code；
- skills；
- recovery；
- verifier；
- runtime critic。

代表：
- Harness VLA；
- SHAPER；
- ASPIRE；
- Zetta。

### Level 3 · Policy Evolution

用真实部署数据更新：
- actor；
- critic；
- flow action expert；
- VLA policy。

代表：
- RLT；
- Q-VGM；
- SmoothRL；
- RedFlow 等。

### Level 4 · Foundation Evolution

把多个任务 / 本体的 Physical Experience 写回下一代 generalist model。

代表：
- PLD；
- Learning While Deploying。

---

## 8. Fast Memory + Slow RL

这是当前长期最值得保留的一个研究问题：

\`\`\`
刚刚发生的 Interaction
        ↓
Fast Memory / Context
秒–分钟级适应
        ↓
经过验证的高价值经验
        ↓
Replay / RL
分钟–小时级更新
        ↓
跨任务稳定经验
        ↓
Foundation Consolidation
小时–天级写回
\`\`\`

关键研究问题：

- 经验何时只需要记忆？
- 何时值得更新 policy？
- 何时值得写回 foundation model？
- 谁来判断“这条经验值得长期保存”？

---

## 9. 单机器人为什么最终不够？

单个机器人可以：
- 自己试；
- 自己改；
- 自己学。

但真正的通用智能需要：

> 机器人 A 踩过的坑，机器人 B 不应该重新踩一遍。

长期要解决：

\`\`\`
Individual Physical Experience
↓
Representation / Validation
↓
Shared Experience
↓
Cross-task / Cross-embodiment Reuse
\`\`\`

这才是 “Experience Scaling”。

---

## 10. 我们自己的长期综合判断

可以用一个乘法式理解：

**Robot Intelligence ≈**

**General Reasoning  
× Physical World Model  
× Fast Policy  
× Memory / ICL  
× Harness  
× RL Data Flywheel**

任何一层长期接近 0，系统都会失效。

但科研不能一次同时优化所有项。

当前项目只抓住最可验证的一段：

\`\`\`
Foundation VLA
+
Online Physical Experience
+
Lightweight RL
↓
Does the robot actually improve?
\`\`\`

先回答这个，再扩到其它层。

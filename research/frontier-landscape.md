# 具身智能自进化前沿工作地图：别人正在做什么，我们能借什么

> 更新：2026-09-11  
> 定位：这是 **知识库 / 灵感地图**，不是当前项目 Roadmap。  
> 当前项目主线仍然是 **Phase 0 — RLT Multi-task Benchmark**。新论文先进入这里，只有实验或强近邻证据足以改变判断时，才进入主线。



## 2026-09-21 追加：XPACE 与 EmbodiedJev

[XPACE](../notes/xpace.md)提供恢复数据构造与监督分流的参考；[EmbodiedJev](../notes/embodied-jev.md)提供模型选择、程序控制和物理判定分离的实例。两项均已核验一手材料，未独立复现。

对当前RLT主线，优先验证部署可得的紧凑表示能否识别可恢复接触偏差，再比较同预算随机/定向恢复数据。可恢复性依赖参考策略、控制器与后续预算；若只预测成功概率，其角色接近value，不能靠命名宣称物理创新。完整[问题定义与五组实验](xpace-jev-rlt-ideas.md)属于候选提案，不改当前实验事实。

## 2026-09-21 增量：ForceDelta-VLA 与 RPent

此次更新属于知识库；以下是研究分析与待验证实验，不是实验结果或主线切换。

| 新工作 | 核心机制与证据来源 | 对当前研究的具体影响 |
|---|---|---|
| [ForceDelta-VLA](https://arxiv.org/html/2609.18242v1) | 教师成对预测差监督力修正，另建延迟补偿；九项真机实验 | 强近邻：增加同传感器、同历史、同容量、同时序对照；区分教师差与实测后果 |
| [RPent](https://github.com/RLinf/RPent) | Planner/技能/环境/持久记忆；关联已有Harness VLA | 系统层：探索与评测分离；当前文档仅LIBERO支持Exploration，不用RoboTwin榜单证明持续学习 |

完整专题：[ForceDelta-VLA](../notes/forcedelta-vla.md)、[RPent](../notes/rpent.md)。ForceDelta-VLA 不等于 FD-VLA（2602.02142）；RPent 是系统条目，不重复算作另一篇 Harness VLA。

候选科学问题进一步收敛为：**相同观测历史、参考策略、容量与执行时序下，真实动作后果监督的紧凑状态能否降低接触条件变化后的在线适应成本？** 先做时序/感知归因，再做后果监督与冻结更新对照，最后才检验新任务适应及旧任务保留。

---

## 0. 为什么要单独维护这张地图？

具身“自进化”已经不是单一路线。现在可以看到至少七种不同的能力改进回路：

1. **Policy Evolution**：直接用 RL / value 更新策略。
2. **Failure & Recovery Evolution**：把失败变成 correction / recovery 数据。
3. **Physical Representation Evolution**：让策略表示更多未来几何、力、触觉或动作后果。
4. **Context / Memory Evolution**：权重不变，通过部署时 memory / ICL 变强。
5. **Harness / Skill Evolution**：模型不一定更新，外部 skill、critic、code、tool orchestration 持续升级。
6. **Execution / Runtime Evolution**：自适应 chunk、replan、async credit assignment，让“执行方式”本身变聪明。
7. **Foundation / Fleet Evolution**：把多机器人、多任务的部署经验重新写回 generalist foundation policy。

这些路线不是互斥的。更像不同时间尺度：

\`\`\`
毫秒–秒       Controller / execution
秒–分钟       Context / runtime critic / correction
分钟–小时     Online RL / residual adaptation
小时–天       Skill / harness / policy consolidation
天–更长       Fleet / foundation model update
\`\`\`

对我们的意义：**不要把“自进化”压缩成一个新 token 或一个新 RL loss。**

---

# 1. Policy Evolution：直接让动作策略从部署经验变强

## 1.1 RLT：冻结大模型，让小策略在线学

**RL Token: Bootstrapping Online RL with Vision-Language-Action Models**

核心思想：

- 大 VLA 保留预训练能力；
- 学一个紧凑 RL representation；
- 轻量 actor / critic 看 VLA reference action；
- Online RL 只更新小网络。

最重要的范式不是“RL Token”名字，而是：

> **Foundation Prior + Lightweight Online Specialist**

对我们最直接，因为当前 Phase 0 就以它为 baseline。

**可借鉴：**
- 冻结范围；
- reference-conditioned actor；
- action chunk 作为 RL 决策单元；
- replay；
- BC / action anchor；
- critical phase / full-task 比较。

**不能直接假设：**
- RLT 失败 = representation 不懂 physics；
- 任何 residual actor 都等于原论文 RLT。

---

## 1.2 SERL：真正的机器人 RL 是一整套系统

**SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning**

SERL 的意义不是某个新 loss，而是提醒研究者：

> reward、reset、controller、demo、human intervention、replay、learner、logging，任何一个地方做错，机器人 RL 都可能失效。

作者在 PCB 插装、线缆布线、物体搬运等真实任务上报告约 25–50 分钟即可学出高成功率策略。

对我们 Phase 0 的启示：

- 多任务 benchmark 的工程稳定性与算法同样重要；
- “能启动训练”远远不等于 baseline；
- intervention / recovery 数据值得从一开始纳入 schema；
- episode-level raw metrics 和失败视频必须保存。

---

## 1.3 Q-VGM：不再只训练小 actor，而是让 Flow VLA 本体吃 Q-gradient

**Q-VGM: Q-Guided Value-Gradient Matching for Flow-Matching VLA Policies**

Flow-matching VLA 的困难：

- 没有传统 Gaussian policy 那么方便的 log-prob；
- 直接通过多步 denoising / ODE solver 反传 Q 容易不稳定。

Q-VGM 把 critic 的 value gradient 转成 denoising-time gradient field，从而更新 flow policy。

作者报告：
- LIBERO：75.0% → 92.5%
- RoboTwin 2.0：76.4% → 87.2%
- 两个真机 tabletop tasks：40.0% → 67.5%

对我们最有意思的是：

> 它的 critic 仍然使用 compact RLT features。

也就是说未来可以形成两层问题：

1. RLT compact state 是否有价值？
2. 改进动作的载体应该是 lightweight actor，还是直接回写 flow action expert？

当前阶段不急着选第二条。先让 RLT baseline 给出瓶颈证据。

---

# 2. Failure / Recovery：失败不是废数据，而是最高价值的数据源

## 2.1 FailSafe：系统性地产生 failure-action pairs

传统 imitation datasets 大量是成功轨迹。

问题是：

> 机器人真正部署时最稀缺的不是“再看一次正确动作”，而是“我刚才为什么失败，以及下一步怎么恢复”。

FailSafe 自动构造失败案例和可执行恢复动作，并训练 failure-aware reasoning / recovery 支持模块。

**可借鉴：**
- failure taxonomy；
- failure generation；
- recovery action pairing；
- 对不同空间、视角、本体泛化的检查。

这与我们的 D4 非常一致：

> 普通 expert 数据 vs failure / near-failure / recovery 数据，哪一种更值钱？

---

## 2.2 RedFlow：把失败直接改写成 action-level correction

RedFlow 更进一步，不满足于：

> “这次失败了。”

而是试图回答：

> “这个动作具体应该怎么改？”

这条路线和我们未来的 Correction Benefit / action consequence 很接近。

如果后面做 failure-driven learning，应重点比较：

- binary failure label；
- progress / severity；
- action-level correction；
- correction benefit；
- recovery trajectory。

这些监督粒度到底谁最值钱。

---

## 2.3 RL²-VLA：不是每一步都纠正，而是先学“什么时候需要 steering”

很多 correction 系统容易遇到：

> correction 本身也会犯错。

RL²-VLA 的重要思想是 **adaptive steering**：
- base policy 可能失败时才触发；
- 尤其面向 OOD；
- 不修改原 VLA，靠 latent compositional steering。

这对应我们的 R2：

> “纠偏是否值得发生”本身也是一个学习问题。

---

# 3. Physical Representation：物理信息到底应该进入哪里？

这是最容易“想法很多、证据很少”的区域。

## 3.1 Pri4R：未来几何 supervision

Pri4R 使用训练期 privileged future 3D/4D geometry / trajectories 塑造 VLA 表征，部署时移除 privileged input。

它直接占掉了一部分“Physical Token”创新空间：

> 不能再简单说“给 VLA 增加物理监督”。

必须问：
- 为什么这个 target 是 decision-relevant？
- 它比 future geometry / future latent 多了什么？
- 是否真的改善 online adaptation，而不仅仅是 offline representation？

---

## 3.2 PHR-VLA：普通 future latent 可能已经很强

PHR-VLA 让我们必须设置一个重要 baseline：

> **普通未来视觉 / latent prediction。**

如果：
- future latent 已经提供大部分收益，
- 显式 contact / physics 标签没有额外增益，

那么 Physical Representation 的故事会变弱。

所以 D3 不能只有：
- reconstruction
- physical consequence

还应该有：
- generic future latent。

---

## 3.3 FD-VLA / HapticVLA：训练时用力 / 触觉，部署时不用

这两类工作共同说明：

> Privileged physical sensing 可以作为 teacher，而不一定成为部署输入。

对我们已有 physics sidecar 很关键。

sidecar 有三种不同用途：

1. **Logging / Diagnosis**
2. **Critic / Value privileged input**
3. **Representation distillation target**

不要一上来就把所有字段 concat 给 actor。

---

## 3.4 MSDP：actor 和 critic 不一定应该看同样的信息

MSDP 在 contact-rich RL 中使用 vision / force / proprioception 的 multisensory pretraining，并设计 asymmetric actor/critic readout。

这给我们一个强问题：

> 物理信息为什么一定要进 actor？

可能更好的路径是：

\`\`\`
Actor:
部署可观测的稳定状态

Critic / Teacher:
更多 privileged physics
\`\`\`

然后再把价值或表征蒸馏回可部署策略。

这与经典 Asymmetric Actor Critic 的思想一致。

---

# 4. World Model：从“预测未来”到“预测与任务有关的后果”

## 4.1 SR-WM：不是预测像素，而是预测角色、关系和 phase

**Beyond Instance Slots / SR-WM**

它把任务状态拆成：

- gripper
- target
- goal
- relation
- phase

再预测：
- grasp / contact
- relation preservation
- fixture state
- phase change

真正值得我们借鉴的是：

> World model 的目标不是“把未来画出来”，而是给 decision making 一个 action-sensitive interface。

所以如果 Phase 2 最终做 consequence model，我们更应该问：

> 哪些 future events 能改变 action ranking？

而不是追求完整视频预测。

---

## 4.2 PIN-WM：显式 physics-informed world model

PIN-WM 是另一端：

- 更明确的 physics prior；
- system identification；
- non-prehensile dynamics。

它提醒我们，如果以后声称“Physical World Model”，必须明确：
- 物理约束是什么？
- 参数是否可辨识？
- 如何影响 planning？
- 与普通 latent dynamics 的差别？

当前阶段不需要完整 WAM / world model。

先证明局部 consequence signal 的价值。

---

# 5. Context / Memory Evolution：不更新权重也可以“越做越好”

## 5.1 Zeva：Action → State Change 变成 Causal Memory

Zeva 的核心不是普通 history。

它明确把：

\`\`\`
Executed Action
      +
Observed State Change
      ↓
Causal Interaction Signal
\`\`\`

写入双时间尺度 memory。

它提出了非常重要的自进化分层：

### Fast Adaptation
Memory / Context 更新。

### Slow Adaptation
Policy / weight 更新。

对我们的长期路线可写成：

\`\`\`
Fast Memory
   +
Slow RL
\`\`\`

未来值得研究：
- 哪些经验只需要临时记？
- 哪些经验应该进入 replay？
- 哪些经验值得最终写回 foundation model？

---

## 5.2 Rapid Motor Adaptation：history 本身就是物理传感器

Rapid Motor Adaptation for Manipulator Arms 说明：

> 如果某些动力学变量不可直接观察，可以从短 interaction history 中推断。

这非常重要，因为很多“需要 physics token”的问题，可能其实是：

> 你的 policy 只有当前帧，根本没有观察到执行偏差。

所以 D1 应永远排在复杂 representation 前面：

\`\`\`
command only
vs
actual proprio
vs
short history
\`\`\`

---

# 6. Execution / Runtime：模型能力没变，但系统可以更聪明地执行

## 6.1 VLA-Corrector：open-loop action chunk 的盲区

Action chunk 很高效，但问题是：

> chunk 执行期间世界已经变了，policy 还在按旧计划走。

VLA-Corrector 用轻量 detect-and-correct 路径，在必要时中断 / 纠正。

对我们：
- D5 的直接 baseline；
- 不必一看到反馈慢就立刻上复杂 online RL；
- inference-time correction 可能已经解决大部分问题。

---

## 6.2 BCP：学习“继续执行还是重新规划”

固定 C 是非常粗糙的设计。

BCP 把它改成：

\`\`\`
Continue?
or
Replan?
\`\`\`

并同时优化成功率和 VLA 调用成本。

这意味着未来我们的 action chunk 实验不应该只比较：

- C=1
- C=5
- C=10

还应该问：

> 能否让 horizon 本身变成 learned decision？

---

## 6.3 SmoothRL：异步以后，RL transition 定义都会变

异步系统里：

\`\`\`
generated action ≠ executed action
\`\`\`

一个 chunk 有：
- committed
- execution
- discarded

因此：
- Critic 必须知道真实作用于环境的 action sequence；
- Actor 不能为从未执行的 action 接收 value gradient。

这说明：

> 异步不是把 inference 放到另一个线程就完了。

一旦进入 async，算法定义本身也要跟 deployment timing 对齐。

---

## 6.4 Strict Streaming RL：最后再讨论

普通 Online RL 可以：
- replay；
- minibatch；
- delayed update。

Strict Streaming RL 更接近：
- 每条 transition 到来就处理；
- batch size≈1；
- 不依赖 replay。

当前没有理由为了“更像自进化”而删除 replay。

只有当：
- replay memory；
- batch update；
- learner latency；
- continual stream

真的成为瓶颈，再进入 Streaming 路线。

---

# 7. Harness / Skill / Agent Evolution：模型不变，系统也能持续长能力

## 7.1 Harness VLA：把 VLA 当成可验证 primitive

核心观点：

> VLA 不一定要负责完整任务，它可以只是一个 contact-rich primitive。

外面还有：
- grounding
- staging
- transport
- release
- success verification
- retry / recovery

Harness 学的是：
- 这个 primitive 在什么 operating range 靠谱？
- 什么时候应该调用？
- 什么时候应该重试？

对我们最关键的区分：

### Primitive Failure
底层控制本身不行。

### Orchestration Failure
调用 / 阶段 / 状态管理不行。

Phase 0/1 先把这两类 failure 分开。

---

## 7.2 SHAPER：演化外部 skill + harness，而不是权重

SHAPER 保持 foundation model frozen，通过 rollout 优化：
- reusable skills
- context-code harness

它代表：

> **Non-parametric Self-Evolution**

这条线和 RL 并不冲突。

长期可以是：

\`\`\`
Parametric:
RL / fine-tuning

Non-parametric:
Memory / skills / harness
\`\`\`

---

## 7.3 ASPIRE：把“训练”重新定义成 skill refinement

ASPIRE 的一句话很有启发：

> Trained model 不一定是一堆 weights，也可以是一套越来越可靠的 skill repository。

循环：

\`\`\`
Execute
↓
Failure Trace
↓
Local Code Repair
↓
Re-run
↓
Validate
↓
Save Skill
\`\`\`

非常值得借的是：
- failure attribution；
- localized repair；
- validation before consolidation；
- reusable skill。

不值得照搬的是：
- 用代码替代高频 contact control。

---

## 7.4 Zetta：三个时间尺度的 Harness Self-Evolution

Zetta 非常接近“系统化自进化”：

### 高频
runtime critic / governance

### rollout 级
failure → critic / recovery proposal

### skill 更新级
只有通过 validation 才写入 skill

作者报告：
- LIBERO-Pro 90.8%
- RoboCasa 93.6%
- 11.1× inference speedup

对我们的长期启发：

> **Experience 必须经过 validation gate，才能进入长期能力库。**

未来不仅 skill 如此，RLT replay / distillation 也可以问：
- 哪些经验值得长期保留？
- 哪些只是偶然成功？
- 哪些会造成 catastrophic forgetting？

---

## 7.5 ENPIRE：Coding Agent 参与“研究 / 训练闭环”

ENPIRE 的重点不只是 Agent 控机器人。

而是 Agent 参与：

\`\`\`
Reset
→ Rollout
→ Verify
→ Inspect Logs
→ Modify Code / Training Recipe
→ Retry
\`\`\`

这非常接近未来的：

> Autonomous Robotics Research Harness

对我们而言，不是当前要替代算法研究，而是未来可以把：
- experiment log
- failure videos
- config
- training scripts
- evaluation
- hypothesis table

都接入 Agent，让它自动执行低风险科研循环。

---

# 8. Foundation / Fleet Evolution：真正的数据飞轮

## 8.1 PLD：RL specialist 只是经验生成器

一条很重要的思想变化：

过去：

> RL = 得到一个更强 specialist

未来：

> RL = 在部署分布中产生 foundation model 最缺的新经验

然后：
- collect
- filter
- distill
- merge

这就是 Policy Evolution → Foundation Evolution。

---

## 8.2 Learning While Deploying：机器人 fleet 共享经验

LWD 把这个概念放大：

\`\`\`
16 Robots
↓
Autonomous Rollouts + Human Interventions
↓
Shared Experience
↓
Offline-to-Online RL
↓
Single Generalist VLA
↓
Redeploy
\`\`\`

作者在 8 个真实任务上报告最终平均成功率 95%。

这非常接近我们长期想讲的：

**Physical Experience Flywheel**

但我们现在应该做的是它的最小版本：

\`\`\`
1 task / few tasks
↓
RLT adaptation
↓
failure / recovery experience
↓
independent evaluation
\`\`\`

先把这个闭环做对，再谈 fleet。

---

# 9. 一张统一地图：到底“更新了什么”？

| 路线 | 更新对象 | 典型工作 | 时间尺度 | 最适合解决 |
|---|---|---|---|---|
| Context Evolution | Memory / Context | Zeva | 秒–分钟 | 新环境快速适应 |
| Runtime Evolution | Horizon / Corrector / Critic | VLA-Corrector, BCP, SmoothRL | 毫秒–秒 | feedback / latency / chunk |
| Policy Evolution | Actor / Critic / Flow Policy | RLT, SERL, Q-VGM | 分钟–小时 | 局部技能改进 |
| Failure Evolution | Corrective dataset / recovery | FailSafe, RedFlow, RL²-VLA | episode–小时 | long-tail failure |
| Representation Evolution | latent / physics features | Pri4R, FD-VLA, MSDP | 训练阶段 | physical observability |
| World Evolution | dynamics / consequence model | SR-WM, PIN-WM | planning / training | action consequence |
| Harness Evolution | Skills / Code / Recovery logic | Harness VLA, SHAPER, ASPIRE, Zetta | episode–天 | orchestration / reliability |
| Agentic Evolution | Training / experiment loop | ENPIRE | 实验周期 | 自动科研 / policy improvement |
| Foundation Evolution | Generalist VLA weights | PLD, LWD | 小时–周 | 经验规模化复用 |

---

# 10. 对我们当前项目最重要的“不要被带偏”规则

## 规则 A：Phase 0 不因为新论文而改变

当前：
- RoboTwin2
- Multi-task RLT
- Reference
- Evaluation
- Logging

先做稳。

## 规则 B：每篇论文必须被压成“项目动作”

只有四种合法结果：

1. **Add baseline**
2. **Add ablation**
3. **Add diagnosis**
4. **Archive / no action**

不能因为论文看起来酷就新增一个模块。

## 规则 C：把新工作放进“更新对象”坐标系

看到任何新论文先问：

> 它到底让什么发生了变化？

- weights？
- memory？
- skills？
- action horizon？
- critic？
- data？
- world model？
- training code？

这样不会被“Self-Evolving”标题迷惑。

---

# 11. 当前最值得持续跟踪的 12 篇

如果时间有限，优先：

1. RLT
2. SERL
3. SmoothRL
4. Q-VGM
5. PLD
6. RedFlow
7. Zeva
8. Pri4R
9. V-GPS
10. Harness VLA
11. Zetta
12. Learning While Deploying

它们基本覆盖：
- baseline
- online RL
- execution
- value
- failure
- memory
- physical representation
- harness
- fleet / foundation evolution

---

# 12. 这张知识库应该怎么长期长大？

每次新增工作，统一记录：

\`\`\`
Title
Year
Layer
What changes?
What feedback?
Timescale?
Core mechanism
Main evidence
What can we borrow?
What does it NOT solve?
Which project phase is it relevant to?
Read / To-read / Archived
\`\`\`

这样网站会越来越像一个：

> **Embodied Self-Evolution Research Index + Decision Memory**

而不是简单收藏夹。

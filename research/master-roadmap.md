# 面向物理交互的机器人自我改进：研究总路线

> 版本：2026-09-11  
> 用途：项目主线、实验协议、论文边界与滚动计划的统一文档。

## 0. 核心结论

当前项目不再以“Physical Token / RL Token 改造”为上位故事，而采用：

**Physical Interaction + Self-Improvement**

RLT 是当前最合适的轻量 Online RL baseline / scaffold，不是最终研究叙事。

真正要回答的是：

> 在固定或主要固定基础 VLA 时，哪些 Physical Experience、数据选择和轻量更新机制，能让机器人在接触密集、精细操作和动力学变化下，用较少真实交互持续改善策略？

研究方法采用：

**Baseline → Diagnose → Small Hypothesis Test → Multi-task / OOD → Self-Improvement Loop → Real Robot**

任何候选方向只有得到上一阶段证据后才升级。

---

## 1. 当前项目状态

### 已有工程资产

- RoboTwin `beat_block_hammer` 基础环境已打通。
- 三相机、14D observation/action interface 已有。
- 50 条成功 expert episodes。
- 7,884 LeRobot transitions。
- physics sidecar / contact / grasp 等辅助数据已记录。
- π0.5 SFT 5k / 10k / 15k / 20k checkpoints 已生成。

### 仍未完成

- Reference checkpoint 的正式选择与独立评估。
- 论文语义清晰的 RLT-π0.5-adapted baseline。
- 多任务 RoboTwin / RoboTwin2 benchmark。
- RoboDojo Dojo-Eval / Dojo-RL。
- Physical Token、Streaming、WAM 等均仍是候选，不是已验证结果。

---

## 2. RLT 在项目中的正确定位

把 RLT 抽象成：

```
Frozen Foundation Policy
        ↓
Compact State Interface
        ↓
Lightweight Actor / Critic
        ↓
Online Physical Experience
        ↓
Policy Improvement
```

我们未来可以改 State Interface、Critic、Actor、Data、Execution Schedule、Replay、Distillation，但不应把“RL Token”本身当成总故事。

### 两类 baseline 必须分开

#### RLT-π0.5-adapted

尽量保留原论文：
- compact readout；
- reference-conditioned actor；
- action anchoring；
- reference dropout；
- chunk-level TD。

只做基础模型和环境适配。

#### Local-Residual

本地 residual actor、K=1、特定 switch 等工程变体。

可用于 bring-up，但必须独立命名，不能声称是原论文忠实复现。

---

## 3. Baseline Contract

任何实验前，必须记录：

1. 基础模型 checkpoint 和 SFT 数据。
2. compact readout 来自哪层。
3. Stage 1 / Stage 2 哪些参数更新或冻结。
4. Actor 输出完整 chunk 还是 residual。
5. Critic input / target / TD backup。
6. VLA horizon H、execution chunk C、control frequency。
7. replay 存计划 action 还是 executed action。
8. reward / terminal / timeout。
9. critical phase / policy switch 逻辑。
10. train/eval seeds 与预算单位。

Baseline 完成不等于“程序能跑”。至少需要：
- Reference 与 RLT 独立评估；
- learning curve；
- 固定 train/eval seeds；
- checkpoint/config 可恢复；
- episode-level raw metrics；
- 失败视频；
- 没有未解释的 action/timing/input 差异。

---

## 4. 双环境定位

### RoboTwin / RoboTwin2

主要负责：
- Online RLT 开发；
- 大规模多 seed；
- branch rollout；
- privileged sidecar；
- debugging；
- dynamics randomization。

任务按物理机制扩展：
- hammer：tool / impact；
- click_bell：point contact；
- insertion：precision / constrained contact；
- push / articulated：sustained contact。

### RoboDojo

拆成两层：

#### Dojo-Eval
- policy loading；
- observation/action contract；
- 完整 episode；
- 可重复 evaluation。

#### Dojo-RL
- stable reset/step；
- transition-level data；
- reward/termination；
- learner update；
- policy weight sync；
- training-time evaluation。

Dojo-Eval 不是 Online RL 已接通。

---

## 5. 诊断优先于方法

Baseline 失败后先做 D1–D5。

### D1 · Input / History

比较：
- command target；
- + actual q；
- + short history。

问：缺的是 physics，还是 observability？

### D2 · Candidate Headroom

同一个 state 执行：
- base action；
- 少量合法 candidate correction。

后续 policy 固定。

问：Reference 附近到底有没有可利用的 improvement headroom？

### D3 · Supervision Purpose

控制 feature / data / capacity，比较：
- reconstruction；
- future latent；
- physical consequence；
- correction benefit。

问：physics 最适合进入 representation、value 还是 correction？

### D4 · Data Coverage

相同新增预算：
- 普通 expert；
- failure / near-failure / recovery。

问：改进来自算法，还是来自失败附近的数据覆盖？

### D5 · Execution Horizon

固定 C=1/5/10，记录：
- control frequency；
- VLA calls；
- actual executed action span。

问：是不是 action chunk 太长、反馈太慢？

---

## 6. 候选路线

### R0 · Action Consequence

如果 D3 显示 action-effect supervision 明显改善 decision-relevant representation，再升级。

### R1 · Value-Oriented Physics

如果 D2 显示 candidate set 中已有明显更优动作，研究 physics-informed critic / value teacher。

### R2 · Correction Benefit

如果存在 correction headroom，但误介入较多，学习“是否值得纠偏 / 哪种纠偏更好”。

### R3 · Execution History

如果 D1 的 actual q + short history 带来主要增益，优先做 execution-aware observer / policy。

### R4 · Failure Recovery Data

如果 D4 显示 recovery data 是主要增益来源，转向 failure-driven experience flywheel。

### R5 · Adaptive Execution

如果 D5 的短 C 显著改善，优先研究 adaptive chunk / async correction。

### R6–R9

结构化 residual、contact-aware replay、actor/critic split、future event features，均作为二级候选。

---

## 7. Self-Improvement Protocol

### Context Adaptation

参数不更新，只改变 Memory / Context。

代表：Zeva。

### Online Policy Adaptation

更新轻量 actor / critic / readout。

代表：RLT / SmoothRL。

### Experience Consolidation

把验证过的新经验写回基础 VLA，并检查旧能力保持。

代表：PLD。

### 最小多轮协议

1. 冻结 task set、开发条件、final test 和总交互预算。
2. Round 0 保存基础策略和独立评估。
3. 每轮各方法获得相同新增交互预算。
4. 记录 success / failure / recovery / human intervention。
5. 更新后在本轮未参与训练的 initial states 上独立评估。
6. 至少观察数轮，并每轮回测旧任务 / 旧 dynamics。

核心指标：
- 每单位新增交互收益；
- recovery success；
- invalid intervention；
- old-skill retention；
- human / data / compute cost。

---

## 8. 远期模块的触发条件

- Shared representation：至少两个任务出现同类表示增益。
- Distill back to VLA：轻量 adaptation 已经产生稳定高质量 recovery data。
- Strict streaming RL：replay / storage / update delay 变成真实瓶颈。
- Full WAM：局部 consequence prediction 已证明 long-horizon prediction 必要。
- Agent / skill evolution：失败主要来自 task decomposition / skill orchestration，而不是局部控制。

---

## 9. 近期行动

### P0
评估 hammer SFT checkpoints。

产物：
- success；
- 阶段画像；
- 失败视频；
- checkpoint selection 记录。

### P1
审计 RLT 与本地实现差异，完成首任务 baseline。

### P2
加入第二个 RoboTwin contact task。

### P3
完成 RoboDojo Dojo-Eval。

### P4
补 Dojo-RL 最小闭环。

### P5
从 failure profile 中选择 D1–D5 的 1–2 个最便宜实验。

---

## 10. 每日论文阅读的角色

论文不是 roadmap。

每篇论文固定回答：
1. 它解决什么问题？
2. 核心方法是什么？
3. 最重要证据是什么？
4. 它占掉我们哪块创新空间？
5. 它是否需要改变当前 baseline / 对照 / 诊断？

如果答案是“没有”，就归档，不改主线。

---

## 11. 长期 North Star

**Physical Experience Flywheel**

```
Deploy
  ↓
Experience
  ↓
Evaluate
  ↓
Learn
  ↓
Redeploy
  ↓
Consolidate
  ↓
Share
```

最终目标不是单个机器人不断重新试错，而是让一个本体自主纠错产生的经验，能够被后续任务、后续本体和下一代 foundation policy 复用。

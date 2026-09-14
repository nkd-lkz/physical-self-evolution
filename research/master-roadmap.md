# Universal Physical Token：研究总路线

> 版本：2026-09-14  
> 当前状态：**领导约束后的新主线**  
> 主规范：[`physical-token-leadership-spec.md`](physical-token-leadership-spec.md)

---

## 0. 主线纠正

此前 Research OS 将项目扩展成“RLT Multi-task Benchmark → Failure Diagnosis → Physical Experience → Self-Improvement”的宽泛四阶段路线。

该结构现在降级为**历史探索框架**，不再作为当前实验主规范。

当前项目严格收敛到：

> **Universal Physical Token for Robot Self-Evolution**

核心问题：

> **能否从已有 action model 的 action-generation head 读出一个紧凑 token，并通过 measured transition prediction 与有效 physics constraints 对它进行 grounding，使冻结 action model 在变化的接触动力学下通过小型在线 learner 持续适应？**

这一定义优先于此前由 AI 辅助发散出的 Physical Experience / World Model / Harness / Fleet 等宽泛主线。那些内容保留在知识库作为 related work 与备选方向。

---

## 1. 核心结构

```text
Frozen Backbone / Perception
          ↓
Frozen Action Head
          ↓
Pre-output features F_t^head
          +
Robot history h_t
(state + actual/executed actions)
          +
Robot metadata r
          ↓
Model adapter A_m + learned readout E_phi
          ↓
Physical Token z_t  (fixed K × d)
          ↓
Small online actor / critic
          ↓
Adapted action
```

当前 Physical Token 的研究对象是 **action-head readout**，不是一个泛化的“大世界模型”。

---

## 2. Universal 的严格边界

“Universal”当前只表示：

- shared token shape；
- shared physical objectives；
- lightweight model-family adapters；
- lightweight robot / embodiment adapters。

它目前仍是**可检验假设**，不是结果。

必须通过：

1. 当前 model family / robot 上先验证；
2. held-out action-head family；
3. held-out robot embodiment；

才能讨论 cross-model / cross-robot universality。

---

## 3. 表示学习目标

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

### 3.1 `L_ro` · Readout / Reconstruction

- reconstruct fixed stop-gradient action-head feature target；
- 保留 action-head 已有任务与动作信息；
- 不修改 base action model。

### 3.2 `L_dyn` · Measured Transition Prediction

action-conditioned decoder：

```text
D(z_t, u_t, r) -> measured future physical state
```

其中：

- `u_t` 使用 actual / executed action；
- target 使用真实测得的 transition；
- 使用 validity mask；
- 按 physical units 做 normalization；
- terminal/reset 边界严格隔离。

第一阶段优先 joint / EE / relative motion 等可靠 measured outcome。

### 3.3 `L_phys` · 有效 Physics Constraints

第一版优先：

- kinematic consistency：`||v_EE - J(q) q_dot||²`；
- joint limits；
- speed limits；
- 明确的 actuator/control feasibility。

Contact、friction、force/torque、rigid-body dynamics 只有在 sensing / model / calibration 有效时才加入。

**不因为模拟器能导出某个字段，就默认它可以成为主实验中的物理监督。**

---

## 4. Online Self-Improvement

当前 self-improvement 的严格定义：

> 冻结大 action model，通过 Physical Token + 小型在线 learner，利用真实 executed action、reward 与 measured outcomes 改进行为。

在线阶段默认：

- base model frozen；
- action head frozen；
- token encoder/readout frozen；
- small actor/critic trainable；
- outcome decoder 单独用 measured transitions 更新；
- actor optimization 时 decoder weights frozen，但保留对 action 的 gradient；
- hard execution limits 与 learned physical regularization 分开。

---

## 5. 第一组正式实验

领导给出的第一组验证不是“堆更多模块”，而是一个严格的递增消融：

| ID | 方法 | 新增内容 | 回答的问题 |
|---|---|---|---|
| B0 | RL Token / matched head-readout baseline | compact readout | baseline |
| B1 | B0 + transition loss | measured outcome prediction | transition grounding 是否有增益？ |
| B2 | B1 + physics loss | valid kinematic / actuator constraints | physics constraints 是否提供额外增益？ |

必须 matched：

- token size；
- online learner capacity；
- base model；
- task data；
- interaction budget；
- reward；
- seed；
- action chunk / control frequency。

主要指标：

- task success；
- physical violations；
- adaptation time / interaction cost；
- old-task retention；
- repeated seeds；
- uncertainty intervals。

---

## 6. 当前已有资产如何重新定位

### 6.1 RL Token reproduction clips

现有：

- block assembly；
- drawer opening + block placement。

准确口径：

> **RL Token qualitative baseline demonstrations**

它们不是 Physical Token 结果，也不是 transition / physics loss 的比较结果。

### 6.2 Hammer / RoboTwin 资产

保留：

- 环境 bring-up；
- 数据、norm、checkpoint；
- actual state / contact / geometry logging；
- evaluation / video / seed / timing infrastructure。

但 hammer 不再定义论文上位故事。它可以用于：

- pipeline regression；
- transition target 验证；
- physics loss feasibility；
- controlled ablation。

### 6.3 Physics sidecar

从“未来可能直接送进 policy 的 privileged physics”改为：

- measured / privileged target 候选；
- validity audit；
- failure analysis；
- physical constraint feasibility 检查。

部署输入仍应优先来自 robot history、actual execution 与可获得 metadata，而不是 simulator-only truth。

---

## 7. Action-head extraction contract

不同 action model 必须先固定 extraction convention：

- Regression / MLP：penultimate activations；
- Diffusion / Flow：selected sampling-step features，并包含 noise/time context；
- Autoregressive：causal states before logits；
- 禁止 future demonstrated actions leakage。

同时必须保留：

```text
Backbone tap vs Action-head tap
```

对照，验证 action head 是否真的更适合物理 readout。

---

## 8. Streaming RL 的位置

此前探索把 Streaming RL 与 Physical Token 同时放进首轮创新。

现在调整为：

> **先验证 token grounding，再验证 online-learning efficiency。**

当前顺序：

```text
B0 RL Token / head readout
   ↓
B1 + transition loss
   ↓
B2 + physics loss
   ↓
matched online actor-critic
   ↓
physical/contact shift
   ↓
held-out model / robot
   ↓
Streaming RL / uncertainty-aware update（后续）
```

Streaming Actor-Critic、batch≈1、无 replay、uncertainty-aware learning rate、安全 fallback 继续保留，但不是第一组实验必须同时引入的变量。

---

## 9. 当前执行 Gate

### Gate A · Baseline / extraction

- RLT / RL Token baseline 可重复；
- 明确 action-head feature tap；
- 明确 robot history / executed action contract；
- action-head vs backbone tap 对照可跑。

### Gate B · Transition grounding

- B0/B1 token capacity matched；
- held-out transition prediction 有稳定差异；
- 不存在 future leakage；
- actual/executed action 与 target 时间对齐。

### Gate C · Physics grounding

- 只加入有严格定义与有效量纲的 constraints；
- B2 相对 B1 的增益可独立归因；
- 同时报告 physical violation，不只报告 success。

### Gate D · Online adaptation

- frozen base/head/token；
- actor/critic 真正更新；
- 使用 actual executed action 与 reward；
- matched interaction budget；
- old-task retention 可测。

### Gate E · Universal hypothesis

- 当前模型/机器人上先成立；
- 再 held-out head family；
- 再 held-out embodiment。

---

## 10. 当前禁止的过度表述

没有实验前，不写：

- “Physical Token 已经提升成功率”；
- “学会物理规律”；
- “Universal 已跨模型/跨本体成立”；
- “接触/摩擦定律已显式建模”；
- “机器人已实现开放环境无限自进化”；
- “Streaming 一定优于 replay”。

当前最准确的研究表述：

> **提出一个 action-head Universal Physical Token 假设：以 measured transition prediction 和有效 physics constraints grounding compact readout，再通过轻量在线 learner，在冻结 action model 的条件下适应变化的接触动力学。**

---

## 11. 知识库与主线的关系

RISE、Motus2、LWD、Zeva、Zetta、SmoothRL 等继续保留在 Frontier Knowledge Base。

它们用于：

- 找 baseline；
- 找创新边界；
- 找实现技巧；
- 解释结果。

但不会自动改变上述 Physical Token 主规范。

如果论文观点与领导主线冲突，默认：

> **先按领导定义完成可验证实验，再把论文作为对照/扩展。**

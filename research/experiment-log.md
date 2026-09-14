# 实验日志

## 2026-09-14 · 领导方案约束后的科研主线修正

### 事实

- 领导提供的 Physical Token 方案把研究问题明确收敛为：从现有 action-generation head 读取 compact token，用 measured transition prediction 与有效 physics constraints 进行 grounding，再通过小型在线 learner 在冻结 action model 的条件下适应变化的接触动力学。
- Physical Token 第一版输入侧包含 action-head pre-output features、recent measured robot state、actual/executed-action history 与 robot/control metadata。
- 当前“Universal”只定义为 shared token shape + shared physical objectives + lightweight model/robot adapters；跨 model family / embodiment 仍是待验证假设。
- 第一组正式比较固定为：B0 RL Token / matched head-readout baseline；B1 + measured transition loss；B2 + valid physics loss。
- 首轮 physics loss 只优先使用 kinematic consistency 与 actuator feasibility；contact/friction/force/rigid-body residual 只有 sensing、model、calibration 有效时才加入。
- 在线阶段默认 freeze base model、action head 与 token encoder/readout，只更新 small actor/critic。
- Streaming RL 保留为后续 online-efficiency 方向，不与首轮 Physical Token 表示变量同时改变。
- 现有 block assembly、drawer opening + placement 视频只记为 RL Token qualitative reproduction，不记作 Physical Token result。

### 解释

今天不是新增一个模块，而是**收敛科研问题**。

此前 Research OS 中的四阶段路线和大量 related-work synthesis 继续保留，但它们现在只作为：

- 历史探索；
- related work；
- 未来扩展；

不再自动决定当前实验。

当前 Source of Truth 是：

`research/physical-token-leadership-spec.md`

### 下一步

1. 固定 action-head extraction contract，并实现 backbone-tap vs head-tap 对照。
2. 整理 B0 matched baseline：token size、learner capacity、data、reward、interaction budget、seed、chunk/timing 全部锁定。
3. 实现 B1 measured transition prediction，只用 actual/executed action 与 measured next-state targets。
4. 实现 B2 第一版 physics loss：kinematic consistency + actuator feasibility。
5. 在 nominal setting 做 B0/B1/B2，再进入明确 physical/contact shift。
6. 只有当前 model/robot 上成立后，才做 held-out head family 与 held-out embodiment。

---

## 2026-09-12 · RLT Phase 0 关键推进

### 事实

- Hammer task-SFT checkpoint 快筛已完成：5k/10k/15k/20k 在同一 4-env 开发设置下分别为 1/4、0/4、2/4、2/4；20k 另一次独立快评为 1/4。
- 当前只固定了环境 reset seed，π0.5 action sampling 的初始随机噪声尚未独立固定，因此以上结果只用于开发期快筛，不作为正式成功率。
- RLT Stage 1 的 paper-aligned base-init 1-step smoke 已通过：total loss 3.49118、RLT loss 3.06114、VLA loss 0.43004、grad norm 5.7397；保存 667 个 model tensors + 62 个 RLT tensors，均为有限值。
- post-SFT warm-start 首次 smoke 因 legacy checkpoint key 转换不完整被判无效；修复后已实现 667/667 base tensor 全量匹配并通过工程 smoke，但不作为论文主线初始化。
- Stage 2 的正式动作块口径已恢复为 C=10，reference horizon H=50，reference dropout=0.5；逐子步 reward/done/switch、early-done、actual executed length、terminal observation 与跨 chunk done freeze 已通过 mock 测试，真实 RoboTwin rollout 尚未验收。
- RoboTwin 2.0 main bridge 已完成 20/20 transition alignment 与相关单测，但真实 learner smoke 暂未做；当前不让 main migration 阻塞 pinned RLinf_support baseline。
- RoboDojo/B300 仍未开始本机兼容性实测，目前没有“兼容/不兼容”的实验结论。

### 解释

这些结果继续保留为 baseline / infrastructure evidence，但 2026-09-14 之后不再自动决定上位研究方向。

### 下一步

后续 RLT 基线工作应服务于 B0/B1/B2 matched comparison，而不是独立扩展成新的主故事。

详细记录：`research/progress-2026-09-12.md`。

---

## 2026-09-11 · 历史探索：进入 Phase 0

此前将主线组织为 RLT Multi-task Benchmark → Failure Diagnosis → Physical Experience → Self-Improvement。

该结构保留用于历史追溯；2026-09-14 起被领导版 Universal Physical Token 研究合同取代。

---

## 记录模板

### 日期 · 标题

**事实**

**证据**
- checkpoint:
- config:
- log:
- video:

**解释**

**影响哪个研究假设**

**下一步最便宜的证伪实验**

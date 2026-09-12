# 实验日志

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

今天最重要的推进不是新算法，而是把第一条 RLT baseline 的复现口径进一步纠正清楚：

1. paper-aligned Stage 1 从通用 π0.5 base 开始，在目标任务 demonstrations 上联合做 VLA task loss + RLT reconstruction；
2. 独立 20k task-SFT 继续保留为 standalone reference / post-SFT 对照，不作为主线 Stage 1 必要初始化；
3. 正式 Stage 2 必须验证 C=10 的真实环境时序，C=1 只用于接线调试；
4. RoboTwin 2.0 / RLinf_support pinned baseline 与 RoboTwin 2.0 main migration 分成两个阶段；
5. physics sidecar 当前继续只做 logging / diagnosis / future probe，不泄漏给第一条 baseline policy。

### 下一步

1. 运行 paper-aligned base-init 的 2,000-step Stage 1 joint-full。
2. full 完成后验证 Stage 2 feature loader/checkpoint 完整加载。
3. 在真实 RoboTwin 上做 C=10 Stage 2 smoke，检查 transition/replay/critic/actor/update/sync/checkpoint 全链路。
4. 正式 30-seed reference/RLT 配对评估前补 action-sampling seed。
5. RoboDojo/B300 支线只推进一个小步骤：system manifest + 第一项官方兼容性 smoke。

详细记录：`research/progress-2026-09-12.md`。

---

## 2026-09-11 · 主线更新：进入 Phase 0

### 事实

- 现有 hammer 工程资产可用，但单任务不再作为项目唯一主线。
- π0.5 SFT 5k / 10k / 15k / 20k checkpoints 已生成。
- Reference checkpoint 尚未完成正式独立评估。
- RLT baseline 仍无正式可引用结果。
- RoboDojo 将作为 B300 上的每日小任务旁线推进。

### 解释

当前最缺的不是新 idea，而是：

1. 多任务 RLT baseline；
2. 统一 task / logger / evaluator；
3. 明确 RLT 原论文与本地实现差异；
4. 之后才能做 failure diagnosis。

### 下一步

1. Hammer checkpoints 统一 seeds 评估。
2. 冻结 Reference。
3. RLT 代码审计。
4. Hammer RLT baseline。
5. RoboTwin2 新增两个不同物理机制任务。
6. B300 上每天推进 RoboDojo 安装 / smoke。

---

## 2026-09-11 · 旧实验资产如何复用

### 保留

- hammer env / collector；
- 50 demos；
- LeRobot 数据；
- norm stats；
- π0.5 SFT；
- physics sidecar；
- contact / grasp / geometry labels；
- eval / logging / video scripts。

### 重新定位

- hammer：Pilot / Regression Task。
- physics sidecar：先做 logging / diagnosis，不直接变成 actor input。
- Physical Token：从“计划中的下一模块”降为 Phase 2 候选。

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

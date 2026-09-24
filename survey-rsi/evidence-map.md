[首页](README.md) · [主题](topics.md) · [论文总索引](papers/README.md) · [综述提纲](survey-outline.md)

# 证据对照：究竟改进了什么？

本页是整理者基于阅读卡片的横向归纳，不是跨论文统一排行榜。任务、数据、人工投入和指标不同，不能直接比较成功率高低。所有数字均来自作者报告，未独立复现。

## 近日工作：机制和证据并排看

| 工作 | 实际更新对象与保留范围 | 物理证据与人工条件 | 可以支持 / 不能支持 |
| :--- | :--- | :--- | :--- |
| [BEE](papers/bee.md) | 残差策略、纠正分布及约束；跨 episode 保留，基础 VLA 冻结 | 三项真机、一项仿真；接管与标签依赖人 | 接管驱动在线改进；不能称全自主或通用跨任务 RSI |
| [HiRE](papers/hire.md) | 成败支持集编辑奖励，再训练策略 | 四项仿真、两项 YAM 真机；真机成败由人标注 | 奖励随经验适配；并未修改奖励编辑规则本身 |
| [Banana Kick](papers/banana-kick.md) | 奖励目标参数与 PPO 策略迭代保留 | 仿真训练，G1 上 30 次冻结策略试验 | 新技能的目标—策略共同更新；不是真机在线学习 |
| [Advantage-guided VLA](papers/advantage-guided-vla-post-training.md) | 固定部署数据上的离线权重更新 | 四项双臂任务，各设置每任务 20 次 | 后训练设计对照；不是连续多轮部署改进 |
| [CMA](papers/counterfactual-memory-audit.md) | 审计时替换/恢复任务内记忆，策略冻结 | 仿真成对干预；PiPER 每任务 8 对 / 32 次 | 记忆的决策效用审计；故障恢复不是持续能力增长 |
| [RegenHarness](papers/regenharness.md) | 协议拟跨任务修订配置；现有结果是执行案例 | 四足巡检与环路实例，缺少修订前后对照 | 系统契约与发布设计；递归收益尚未实证 |

## 结果摘录必须连同分母和预算

| 工作 / 指标 | 作者报告 | 引用时必须同时写明 |
| :--- | :--- | :--- |
| BEE / 成功率 | 100%、85%、90%、90% | 每任务 3×20 次评测；前述手机、布料为精细阶段成功，另两项为全任务；真机训练每任务 20＋70 episode |
| HiRE / 瓶子任务 | 6/30 → 20/30 | 基础策略已有示范训练；60 与 70 个在线 episode 的检查点；另一个任务的 73.3% 为峰值 |
| Banana Kick / 固定评测分 | 912.8 → 1093.7 | 对照为学习进展课程；五种子、每种子 4096 匹配情境；不是任务成功率 |
| Advantage-guided VLA / 平均成功率 | SFT 0.11 → 加权 0.74 | 四任务各 20 次；增加 63 个百分点；同表 DAgger 0.45、硬筛选 0.50 |
| CMA / 故障恢复成功 | 6/36 → 20/36 | 人为注入记忆故障后的锚点恢复；未扰动参照为 26/36；不代表常态持续进步 |
| RegenHarness / 到达残差 | 0.11、0.17、0.25 m | 来自系统自身定位记录，容差 0.4 m；不是学习收益，也不是外部计量的定位精度 |

## 已有卡片怎样成为对照组

| 要比较的论点 | 放在一起读 | 要控制的混淆 |
| :--- | :--- | :--- |
| 在线参数更新是否有用 | [RAPolicy](papers/rapolicy.md)、[ForceRFT](papers/forcerft.md)、[BEE](papers/bee.md)、[DexPIE](papers/dexpie.md) | 全模型/残差、在线/批次、接管时长、交互预算、任务成功口径 |
| 记忆是否变成长期能力 | [MessyMem](papers/messymem.md)、[2AM](papers/2am.md)、[Zeva-Ego](papers/zeva-ego.md)、[CMA](papers/counterfactual-memory-audit.md) | 同实例跨尝试与跨任务不同；是否重置；记忆使用是否被干预验证 |
| 代码是否真的累积改进 | [机器人软件学习与迁移](papers/learning-transferring-robot-software.md)、[LEMCA](papers/lemca.md)、[Local Coding Agent](papers/generalizing-manipulation-local-coding-agent.md) | 控制程序演化、同任务会话缓存、基础模型或外层搜索规则更新应分列 |
| 不同反馈能否可信验收 | [No Free Checker](papers/no-free-checker.md)、[HiRE](papers/hire.md)、[SeeQ](papers/seeq.md)、[SRPO](papers/srpo.md) | 提议器与验证器共因错误、稀疏标签依赖、奖励投机、外部任务指标 |
| 进步是否伴随遗忘 | [FAN](papers/fan.md)、[持续世界模型基准](papers/compositional-continual-world-models.md)、[MEMOBench](papers/memobench.md) | 后向迁移、学习速度、旧能力保持与最终成功率不同 |
| 系统能否连续自主运行 | [HALTER](papers/halter.md)、[LIBERO-RECOVER](papers/libero-recover.md)、[SPINE](papers/spine.md)、[RegenHarness](papers/regenharness.md) | 复位、恢复和验证的成本；演示可运行不等于自我改进有效 |

## 严格递归还缺什么

把“自身执行 → 更新策略”与“改写产生更新的程序/学习规则 → 后续改进更有效”分开评测。建议要求：固定外部任务指标、相同累计预算、冻结改进器对照、多轮轨迹、旧能力保持，以及对验收器变动的单独消融。本轮六篇没有充分实证严格递归增强；这是对本轮证据的判断，不是对整个领域的否定。

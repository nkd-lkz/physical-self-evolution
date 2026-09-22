# 迁移后如何接回进度：冻结 reference 与小规模物理后果实验

> 2026-09-22；依据迁移快照的代码/元数据/历史日志核查、用户评测截图和本仓库历史记录。没有在新机器上重新训练或重跑55%评测。<br>
> [脱敏核查摘要](https://github.com/nkd-lkz/physical-self-evolution/blob/main/data/recovery-audit-2026-09-22.json) · [干预机制](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/rlt-intervention-2026-09-22.md) · [研究合同](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/physical-experience-protocol-2026-09-22.md)

## 1. 当前到底做到哪里？

| 项目 | 已有证据 | 限制 |
|---|---|---|
| 数据划分 | clean500排除10条动作异常，得到clean490；train450/eval40，70,640/6,238个帧索引，无seed交叉 | 迁移保存元数据不等于保存了原始数据 |
| 接触有效性 | 训练集另有10条动作有效但接触证据弱的轨迹 | 保留动作监督；contact/impulse目标需mask，不能作为无接触负样本 |
| 新 Stage1 | generic pi05_base，VLA+RLT joint、H50、batch64、alpha1；最后日志step10823 | 计划30k未完成；日志值不是闭环能力 |
| 新权重 | 历史记录原机有完整5k/10k保存点 | 当前迁移包没有模型权重，未在新机验收可加载性 |
| 新10k推理 | 同eval40两次22/40，55%；return0.55，平均长度196.25/200 | 来自截图与09-18记录；迁移包未找到相应原始eval40结果，尚不能逐seed复核 |
| 旧 reference | clean50的6k/8k/10k/12k分别8/7/8/10成功，各20回合 | 旧cohort不同，不直接拿50%与新55%宣称提升 |
| 旧 Stage2 | 旧clean50/12k，周期评测约45%→15%，约985轮停止 | 不是train450/10k的Stage2；没有接通Hammer专家干预 |
| Physical Token | 方法定义、数据合同与诊断基础 | 没有B1/B2、减干预或Universal实验结果 |

新10k的两次评测是同一开发cohort重复运行，不能合并为80个独立seed；聚合一致不证明逐轨迹一致。平均reward约0.00287是按步平均，不是成功奖励幅度；W&B的0 media不说明本地没有视频。详见[评测证据记录](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/progress-2026-09-22.md)。

末条Stage1日志的总loss约0.0532、RLT loss约0.0524、VLA loss约0.000808，只是进度条舍入值。`stage1_exit=1` 与历史主动中止记录可以并存，不能单凭它判断10k权重损坏。

## 2. 最简切入口

**先恢复一个冻结的 train450/10k reference，验收少量闭环和最小专家纠错，再做缓存特征上的后果预测。** 不需要先续训Stage1到30k，也不应直接恢复已退化的长程Stage2。

当前硬件与依赖可用性需在实际计算会话重新测量；本页不把原服务器配置或某次设备探测当作永久环境事实。只恢复 Hammer 一条 native 栈，RoboTwin native、RoboTwin2 main和RoboDojo/Isaac分别维护。原迁移manifest未包含所核查的常见模型/数据张量文件，不能把代码快照当作完整实验备份。

### 2.1 最小资产清单

| 优先级 | 资产 | 用途 |
|---|---|---|
| 必需 | train450/10k完整actor wrapper权重，例如保存点中的 `model_state_dict/full_weights.pt` | 包含匹配VLA与RLT模块，恢复同一个模型 |
| 必需 | 同run的norm、resolved config、split与eval seeds | 恢复输入/动作变换和评测协议；元数据已保留，使用前核对哈希 |
| 必需 | tokenizer、固定版本模型代码、迁移时的本地补丁 | 完整加载和预处理；不能直接替换成最新官方分支 |
| 闭环必需 | Hammer机器人/物体mesh、纹理、规划资源与匹配模拟器 | 执行真实仿真而非仅导入模块 |
| 优先补充 | 一份真实观测和对应旧模型输出 | 不启动完整训练的推理/变换对齐 |
| probe需要 | 约10–30条成功/失败交互的小包，含图像、实际状态/命令、时间和结果 | 一次性特征导出与小网络拟合 |

只做推理无需搬回450条完整训练数据或optimizer。完整wrapper加载路径若覆盖全部所需参数，通常无需另下载整份base权重，但配置、tokenizer和加载核查仍必需。精确续训时才额外需要optimizer、scheduler、RNG、训练状态和完整数据。

如果旧权重取不回，公开pi05_base不等于具有55%能力的Hammer reference。此时可以分析已有证据，或用脚本专家采集小数据建立新的状态→后果基线；新的任务适配必须标为新实验，不能称为恢复10k。

### 2.2 代码恢复顺序

1. 以迁移的 Hammer worktree与native RoboTwin补丁为起点，参数化旧launchers中的路径、设备编号与解释器。
2. 验收完整wrapper加载；用单观测检查动作维度、norm、prompt、采样和prefix-cache一致性。
3. 单环境单seed，再4–8个开发seed串行；保留H50/C50 native_macro与历史模型采样约定，记录显存、每chunk延迟和真实执行时长。
4. 接入并验收一个可恢复失败类型的专家干预，再做小规模后果probe。

旧eval worker的采样噪声还与batch形状和chunk调用有关。串行化适合小算力配对比较，但不保证逐轨迹重现原40并行评测，更不能预告仍会恰好22/40。新协议记录每回合实际environment/action seed与noise约定，候选方法使用相同新协议。

## 3. 现在没有模型也能做什么？

本地迁移工作区已有 `recovery/inspect_migration.py` 和派生的 `audit.json`、`train450_loss.csv`、`old12k_physics_episodes.csv`。这些是本地工具与证据文件，不是本公开网站仓库的可运行训练入口。公开同步仅包含脱敏摘要，原始日志和内部路径保留在本地。

已有旧12k的20条物理诊断回合为10成功/10失败、每回合4次策略chunk；成功约6.09–7.45模拟秒，失败约8模拟秒。可结合本地视频标注未抓住、持有后滑移、敲击位置偏差、接触不足、预算耗尽或无法判断，记录发生阶段与证据时间。**这是旧12k的失败复盘，不是新10k的18条失败。**

这些标注能决定第一个专家恢复类型与预测目标。视觉现象不能独自证明摩擦、冲量等物理成因，保留多重原因和未知标签。未来若拿回新10k的日志/视频，再单独补新cohort的失败分析。

## 4. 小算力探索清单

| 顺序 | 最小探索 | 可交付的证据 | 不能提前声称 |
|---|---|---|---|
| A | 现有日志/视频失败分型与时间审计 | 阶段、实测时长、命令与实际响应偏差 | 物理规律已被学会 |
| B | 一个专家、一类偏离状态、固定门控 | 实际接管、纠正动作、当前状态恢复率、专家秒数 | TOPP自动理解并修复所有失败 |
| C | 20–30条交互的冻结特征probe | state/history、RLT、head readout的后果预测对照 | 在线训练更快或最终成功率更高 |
| D | 一个物理参数3档×4–8个配对回合 | 扰动敏感性、阶段差异、初步信号 | 小样本显著性或多任务泛化 |
| E | 缓存数据上的小actor BC/reference一致性 | 反归一化动作、gripper、clip与少量闭环一致性 | BC loss小等于critic可信 |
| Later | 固定候选池评分、小预算B0/B1与learned gate | 对应研究合同的受控比较 | 所有变量一起变时的表示归因 |

C可以在可用GPU上只导出一次特征，再回到CPU或小GPU训练小MLP；不必保存所有层和所有去噪步。先预测measured关节/相对物体运动，contact/slip仅用有效标签。环境交互、图像/特征导出仍有成本，不能将“训练小头”称为整个系统零成本。

旧 BC 验证脚本虽然关闭actor的Q项，却仍会训练critic并包含较大warmup；它不是现成的低算力入口。若要节省计算，先单独做离线actor拟合，再查Q排序、时长折扣和终止语义。

## 5. 第一轮验收与后续门槛

第一轮的具体交付应是：一个能加载的旧checkpoint、一套匹配norm、单环境推理与少量闭环记录；一种从当前偏离状态恢复的专家；一张固定数据的后果预测对照表。预算数字为试验建议，尚未执行。

在此之后才能讨论“达到同等无专家成功率需要多少专家秒数”，或“相同专家预算时能否更早预判并提高辅助成功率”。这两种比较的完整指标、反事实边界和停止条件见[研究合同](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/physical-experience-protocol-2026-09-22.md)。

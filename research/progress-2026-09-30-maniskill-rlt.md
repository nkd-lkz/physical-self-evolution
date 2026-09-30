# ManiSkill RLT 复现与探索进展 — 2026-09-30

这份快照把 ManiSkill `PegInsertionSide` 的 baseline 复现和四条研究探索线放在同一证据表中。Stage 1 的 20 回合闭环评测已经完成，正式 baseline Stage 2 正在运行；FLARE 启发分支完成了 100 轮 matched smoke，但没有出现评估成功；Zeva、PICO VR 和新的 Jev 启发分支继续保持隔离。当前没有证据证明任一新增机制已经加快在线 RL 收敛、减少人工干预或实现跨任务迁移。

## 代码与实验边界

| 实验线 | 分支与提交 | 截至本快照可接受的结论 |
| --- | --- | --- |
| Baseline | [`baseline/maniskill-rlt-2026-09-25`](https://github.com/nkd-lkz/UPT_dev/tree/baseline/maniskill-rlt-2026-09-25)，`d9ba471e` | Stage 1 step 2000 的 20 回合成功率为 40%；正式 Stage 2 正在运行，尚未结束 |
| FLARE 启发 | [`research/rlt-flare-latent-dynamics`](https://github.com/nkd-lkz/UPT_dev/tree/research/rlt-flare-latent-dynamics)，`4225d601` | 增量未来 latent 预测的离线指标为正；100 轮在线对照流程通过，但两组 10 次评估均为 0 成功 |
| Zeva 启发 | [`research/rlt-zeva-interaction-memory`](https://github.com/nkd-lkz/UPT_dev/tree/research/rlt-zeva-interaction-memory)，`715d9656` | memory reader 能真实更新和恢复；learned reader 尚无稳定预测优势 |
| Jev 启发 | [`research/rlt-jev-atomic-decisions`](https://github.com/nkd-lkz/UPT_dev/tree/research/rlt-jev-atomic-decisions)，`020e0cf6` | 有限动作候选、真实 replay 和选择器更新已实现并通过 CPU 验证；尚未执行 GPU / ManiSkill smoke |
| PICO VR | [`feature/rlt-pico-vr-intervention`](https://github.com/nkd-lkz/UPT_dev/tree/feature/rlt-pico-vr-intervention)，`32586bb3` | Windows 本地仿真和手柄控制已调试；服务器 scripted takeover smoke 通过，真实跨机器人工闭环未完成 |

五条线尚未互相合并。大型 checkpoint、replay、视频、cache 和原始交互记录继续留在 NAS，不进入 Git。

## Baseline：Stage 1 得到 40%，Stage 2 正在运行

Stage 1 使用 400 条成功示范，在两张 L40 上从 step 750 保留 optimizer 状态恢复并完成 `2000/2000`。最终训练日志为 total / RLT / VLA loss `0.42236 / 0.41457 / 0.00779`，但训练 loss 只说明优化过程，不代表闭环成功率或收敛。

修复评测的 `policy_setup` 后，step 2000 checkpoint 在 20 个固定 reset、每回合最多 500 个控制步下完成评测：

- `eval/success_once = 0.4`，即 8/20 成功；
- `eval/return = 0.4`；
- `eval/episode_len = 335.25`；
- job 正常退出，exit code 为 0；
- 总评测用时约 44 分钟。

录像 wrapper 对两个 `numpy.bool_` 字段发出 metadata 类型警告，但 rollout 继续运行并得到完整聚合结果。是否 20 路视频全部可解码、每个失败的终止原因以及成功/失败分别耗时仍需单独审计。40% 只是一组 20 回合点估计，不能单独证明 Stage 1 已充分收敛或没有过拟合。

正式 baseline Stage 2 已在 GPU 0/1 上启动，配置为 64 个训练环境、256 个固定评估环境、总预算 5000 个 global step，自动 expert 关闭。截至读取快照时至少运行到 `149/5000`，`rlt/update_step=46400`。前五次评估为：

| Global step | 24 | 49 | 74 | 99 | 124 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `eval/success_once` | 37.89% | 36.33% | 40.23% | 35.94% | 42.19% |

这些是同一在途训练的周期快照，不是五个独立 seed 实验，也不是最终最优 checkpoint。当前 `intervention_rate=0`，因此这条 run 不能衡量人工或 expert 接管减少量。训练完成前不据此宣布提升、退化或收敛。

## FLARE 启发：预测链路有效，控制收益尚未出现

该分支不生成未来画面，也不是 FLARE 的完整复现。冻结 VLA 后，小型 sidecar 根据当前 RL token、本体状态和实际动作前缀，预测真实后续观测经同一冻结 VLA 得到的未来 latent 与关节变化。离线训练中，增量预测在固定划分和三个初始化上优于直接预测与状态保持；这是目前保留的正向表征证据。

最新在线比较给 baseline 和 FLARE 各运行 100 个 global step。两组共享 Stage 1 step 2000、seed、2 个训练环境、1 个评估环境、500 控制步 episode、每轮最多 2 次 actor/critic 更新，并每 10 step 评估一次。两组均 exit 0。

| 在线结果 | Baseline | FLARE sidecar |
| --- | ---: | ---: |
| 训练 episode | 200 | 200 |
| actor / critic 更新 | 各 200 | 各 200 |
| 训练成功 episode | 1 | 2 |
| 10 次单环境评估成功 | 0 | 0 |
| 平均 step time | 38.12 s | 38.18 s |

训练成功全部发生在第 0 个 global step，当时 `actor_switch_rate=0`，实际执行的是 VLA reference；从第 1 步起 actor 接管后，两组训练成功均为 0。因此不能把 FLARE 的 2 次与 baseline 的 1 次解释为新模块收益。

在线未来预测确实更新：相邻 checkpoint 间 `latent_world.*` 的 54 个张量中有 50 个变化，4 个不变张量是只在离线使用的 behavior BC head。未来预测总损失的前 10 轮均值约 `0.217`，后 10 轮约 `0.146`；由于 replay 分布同时变化，这不等同于固定验证集收敛，更不等同于控制能力改善。

这次对照还存在一处配置差异：baseline 的 FSDP `use_orig_params=False`，FLARE 为 `True`。下一轮必须统一这一设置，并先延长 actor 的 BC 热身、确认其能基本跟随 reference，再进行至少 20 个固定评估初态的同预算对照。当前不把 smoke 直接延长成大训练。

## Jev 启发：限制探索空间，而不是增加外部决策 API

新的 **RLT Atomic Decisions** 分支把 Stage 2 actor 从自由输出整个连续 chunk，改成在 VLA reference 附近选择最多 17 个完整候选：reference、受限的关节减缓/制动，以及 7 个关节各自的正负修正。默认每一步修正不超过归一化控制量 `0.08`，夹爪命令继承 reference。关节修正不是笛卡尔方向技能，也不是碰撞安全保证。

这条线借鉴 Jev 的有限选项和结构化选择接口，但不调用 Jev API，不读取额外几何/接触 oracle，也不使用模拟器预演候选。连续 twin-Q critic 继续评价实际执行动作，包括候选集合之外的接管动作；选择器学习 critic 和 BC 共同给出的全部候选改进分布。下一状态价值对有限候选精确求期望。

第一版直接最小化期望候选代价时，CPU 合成任务出现 selector 过早饱和：critic 已能选出正确候选，selector 仍保持错误选择。生产实现改为蒸馏 detached improvement distribution；相同数据和三个 seed 下，critic 与 selector 均恢复到 100% 选择合成最优动作。该结果只验证学习链路，不能证明插销任务样本效率。

工程验证结果为 229 passed、4 skipped、1 个在原 baseline 上也失败的依赖兼容测试单独排除；其中 23 项为新增组件测试，覆盖真实 replay、接管动作、梯度隔离、checkpoint 恢复、有限候选 target 和关闭功能后的 baseline 一致性。GPU 2 的 `--check` 只读预检已通过，确认配置、Stage 1 权重、norm 和 placement 声明；它没有启动 Ray、CUDA 或训练。实际 `--probe` 与 `--run` 尚未执行。

## Zeva 与 VR：结论保持不变

Zeva 启发分支已经证明完成交互的历史记录可以进入 replay，memory reader 在 FSDP 下会真实更新并可恢复；但当前 learned reader 在成功示范和隐藏 PD 刚度诊断中没有稳定优于无记忆对照。固定历史响应公式明显更准，说明历史中有可辨识信息，但当前读取网络尚未有效利用。

PICO VR 分支已在 Windows 运行 ManiSkill 画面，PICO 手柄可以驱动末端跟随，并暴露工作空间限位、碰撞后暂停、夹爪映射和 episode 过短等问题。服务器侧 40-transition learner smoke 含 12 条 scripted takeover，不能计作真实人工样本。Windows / PICO → 校园网 → GPU learner → 更新动作返回本地的完整闭环仍未验收。

## 当前判断与下一步 Gate

1. **Baseline 是当前计算主任务。** 保持 GPU 0/1 的 Stage 2 run 不受干扰，按 25 step 评估和 50 step checkpoint 持续记录；只有完整运行或预先定义的停止条件触发后，才选择 checkpoint。
2. **Jev 启发分支先做最小 GPU 2 smoke。** GPU 2 空闲后依次执行 placement probe 和 2-step smoke，验收 replay、有限候选、FSDP 更新和保存恢复；随后与同样 `0.08` 边界的连续 residual actor 做公平对照，区分“限制探索”与“离散选择”的贡献。
3. **FLARE 先修实验合同。** 统一 FSDP 配置，延长并验证 actor BC 热身，使用同一初始权重与至少 20 个固定评估初态；报告 success 曲线、transition、额外时延和显存，而不是只看 prediction loss。
4. **Zeva 不扩大在线训练。** 先冻结新测试集，比较无记忆、近期历史、检索历史和显式响应统计，并加入失败/恢复轨迹。
5. **VR 保留为人工反馈通道。** 先完成一个真实 PICO 回合的动作上传、实际执行记录、learner update、policy version 和动作回传，再考虑与 64 环境训练协同。
6. **继续保持单变量分支。** FLARE 研究动作后果表征，Zeva 研究历史经验，Jev 研究有限决策空间，VR 研究人工反馈；在各自 matched 对照成立前不混合。

当前可以证明的是：baseline 已形成可运行的 Stage 1/Stage 2 链路，三种经验机制与一个人工接口均有独立工程原型。当前不能证明的是：机器人已经获得通用物理规律、持续成长、减少干预或跨任务泛化。

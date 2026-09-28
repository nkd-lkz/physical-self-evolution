# ManiSkill RLT 复现与探索分支进展 — 2026-09-28

这份快照记录新的 ManiSkill `PegInsertionSide` 实验线。它与仓库此前的 Hammer / RoboTwin clean490 记录是不同的数据、任务实现和 checkpoint 系列，成功率与训练 step 不可直接横向合并。当前已经完成 Stage 1 训练，并分别建立 FLARE 启发的动作后果表征、Zeva 启发的交互记忆和 PICO VR 接管三个隔离分支；尚未得到 Stage 2 收敛加速、减少人工干预或跨任务迁移的证据。

## 可复现代码边界

| 实验线 | 分支与最新提交 | 当前可接受的结论 |
| --- | --- | --- |
| Baseline | [`baseline/maniskill-rlt-2026-09-25`](https://github.com/nkd-lkz/UPT_dev/tree/baseline/maniskill-rlt-2026-09-25)，`853e664c` | Stage 1 完成 2000 step；20 个固定 reset 的闭环评测正在运行；Stage 2 长程效果未验证 |
| FLARE 启发 | [`research/rlt-flare-latent-dynamics`](https://github.com/nkd-lkz/UPT_dev/tree/research/rlt-flare-latent-dynamics)，`f0f14946` | 增量式未来 latent 预测在固定划分、三个初始化上优于状态保持与直接预测；真实 Stage 2 smoke / resume 通过；在线控制收益未验证 |
| Zeva 启发 | [`research/rlt-zeva-interaction-memory`](https://github.com/nkd-lkz/UPT_dev/tree/research/rlt-zeva-interaction-memory)，`715d9656` | 交互记忆已进入 replay、critic 更新和 checkpoint；真实 reader 参数会更新；当前学习型 reader 没有稳定预测优势 |
| PICO VR | [`feature/rlt-pico-vr-intervention`](https://github.com/nkd-lkz/UPT_dev/tree/feature/rlt-pico-vr-intervention)，`32586bb3` | Windows 本地仿真与 PICO 控制已进入人工调试；GPU 2 单环境 learner 的脚本接管 smoke 通过；真实 PICO → 校园网 → learner 闭环未验收 |

这些分支都从同一个 ManiSkill baseline 分出，尚未彼此合并。大型 checkpoint、cache、replay、视频和原始交互记录保存在 NAS，不进入 Git。

## Baseline：Stage 1 完成，闭环能力仍在评估

Stage 1 使用 400 条成功示范、`pi05_base`、联合 VLA action loss 与 RLT reconstruction loss，在两张 L40 上训练。训练从 step 750 保留 optimizer 状态恢复，最终完成 `2000/2000`。结束时记录为：

- total loss：`0.42236`；
- RLT loss：`0.41457`；
- VLA loss：`0.00779`；
- gradient norm：`1.51172`；
- `global_step_2000/actor/model_state_dict/full_weights.pt` 已导出，大小约 9.93 GB；
- W&B run：[`8oblhtio`](https://wandb.ai/c6522513-sustech/rlinf-rlt/runs/8oblhtio)。

launcher 在训练与权重导出后出现 shell 引号解析错误，因此进程退出码为 2；checkpoint 文件、FSDP shard 和 W&B 完成状态均表明训练主体已结束。该错误不能当作模型缺失，也不能反过来证明闭环能力。

20 个固定 reset ID 的评测使用物理 GPU 2，关闭 Stage 2 phase switch 和 expert takeover，最多执行 500 个控制步，并录制 20 路同步拼接视频。第一次启动在 action preparation 处因 `policy_setup=None` 失败，未产生有效 episode，不能计入结果。baseline 随后显式设置 `policy_setup: panda-qpos`，提交 `853e664c`；重新运行已经越过首次动作执行并进入 rollout / 视频录制。截至本快照，最终 `eval/success_once`、20/20 episode 完成状态和 MP4 完整性仍待任务结束后入库。

因此目前只能写成：**Stage 1 优化完成，闭环评测进行中**。训练 loss 下降不是成功率，也不能证明 RL token 已经编码物理规律。

## FLARE 启发：动作条件化未来表征

该分支没有生成未来画面，也没有复现 FLARE 的完整 flow-matching policy。冻结 VLA 后，小型外挂网络读取当前 RL token、本体状态和实际动作前缀，预测未来 RL token 与关节变化；未来标签来自真实示范中的后续观测，并由同一冻结 VLA 提取。Stage 2 将当前预测上下文交给 actor / critic，同时用真实 replay 的未来监督更新外挂网络。

直接回归未来 token 的首轮结果弱于简单的“状态不变”预测，因此后续加入增量形式：

```text
future latent = normalized current latent + predicted residual
```

固定数据划分后，初始化与采样 seed 为 2026 / 2027 / 2028，每个模型训练 300 次更新。独立测试 episodes 12–23 的 cosine error 如下，越低越好：

| Horizon | 状态保持 | 直接预测，均值 ± 标准差 | 增量预测，均值 ± 标准差 |
| --- | ---: | ---: | ---: |
| 1 | 0.012456 | 0.073905 ± 0.000946 | **0.010605 ± 0.000108** |
| 5 | 0.071462 | 0.073711 ± 0.001061 | **0.029521 ± 0.000537** |
| 10 | 0.158003 | 0.073513 ± 0.001411 | **0.043414 ± 0.002442** |

三个 seed 的增量版在三个 horizon 上都得到更低误差；打乱动作后误差上升，说明网络使用动作输入。真实 GPU Stage 2 smoke 完成两个 global step，54 个 `latent_world.*` 张量中有 50 个更新；4 个未更新张量属于仅离线使用的 BC head。增量 sidecar 从 step 2 恢复到 step 4 后，两个 optimizer 的 step 从 4 增至 8。

当前证据支持“小预算下，增量式动作后果预测比直接重建更适合这批数据”，但不支持“已经学到通用物理规律”。测试集已经参与过前序分析，且只有单任务成功示范；下一项关键证据必须来自固定交互预算的 baseline / direct / residual 在线控制比较，而不是继续优化同一离线指标。

## Zeva 启发：完成交互的显式记忆

该分支在每个动作 chunk 完成后保存起始关节、实际命令、真实关节变化、有效执行长度和终止信息。下一次决策读取近期记录与 archive 检索结果，压缩成 64 维上下文后拼接到 actor / critic。replay 保存当时可见的记忆快照，禁止用未来经验回填过去。

真实 Stage 2 smoke 最初正常退出，但 17 个 memory reader 张量没有变化。根因是 FSDP 参数展平破坏了按名称分配 optimizer 的假设；设置 `use_orig_params=True` 并增加 checkpoint 参数差异审计后：

- step 1 → 4：`17/17` reader 张量更新，最大绝对变化 `0.00057749`；
- step 4 → 6：恢复后仍有 `17/17` reader 张量更新；
- 两个 optimizer 的 step 从 8 增至 12，证明保留状态继续更新。

效果诊断没有得到同样积极的结果。在成功示范上，有记忆预测真实关节变化并未跨 seed 稳定优于同尺寸无记忆网络。进一步构造隐藏 PD 刚度 250 / 1000、相同初态与相同命令的成对数据后，attention reader 的测试 MSE 仍只比无记忆对照略低；显式按历史响应估计 per-joint gain 的固定公式则把完成至少 4 个 chunk 后的 MSE 从约 `0.00019090` 降到 `0.00001657`。

这说明历史中存在可提取的动作响应信息，但当前 learned reader 没有稳定利用它。该负结果把下一步从“扩大在线训练”改成“先解决可辨识统计量、失败/恢复数据和读取机制”，避免把“网络看过历史”误写成“经验已经有用”。固定公式只是诊断，不是可部署 actor，也不是接触因果模型。

## VR 接管：工具链与算法证据分开

Windows RTX 4060 已运行 ManiSkill 本地画面，PICO 4 Ultra Enterprise 通过企业串流 / SteamVR 提供手柄输入。操作者已经验证侧握键可驱动机械臂末端跟随，同时暴露了工作空间限位、碰撞后暂停、夹爪映射和 100 步 episode 过短等问题；分支随后增加诊断日志、故障恢复和更长校准 episode。该阶段是本地控制验收，不是在线 RL 结果。

服务器侧另有一个隔离的单环境、单步 learner。两次 40-transition GPU 2 smoke 均退出 0；最终 trial 记录：

- 40 条实际仿真 transition，12 条 scripted takeover；
- critic / actor 更新各 33 次；
- actor 发布版本达到 32，并用于后续动作；
- actor / critic 最大权重变化分别为 `0.00355607 / 0.00254076`；
- checkpoint 恢复后 optimizer 非空，update 33 → 34。

这些接管样本由脚本产生，不是 PICO 人工操作。当前还没有完成 Windows / PICO → 校园网 RPC → GPU 2 learner → 更新后动作返回 Windows 的整链验收，也没有合入正式 10 步、64 环境 Stage 2。VR 分支现阶段的价值是提供可审计的人工动作、真实执行结果和接管成本，而不是提供成功率提升。

## 当前判断与下一步 Gate

四条线的证据等级不同：

1. **Baseline** 已完成训练，但必须先得到 20 个固定 episode 的成功率、逐 episode 终止原因和完整视频，才能成为 Stage 2 reference。
2. **FLARE 启发分支**目前拥有最明确的正向离线信号；下一步应做等预算在线消融，检查它是否提高早期成功率、降低达到阈值所需 transition，或改善失败恢复。
3. **Zeva 启发分支**已经证明“历史有信息”和“当前 reader 会更新”，但尚未证明“reader 有用”；下一轮应预先冻结测试条件，引入隐藏动力学与失败/纠正轨迹，再比较无记忆、近期记忆、检索记忆和显式响应统计。
4. **VR 分支**先完成单个真实 PICO 回合的端到端上传、人工样本计数、optimizer 更新和动作回传，再讨论与 64 环境训练融合。人工控制一个环境不等于同时接管 64 个环境。
5. 三个研究分支保持独立；在单变量对照成立之前，不把未来预测、记忆和 VR 接管同时并入 baseline。

当前最小科研闭环仍是：

```text
可信 Stage 1 reference
        ↓
等预算 Stage 2 baseline
        ↓
一次只加入一个经验机制
        ↓
success / 收敛 transition / intervention seconds / failure recovery
        ↓
独立 seed 与新动力学条件复测
```

这份快照记录工程与小规模诊断进展，不宣称 Stage 2 已收敛，也不宣称已经实现机器人持续自进化。

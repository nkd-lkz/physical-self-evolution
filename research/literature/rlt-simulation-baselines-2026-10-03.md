# RLT 仿真两阶段 baseline 核查 · 2026-10-03

这份核查比较公开 RLT 实现是否具备 Stage 1、在线 Stage 2、仿真评估与配套结果，以决定当前两卡研究的最小验收路径。来源是仓库源码、作者文档、权重清单和公开日志；本项目尚未安装运行这些新增候选，不能把源码核查写成独立复现。

## 仿真入口与复现证据

| 实现 | 核查 revision | 两阶段与主要场景 | 当前判断 |
| --- | --- | --- | --- |
| [RLinf](https://rlinf.readthedocs.io/zh-cn/latest/rst_source/examples/embodied/rlt.html) | main c70606f | Stage 1＋在线 actor／critic，ManiSkill 与真机配置 | 现有本地链路保留，Stage 2 收敛尚未验收 |
| [Yyshadow/openpi-RLT](https://github.com/Yyshadow/openpi-RLT) | c1e40ac | token 训练与在线 RL，AgileX 真机 | 继承的 LIBERO VLA 示例不等于接通 RLT 仿真在线训练 |
| [MINT-SJTU/Evo-RLT](https://github.com/MINT-SJTU/Evo-RLT) | 8d02d99 | VLA／token／transition cache／actor-critic，双臂 SO101 | 主要 learner 示例读取缓存；没有核实自主 LIBERO／RoboTwin 闭环配方 |
| [yknxh/rlt-openpi](https://github.com/yknxh/rlt-openpi) | 6a3cf09 | 两阶段、TD3、warmup、干预接口，Franka／DROID | README 明确仿真未验证，仍需移植与验收 |
| [RL-Token-SmolVLA](https://github.com/RajatDandekar/RL-Token-SmolVLA) | 452249c | 两阶段，SO101 相机与人工反馈 | 未找到完整仿真训练配方 |
| [akashspacesky/vla-rlt](https://github.com/akashspacesky/vla-rlt) | 4cb424a | 预训练与在线 SAC，SmolVLA／SO101 | 仿真仍列为待办，dry run 不是仿真收敛 |
| [AlphaBrain](https://github.com/AlphaBrainGroup/AlphaBrain) | 604924b | encoder 预训练→LIBERO 在线 TD3→评估 | 新候选中优先验收；尚未证明本地稳定重训 |

本次没有找到证据同样完整的 RoboTwin RLT 两阶段开源配方。这是有范围和日期的检索结果，不是断言全网不存在。

## AlphaBrain 两条路线不可混用结果

| | RLT_a | RLT |
| --- | --- | --- |
| 输入 | action-query hidden states | 完整 VLM token 序列 |
| token | 256 维投影 bottleneck | VLA hidden dimension 的单 token |
| Stage 1 | rollout 观测的 encoder 预训练 | 支持 demo 数据与可选联合 VLA loss；省略 demo 配置会回退 rollout |
| backbone | 已接通 QwenOFT | QwenOFT 与 π0.5 |
| 公开证据 | 配套 VLA、encoder／actor／critic、评估 JSON | 训练评估入口与部分任务曲线；仍需核实完整资产和重训 |

[实现说明](https://github.com/AlphaBrainGroup/AlphaBrain/blob/604924beb77b04b0da49326dfae6ea423a27d28a/scripts/run_rl_scripts/README.md) 与 [Stage 1 说明](https://github.com/AlphaBrainGroup/AlphaBrain/blob/604924beb77b04b0da49326dfae6ea423a27d28a/AlphaBrain/training/reinforcement_learning/algos/RLT/README.md) 明确列出了差异。VLA 的先行 SFT、RL-token encoder 训练和在线 actor／critic 训练要分别记录，不能只看到文档的“两阶段”就认定与 RLT 原方法完全相同。

[发布的 Qwen RLT_a 模型](https://huggingface.co/AlphaBrainGroup/alphabrain-rlt-5traj-alltasks-libero-goal) 报告 LIBERO-Goal 10 个任务、每任务 50 回合，总体 92%。[配套 VLA](https://huggingface.co/AlphaBrainGroup/qwenoft-5traj-libero-goal) 也公开。这是作者评估，不是本项目复现，也不能在缺少匹配 VLA-only 评估时直接计算 RL 增益。

下载核对 [metrics.json](https://huggingface.co/AlphaBrainGroup/alphabrain-rlt-5traj-alltasks-libero-goal/blob/main/metrics.json) 后，400 行记录末次累计为 2,497,595 环境 step；仅前 47 行有新增 step，后续 iter_env_steps 与 actor_loss 均为 0。应查明日志生成和实际训练的对应关系；不能仅由这些零值断言任务失败，也不能承诺快速稳定重训。没有足够 wall-clock 数据估计两张 A6000 的总训练时长。

公开 [π0.5 RLT 曲线](https://github.com/AlphaBrainGroup/AlphaBrain/blob/604924beb77b04b0da49326dfae6ea423a27d28a/scripts/run_rl_scripts/example_results/rlt_ori_eval_curves.png) 显示不同任务收益不一致：5-demo task 0 从约 74% 到末次约 98%，1-demo task 3 的末次值低于其初始 VLA。图中不同面板的评估回合数不同，且不是多训练 seed 置信区间；best checkpoint 和末次 checkpoint 不混报。

## 两卡验收前需要整理的入口

- 模型卡评估脚本名称与当前源码存在差异；RLT_a 应匹配 action-token evaluator 与发布架构，不能加载进 full-token RLT。
- RLT_a 评估 shell 默认三 GPU 分片，不能简单传入两个 GPU 编号；其清理逻辑还会匹配同用户的其他 LIBERO worker，需要限定为本任务进程。
- 部分 Stage 2 脚本写死 seed=42，设置一个未读取的环境变量不会切换随机种子。
- encoder 自动发现依赖目录命名；使用明确的 encoder 路径并检查对应 VLA、normalization、维度与 chunk 长度。
- 当前 action-token actor 直接输出动作；不能只依模型卡的 residual 描述假设初始化等于 VLA，必须检查 BC warmup 后的执行能力。
- 并行环境数量和 UTD 的定义要按实际 transitions、batch 与更新数核算，不能跨框架只比较同名数值。

这些是源码核查发现的验收事项，目前尚未修改或运行 AlphaBrain 训练脚本。

## 无 VR 的 Stage 2 如何成立

仿真环境提供 reward／success／termination；演示和参考 VLA 提供初始行为；人工纠正只是额外数据来源。可先做无辅助训练与评估，保留失败 transitions。若初始 VLA 几乎无法成功，稀疏奖励不足以可靠地区分更好的动作，需要先改善 reference 或明确引入演示／expert 数据，并对所有实验组匹配该预算。

没有真人干预的仿真实验不能报告“节省人工分钟”。可先报告 expert 请求次数、控制时长等代理指标，并与未来真人测量分开。

## 验收顺序与退出条件

1. 配套公开 VLA 与 RLT_a 成品复评：同任务、同初态、同动作协议，先 3×20 排查，再 10×50 对齐作者口径。
2. 同一已验收环境重新训练 full-token RLT＋Qwen：显式 demo 配置，核查 actor warmup、真实采样、TD 更新、terminal 和保存恢复。π0.5 是需要另验资产的选项。
3. 至少 3 个 seed 比较初始 VLA；同时记录无辅助成功率、实际 env steps／chunks、wall-clock 和波动。两卡吞吐实测后再确定训练预算。
4. baseline 通过后再做 Zeva 记忆和 Stage 1B。若发布权重也无法达到合理能力，先定位预处理／controller／checkpoint；若重训反复退化，不继续扩大新网络。

决策是优先验收候选，尚未认定替换 RLinf。最新进度与材料入口见 [10-03 日报](../progress-2026-10-03.md)。

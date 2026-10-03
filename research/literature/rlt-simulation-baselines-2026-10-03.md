# RLT 仿真两阶段 baseline 核查 · 2026-10-03

这份核查比较公开 RLT 实现是否具备 Stage 1、在线 Stage 2、仿真评估与配套结果，以决定当前两卡研究的最小验收路径。来源是仓库源码、作者文档、权重清单和公开日志；本项目尚未安装运行这些新增候选，不能把源码核查写成独立复现。

**同日续查结论：优先 LIBERO。需要现成两阶段 RLT 仿真，先验收 AlphaBrain 的发布模型和训练入口；希望保留 RLinf／π0.5，则先用公开 SFT＋LIBERO DSRL 做独立基准检查，再移植 action-space RLT。DSRL 是工程检查和邻近算法，不冒充 RLT。RoboTwin 留到单臂链路稳定之后。** 这轮新增三类候选，总计十个仓库；没有启动训练或改动训练机器。

## eRLT 仿真到底来自哪个仓库

[eRLT v1，§5.1 与附录 C.2/C.4](https://arxiv.org/html/2610.00913v1) 给出的证据有明确边界：

| 场景 | 论文明确交代 | 尚不能推断 |
| --- | --- | --- |
| USB／排线真机 | C.4 指明 RLT implementation 建立在开源 RLinf 上 | 不等于 eRLT 改动已合入 RLinf main |
| LIBERO | DSRL 风格的小 actor 在噪声空间控制冻结 VLA；加载 RLinf-Pi0-LIBERO-Spatial-Object-Goal-SFT | 使用 RLinf 权重不等于使用 RLinf 训练仓库 |
| RoboTwin | 同类噪声空间框架；加载 pi0.5_robotwin2 | 使用 RoboTwin 环境不等于其官方仓库提供 eRLT learner |

截至 2026-10-03，本轮在论文、作者公开链接、GitHub 仓库搜索和网络搜索中**没有核实作者独立 eRLT 仿真代码发布**。不能在 RLinf、官方 DSRL 或用户列出的社区 RLT 仓库中擅自选一个，声称就是 eRLT 的实现来源。

还应区分两种 baseline：仿真表中的 **RLT\*** 是 DSRL 骨架中的 RLT 表征对照；真机的 RLT 是动作空间 actor。LIBERO 仿真协议写的是 32 维噪声沿 10 步重复、3 次 flow 积分、执行 10×7 动作；RoboTwin 执行 32×14 双臂动作。当前 RLinf DSRL 示例执行 5 步，不能直接复制其配置复现 eRLT 表格。附录同时出现 Pi0 命名的 LIBERO 权重与 π0.5 模型描述，精确复现还需澄清这一配置不一致，不能自行认定两种权重等价。

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
| [nakamotoo/dsrl_pi0](https://github.com/nakamotoo/dsrl_pi0) | 7f48937 | 作者 JAX 实现，冻结 π0＋噪声空间 SAC，LIBERO／Aloha | 适合作为冻结 VLA 在线 RL 的独立参照；没有 RLT token Stage 1 |
| [verl-project/verl-vla](https://github.com/verl-project/verl-vla) | c1de826 | π0.5＋LIBERO DSRL，公开初始权重和逐次评估 | 有明确配方，但文档验证的是八 GPU；不是当前两卡开箱保证 |
| [TihayaKousaka/rlt-openpi-libero](https://github.com/TihayaKousaka/rlt-openpi-libero) | 231c718 | 上游 rlt-openpi 的 LIBERO Stage 1 扩展 | 只找到 LIBERO 数据／预训练入口；Stage 2 仍是 Franka 示例，不能按仓库名字判定已完成 LIBERO RL |

本次没有找到证据同样完整的 RoboTwin RLT 两阶段开源配方。这是有范围和日期的检索结果，不是断言全网不存在。

进一步代码核查发现：`Yyshadow/openpi-RLT/scripts/eval_rlt.py` 计算的是 token 重建 MSE／MAE／cosine 等离线指标，不是 LIBERO 闭环成功率；`akashspacesky/vla-rlt` README 描述 SmolVLA，但当前 `scripts/pretrain_rlt.py` 导入 `groot_rlt` 并加载 GR00T，`--dry_run` 用 mock 特征。因此这两个文件名或 README 不能单独证明目标 baseline 可复现。Evo-RLT 的公开数据／模型以双臂螺丝真机为主，也不能直接代替 LIBERO 权重。

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

## 可直接定位的入口与配套资产

### 1. AlphaBrain：优先完成成品复评，再重训

已通过 Hugging Face API 核实发布包内确实有 `actor.pt`、`critic.pt`、`encoder.pt`、`metrics.json`、`eval_summary.json`。模型 revision 为 `b5c0080e46f4b900c049e76bd9f3df68befac12a`。92% 与评估 JSON 一致，但不能证明当前 main 一定无修改加载成功；先完成成品与源码兼容检查。

当前源码的实际入口：

- Stage 1：`scripts/run_rl_scripts/run_rlt_pretrain.sh`，`TRACK=rlt` 为 full-token 路线，`TRACK=rlt_a` 为 action-query 路线。
- Stage 2：`scripts/run_rl_scripts/run_rlt_rl.sh`；full-token 支持 `BACKBONE=qwen` 或 `pi05`。
- full-token 评估：`scripts/run_rl_scripts/run_eval_rlt.sh`。
- 发布的 Qwen RLT_a 评估：`scripts/run_rl_scripts/run_eval_rlt_a.sh`，底层为 `AlphaBrain/training/reinforcement_learning/eval/eval_libero.py`。

模型卡里的 `cd VLA-Engine-Developer`、`run_rlt_5traj_alltasks.sh` 和旧评估命令已与当前 main 不完全一致；RLT 子目录 README 的 `run_rlt_rl_task0_release*.sh` 也不是当前树里的入口。以锁定版本的真实文件为准。

下列是**源码核对后的单 GPU 成品评估命令模板，未在本项目运行**。先按仓库说明安装 VLA 依赖与独立 LIBERO Python 环境，设置 `LIBERO_HOME`、`LIBERO_PYTHON`、`PRETRAINED_MODELS_DIR`；省去默认三卡 shell 的分片与全局 worker 清理，避免与其他实验进程相互影响。

```bash
# 在 AlphaBrain 仓库根目录；先下载成品，不重新训练。
hf download AlphaBrainGroup/qwenoft-5traj-libero-goal \
  --local-dir results/training/QwenOFT-5traj-libero_goal/final_model
hf download AlphaBrainGroup/alphabrain-rlt-5traj-alltasks-libero-goal \
  --revision b5c0080e46f4b900c049e76bd9f3df68befac12a \
  --local-dir results/rlt_release

export PYTHONPATH="$PWD:${PYTHONPATH:-}"
export MUJOCO_GL=egl
CUDA_VISIBLE_DEVICES=0 python \
  AlphaBrain/training/reinforcement_learning/eval/eval_libero.py \
  --vla_ckpt results/training/QwenOFT-5traj-libero_goal/final_model \
  --action_token_ckpt results/rlt_release/rl_offpolicy_iter_00400 \
  --suite libero_goal --task_ids 0,3,6 --n_eps_per_task 20 \
  --gpu 0 --num_workers 1 --seed 42 \
  --bottleneck_dim 256 --encoder_layers 2 --encoder_heads 4 \
  --actor_hidden_dim 512 --ref_dropout 0.5 --fixed_std 0.1 --prop_dim 8 \
  --results_json results/rlt_release/smoke_tasks_0_3_6.json
```

这只是排障子集，不能与作者 10×50 的总体 92% 直接比较。验收后扩大相同初态协议，并做 VLA-only 配对。π0.5 路线的代码存在，但本次未在 AlphaBrainGroup 模型清单查到对应公开 π0.5 成套资产；默认 checkpoint 指向本地训练目录。Qwen 权重不能加载到 π0.5，也不能用改路径的方式把 RLinf 权重直接当成 AlphaBrain 格式。

### 2. 保留 RLinf／π0.5：LIBERO 独立检查最省迁移工作

[RLinf RLT 文档](https://rlinf.readthedocs.io/en/latest/rst_source/examples/embodied/rlt.html) 目前提供 ManiSkill 和真机 RLT；[DSRL 文档](https://rlinf.readthedocs.io/en/latest/rst_source/examples/embodied/dsrl.html) 提供 LIBERO。源码中的四个现成同步／异步配置为：

```text
examples/embodiment/config/libero_spatial_dsrl_openpi.yaml
examples/embodiment/config/libero_spatial_dsrl_openpi_pi05.yaml
examples/embodiment/config/libero_spatial_async_dsrl_openpi.yaml
examples/embodiment/config/libero_spatial_async_dsrl_openpi_pi05.yaml
```

首轮选择同步版本，减少异步时序变量。配套 [RLinf-Pi05-LIBERO-SFT](https://huggingface.co/RLinf/RLinf-Pi05-LIBERO-SFT) 核实有 `model.safetensors` 与 `physical-intelligence/libero/norm_stats.json`，revision `45ccfcc4e28634f1576ebf78cab0fbe2fd82432d`。Pi0 对应另一个模型 [RLinf-Pi0-LIBERO-Spatial-Object-Goal-SFT](https://huggingface.co/RLinf/RLinf-Pi0-LIBERO-Spatial-Object-Goal-SFT)，revision `4ec11623fba96e1432e535e2c76a634a5e0bdb96`，不要混用两种模型配置。

先验收纯 VLA；此时不应让随机初始化的 DSRL actor 生成测试噪声。示例命令只执行 task 0 的小范围检查，完整评估再增加初态和任务：

```bash
# 在 RLinf 根目录及已安装的 openpi / LIBERO 环境内。
hf download RLinf/RLinf-Pi05-LIBERO-SFT \
  --revision 45ccfcc4e28634f1576ebf78cab0fbe2fd82432d \
  --local-dir checkpoints/pi05_libero_sft
bash evaluations/run_eval.sh libero_spatial_openpi_pi05_eval \
  rollout.model.model_path="$PWD/checkpoints/pi05_libero_sft" \
  env.eval.total_num_envs=20 '+env.eval.task_id_filter=[0]'
```

通过后，复制同步 DSRL YAML 为个人实验配置，填好 `actor.model.model_path` 与 `rollout.model.model_path`，再用 `bash examples/embodiment/run_embodiment.sh <配置名> LIBERO` 启动。该训练 shell 的第二个参数是平台名，**不会自动转发任意第三个 Hydra 参数**；额外设置请写进复制的 YAML 或直接使用 Python 入口。

必须明确修改／记录的配置：

| 项 | 原例子／风险 | 验收方法 |
| --- | --- | --- |
| `specific_reset_id: 0` | 所有环境可能重复同一个 task 0、trial 0 | 做多初态时设为 `null`；通过 `task_id_filter` 选任务；显式保存 train/eval 初态列表 |
| `runner.val_check_interval: -1` | 不能假设训练会自动产生周期评估曲线 | 设置合适正整数并检查实际触发 |
| 16 train／500 eval envs | 是示例并行度，不是两卡最低资源要求 | smoke 可用 2–4 train／20 eval；批量、放置与整除约束一并检查，再做吞吐实测 |
| 5 步执行、3 次积分 | 与 eRLT 的 10 步执行不同 | 第一轮沿用自身匹配基线；复现 eRLT 时另建明确协议 |
| 模型／norm／动作 | 正确权重配错误 processor 仍会失败 | 同帧同噪声比较官方推理与集成推理，再检查实际环境动作 |

上述缩小资源的配置是工程建议，不是已验证的新 recipe；不要据此承诺单卡显存、两卡耗时或成功率。

要在 RLinf 里做真正 LIBERO RLT，还需完成五项移植：LIBERO Stage 1 dataconfig 与示范；保存含 token 模块的完整 checkpoint；Stage 2 feature-model 的两图／8D state／7D EEF delta action 对齐；替换 ManiSkill 特定的 near-hole 阶段门控；验收 chunk reward、terminal、replay 与实际 actor 控制比例。`loss_type: rlt_ac` 和小网络模块可复用，但**不存在本次已核实的官方 `libero_rlt_stage2` 开箱配置**。这一工程扩展应单独验收，再接经验记忆。

### 3. 两个 DSRL 参照的实际局限

[官方 dsrl_pi0](https://github.com/nakamotoo/dsrl_pi0) 有 `examples/scripts/run_libero.sh`、训练代码和 W&B 链接，适合核对算法与独立实现；需要 JAX／OpenPI／LIBERO submodules。当前 `examples/train_sim.py` 默认写死 `libero_90` 的 task 57，不能把运行脚本当成已覆盖全套 LIBERO。它与 eRLT 的 RLinf checkpoint、chunk 和表征不自动相同。

[verl-vla 的具体配方](https://verl-vla.readthedocs.io/en/latest/reinforcement-learning/dsrl/pi05/libero-spatial.html) 提供 [SFT step-100 权重](https://huggingface.co/Miical/pi05-libero-spatial-sft-step-100)、两个启动脚本和逐次评估；作者报告 Spatial task 9 从 60% 到最佳 82%／末次 74%，task 2 从 74% 到末次 88%。但其验证设置是八 GPU、32 环境，算法还有 CQL、正负 replay 比例等选择。85 分钟是作者该配置下 task 2 的运行时间，不能当成两卡预测。它是较完整的额外参照，不建议仅因数字好看就再次换框架。

### 4. RoboTwin 暂不作为第一迁移站

[RoboTwin 官方仓库](https://github.com/RoboTwin-Platform/RoboTwin) 提供仿真与策略接入；[RLinf RoboTwin 文档](https://rlinf.readthedocs.io/en/latest/rst_source/examples/embodied/robotwin.html) 有 SFT／PPO／GRPO 等路径。RLinf 当前也有 `robotwin_adjust_bottle_openpi_pi05_eval.yaml` 和 `robotwin_adjust_bottle_ppo_openpi_pi05.yaml`。这些能验收基座，但不是 RLT 或 eRLT 的两阶段配方。双臂动作维度、相机、数据资产与接触归因同时改变，会增加当前 baseline 排障变量。

## Stage 1／Stage 2 效果不佳：按故障位置拆开

本轮未访问用户训练机器。09-30 的 Stage 1 8/20 只能作为历史开发点估计；不能据此判定当前代码故障或 RL 算法无效。建议按下表逐关验收，不同时更换环境、基座、RL 目标和记忆模块。

| 关卡 | 固定什么、测什么 | 若失败优先查什么 |
| --- | --- | --- |
| 原始 SFT | 官方任务权重＋匹配 processor，先纯 VLA 20–50 回合；保留每个初态 | 相机顺序／翻转、图像范围、state 语义、delta/absolute、夹爪正负、norm、执行前缀 |
| Stage 1 表征 | 先冻结已经可用的 VLA，只学 encoder/decoder；同帧同噪声核对 reference | 是否误更新 VLA、漏载权重、推理与训练 transforms 不同；重建 loss 不等于动作质量 |
| actor 热身 | 关闭探索噪声，BC 后评估 actor 与 reference；若是结构 residual 则验证零残差等价 | 直接输出动作的 actor 不会因 reference 作为输入就自动复制它；先确认 warmup 能工作 |
| 接管与 replay | 记录 actor/reference/expert 来源、实际执行前缀、被保存 transition 数 | actor 是否真正接管；门控是否一直 false；actor 是否一接管便离开成功轨迹 |
| 在线更新 | critic／actor 更新数、Q/BC 梯度量级、成功 transition 占比、target、终止语义 | reward 稀疏、Q 外推、BC 压制或过弱、chunk 折扣和截断错误、恢复丢 replay |
| 稳定性 | 独立验证初态、多训练 seed；同交互预算、同执行 horizon | 少量评估噪声、训练初态重复、best checkpoint 选择偏差；不能只看重建 loss 或单条成功视频 |

冻结 VLA 的 Stage 1 排障变体不等于原论文联合 SFT 的完整复现；通过后再恢复并比较联合训练。当前小 actor 的 `rlt_ac` 目标也不是标准最大熵 SAC，不能仅凭配置出现 `embodied_sac` 就照搬 SAC 超参数。

baseline 成立后再回到主问题：同一任务中只加入交互 context，先比较 none／recent／固定响应／学到的记忆；再扩大到物理条件变化。LIBERO 成功率提升本身不证明物理经验可迁移；真正的接触条件留出、标签来源与记忆读写边界仍需独立设计。

## 本轮源码版本与检索范围

核查日期 2026-10-03；读取上述十个仓库的默认分支文件树、README 和关键脚本／配置，并核实公开权重清单。版本用于后续审计，不表示已经安装验收。

| 仓库 | 完整 commit |
| --- | --- |
| RLinf/RLinf | `c70606f08cdca259b8dec03d4430926b5b8fac9d` |
| Yyshadow/openpi-RLT | `c1e40ac360185778c98cf20da2820e22d2d415e7` |
| MINT-SJTU/Evo-RLT | `8d02d994cad6bbda3d2ad2ce149bad6157b0bd16` |
| yknxh/rlt-openpi | `6a3cf09472b071516ad9742c15e0a55d9e299b18` |
| RajatDandekar/RL-Token-SmolVLA | `452249c4e21885ff3aaa49c36d9d62b2be9cafff` |
| akashspacesky/vla-rlt | `4cb424a04bcbd4b4176db4568f467823456d67b3` |
| nakamotoo/dsrl_pi0 | `7f48937d4553e95244cd81c79236a3256df80597` |
| AlphaBrainGroup/AlphaBrain | `604924beb77b04b0da49326dfae6ea423a27d28a` |
| verl-project/verl-vla | `c1de826c7c9256e4d9b6900091e4b0e243d16f5e` |
| TihayaKousaka/rlt-openpi-libero | `231c718cab0679f09f5086b2869f70a6e796091d` |

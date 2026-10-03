# eRLT：动作相关 Token 路由，如何改进 RLT

更新：2026-10-03。已核对 v1 方法、实验与实现附录；未复现。来源：[论文 / 版本记录](https://arxiv.org/abs/2610.00913)、[正文及附录](https://arxiv.org/html/2610.00913v1)。2026-10-01 首发；本次未核实独立作者代码发布，不把论文引用的 RLinf 当成 eRLT 开源仓库。

**一句话：eRLT 让小型 RL 网络读取“有助于做动作和判断价值”的 VLA 信息，而不是固定读取重建出来的信息。**

直白地说：大脑仍然冻结，但交给小脑的摘要可以改变。先用示范动作教它提取有用信息，再用真实交互中的 critic 误差继续调整摘要。它改的是表征接口，不是显式学习摩擦定律，也不是给物体注意力热图加人工标签。

完整定位见 [RLT 后续工作关系图谱](../research/literature/rlt-followups.md)；本项目 [RLT baseline 笔记](rlt.md) 区分原论文与 RLinf/π0.5 适配。

**10-03 代码续查**：[十个候选仓库与仿真复现入口](../research/literature/rlt-simulation-baselines-2026-10-03.md) 已核对。C.4 明确真机实现基于 RLinf；C.2 只明确仿真采用 DSRL 风格与公开权重，没有说明确切训练仓库。本轮未核实作者独立 eRLT 仿真代码。RLinf 的 LIBERO DSRL 是可用参照，不应标成作者 eRLT 源码。附录的 LIBERO 权重名为 Pi0，而附近文字称 π0.5，精确复现需澄清配置；RLT*、原 RLT 与各社区变体必须分开。

## 1. 到底改了哪里

| 组件 | eRLT 的设计 | 实现时的含义 |
|---|---|---|
| Token 读取 | 在独立 routing forward 中追加可学习 query；跨多个深度读取 prefix | 原 prefix 不读取追加 token，避免改变基础 VLA 的动作路径 |
| 层融合 | 每层 routing 状态先池化，再按 softmax 权重融合 | token 摘要随输入变化；层权重是任务内共享参数，不是每张图重新预测的 gate |
| 离线监督 | 临时 MLP 从摘要预测专家 action chunk，MSE 训练 | 标签来自已有示范；训练后丢弃预测头 |
| 在线监督 | critic 的 TD loss 周期性更新 router；actor 对摘要 stop-gradient | replay 要能重算新表征，不能只永久缓存旧 token |

论文默认接口：一个 routing token；隐藏维度 **2048**；读取索引 **{0, 3, 6, 9, 12, 15, 18}**；最终输出仍为一个 2048 维向量。路由有效参数为 **2048 + 7 = 2055**，实现分配 2112 个参数，其中多余层 logits 不参与更新。这个数不包含 actor、critic、离线预测头，也不代表计算成本只有小网络级别。（附录 A–C）

一种便于理解的等价记法：

```text
u_i(o) = Pool(第 i 个读取位置的 routing-token hidden states)
alpha = softmax(layer_logits / temperature)
z(o) = sum_i alpha_i * u_i(o)

离线：min MSE(g(z(o)), 专家动作 chunk)
在线：min [Q(z(o), action) - stop_gradient(TD_target)]²
```

`z` 是分布式特征，不应把某一维解释成“摩擦系数”或“接触力”。它也不是动作 token 本身。LIBERO 的临时预测头为 2048→256→256→70，70 对应 10 步×7 维；换本体、动作归一化或 chunk 长度时，标签合同必须相应改变。

## 2. 冻结模型为什么还能训练 routing token

冻结的是 VLA 权重，不是整个计算图。以一般函数写成 `z = F_W(o, e)`：`W` 不更新，输入侧的可学习 token `e` 更新。因此仍要计算 `∂loss/∂e`。

下面是我们的实现提示，**不是作者代码**：

```python
for parameter in backbone.parameters():
    parameter.requires_grad_(False)

# routing 更新时保留计算图；不要将整个 forward 放进 no_grad。
z = routing_forward(observation, learnable_tokens, backbone)
critic_loss = td_loss(critic(z, executed_action), detached_target)
critic_loss.backward()  # optimizer 只收 router 与 critic 参数

# actor 更新不改变 router；具体 action-space/noise-space接口分别实现。
actor_context = z.detach()
```

还需要 target router、target critic 的一致更新及原始观测 replay。论文仿真采用稀疏 router 更新；即使可训练参数很少，穿过冻结 backbone 的反传仍有显存和耗时。先测 step time、峰值显存、吞吐，再讨论是否适合在线真机。

## 3. 结果应该怎样读

| 作者报告，v1 | eRLT | 对照 | 正确解释 |
|---|---:|---:|---|
| 7 个仿真任务平均归一化学习曲线 AUC | 0.626 | RLT* 0.506；DSRL* 0.585 | 相对 RLT* +23.7%；不是成功率增加 23.7 个百分点 |
| USB 真机 AUC / 末窗口成功率 | 0.562 / 90% | RLT 0.269 / 50% | 学习速度与末窗口表现均改善 |
| 排线真机 AUC / 末窗口成功率 | 0.710 / 100% | RLT 0.484 / 100% | 更快学会；最终窗口成功率相同 |

重要协议边界：仿真主比较把不同表征放在统一的 **DSRL 风格噪声空间学习骨架** 中，RLT* 不是原论文整套 action-space RLT；真机使用 RLinf 的 RLT 动作空间流程。不能直接用这张表预测本项目 ManiSkill/π0.5 的提升。真机指标是在线训练预算中的窗口统计，不能冒充多种子独立测试集结果。各方法仍使用示范、任务奖励及人工辅助。（正文 §5，附录 C）

## 4. 对我们的 loss-first 路线，最直接的影响

10-03 主方向已更新为 [Stage 1 经验编码＋双时间尺度记忆＋Stage 2 RL](../research/zeva-rlt-implementation-2026-09-26.md)。下表是其中用于识别监督收益的局部对照，不能替代完整记忆路线。主方案首先保留原 RL token/reference，新增独立经验条件；完整替换 readout 是另一个实验因素。

**研究判断：只说“RLT 的重建损失不好，改成动作相关监督并在线适应”已经不足以构成差异。** eRLT 是必须比较的直接近邻。但“专家想做什么”与“某动作实际造成什么接触后果”仍是不同目标，需要通过实验分离。

先在同一个已验收 RLT 适配实现上做以下小对照，不同时更换 actor、执行时序和奖励：

| 编号 | 同容量 readout 的训练目标 | 回答什么问题 |
|---|---|---|
| B0 | 原实现的重建目标 | 现有 baseline |
| B1 | 专家动作预测，训练后丢弃预测头 | eRLT 启发的低成本控制组；不是完整 eRLT 复现 |
| B2 | 重建＋实际执行动作条件下的后果预测 | 实测后果是否有独立收益 |
| B3 | 专家动作预测＋同一后果目标 | 后果监督能否在 action-relevant 表征之上继续增益 |

B1–B3 匹配 encoder 容量、历史长度、数据、归一化、训练步数与调参预算；额外报告辅助头参数和训练 FLOPs。第一轮固定在线表征。若离线与小预算闭环出现稳定差异，再加“固定／critic 更新”这个正交因素；完整多层 router 作为后续强对照。

建议的后果目标：实际关节变化、末端与物体的相对位移、有效接触建立/丢失事件。仿真可以用状态/接触作为**训练标签**，部署输入仍只含可获得观测。使用真实执行前缀、时间戳和有效掩码；被中断后未执行的 chunk 不生成伪标签。没有触觉时，不能把关节响应写成真实力标签。

关键判据：在封存的摩擦、负载或刚度变化条件下，比较成功率–交互量 AUC、达到预注册目标成功率的交互数、失败类型、人工控制秒数，以及墙钟时间。参数留出但无可辨识反馈时可能根本预测不了，失败不自动证明网络太小。预测误差下降只是中间证据。

## 5. 先做什么，暂缓什么

1. 在当前真实数据/回放接口上打通 B1；按轨迹划分训练与验证，避免邻近帧泄漏。
2. 审计 B2 的动作—时间—后继标签对应关系，独立保存 command、实际执行及控制来源。
3. 只选一个有可靠接触标签的现有任务跑匹配预算 pilot，再决定是否投入完整 eRLT router。

这些是新增研究假设与对照建议，**尚未实现或运行**。无需因一篇新论文同时加入 memory、attention loss、世界模型和 harness；当前目标仍是证明实测交互经验在什么条件下改善 RLT。

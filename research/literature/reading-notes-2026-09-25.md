# 2026-09-25 · 六篇相邻工作速记：未来、几何、注意力与动作接口

> 阅读等级：**初读/讨论笔记，未复现**；为决定下一步实验而写，不代表完成附录、代码和复现实验审查。关联 [阅读总账](reading-ledger.md) 与 [FLARE × RLT 实验草案](../flare-rlt-contact-experiments-2026-09-25.md)。文中“建议”均是本库假设，不是原论文的结果。

| ID / 来源版本 | 一句话 | 与 RLT 研究的关系 |
|---|---|---|
| [P003 FLARE](https://proceedings.mlr.press/v305/zheng25a.html)，CoRL 2025 / PMLR 305 | 让动作生成网络内部的少量未来 token 对齐未来观测特征，同时继续学习生成动作。 | **最直接的未来特征监督对照**；其证据主要是模仿学习性能，不能代替 RLT 在线 RL 的收敛证据。 |
| [P002 Pri4R](https://arxiv.org/html/2603.01549v2)，arXiv v2 | 用训练期可得的 3D 点轨迹作辅助监督，部署时移除特权信息分支。 | 测试几何后果标签的价值；仿真可用物体点轨迹标签，真机需确认估计误差。 |
| [P004 AGRA](https://arxiv.org/html/2606.12217v1)，arXiv v1 | 对齐动作侧使用的视频特征与空间表征，针对“能预测合理画面却没有看准操作区域”的失配。 | 先诊断关键交互区域的注意力及因果敏感性；不等于加一张注意力热图就能学到接触。 |
| [P010 Spline Policy](https://arxiv.org/html/2606.07386v2)，arXiv v2 | 用二次样条系数代替逐步 action chunk 表示连续轨迹。 | 是动作时序参数化对照；首轮固定 RLT 的执行时序，不同时改 action head。 |
| [P005 CometVLA](https://arxiv.org/html/2608.30289v1)，arXiv v1 | 用 GAP token 连接视觉语言基座与连续动作专家，联合离散动作/语言/连续动作目标。 | 紧凑桥接与“physical”监督均有先例；其联合预训练不等于冻结 VLA 的 RLT 在线适配。 |
| [P006 PAR](https://arxiv.org/html/2508.09822v1)，arXiv v1 | 共享视频与动作的 physical tokens，利用视频生成预训练学习联合演化。 | **physical token 这一名称并非本课题首创**；要清楚区分生成 token 与实测后果约束的控制读出。 |

## FLARE：Robot Learning with Implicit World Modeling

**直白地说：** 机器人做动作时顺便练习“动作做完后我会看到什么样的特征”，训练时看到了真实未来来打分；上线后不需要真实未来，未来 token 仍在网络中参与推理。

源论文：PMLR [摘要及出版信息](https://proceedings.mlr.press/v305/zheng25a.html)；作者的 [项目说明](https://research.nvidia.com/labs/gear/flare/)明确未来特征损失与动作 flow matching 同训，测试阶段不计算未来图像的 teacher embedding。动作感知的未来目标由另一个编码器提供；输入未来画面只用于构造训练标签。它不是从若干候选动作的真实反事实中训练出的在线 Q 函数，也没有证明任意物理参数可辨识。

**可借鉴：** 保留原始 RLT 的 frozen VLA 与小 actor–critic，另从已执行前缀的后续观测构造未来表示标签，先训练同容量 readout；对照重构、通用未来特征和实测物体/末端位移。**边界：** FLARE 原架构直接修改动作 DiT；在 RLT 上仅加未来读出是一种新组合提案，不能声称复现 FLARE。其论文报告的 imitation learning 收益不是本项目的在线 RL 收敛收益。

## Pri4R：Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation

**直白地说：** 仿真知道哪些物体表面点在随后怎么动，训练时让机器人的网络学会猜这些点的变化；真实执行时丢掉负责评分的辅助头。

论文 [v2 方法与结果](https://arxiv.org/html/2603.01549v2)使用轻量 point-track head，把训练期特权 4D 监督融入 VLA 表征；摘要报告 RoboCasa / LIBERO-Long 改善。视觉估计、仿真真值和真实触觉是不同来源，训练标签的特权性必须记录。**可借鉴：** 在有物体状态的 RLT 仿真先监督末端相对物体位移 / 点位移，并做 `只用本体历史+动作` 的预测器对照；不要把点轨迹准确率当作接触成功率。

## AGRA：Making Foresight Actionable

**直白地说：** 模型想象的未来画面看着对，动作却可能盯着背景看；AGRA 让连接视频和动作的特征更容易定位正在交互的地方。

论文 [v1](https://arxiv.org/html/2606.12217v1)为世界—动作接口使用表征对齐，报告 attention-in-mask ratio、注意力质心误差和对无关区域扰动的响应。**可借鉴：** 在 RLT 冻结基座上先保存可映射到图像 patch 的特征/归因，标记目标和接触区域；比较成功/失败的归因、遮挡关键区域与遮挡背景后的动作变化。压缩后的 RL token 本身未必保有可直接绘制的空间注意力；热图只能诊断，不能直接推出因果。若后续做监督，需单独设置与相同标注量的遮挡增强对照。

## Spline Policy：A Structured Representation for Robot Policies

**直白地说：** 动作头先输出一条可连续求值的曲线，再按控制频率取点执行，减少固定离散 chunk 的时序僵硬。

论文 [v2](https://arxiv.org/html/2606.07386v2)研究分段二次样条与可选的状态依赖流场解释；这解决轨迹的参数化和时间表达，不自动给模型触觉、摩擦规律或历史记忆。**可借鉴：** RLT 收敛验证完成后，以相同物理执行时长、控制频率和计算预算单独消融“常规 chunk / 样条轨迹”；尤其检查接触瞬间是否因过度平滑而退化。

## CometVLA：Co-Training on an Embodied Data Pyramid towards Physical Understanding

**直白地说：** 一个短的 GAP 中介表示把 VLM 中关于任务与运动的线索送给动作专家，三类损失分别训练语言理解、离散动作和连续动作。

论文 [v1 §3.3](https://arxiv.org/html/2608.30289v1)将 GAP token 放在 VLM 序列中，动作专家跨注意力读取；`L_AR` 是语言自回归交叉熵，`L_fast` 是 FAST 离散动作 token 目标，`L_fm` 是连续动作 flow matching。`L_fm` 的 stop-gradient 保护基座，仍可更新动作头与 GAP 参数；并不是“三种损失都在预测物理规律”。原文将它称为 dedicated GAP token，本笔记**不臆测固定 token 维数/个数可以跨实现通用**。其训练涉及大规模多源联合数据和多机 H200，首轮 RLT 不直接搬运。

## PAR：Physical Autoregressive Model for Robotic Manipulation without Action Pretraining

**直白地说：** 把画面和机器人动作编码到同一序列里，学“接下来的视频和动作”，所以它已经公开使用 physical tokens 这个术语。

[arXiv v1](https://arxiv.org/html/2508.09822v1)讨论视频—动作共享的生成表示；“physical”在此是模型对联合演化表征的命名，不是证明每个 token 显式对应摩擦系数、力或接触模式。**对本课题的写法：** 不声称首创 Physical Token；用“从 RLT 读出的紧凑、动作条件、实测后果监督的 latent”界定机制，靠匹配对照与新任务验证其效用。当前原文可确认 arXiv 预印本，若写投稿/期刊状态须另核对正式出版来源。

## 共同科研判断

未来 latent（FLARE）、未来 3D 几何（Pri4R）、空间对齐（AGRA）、紧凑接口（CometVLA）、生成 physical token（PAR）与样条轨迹（Spline）各有先例。可研究的增量是：**以 RLT 的冻结基座 + 小型在线 learner 为固定起点，让动作条件的实测接触后果监督帮助减少固定成功要求下的交互和专家时间，并在留出接触条件/任务上仍有效。** 与已有方法重合度高，正式写论文前仍需代码与附录审查。

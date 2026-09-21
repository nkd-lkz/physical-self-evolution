# EmbodiedJev：决策概率、物理结果与学习更新必须分开

> 核验日期：2026-09-21。对象为 FBddcz/embodied-jev（行知）；已读官方 README、JEV_EVALUATION、Meta-World 结果和关键控制/预演源码。属于开源系统专题，不是本文已独立复现的学术结果。

[项目仓库](https://github.com/FBddcz/embodied-jev) · [控制实验](https://github.com/FBddcz/embodied-jev/blob/main/docs/JEV_EVALUATION.md) · [Meta-World 协议](https://github.com/FBddcz/embodied-jev/blob/main/docs/BENCHMARK_EXPERIMENTS.md)

## 1. 它是什么

工作台把模型候选选择接到 MuJoCo 控制、结果判定与轨迹记录。可选技能、短步 XYZ 与分层控制。当前 Jev 接口读取结构化文本；RGB-D 检测坐标与直接图像输入是不同模式，不能混写为 Jev 端到端视觉控制。候选动作、几何计算、IK 和物理预演由程序提供。[README](https://github.com/FBddcz/embodied-jev/blob/main/README.md)

项目展示的是观察→选择→执行→再观察。这个回路本身不证明模型权重随经验更新，也不证明已经获得可迁移物理表征。

## 2. 值得借鉴的三个接口

| 接口 | 已核验实现 | 对 RLT 的借鉴（研究分析） |
|---|---|---|
| 明确的动作选择空间 | 分层时先选子目标，再选 XYZ/夹爪通道；程序计算步长 | 将“选择何种恢复模式”与“连续动作怎么执行”作为可独立评估的变量 |
| 实际执行证据 | 记录当前接触、抓持、实际位移与目标状态 | token 可监督动作后果，而非只重建发出的命令 |
| 仿真预演 | 在仿真副本检查候选，拦截配置的碰撞/失抓；代码将其标为 simulator filter | 用来产生训练标签或 oracle 上界；不能默认为部署时可得的模型能力 |

源码入口：[hierarchical.py](https://github.com/FBddcz/embodied-jev/blob/main/src/embodied_jev/hierarchical.py)、[planning.py](https://github.com/FBddcz/embodied-jev/blob/main/src/embodied_jev/planning.py)、[physics.py](https://github.com/FBddcz/embodied-jev/blob/main/src/embodied_jev/physics.py)。本轮是静态代码核验，未执行其状态克隆或仿真。

## 3. 结果与评估边界

早期两个同 seed 搬运回合满足终态判定，但下放时均失抓。最新 Meta-World 开发子集报告 Jev 和 GPT-6 Astra 各 5/6，三任务各两个 seed，输入为结构化特权状态。分层版本同时改变状态表达、提示和控制阶段；直接控制历史组预算不同。这些结果不能推导通用成功率，也不能证明单一分层模块因果有效。[控制实验](https://github.com/FBddcz/embodied-jev/blob/main/docs/JEV_EVALUATION.md) · [开发子集结果](https://github.com/FBddcz/embodied-jev/blob/main/docs/results/metaworld-hierarchy-v2-2026-09-21/RESULTS.md)

最新协议还明确抓放成功阈值不要求松手撤离。对接触操作论文，应该同时报告官方 success 与更细的持抓、稳定支撑、松手后保持等指标，不能悄悄换官方判定。旧 JEV_RESULTS.md 的代码发布状态与当前源码不一致，故不据旧文字宣称目前缺少分层实现。

## 4. 概率不是物理成功率

候选概率表达接口对选项的偏好；没有用执行结果校准时，不能解释为动作成功概率，更不能将 X/Y/Z/夹爪通道概率相乘当作联合任务成功率。

对本项目可改成一个可检验预测任务：给定部署可得历史、候选动作与执行时长，预测实际是否保持抓持、是否恢复到可继续任务的状态。标签来自独立物理执行；报告 Brier score、可靠性曲线和失败召回。若只预测最终成功概率，其数学角色接近有限时域 value，不能靠“直觉”命名形成创新。

## 5. 与当前主线如何连接

先做离线 probe，验证现有 RLT token、同容量历史编码与 action-side token 是否能区分可恢复/不可恢复偏差。若结果支持，再用于采集或筛选恢复经验。不要同时加入云端 Jev、规划器、记忆和新 token，否则无法知道改进来源。

自进化的最小证据仍是：同预算下新经验使参数或持久记忆更新，独立评测改善；冻结更新组没有同等改善；旧任务保留可衡量。详细方案见 [研究设计](https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=research/xpace-jev-rlt-ideas.md)。

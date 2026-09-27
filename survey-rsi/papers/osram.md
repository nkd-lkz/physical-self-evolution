[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Online Sim-to-Real Adaptation via Closed-Loop System Modeling

> **一句话：** OSRAM 在部署后用少量真实 reference–response 轨迹微调闭环模型，再在线修正参考命令；它提供真机持久适应证据，但底层策略始终冻结，改进发生在控制接口而不是策略本身。

短名：OSRAM　作者：Yuhao Huang, Samuel A. Moore, Boyuan Chen　首次发表：2026-09-24　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.28878](https://arxiv.org/abs/2609.28878)　项目页：[General Robotics Lab / OSRAM](http://generalroboticslab.com/OSRAM)　最后核查日期：2026-09-27

![OSRAM 原文 Figure 2](https://arxiv.org/html/2609.28878v1/pipeline.png)

*图注：OSRAM 先在域随机化仿真中元训练闭环 command–response 模型，部署后用真实轨迹微调，再由 MPPI 选择能补偿系统偏差的参考命令。来源：原文 Figure 2，arXiv v1。*

## 解决什么问题

sim-to-real 策略即使保持稳定，也可能因质量、摩擦或执行器增益偏差产生系统性跟踪误差。直接重训策略或完整辨识物理动力学代价较高。论文把已部署机器人与控制器视为统一闭环系统，尝试只从任务级输入输出修正误差。

## 核心方法

OSRAM 用 Reptile 风格元学习在随机动力学仿真中训练闭环 meta-dynamics，输入历史参考命令与真实响应，输出未来响应。部署后采集少量 reference–response 数据微调该模型；MPPI 在滚动窗口内搜索新参考轨迹，使模型预测的真实响应逼近原目标，同时惩罚过大偏移和不平滑命令。PPO 底层策略不更新，持久变化是闭环模型参数；运行时变化是每步参考命令。

## 主要结果

- **仿真速度跟踪：** LimX Tron1 在 0.4/0.7/0.9 m/s 下，OSRAM 的 RMSE 为 0.0733/0.0929/0.1560，成功率均为 100%；RNN-Adapt 为 0.1415/0.1614/0.2082，Res-Adapt 为 0.1421/0.1833/0.2062。两种 open-loop 动力学基线在 0.9 m/s 都是 0% 成功。
- **硬件速度跟踪：** 0.7 m/s、每方法 5 次真机试验，未做 dynamics adaptation 的 RMSE 为 0.2847，RNN-Adapt 为 0.2109，OSRAM 为 0.2014，OSRAM 加 RNN-Adapt 为 0.1962；四者成功率均为 100%。误差只在成功试验上平均，成功率使用全部试验。
- **硬件 loco-manipulation：** 端执行器正弦轨迹的 x 方向 RMSE 从 36.94±3.02 cm 降到 3.11±0.31 cm，y 方向从 3.48±0.45 cm 降到 2.72±0.23 cm。单张 RTX 4090 上规划 50 Hz、训练 2 Hz；速度任务约 30 次梯度步后预测误差趋稳，loco-manipulation 使用 70 步。

## 综述可借鉴之处

OSRAM 说明“部署后改进”不仅可以改策略，也可以改**机器人—控制器闭环模型和动作接口**。综述可用它与残差策略、RMA 式隐变量适应并排：比较相同目标域数据预算下，改低层动作、隐状态、世界模型还是 reference interface。它也提醒评价必须同时报跟踪误差和失败率，不能只对成功试验统计精度。

## 证据边界

真机每设置 5 次，样本小；研究集中在低维 reference space 和系统性跟踪偏差，不涉及开放词汇任务或高层技能积累。更新后的模型可在部署中继续使用，但原策略冻结，也没有跨多个任务序列的遗忘/迁移评价。采样规划对超参数敏感。它是持续部署适应和模型—控制支撑组件，不是策略 RSI 或递归改进器。

## 原文定位

§III-A–C 与 Algorithm 1；§IV-A–F；Figures 2–5；Tables II–III；§V 限制；采用 arXiv v1。全文方法、仿真与硬件协议、算力和表格已核查；未复现。

标签：闭环模型 / 真机跟踪反馈 / 部署后持久更新 / 自动微调与规划 / LimX Tron1硬件 / 任务指标 / 策略冻结 / 支撑组件。

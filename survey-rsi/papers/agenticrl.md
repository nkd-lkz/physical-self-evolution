# AgenticRL: Agentic Reinforcement Learning with Self-Refinement for Complex UAV Navigation

作者：Roohan Ahmed Khan；Yasheerah Yaqoot；Amir Atef Habel；Muhammad Ahsan Mustafa；Dzmitry Tsetserukou　|　arXiv v1：2026/06/02；采用v4：2026/09/18

[论文](https://arxiv.org/abs/2606.03963) · [采用版本 v4 全文](https://arxiv.org/html/2606.03963v4) · [PDF](https://arxiv.org/pdf/2606.03963v4)

**收录：**2026-09-22　**类别：**核心策略改进 / 奖励代码自精炼 / UAV / 仿真到真机 / 版本修订　**阅读状态：**v4方法及指定实验/表格已核查；未复现。

![Figure 2：AgenticRL系统架构](https://arxiv.org/html/2606.03963v4/images/sys_arch_v2.png)

*原文Figure 2：任务落地后，奖励生成、PPO训练、行为诊断和奖励再生成组成离线闭环，保留最佳策略后部署。[原图](https://arxiv.org/html/2606.03963v4/images/sys_arch_v2.png)，版权归原作者。*

**解决什么问题：**一次性LLM奖励代码即使语义合理，也可能诱发停滞、碰撞或投机行为；广泛采样候选又昂贵。论文希望用策略实际失败证据定向修改奖励。

**核心方法：**角色化代理先固定任务、动作/观测接口、终止条件和诊断标准；每轮生成Python奖励、用PPO训练、在随机场景评测，把行为、几何和安全指标整理成诊断包，再结合当前奖励和场景图像生成修改指令。修订并非单调，因此系统保留满足任务标准的最佳策略。

**主要结果：**八项UAV任务各100次仿真；其中五项线速度任务各10次真机。五项任务平均仿真成功率从37.2%升至96.4%，真机汇总成功率90.0%，S2R比率93.4%。同预算设置下，racing/clutter成功率为100%/88%，Eureka为91%/75%，Text2Reward为0%/19%；AgenticRL分别只训练2/3个PPO候选，但输入上下文明显更多。

**综述可借鉴之处：**它适合作为“失败诊断→可执行奖励修改→重新训练→独立评测→最佳保留”的闭环案例，并清楚展示搜索预算、非单调改进和sim-to-real验证。可与Eureka、Text2Reward、自动研究循环并列，讨论改进对象是奖励程序而非基础模型本身。

**证据边界：**比较实验在每场景固定PPO训练种子，每个奖励候选只训练一次，不能代表跨种子稳健性。环境终止、观测空间、安全约束和任务配置仍需人工指定；真机使用Vicon评测，body-rate任务的PX4部分为Gazebo SITL。更新发生在离线任务特定循环，没有跨任务长期累积，也没有让诊断/改进器本身递归提升。

**原文定位：**§III–VI；Figures 2、5、8–9；Tables II–V。训练预算为每奖励10M–70M环境步，按任务而异。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-22.md)

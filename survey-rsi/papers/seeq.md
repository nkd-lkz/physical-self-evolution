# SeeQ: Training Generalist Value Functions for Long-Horizon Robotic Manipulation

短名：SeeQ　作者：Saksham Singh, Zheyuan Hu, Max Sobol Mark, Jeffrey Yu, Zackory Erickson, Aviral Kumar　首次发表：2026-09-18　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.22085](https://arxiv.org/abs/2609.22085)　项目链接：[作者项目页](https://saksham002.github.io/seeq/)　模型：[SeeQ-3B](https://huggingface.co/CMU-AIRe/SeeQ-3B/)　最后核查日期：2026-09-23

![SeeQ框架图](https://arxiv.org/html/2609.22085v1/seeq_teaser.png)

*图注：SeeQ先解释当前子任务，再为动作块估值并从VLA的多个候选中选择；原始来源为论文Figure 1，arXiv v1。*

**解决什么问题：** 长程操作的基础策略容易在局部错误后继续执行；现有reward/value通常对新任务需要大量专用数据。论文希望训练一个可迁移的视觉语言Q函数，给冻结VLA提供推理时方向。

**核心方法：** VLM-backed Q先输出当前活跃子任务语言，再估计子任务Q；用TD best-of-N目标训练。部署时基础策略提出N=8个动作块，执行Q值最高者。critic先在RoboCOIN的131个任务、约23万step预训练，下游再用1–2万step微调；任务策略是各自训练2万–7万step的π0.5。

**主要结果：** 四项真机任务包括三项双xArm7和一项双YAM，控制频率60 Hz，每项24次试验。基础策略到SeeQ选择后的成功次数分别为10→22、10→15、9→17、5→10，平均成功率35.4%→66.7%。不同任务的数据量并不相同，例如grocery为473个episode、lego为97个episode；RaC数据混合人工干预与遥操作专家。

**综述可借鉴之处：** 是“验证器/价值模型如何进入改进环”的强支撑组件，可与reward model、过程验证器和best-of-N动作搜索统一讨论；它也提示评测必须把策略参数学习与推理时选择分开。

**证据边界：** 部署时冻结基础策略，只做候选动作选择，并未从部署经验持续更新策略；critic的预训练和下游微调发生在部署前。部分基础策略使用人工定义的子任务提示。因此应标为支撑组件，不作为独立RSI实证。

**原文定位：** arXiv v1 §3、§4.1–4.4，Appendix A.1/A.3/A.4，Figure 1，Tables 1/3/5–7。方法、数据量与指定真机结果已读；未复现。

标签：价值函数 / 离线机器人数据 / 推理时best-of-8 / 固定策略 / 真机 / 验证器与奖励支撑组件。

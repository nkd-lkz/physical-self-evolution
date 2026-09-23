# ForceRFT: Refining VLA Actions through Force-Guided Residual Reinforcement Learning

短名：ForceRFT　作者：Yichen Wang, Chaoyang Zhang, Xuqi Su, Jun Ma, Haiyue Zhu, Xiaocong Li　首次发表：2026-09-19　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.22840](https://arxiv.org/abs/2609.22840)　项目/代码：未核实到公开入口　最后核查日期：2026-09-23

![ForceRFT框架图](https://arxiv.org/html/2609.22840v1/1.png)

*图注：冻结的力条件VLA先验、残差actor/双critic、人类纠正与自主transition的分流训练；原始来源为论文Figure 1，arXiv v1。*

**解决什么问题：** 接触丰富操作中，视觉动作策略难以感知插入、套环、擦拭等细微接触状态；直接重训大VLA又昂贵且容易破坏原能力。论文只学习一个力引导残差来修正基础动作。

**核心方法：** 冻结force-conditioned SmolVLA，把状态、基础动作、当前六维wrench与wrench差分送入轻量残差actor和双critic。人类接管片段用于残差行为克隆；经操作者/结果检测器确认的自主transition用于TD学习。接管边界禁止bootstrap，避免把人类动作误归因为自主策略价值。持久更新对象是残差actor与critic，不是基础VLA。

**主要结果：** 平台为FR3、Robotiq 2F-85、OnRobot HEX-E力矩传感器以及D435i/D405相机；每任务50条示范，在线交互预算30分钟，三个任务每种设置各30次自主评测。成功次数依次为：SFT 7/10/2，force prior 12/17/4，残差模仿19/22/8，ForceRFT 25/27/11（插接/套环/擦拭）。论文同时报告接触质量等过程指标；擦拭任务的绝对成功率仍明显较低。

**综述可借鉴之处：** 可作为“保持基础模型、在线演化低容量适配器”的代表，说明更新范围本身是安全—可塑性折中；也适合与全参数VLA-RL、人类纠正、force feedback三条证据链比较。

**证据边界：** 依赖人类接管以及固定的结果确认/检测流程；任务特定、未测跨任务保持，残差容量也限制可修正范围。它实现的是策略组件的部署期更新，不是改进器递归增强；30分钟与30次评测不足以证明长期稳定性。

**原文定位：** arXiv v1 §III–V，Figure 1，Tables I/II。方法、三项真机实验和表中分母已读；未复现。

标签：残差策略与critic / 力觉、结果验证、人工纠正 / 跨rollout持久更新 / 人在环 / 真机 / 核心自我改进。

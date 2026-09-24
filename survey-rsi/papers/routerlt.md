# RouteRLT: Learning When and Which RL Specialist Should Control a VLA Policy

短名：RouteRLT　作者：Chongyu Zhu, Jaden Hinds, Hyegang Kim, Juan Sebastian Rojas, Ramy Elmallah, Chi-Guhn Lee　首次发表：2026-09-22　采用版本：arXiv v1　发表状态：IROS 2026 workshop accepted

论文链接：https://arxiv.org/abs/2609.26467　最后核查日期：2026-09-24

![RouteRLT真机线缆拾取与插入部署](https://arxiv.org/html/2609.26467v1/figures/routerlt_deployment.png)

*图注：原文真机部署图，展示线缆拾取与插入阶段的VLA/专家切换；来源为arXiv v1。方法总览见原文系统图。*

**解决什么问题：** 端到端VLA在精细接触阶段常不够稳定，而为整条任务重训又昂贵。论文研究何时、在哪个阶段把控制权交给RL专家，同时避免动作块切换产生陈旧动作。

**核心方法：** 冻结SmolVLA通用策略，预先训练若干阶段专用的RLT actor-critic专家。路由器只读冻结VLA的潜变量时间窗，输出阶段/专家选择；滞回和最短驻留时间减少抖动，边界感知动作块管理器在切换时丢弃旧动作后缀。训练路由器时使用特权阶段标签，部署时不再使用该标签。部署阶段不从新经验更新VLA、专家或路由器。

**主要结果：** 在LIBERO多物体仿真任务上，SmolVLA成功率85.00%，RouteRLT为92.22%，接近使用真阶段标签的Oracle；按每1000步成功数计，相对SmolVLA提高14.3%，但仅看拾取后的完整任务差距约0.56个百分点。Trossen真机线缆拾取与插入中，通用策略完整轨迹成功率6.7%，RouteRLT为35.0%；SmolVLA和Oracle各30次，RouteRLT 20次。真机协议含操作员对齐/交接，不能视为完全自主闭环。

**综述可借鉴之处：** 适合放在“模块化可塑性与能力保持”或“VLA-RL支撑组件”：冻结通用能力、让小专家承担可塑性，再由显式路由解决接口问题。它为ForceRFT的“冻结骨干+可塑残差”提供另一种系统分工对照。

**证据边界：** 论文证明的是预训练专家的部署期选择，不是部署后学习；没有跨episode持久改进，也没有改进器自身增强。仿真和真机样本量不同，真机还含人工交接。应作为RSI闭环的策略组合组件，而非核心自我改进证据。

**原文定位：** §III-A–E方法，§IV-A–B仿真与真机；Table II和deployment figure；真机试验次数与对齐协议见实验设置。方法及指定结果已读，未复现；未核到可公开代码。

标签：专家路由 / 预训练RL专家 / 部署期固定 / 半自主 / 真机+仿真 / 作者自评 / 支撑组件。

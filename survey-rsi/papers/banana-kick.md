[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Banana Kick: Response-Informed Skill Evolution for Humanoid Soccer

> **一句话：** 根据物理响应调整奖励目标，使普通踢球先验学出弧线球。

**首次公开：** 2026-09-23　**采用版本：** arXiv v1　**核查日期：** 2026-09-24　**状态：** 预印本；方法及指定实验已核查，未复现。

**作者：** Zhang, Hao E.；Geng, Ruize；Haque, Raihan；Zbiss, Khalil；Luo, Guanyang；Wang, Hui-ping；Tseng, H. Eric；Zhao, Ding

[摘要与版本](https://arxiv.org/abs/2609.27269) · [全文 v1](https://arxiv.org/html/2609.27269v1) · [PDF](https://arxiv.org/pdf/2609.27269v1) · [论文所列项目地址](https://haozhang-thu.github.io/bananakick/)（2026-09-24 返回 404；结论依据论文正文）

**综述定位：** 核心自我改进 / 目标演化 / 技能学习 / 仿真到真机

![Banana Kick / RISE 原文图](https://arxiv.org/html/2609.27269v1/figures/fig_method_overview.jpg)

*原文 v1 Figure 2：普通踢球先验、物理响应诊断、受限目标提议、策略训练和更新验收。 [原图](https://arxiv.org/html/2609.27269v1/figures/fig_method_overview.jpg)，版权归原作者。*

## 解决什么问题

 一个稳定的普通踢球策略可能始终探索不到产生旋转的新接触方式；当奖励在当前物理响应附近几乎没有有效梯度时，单纯加强最终目标或增加训练并不一定有用。

## 核心方法

 Response-Informed Skill Evolution（RISE）从模仿得到的普通踢球先验出发，观察接触位置误差、切向速度、旋转和出球速度。根据缓存响应对奖励尺度/权重提议排序，限制目标变动范围，热启动 PPO 训练；只有物理响应有进展且正确触球可靠性过门槛，才保留新目标和策略。失败提议缩小信任域。注意：这里的 RISE 与既有报告的 **RISE: Self-Improving Robot Policy with Compositional World Model** 不是同一论文。

## 主要结果

 五个种子，每种子使用 **4096 个匹配评测情境**，初始球位置扰动 ±5 cm。以统一固定评分比较，RISE 得分 1093.7，学习进展课程基线 912.8，约高 19.8%；联合物理目标覆盖率为 50.88% 对 15.23%。区间主要基于匹配情境 bootstrap，不能把数千情境视作独立训练种子。G1 硬件部署时策略冻结，作者报告 **30 次动捕记录的真机试验**，展示图只画其中 20 条轨迹；真机保留弯曲飞行方向，没有硬件在线学习。

## 综述可借鉴之处

 可用来论证自我改进对象包括“训练目标”，并展示以物理响应验收能力变化的方式。适合与 AgenticRL 的奖励代码修改、自动课程学习比较：目标参数怎么提议、是否训练验证、什么标准决定留下更新。

## 证据边界

 依赖预设响应通道、校准物理模型、普通踢球先验和人工定义验收门槛；外层目标提议与接纳规则没有自我修改。适合归入有反馈的目标—策略共同更新，尚不构成改进器递归增强。未核得统一总训练墙钟预算，不能将缓存提议排序的节省扩大成整套算法等计算量优势。

## 原文定位

 §III，§IV-A–D；Figure 2、Figures 4–11；Tables I–III。 已核对原文方法、指定结果和样本口径；未复现代码。

**标签轴：** 更新对象：奖励权重/尺度与 PPO 策略；反馈：接触/速度/旋转响应＋可靠性门槛；保留范围：仿真迭代保留；硬件冻结策略；物理证据：G1 人形机器人；仿真训练→真机。

[证据对照](../evidence-map.md) · [综述提纲](../survey-outline.md) · [本轮记录](../daily/2026-09-24-follow-up.md)

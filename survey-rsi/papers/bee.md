[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# BEE: Intervention-Adaptive Real-World Reinforcement Learning with Vision-Language-Action Models

> **一句话：** 把人类接管的不确定性变成逐维约束，保留在线学习的残差策略。

**首次公开：** 2026-09-23　**采用版本：** arXiv v1　**核查日期：** 2026-09-24　**状态：** 预印本；方法及指定实验已核查，未复现。

**作者：** Zhao, Weihui；Yan, Xiaohan；Wan, Zunian；Du, Xuan；Chi, Zhaozhan；Mao, Jianbo；Wu, Ruipu；Yang, Rushuai；Li, Houlin；Yang, Shukai；Wu, Jing；Yan, Yuxiang；Liu, Yongcheng；Li, Chuankang；Ren, Guanghui；Shan, Wei；Yao, Maoqing

[摘要与版本](https://arxiv.org/abs/2609.27450) · [全文 v1](https://arxiv.org/html/2609.27450v1) · [PDF](https://arxiv.org/pdf/2609.27450v1)

**综述定位：** 核心自我改进 / 在线VLA-RL / 人在环 / 真机与仿真

![BEE 原文图](https://arxiv.org/html/2609.27450v1/teaser_tasks_norobot.png)

*原文 v1 Figure 2：三项真机接触操作与一项仿真任务。HTML 中 Figure 1 框架图未提供可独立嵌入的图像资源；请在 PDF 中查看 Figure 1。本图是任务展示，不冒充框架图。 [原图](https://arxiv.org/html/2609.27450v1/teaser_tasks_norobot.png)，版权归原作者。*

## 解决什么问题

 冻结 VLA 后直接做在线强化学习，容易在接触精度要求高的阶段退化；直接模仿人类纠正，又会把不同维度、不同状态下的不确定纠正一视同仁。

## 核心方法

 冻结任务微调后的 π0.5 及状态特征接口，学习叠加在 VLA 动作上的残差策略。纠正模型根据状态和 VLA 原始提议，预测人类残差的均值与逐维方差；以 Mahalanobis 约束对稳定纠正维度收紧、对高方差维度放宽，再学习状态相关的约束乘子。执行与接管数据持续回放，参数保留到后续 episode；基础 VLA 权重不更新。

## 主要结果

 三项真机任务均为 20 个接管种子 episode＋70 个在线 episode；LIBERO-PRO 仿真为 20＋25。每任务做 **3 轮×20 次**自主评测，误差条来自评测轮次，不能称为三次独立训练。BEE 的手机充电、零食悬挂、布料对齐、碗放置成功率分别为 100%、85%、90%、90%；同预算下作者实现的 RLT 为 58.3%、21.7%、73.3%、76.7%。任务 SFT 使用每任务约 200–900 条示范，在线训练主要使用单张 RTX 4090D。

## 综述可借鉴之处

 放入“人类反馈如何进入自主策略改进”和“冻结基础策略、更新外挂组件”。与 RAPolicy、ForceRFT 对照时，重点比较人工投入、更新对象及机器人交互预算，而非仅比较最终成功率。它给出了“反馈可信度决定更新幅度”的具体实现。

## 证据边界

 手机充电、布料对齐只报告精细接触阶段成功率，另两项才是全任务成功率，因此论文总体 91.2% 不能写成通用长程任务成功率。接管率是训练期间被接管的控制步比例，布料任务仍达 65.3%；仿真接管率也未低于 RLT。RLT 为作者复现，在约三倍数据时手机任务可达 96.7%，结论依赖预算。存在人工完成标签/接管，未证明全自主运行、跨任务持续积累或改进器递归增强。

## 原文定位

 §§III–V，Figure 1，Table I；Appendices A–F、Tables II–IV。 已核对原文方法、指定结果和样本口径；未复现代码。

**标签轴：** 更新对象：残差策略、critic、纠正分布、约束乘子；反馈：人类接管＋任务完成标签；保留范围：跨 episode 保留参数；同任务在线训练；物理证据：三项真机＋一项仿真。

[证据对照](../evidence-map.md) · [综述提纲](../survey-outline.md) · [本轮记录](../daily/2026-09-24-follow-up.md)

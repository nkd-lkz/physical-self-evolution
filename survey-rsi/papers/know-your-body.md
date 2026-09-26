[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Know Your Body: A Harness for Direct and Self-Improving Robot Control with VLMs

> **一句话：** 在冻结 VLM 权重的情况下，KnowBody 把机器人的动作—身体关系写成可查询、可验证、可跨 episode 修订的 body model；真机四任务固定预算成功率为 12/16，而原生 harness 为 4/16。

短名：KnowBody　作者：Zeyu Lou、Yanhong Zeng、Yong Wang、Chenyang Si　首次发表：2026-09-22　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.28530](https://arxiv.org/abs/2609.28530)　项目链接：[作者项目页](https://loule0-0.github.io/KnowBody/)　最后核查日期：2026-09-26

![KnowBody 原文 Figure 2](https://arxiv.org/html/2609.28530v1/fig9_harness.png)

*图注：原文 Figure 2（v1）。在线状态 `M` 服务当前决策；跨 episode 的 body model `B` 与知识 `K` 只有通过验证后才发布，依赖旧 body estimate 的知识会被重新检查。*

## 解决什么问题

通用 VLM 能理解“要做什么”，却不知道特定机器人、工具与相机之间怎样把命令变成物理效果。直接把历史塞进上下文既难复用，也会让已经失效的身体知识继续传播。

## 核心方法

系统先用一条与下游任务无关的轨迹建立部分 body model，记录控制量、末端执行器、腕部视野地标、工具作用点等动作相关关系。每次执行把计划、实际运动和观测变化写入 episode 状态；跨 episode 更新先形成候选 body relation，再通过专门探测或后续交互核验。若 body estimate 改变，依赖它的任务知识会被撤回或重验。VLM/GPT6 权重始终冻结；可留存更新发生在 harness 的模型、规则和证据库。

## 主要结果

真机平台为 Franka Research 3、Robotiq 2F-85、腕部 ZED Mini 和两台第三人称 ZED 2i。固定预算协议含鸭子放置、苹果推动、写字和倒水四任务，每方法每任务 4 次，共 32 次；跨 episode 更新关闭，只比较同一初始化后的 harness。KnowBody 完成 12/16（75%），原生 Codex harness 完成 4/16（25%）；分任务由 1/4→4/4、2/4→3/4、1/4→3/4、0/4→2/4。两者都成功的三项任务中，KnowBody 的成功轨迹平均少 17–44% 规划轮次。

开启持久更新后，论文只画出每项任务前五次“记录到的成功”：第 1 次到第 5 次成功所需轮次分别从 17→10、19→9、45→32、71→48，下降 29–53%。中间失败也参与更新但没有画在横轴，因此不能把该曲线直接解释为总尝试样本效率。

## 综述可借鉴之处

它是“冻结基础模型、演化可执行 harness”的直接真机例子，可与参数更新型 RAPolicy/BEE 以及代码演化型 RACaP 并列。更重要的是，论文把**候选修订、证据核验、依赖重检和发布**拆开，适合用来定义非参数持久自我改进的最小闭环。

## 证据边界

只有一台机器人、四个任务；固定预算主对照关闭跨 episode 更新，证明的是初始化 harness 的作用。持续曲线没有匹配基线且只索引成功回合。更新的是 body model 与知识规则，不是 VLM 权重，更没有修改生成/验证更新的算法本身，所以不是严格的改进器递归增强。

## 原文定位

全文方法与指定实验已读，未复现。方法见 §§3–4、Figure 2；平台与协议见 §5、Figures 4–5；固定预算结果见 Figure 5；DROID 对照见 Table 1；提示编译、证据与验证细节见附录。

标签：harness / 身体模型 / 交互证据 / 跨 episode / 自动候选＋验证发布 / 单机真机 / 环境成功 / 核心自我改进。

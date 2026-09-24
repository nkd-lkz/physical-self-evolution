[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# DexPIE: Stable Dexterous Policy Improvement from Real-World Experience

短名：DexPIE　作者：Ruizhe Liao, Wenrui Chen, Liangji Zeng, Haoran Lin, Fan Yang, Kailun Yang, Yaonan Wang　首次发表：2026-06-08　采用版本：arXiv v2（2026-09-18）　发表状态：预印本

论文链接：[arXiv:2606.09615](https://arxiv.org/abs/2606.09615)　项目链接：[作者项目页](https://siiuuuuuu.github.io/DexPIE)（arXiv列出；2026-09-23直开失败）　最后核查日期：2026-09-23

![DexPIE总览图](https://arxiv.org/html/2606.09615v2/teaser.png)

*图注：DexPIE从真实部署的失败、干预与中间阶段经验中继续改进灵巧策略；原始来源为论文开篇teaser，arXiv v2。*

## 解决什么问题

 灵巧手策略部署后会遇到示范数据未覆盖的状态，单纯扩充成功示范既贵又浪费失败轨迹中的信息。论文研究如何把失败、人工干预和部分进展一起转化为稳定的策略更新信号。

## 核心方法

 以阶段化DAgger从初始/中间状态收集失败—纠正轨迹；异步推理采用相对动作前缀一致性以减少执行不连续。distributional critic用Monte Carlo目标估计连续最优性，diffusion policy再以classifier-free guidance按最优性条件生成动作。更新写入策略，是真实经验驱动的持久改进。

## 主要结果

 UR5六自由度机械臂加Inspire六自由度手、两相机，三项真机任务各评测50次。初始示范为41/30/43条；后训练轨迹61/37/59条，其中人工干预17/15/27、失败13/11/15，总采集约55.4分钟，且只做一轮采集—更新。论文称相对BC平均成功率提高37.3个百分点、进度提高33.5个百分点；与RECAP使用同一后训练数据，HG-DAgger只学习成功数据。

## 综述可借鉴之处

 它把部署日志从二元成功/失败扩展为连续进展与纠正信号，适合“经验如何转化为可学习监督”章节；真实采集构成也便于统一比较人工预算、失败比例与单轮收益。

## 证据边界

 依赖人类干预与任务阶段设计；只做一轮改进，没有多轮递归闭环、跨任务保持或未知任务迁移证据。37.3是百分点口径且同时受采集协议与系统一致性改进影响，不能解释成完全自主RSI。

## 原文定位

 arXiv v2 §IV-A–C、§V，Figures 1/2/5/7；每任务50次测试及数据构成表。方法、指定结果和版本变化已读；未复现。

标签：灵巧策略与critic / 失败、进展、人工干预 / 单轮持久更新 / 人在环 / 真机 / 核心自我改进 / 版本修订。


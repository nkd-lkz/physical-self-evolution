[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# MessyMem: Learning-from-Doing Memory for Mobile Manipulation

作者：Banwasi, Anuva；Muckelroy III, William；Sundaresan, Priya；Zhao, Linfeng；Bohg, Jeannette；Ho, Cherie　|　arXiv所列日期：2026/09/14（采用版本见下方链接）

[论文](https://arxiv.org/abs/2609.15976) · [采用版本 v1 全文](https://arxiv.org/html/2609.15976v1) · [PDF](https://arxiv.org/pdf/2609.15976v1)

**收录：**2026-09-21　**类别：**核心持续改进 / 持久记忆 / 移动操作 / 仿真与真机　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 2：场景图、交互分析、关键帧与检索规划闭环](https://arxiv.org/html/2609.15976v1/figs/approach_v2.png)

*原文Figure 2：场景图、交互分析、关键帧与检索规划闭环。[原图](https://arxiv.org/html/2609.15976v1/figs/approach_v2.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

## 解决什么问题

机器人发现抽屉锁住、物体被挪动后，能否让之后的任务利用这些交互知识？

## 核心方法

持久3D场景图保存物体、位置和交互揭示的属性，关联关键帧保留细粒度视觉证据；交互分析器把执行结果写回图，检索器在新任务中取回相关知识和图像供规划使用。

## 主要结果

25项连续任务的仿真中，平均任务进度80.0%，图加交互分析的消融为65.2%，RoboEXP为51.1%；Table 1按每方法50次试验报告区间。真机办公室连续搜索的5次试验中，完整方法总体进度1.00。

## 综述可借鉴之处

可以作为“跨任务留存经验”比“单次任务重试”更强的实例，与Zeva、AGM对照；重点比较保存范围、交互事实与视觉证据的互补。

## 证据边界

80%是任务进度，不是整条25任务序列成功率。真机样本少；检测仍用闭集提示，低层技能未在部署中学习，记忆更新器也未递归优化。

## 原文定位

§3–4、Tables 1–2、Limitations；Appendix C.1明确不重置记忆和环境。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)


# Show-Harness: Just a VLM Agent Can Play Robots

作者：Chen, Yanzhe；Bai, Zechen；Cao, Zhijun；Zeng, Wenzheng；Lin, Kevin Qinghong；Lin, Yiqi；Liang, Guoqiang；Ma, Kevin Yuchen；Huang, Qiming；Shou, Mike Zheng　|　arXiv所列日期：2026/09/09（采用版本见下方链接）

[论文](https://arxiv.org/abs/2609.10522) · [采用版本 v1 全文](https://arxiv.org/html/2609.10522v1) · [PDF](https://arxiv.org/pdf/2609.10522v1)

**收录：**2026-09-21　**类别：**边界案例 / 语义动作接口 / harness / 真机　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 3：感知—推理—动作的模块化执行架构](https://arxiv.org/html/2609.10522v1/method.png)

*原文Figure 3：感知—推理—动作的模块化执行架构。[原图](https://arxiv.org/html/2609.10522v1/method.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

**解决什么问题：**通用VLM如何通过容易推理的接口完成细粒度机器人控制？

**核心方法：**提供离散语义动作，形态专用解释器将其确定性落到机器人运动；同一接口支持前沿模型零样本控制、小模型离线微调和GUMI图形示范采集。

**主要结果：**正文报告跨任务、环境和Franka/AgileX形态的优势。Table 3列出真机19任务164个示范episode；这不是成功率。HTML的主性能Table 2未正常渲染，因此本条不抄写该表具体成功率，保留PDF复核项。

**综述可借鉴之处：**可与Harness VLA、Zetta、SHAPER比较“接口设计”“固定执行脚手架”和“脚手架自主改写”，避免因同含harness就归为相同RSI机制。

**证据边界：**已有结果主要证明固定接口释放模型能力与离线适应，不能据此声称机器人自行演化该接口或跨代改进学习算法。

**原文定位：**§3–5、Table 1与3；§5.2说明跨形态FT是双形态共同训练。Table 2数值待PDF复核。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)

[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning

> **一句话：** 把人类遥操作建模成按需规划算子，只在人类擅长、TAMP 不支持的阶段介入，可用相同人力采到约 2.9 倍示范并离线微调 VLA；它优化的是数据生产闭环，不是无人监督 RSI。

短名：TANDEM　作者：Samrat Sahoo, Liang Ji, Tom Silver, Yixuan Huang　首次发表：2026-09-23　采用版本：arXiv v1　发表状态：在审预印本

论文链接：[arXiv:2609.28314](https://arxiv.org/abs/2609.28314)　项目页：[PRPL Group](https://prpl-group.com/tandem/)　最后核查日期：2026-09-28

![TANDEM 原文 Figure 2](https://arxiv.org/html/2609.28314v1/figure2_v7.png)

*图注：VLM 为固定 TAMP 域发明缺失谓词和人类执行的 magic operator，计划交替调用自动 TAMP 与遥操作，并在人工阶段后重新感知、验证效果。来源：原文 Figure 2，arXiv v1。*

## 解决什么问题

全程遥操作会重复演示机器人本来已经会的抓放，而固定 TAMP 又无法覆盖接触丰富的长时阶段。论文研究怎样自动识别能力缺口，把有限人力集中到缺失阶段，并让混合轨迹可用于 VLA 微调。

## 核心方法

给定语言任务和初始图像，VLM 识别基础 TAMP 域无法表达的要求，生成新谓词和由人遥操作的 magic operator，再合成长时任务计划。自动阶段由 TAMP 执行，人工阶段后重新感知并验证预期效果；成功的完整轨迹同时包含两类动作。为减少分布偏移，系统用目标模型预训练数据中的轨迹示例约束 TAMP 运动风格，最终按任务离线微调 π0.5-DROID。

## 主要结果

- 五个长时真机任务中，原始 TAMP 均无法完成；TANDEM 共 130 次尝试收集 100 条成功示范，成功率 76.9%。30 次失败中 93.3% 来自 TAMP 执行、6.7% 来自谓词/算子发明，规划与遥操作阶段未被归因失败。
- 在 Cover Bread Rolls 上匹配人类介入时间：524 s 时收集 40 条示范，对全程遥操作 14 条；785 s 时为 60 对 21，约 2.9× 数据吞吐。
- 每任务 20 条 TANDEM 示范微调后，五任务各 20 次评测的平均成功率由 π0.5-DROID 的 0% 提升到 60%，HITL-TAMP 为 17%；平均任务进度 77.6% 对 55.8%。Cover Bread Rolls 从 20 到 60 条示范时成功率 45%→80%，80 条时回落到 75%。

## 综述可借鉴之处

TANDEM 可放在“自动数据采集与人力预算”章节：改进闭环不仅要统计 episode 数，还要把人工控制秒数、自动阶段失败和数据有效性算进去。它也提供与全程遥操作匹配人力预算的对照，适合约束 Physical RSI 的“自动”表述。

## 证据边界

能力缺失阶段由人完成，任务、成功标准和最终数据筛选均由外部设定；策略在数据收集完成后按任务离线微调，部署时固定。只评估五个真机任务，且任务专用策略各用 20 条示范。它是人机协同数据基础设施，不是自主持续改进，更没有外层改进器更新。

## 原文定位

§§III–V；Figures 2–6；Table I；Appendix Tables II–IV。采用 arXiv v1；全文计划/验证流程、人力预算、130 次采集和下游 5×20 次评测已核查，未复现。

标签：数据采集 / TAMP与人类遥操作 / 离线VLA微调 / 真机 / 人力预算 / 支撑组件 / 非递归。

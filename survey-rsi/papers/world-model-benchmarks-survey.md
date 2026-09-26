[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Do World Models Make Better Robots? A Survey of Evaluation Benchmarks for Predictive Embodied Intelligence

> **一句话：** 160 个 benchmark 中只有 11 个明确比较 VLA 与 world-model 路线、仅 4 个把预测接到执行；现有证据无法仅凭开放环预测质量回答“世界模型是否让机器人行动更好”。

短名：World-Model Benchmark Survey　作者：Gaytri Jena、Kapil Wanaskar、Vinija Jain、Aman Chadha、Vasu Sharma、Amitava Das　首次发表：2026-08-30　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.29669](https://arxiv.org/abs/2609.29669)　最后核查日期：2026-09-26

![原文 Figure 10](https://arxiv.org/html/2609.29669v1/figures/hand_drawn/fig_eval_loop_hand.png)

*图注：原文 Figure 10（v1）。同一闭环、同一预算下运行 direct VLA 与“预测后规划”策略，并按能力切片报告差值，才可识别 prediction 的行动收益。*

## 解决什么问题

VLA 通常按闭环任务成功评测，world model 却多按开放环视频/潜变量预测质量评测；两条轨道几乎不相交。预测看起来更真实，并不自动意味着机器人控制更好。

## 核心方法

综述收集并逐项核实 2017–2026 年 160 个 benchmark，按评价模式、机器人能力和模型家族组织为四条 lane：闭环 policy suite、embodied agent、开放环 world-model evaluation、prediction-to-action bridge。作者进一步比较八篇相近综述，给出“预测优势曲线、反事实准确率、预测—行动 fidelity gap、按能力的对照覆盖”等建议指标。

## 主要结果

160 项中 138 项对模型家族无特定要求；只有 11 项（约 7%）构建 VLA 与 world-model 的显式对照，只有 4 项真正把预测接到执行。反事实能力几乎没有系统测量。该统计支持的是**评价缺口**，不是“world model 无效”或“优于 VLA”。

作者建议在同一环境和预算下比较 direct VLA 与 world-model+planner，报告 closed-loop success 差值并按遮挡、接触、长时程和反事实等能力切片；同时公开开放环质量与闭环收益之间的差距，避免只用生成指标替代控制价值。

## 综述可借鉴之处

这是组织世界模型章节的直接方法论来源：把“预测是否准确”“预测是否可执行”“执行是否优于 matched VLA”“更新后是否保持旧能力”拆成四个问题。对 Physical RSI 而言，世界模型只有进入经验—预测—行动—验收闭环，才是改进支撑，而非 RSI 本身。

## 证据边界

这是预印本综述，未提出新的机器人策略或闭环实验；160 项的分类和 11/4 项统计依赖作者的纳入标准与网页核实。Figure 11 中部分趋势是目标形状的示意，不是观测结果。不能把“缺少对照”反推为具体模型没有价值。

## 原文定位

全文综述、目录与关键统计已读，未复核全部 160 个 benchmark 的每个原始实验。分类与纳入见 §§2–3；四条 lane 与缺口见 §§4–6、Tables 2–8；统计见摘要、Table 10；建议协议 Figure 10、Table 9；图片来源审计 Tables 11–13。

标签：综述 / benchmark 目录 / 2017–2026 / 不更新模型 / 人工系统核查 / 文献证据 / 覆盖统计 / 评价方法。

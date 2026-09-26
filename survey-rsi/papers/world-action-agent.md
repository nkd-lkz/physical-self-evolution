[首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal

> **一句话：** WAA 让 VLM 在视觉动作工作区里预演、修订和执行基础工具，并从专家视频与人工教学形成经审查的多模态技能库；技能冻结后在 LIBERO-Pro 达到 75.6%。

短名：WAA　作者：Yehang Zhang、Haojian Huang、Yifan Chang、Jianchong Su、Bohan Zhou、Yingjie Xu、Wosong Chen、Tianhao Zhou、Chenxu Wang、Tianyi Zhang、Yangkai Wei、Wenqian Li、Shiyuan Deng、Yinchuan Li、Ying-Cong Chen、Zexi Li　首次发表：2026-09-24　采用版本：v1　发表状态：arXiv 预印本

论文链接：[arXiv:2609.29964](https://arxiv.org/abs/2609.29964)　最后核查日期：2026-09-26

![WAA 原文 Figure 2](https://arxiv.org/html/2609.29964v1/waa_method.png)

*图注：原文 Figure 2（v1）。主代理在 contact view 中预演、修订动作；Learner—Editor—Reviewer 从示范/教学更新多模态技能；成功交互 trace 还可蒸馏到小 VLM。*

## 解决什么问题

通用 VLM 有语义与空间推理能力，但常被限制为写程序或提供高层约束；现场写代码又慢且难迁移。WAA 希望让 VLM 直接操作有限且可预览的机器人原语，同时把程序性物理知识保存在可审查技能中。

## 核心方法

视觉动作工作区自动选择接触视角，把每个动作变成可编辑 proposal；Imagination Agent 在执行前预览可行性，in-view correction 用同一视角修正残差。技能由 applicability、步骤、关键状态图像和结果检查组成。Learner 从一个 expert video 提取带帧证据的候选，Editor 合并/修订/退役技能，独立 Reviewer 检查证据后才发布。另一条路径把成功轨迹和审查过的 recovery segment 蒸馏到较小 VLM。

## 主要结果

LIBERO-Pro 有 6 个 split、每 split 10 任务；每种 WAA 设置每 split 60 episode（每任务 6 次），单 episode 最多 50 个主代理 turn、50 次物理操作和 1 小时。Gemini 3.7 Flash 的 WAA zero-shot 平均 28.9%，文本 seed skill 43.3%，只从 LIBERO-90 演化且评测前冻结的技能为 75.6%；ASPIRE 72.0%，RATs 43.8%，CaP-Agent0 18.2%。同 backbone 的 Show-Harness 重跑为 6.7%，但仅 30 episode/split。

在 robosuite 三任务中，冻结 LIBERO 技能的 WAA 为 100/100/100%，无技能为 100/100/60%，每任务分母需看原表协议。另用 112 个成功 episode、1,774 个主代理 tool call 对 Qwen3.5-9B 做 LoRA（4×H20、9.5 小时），out-of-domain 成功由 1.7%→43.3%；这条蒸馏训练使用 LIBERO-Pro 数据，不能与 frozen-skill zero-shot transfer 混为一谈。

## 综述可借鉴之处

WAA 展示两种不同更新载体：非参数技能库与参数化小 VLM。Learner—Editor—Reviewer 的证据门控适合放入“技能发布与退化防护”；视觉 action rehearsal 则是支撑执行的固定 harness，不能单独算自我改进。

## 证据边界

主要结果为仿真；技能来自 expert video 和 human teaching，不是纯自主执行经验。LIBERO-Pro 评测前技能冻结，系统不会边部署边增长。部分 baseline 来自原论文且预算不同；WAA 调用 Gemini/GPT 系列多代理，模型成本和一小时 episode 上限需一同报告。学习规则本身未演化。

## 原文定位

全文方法与指定实验已读，未复现。harness Figure 2、§§3.1–3.2；技能学习 §3.3；LIBERO-Pro 协议与结果 Table 1；调用成本 Table 2；robosuite Table 3；小模型蒸馏 Figure 5、Table 7；技能审查案例 Appendix A.3。

标签：视觉 harness＋多模态技能＋小模型 / 专家示范与交互 trace / 部署前学习、冻结评测 / 审查后发布 / 人机混合 / 纯仿真 / 成功率＋调用成本 / 核心技能演化与支撑 harness。

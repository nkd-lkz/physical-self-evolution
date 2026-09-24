[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# 2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation

短名：2AM　作者：Yutong Hu, Fengjiao Chen, Xuezhi Cao, Renaud Detry　首次发表：2026-09-10　采用版本：arXiv v1　发表状态：预印本

论文链接：[arXiv:2609.11308](https://arxiv.org/abs/2609.11308)　项目/代码：未核实到公开入口　最后核查日期：2026-09-23

![2AM总览图](https://arxiv.org/html/2609.11308v1/figures/teaser.png)

*图注：agent保存任务记忆并给出局部指令/空间提示，动作模型每次调用保持episodically stateless；原始来源为论文开篇teaser，arXiv v1。*

## 解决什么问题

 长程任务若把全部历史直接塞给VLA，会增加上下文负担并产生漂移。论文把长期任务状态交给agent侧记忆，只让动作模型处理局部且可执行的引导。

## 核心方法

 agent维护任务记忆和进度，向动作模型提供局部语言指令，并可附2D抓取、放置或移动提示；动作模型输入RGB/机器人状态，但每次调用本身不保留episode状态。训练通过条件dropout、噪声和抖动，让动作模型适应不完美的上层引导。

## 主要结果

 在10项LIBERO-Mem仿真任务上，复现对齐后的π0依次取得70.79%完成率、37.42%宽松成功率、12.25%严格成功率；2AM为76.29%、63.00%、11.83%。也就是说宽松口径显著改善，但严格成功率略低。仅语言引导为53.72%、19.42%、7.25%，说明空间提示是主要贡献之一。

## 综述可借鉴之处

 适合跨任务记忆/agent—policy接口章节，也是一条重要负面提醒：过程完成度和宽松成功提升不保证严格终态成功。其“agent有记忆、动作模型无记忆”能帮助综述明确更新/存储究竟发生在哪一层。

## 证据边界

 记忆只服务当前任务episode，不跨部署持久学习；没有策略参数在线更新，也没有改进器递归增强。实验为仿真，且主要收益依赖评价口径与上层提示，因此归入任务内记忆边界而非核心RSI。

## 原文定位

 arXiv v1 §2–4、§6，Figure 1，Tables 2/3。方法与三种指标口径已读；未复现。

标签：agent侧任务记忆 / 局部指令与空间提示 / 单episode / 固定动作模型 / 仿真 / 边界案例。


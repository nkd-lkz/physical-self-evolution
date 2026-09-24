[知识库首页](../README.md) / [主题导航](../topics.md) / [全部论文](README.md)

# Embodied-BenchForge: A Closed-Loop Agentic Workflow for Embodied Benchmark Construction

作者：Jiang, Baoyang；Zhang, Fengchun；Wang, Leyuan；Li, Haotian；Wang, Yida；Ji, Zhe；Lai, Jinshan；Ren, Xi；Li, Danyang；Yang, Zheng；Hu, Jianwei；Ma, Qiang　|　arXiv所列日期：2026/09/11（采用版本见下方链接）

[论文](https://arxiv.org/abs/2609.13082) · [采用版本 v1 全文](https://arxiv.org/html/2609.13082v1) · [PDF](https://arxiv.org/pdf/2609.13082v1)

**收录：**2026-09-21　**类别：**评价基础设施 / 基准生成 / 验证修复 / 仿真　**阅读状态：**方法及指定实验/表格已核查；未复现。预印本状态以 arXiv 页面为准，未独立确认录用信息。

![Figure 1：技能编排生成与需求驱动验证修复](https://arxiv.org/html/2609.13082v1/framework0729.png)

*原文Figure 1：技能编排生成与需求驱动验证修复。[原图](https://arxiv.org/html/2609.13082v1/framework0729.png)，版权归原作者。嵌入作者原图，不作改绘；外链失效时可查看上述 PDF。*

## 解决什么问题

怎样把评价意图和异构资源转成可执行、可溯源的具身基准？

## 核心方法

通过可复用技能生成基准产物，再用需求契约与质量关卡检查；失败时根据来源关系局部修复、重执行或回滚，而不是整条链盲目重做。

## 主要结果

构建六个离线具身问答基准和220项交互任务。Table 7中完整系统有效率93.7%，去掉验证与修复后62.4%；人评质量91.28对68.03。这里衡量生成基准的质量，不是机器人策略成功率。

## 综述可借鉴之处

适合“环境/任务/评价生产管线的自动改进”分区。契约、来源追踪和局部回滚也能借鉴到自动研究系统的可审计设计。

## 证据边界

复用技能不等于技能库自动进化；需求与验收规则由设计者规定。LLM Judge分数要与人评和可执行验证分开，不能当独立物理实验。

## 原文定位

方法章节、Figure 1–2、Tables 2、5、7–8；评价基准的构建统计。

[返回文献目录](../README.md) · [当日增量](../daily/2026-09-21.md)


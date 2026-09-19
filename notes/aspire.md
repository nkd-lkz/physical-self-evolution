# ASPIRE：Agentic /Skills Discovery for Robotics

> 阅读状态：**专题阅读完成，偏系统层**  
> 定位：Skill / Code evolution；最值得借的是 fine-grained failure trace。

## 1. 一句话

ASPIRE 把机器人持续学习改写成一个“执行 → 细粒度失败诊断 → 局部代码修复 → 重新验证 → 保存 skill”的开放循环。

## 2. 核心机制

1. Closed-loop execution engine：暴露 perception、grasp、planning、collision、execution 等 trace；
2. Reusable skill library：验证成功的修复沉淀为 reusable skill；
3. Evolutionary search：围绕失败生成、筛选和验证新的 skill/program。

## 3. 与 Physical Token 最相关的地方

不是 Code-as-Policy 本身，而是：

> **Fine-grained Physical Failure Trace**

对于 Hammer / insertion，可记录：

```text
before observation
reference proposal
actual executed action
measured consequence
contact / slip / progress
failure type
```

再形成 episode-level failure card。

## 4. 边界

- Code-as-Policy 更适合流程、工具和离散 recovery；
- 不适合作为高频 contact dynamics 控制的直接替代；
- 它改的是 skill/program，而不是 action-side physical latent。

## 5. Source

- arXiv: https://arxiv.org/abs/2607.00272

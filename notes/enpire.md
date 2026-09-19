# ENPIRE：Agentic Robot Policy Self-Improvement in the Real World

> 阅读状态：**专题阅读完成，偏 Research OS / 实验自动化**  
> 定位：把真实机器人实验过程本身变成可自动迭代的 self-improvement loop。

## 1. 一句话

ENPIRE 围绕真实 robot rollout、verification、日志和 coding agent，让系统不断修改训练 recipe / algorithm / code，再重新执行和验证。

## 2. 核心循环

```text
Environment / Reset
      ↓
Rollout
      ↓
Verification
      ↓
Inspect logs / video / reward
      ↓
Policy / code / recipe improvement
      ↓
Re-run
```

## 3. 对我们的直接价值

更像 Research OS 的方法论：

- 每次实验明确 hypothesis；
- 保存 config / checkpoint / seed / video / reward / failure type；
- 自动 verification；
- failure attribution 后再决定下一项实验；
- proposal 必须经过 validation 才升级为新默认配置。

## 4. 边界

ENPIRE 的“自改进”发生在实验系统和训练流程层面，不代表它解决了 action representation 中的 physics grounding。

因此可以借其科研闭环，不应该把 coding agent 加入 Physical Token 首轮方法。

## 5. Source

- arXiv: https://arxiv.org/abs/2606.19980

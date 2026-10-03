# PEARL：从交互推断任务，再用条件策略行动

2026-10-03 专题阅读，未复现。**Efficient Off-Policy Meta-Reinforcement Learning via Probabilistic Context Variables，ICML 2019，PMLR 97:5331–5340。** [正式出版页](https://proceedings.mlr.press/v97/rakelly19a.html) · [原文 §4–5 / 算法 1–2](https://arxiv.org/html/1903.08254v1) · [作者代码 oyster](https://github.com/katerakelly/oyster)。

**一句话：把少量交互转换成“当前可能是哪种任务”的概率分布，让 actor/critic 根据这一判断工作，而不是每遇到新任务都从头训练。**

直白地说：先保留几种对环境的猜测，按一种猜测连续尝试，再用看到的结果更新猜测。部署适应首先发生在 context posterior，不要求每次都更新策略权重；但这个推断能力和条件策略必须先在任务分布上训练好。

## 哪些定义需要分清

| 对象 | PEARL 的含义 |
|---|---|
| context | 收集到的 transition 集合，通常写作 `(s,a,r,s_next)`；不是提示词文本 |
| latent z | 后验中的任务条件变量；不保证等同质量、摩擦或通用物理常数 |
| encoder | 将各 transition 的 Gaussian factor 汇合，得到置换不变的后验；不是有序长历史 Transformer |
| 训练目标 | 实现中以 critic Bellman loss＋KL 约束训练 encoder；actor 使用 detach 的 latent，基于 SAC |
| 数据采样 | RL batch 可以来自完整 replay；context 偏向近期数据以减小训练/适应分布偏差 |
| 测试适应 | 收集经验并更新后验，进行任务条件采样；原方法没有跨任务检索库的生命周期设计 |

论文报告的样本效率倍数属于其 meta-training 基准，不是 RLT 接触任务的预期提速。原方法学习任务后验，不以本项目的“实际执行后果预测”作为默认主要监督。

## 我们应该借鉴什么

**研究判断：PEARL 迫使我们证明“新监督与可持续记忆”超过普通 context-conditioned RL。** 不能把把历史压成一个 token、拼给 actor/critic 当成贡献。

建议先实现确定性经验条件，并保留一个同容量的 PEARL 启发对照：context encoder 从实际交互预测条件，用 critic 信号训练，暂不加入显式后果 loss。然后比较后果预训练能否加快早期学习。若以后引入概率 latent，再单独比较后验均值、固定分布采样与根据证据更新的后验采样；随机性更大不自动代表有效探索。

三项区别必须体现在实验里：

- **顺序**：接触–卡住–回退的顺序可能重要。保留 Zeva 式有序短记忆，与同记录集合池化比较；不要直接套用完全可观测 MDP 下的置换不变假设。
- **任务与物理条件**：奖励可以帮助辨认任务，但跨任务物理经验不应只记住奖励。比较 reward/task-tag 有无，检查检索是否只是识别任务 ID。
- **预算**：meta-training 的任务数、数据量和 GPU 时间单列；目标任务首次适应与多目标复用后的摊销成本分别报告。

PEARL 与 [RMA](rma.md) 均早于 RLT，归入经典近邻。与本项目的联系是经验条件化与快速适应，不应列进“直接改进 RLT”的计数。具体开发路线维护在 [Zeva–RLT 方案](../research/zeva-rlt-implementation-2026-09-26.md)。

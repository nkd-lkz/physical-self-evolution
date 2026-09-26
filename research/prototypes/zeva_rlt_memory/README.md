# 已完成接触经验的时序原型

本目录是为 RLT 接入准备的**独立 Python 标准库原型**。它实现 BIT/PIM 的时间和 episode 边界，尚未接入 RLinf、RLT、Zeva 权重或任何训练过程。

运行：`python -m unittest discover -s research/prototypes/zeva_rlt_memory -p 'test_*.py' -v`（从仓库根目录）。

调用顺序：`start_episode(EpisodeKey)` → `start_attempt(0)` → **动作决策前** `read(current_phase, decision_step)` → 执行真实 accepted action prefix → 观察后果 → 构造 `CompletedTransition` 并 `write_completed` → 下次决策 `read(...)`。retry 时 `start_attempt(1)` 只清 BIT；新 episode 的 `start_episode` 清两个存储。key 包含 controller version；不要跨本体控制接口混用旧动作。

`phase_at_decision` 和 `effect_embedding` 暂由调用者计算。本原型只有 phase cosine 检索，不包括论文 CTE、记忆合并和条件训练；`measured_delta` 也不是无条件可用的真机标注。不能把本原型的 unittest 当成 RLT 效果验证。下一步是按 [精读方案](../../zeva-rlt-implementation-2026-09-26.md)从 RLinf 的真实 executed prefix/next observation 生成记录，然后训练**确实读取记忆**的小 learner。

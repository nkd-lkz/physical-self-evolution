[案例目录](README.md) · [横向分析](../discussions/physical-rsi-sept24.md)

# Knowin GLOW：执行回执、经验监督与 RSI 叙事

**类型：** 企业技术报告。**来源：**[官方技术页](https://knowinai.com/tech.html)。**核查：** 2026-09-24。**状态：** 主要架构、回执机制与指定评测已读，未复现。

## 最值得借鉴的机制

官方页面描述 KnowinDream 的经验生成、KnowinWorld 的动作条件推演、Experience Compiler 的监督组织，以及统一自回归模型与执行 harness。其中的 **执行回执**：请求位移与实际位移、剩余目标误差、夹爪状态与物体响应共同进入下一步上下文。一教就会展示采用冻结参数的上下文适应。[官方来源](https://knowinai.com/tech.html)

## 结果应该怎样引用

官方技术页报告 **18 个 RoboDojo 仿真任务**平均成功率 62.2%，对应 GPT-6 (Robocurve) 22.2%。这不是 18 个真机任务，也不是完整官方仿真总榜口径，不能与 Simate 的 27.96% 直接排列高低。LIBERO-Pro 表中 86.7% 为所列单策略组第一，混合策略系统另列，不能写成所有系统总第一。

技术页同时提示：演示步数不含模型等待，不支持严格速度排名；整系统成功案例不是各个工具的独立消融；部分记录在物体仍被抓持时触发成功，不能证明释放后的长期稳定。

## 证据边界

本次官方技术页核查没有提供足以确认“改进器递归增益”的多轮、同预算实证。AR 架构、程序回执、记忆和大量数据对成绩的贡献，也不能从整系统比较中单独分离。

**原文定位：** KnowinWorld；Experience Compiler；Hierarchical Memory and Long-Horizon Task State；Execution Receipt；RoboDojo 与 LIBERO-Pro 结果；Execution Examples 的比较边界。

**标签轴：** 模型与运行时 / 执行回执 / 企业自评 / 上下文适应 / 递归路线待逐轮验证。

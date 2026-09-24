[实验主文](README.md)

# 最小接入合同与实施清单

这里只定义接口，并提供标准库日志校验脚本；不是 RLinf 训练实现。没有配置真实 checkpoint、环境版本或 GPU 任务，也不提供虚构的 `train_rlt.py` 命令。

## 1. 从 rollout 取得一行 transition

决策前固定 `decision_time_s` 和历史最新时间；执行后记录实际回执，再生成监督标签。JSONL 每行一个真实执行区间。控制者从 base/actor 切到 expert 时切开区间；未执行的学生动作不能配上专家结果当作学生标签。

| 字段 | 语义 |
| :--- | :--- |
| episode_id / instance_id / condition_id / split | 可公开的匿名标识；同一实例不得横跨训练与验证/测试 |
| decision_time_s / history_latest_time_s | 后者不得晚于决策时刻；还需在特征生成处检查实际时间戳 |
| H / C_requested / C_executed / dt_s / elapsed_s | 预测长度、请求执行长度、实际执行长度、每步时长、总执行时长 |
| u_exec | 实际发送并执行的命令前缀，长度=C_executed；不是测得运动 |
| controller / action_space / feature_tap / feature_version | 控制者、动作单位/坐标/归一化合同、prefix或head、缓存版本 |
| deploy_fields | 白名单内的实际模型输入；teacher 真值与未来结果禁止列入 |
| measured / valid | 执行区间对应的标签与有效性；缺失用 null+false |

模型输入白名单的默认值为图像、本体状态、任务、既往已执行命令、既往时长、冻结特征；可在实现时加真机可得触觉等，但必须同步修改并审查合同。校验器只能检查声明和数值一致性，**不能证明未发生特征泄漏，也不能核实传感器和环境真的执行了动作**。部署边界还需 adapter 与特征导出代码审查。

示例采用恒定控制周期；若环境是可变 dt，adapter 必须输出并校验逐步 dt 序列后扩展合同，不能强塞平均值掩盖早停。标签当前仅包含 `delta_q`、`delta_ee` 与 `contact_event`，对象响应和多事件可以按同样原则扩展。

## 2. 现在可以运行的命令

在仓库根目录执行：

```bash
python survey-rsi/experiments/rlt-contact-memory/validate_transitions.py \
  survey-rsi/experiments/rlt-contact-memory/example.synthetic.jsonl
```

示例只有两行合成记录，专门说明格式，不是机器人采集、训练集或实验结果。把参数换成 adapter 导出的真实 JSONL 即可校验；任何失败会返回非零状态。脚本检查长度、时长、输入白名单、实例划分、必要标签和 finite 数值。

## 3. 接入 RLinf 的五个 hook（接口名为提案，不是现有 API）

1. `before_action`：保存过去历史与冻结 feature，不读取未来；输出 feature tap、版本与归一化 ID。
2. `after_execute`：从执行器取得真实前缀、终止原因、控制者与时间，读取 measured state。
3. `build_targets`：统一坐标和单位，生成 motion/event 标签和 mask；环境私有状态只进入这一步。
4. `offline_grounding`：按 episode/condition 划分缓存，训练小 readout+decoder；相同数据给所有监督对照。
5. `online_observation`：固定版本 readout 将 z 输入 actor/critic；记忆扩展另设开关，首轮关闭；不得静默改变奖励和 replay 语义。

训练开始前填写 [run card](run-card.template.json) 的所有 null：真实代码 SHA、权重 SHA、feature tap、数据划分、预算、目标与接受规则。null 是未决项，不是零预算或默认最优值。adapter 跑通后，先人工抽看 5 条真实片段与回执是否一致。

## 4. 预期失败与处理

- 只在 oracle 物体状态作为输入时有效：降级为标签/可观测性研究，不声称真实视觉部署有效。
- 只在随机帧切分下有效：先修划分，再讨论模型；不把相邻帧泄漏当迁移。
- 运动标签主要为静止：分接触阶段报告并对比零变化，不能靠总体平均误差宣称物理理解。
- 预测改善、成功率不变：检查 actor 是否使用该维度与目标是否控制相关；不能直接加更多模块掩盖。
- memory 需要多次访问同一实例才有效：保留这项结果，但结论限定同实例适应。
- 新库让旧条件退化：报告遗忘，先按版本回退/分层采样，不把库越大当能力越强。

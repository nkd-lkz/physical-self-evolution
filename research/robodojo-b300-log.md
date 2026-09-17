# RoboDojo on B300 · Bring-up / RLinf Integration Log

> 定位：第二实验平台 bring-up，不抢占 hammer / Physical Token 主线。  
> 当前状态（2026-09-17）：**D0–D5 已完成；D6–D10 待执行。**  
> 本页为公开脱敏记录，不保存内部绝对路径、账号、私有 run 标识、GPU UUID 或不必要的完整命令。

---

## 0. 当前目标

RoboDojo 这条线分成两个明确里程碑：

1. **Dojo-Eval**：让 RLinf 中的 frozen reference / VLA 通过 RoboDojo + XPolicyLab 协议完成可复现 episode；
2. **Dojo-RL**：再补齐 `reset/step/reward/done/final_observation/transition`，接入 replay、learner 和 weight sync。

必须保持：

> **原生环境跑通 ≠ Dojo-Eval；Dojo-Eval 通过 ≠ Dojo-RL 已接通。**

而且动作维度相同也不意味着 checkpoint / norm / robot convention 可以直接复用。

---

## 1. Gate 总览

| Gate | 工作 | 当前状态 | 通过后能说明什么 |
|---|---|---|---|
| D0 | 固定源码、系统与安装清单 | **已完成** | 版本与系统事实可追溯 |
| D1 | 子模块 + assets + 无 sudo 工具环境 | **已完成** | 源码/资产完整 |
| D2 | 独立 Isaac Sim / Isaac Lab runtime | **已完成，但历史 doctor 口径已纠正** | 直接 import 路径可用；不再单独依赖旧 doctor import 检查 |
| D3 | B300 headless app + RGB renderer | **已完成** | B300 上最小可见 RGB 路径已实测通过 |
| D4 | XPolicyLab `demo_policy` CPU closed loop | **已完成** | WebSocket / reset / action schema 可用 |
| D5 | 官方原生 task 单 episode | **已完成** | 原生 RoboDojo reset / action / video / result 闭环可运行 |
| D6 | 自建 RLinf reference adapter | 待执行 | RLinf policy 可以驱动 RoboDojo |
| D7 | Dojo-Eval multi-seed | 待执行 | reference evaluation 可重复 |
| D8 | RLinf training bridge / transition alignment | 待执行 | 可生成严格 `(s,a,r,s')` |
| D9 | RLT L0 smoke | 待执行 | actor/critic/replay/sync/checkpoint 工程闭环 |
| D10 | 完整 horizon baseline | 待执行 | 才开始讨论 RoboDojo 上算法效果 |

当前顺序固定为：

```text
D3 ✓ → D5 ✓ → D6 reference-only adapter → D7 multi-seed eval
                                      ↓
                         D8 transition bridge
                                      ↓
                         D9 RLT L0 smoke
                                      ↓
                         D10 baseline
```

---

## 2. 固定版本与运行边界

本轮固定 RoboDojo 主仓到公开 commit：

```text
ee67a1468510da7624a089164402359f2afc72c8
```

子模块、assets 与模拟运行环境保持固定，不通过 `--remote` 漂移。

2026-09-17 的 GPU 验证是在用户明确授权下进行的：允许 Hammer 训练期间短暂共享一张允许使用的 B300 GPU，接受训练变慢；不终止 Hammer，不使用未授权 GPU，不做 GPU reset / host reboot。共享必须显式打开，默认空闲保护继续保留。

一个重要设备语义：

> CUDA-local device `0` 只表示 `CUDA_VISIBLE_DEVICES` 过滤后的本地索引，不等于物理 GPU0。

对于 Vulkan / renderer，仅设置 `CUDA_VISIBLE_DEVICES` 不足以证明渲染器使用目标卡，必须额外检查 renderer active GPU / device table。

---

## 3. D0 / D1：源码、子模块与资产

### 已核实

- RoboDojo 主仓固定到明确 commit；
- XPolicyLab、IsaacLab、CuRobo 三个顶层子模块均按主仓 gitlink 初始化；
- 四类 RoboDojo assets 已落盘并固定版本；
- assets 规模约 66 GB；
- 固定版本可枚举 54 个 runnable task config（包括随机化变体）。

D1 最终：

> **13 PASS / 4 WARN / 0 FAIL**

因此 D1 已完成。

---

## 4. D2：独立 runtime，以及历史 doctor 结论纠正

RoboDojo 使用与 Hammer 隔离的独立 Python / Conda runtime。

历史 post-install doctor 曾记录：

> **14 PASS / 3 WARN / 0 FAIL**

但 2026-09-17 复核发现，旧 doctor 某些 import 检查使用 `conda run ... python -` + stdin 的方式，在本机可能出现 **命令 exit 0 但 stdin Python 实际未执行** 的假阳性。

因此现在的结论修正为：

- 历史 doctor 记录继续保留；
- 不再把该 doctor 的 PASS 单独当作 IsaacLab 已实际 import 的充分证据；
- 通过明确 `python -c` / direct import 重新检查并补齐必要运行依赖；
- 补齐固定 gitlink 对应的 IsaacLab core / assets / tasks 与原生任务所需小依赖；
- 不盲目安装会大范围改变 NumPy / Torch / Hammer 环境的大型可选依赖。

当前 D2 对于 **D5 原生任务路径** 已具备足够 runtime 支持，但不能写成“所有 IsaacLab 可选功能完整安装”。

---

## 5. D3：B300 renderer gate 已通过

D3 不是“程序能 import 就算过”，而是要求：

```text
headless SimulationApp
    ↓
明确可见的最小 USD 场景
    ↓
camera RGB
    ↓
像素类型 / 动态范围检查
    ↓
人工目视确认
    ↓
稳定退出
```

### 调试过程中发现的问题

1. 首次运行缺少 GLU/OpenGL 用户态动态库，shader / MDL 初始化失败；补到独立 RoboDojo runtime 后继续验证。
2. 后续最小场景虽然保存了 RGB，但图像动态范围仅约 0–1，几乎全黑，因此**没有误判为通过**。
3. 收紧自动检查：RGB 必须是 `uint8`，动态范围至少 16，且仍需人工检查可见内容。

### 最终通过证据

使用直接 USD 创建的测试场景后：

- headless app 正常退出；
- RGB shape = `[240, 320, 3]`；
- dtype = `uint8`；
- 像素范围约 `85–247`；
- 人工可见红色立方体、地面和阴影。

因此：

> **D3 通过。B300 上最小 Isaac / USD / camera RGB renderer 路径已有真实证据。**

但这不意味着所有 RoboDojo renderer / sensor / task 路径都已无风险；D5 仍需独立验证官方任务。

---

## 6. D4：XPolicyLab CPU protocol 已通过

`demo_policy` CPU WebSocket closed loop 已完成：

- 10 episodes；
- 每 episode 20 action steps；
- 共 200 action steps；
- reset / single-action / batch-action / message transport 完成。

ARX X5 joint schema：

```text
left arm  6
left EE   1
right arm 6
right EE  1
----------
total    14 float32
```

当前 debug policy action chunk length = 2。

仍需强调：

> **14D 只说明维度相同，不说明语义相同。Hammer / ALOHA 的 checkpoint 与 norm 不能因此直接复用到 ARX X5。**

---

## 7. RoboDojo 原生 state / action 契约

源码审计后，14 维 state/action 的语义必须拆开写。

| 字段 | observation 来源 | action 含义 |
|---|---|---|
| 左右 6+6 arm joints | 实际 `joint_pos` | 绝对关节位置目标，revolute 为弧度 |
| 左右 gripper 1+1 | `prev_control` 反向映射，属于指令值 | `[0,1]` 控制值再映射到物理夹爪位置 / mimic joint |

因此：

> **RoboDojo 当前 14D proprio 不是“全部实测状态”。**

Arm joint 是 measured state；gripper scalar 是 command-derived state。

这条区分对后续 Physical Token / measured-transition 很重要：部署或训练时必须按字段记录来源，不能把全部 14 维统一叫 actual state。

另外，配置中的 gripper scale / URDF limit 只能作为接口事实，不能自动当作经过实验验证的安全策略范围。

---

## 8. 控制时间语义

固定配置中：

- physics `dt = 0.004 s`；
- `decimation = 1`；
- observation collection ≈ 25 Hz；
- 一个 policy target 经控制管理器生成约 10 个内部控制项（插值 + hold）。

因此：

> **一次 policy action 不是单个 physics tick。**

名义上约 0.04 s，但正式 RL 仍需要 runtime trace 实测 `physics_steps` / duration。

这意味着 RLT 的：

- action chunk `C`；
- bootstrap discount；
- early termination；
- replay transition duration；

都必须根据 RoboDojo 的真实执行边界重新定义，不能照搬 Hammer TOPP macro，也不能照搬 ManiSkill 固定频率 C10。

---

## 9. Reward / success / terminal 契约

以当前原生任务为例：

- task 运行前注册多个 completion checks；
- raw reward 为 sparse 0/1；
- progress score 与 raw reward 是不同字段，不能混用；
- 成功时 episode end；
- 达到 step limit 或环境失败也会结束。

另一个需要避免的陷阱：环境内部某个 `success` 初始字段不能直接当成真实 task success。

评测接口也没有直接提供标准 RL `terminated / truncated` 语义。因此后续 D8 training bridge 必须显式区分：

```text
success terminal
vs.
time-limit truncation
vs.
task/environment failure
vs.
simulator/runtime error
```

并保留 terminal observation。

不能从聚合 `_result.json` 或视频反向拼 replay transition。

---

## 10. D5：原生 `stack_bowls / arx_x5 / joint` 单集已通过

D5 的目标只是验证官方原生环境闭环，不评价 learned policy。

### 中间调试事实

D5 依次暴露并修复了：

- 缺失 IsaacLab 原生 task runtime 依赖；
- X5 planner 配置生成文件缺失；
- B300 `sm_103` 与旧 NVRTC 编译器不匹配；
- 录像进程找不到 runtime 内的 ffmpeg。

这些修复均限制在独立 RoboDojo runtime / child process 中，没有修改 Hammer 模型、Hammer venv 或其 Torch/NumPy 环境。

对于 B300 `sm_103`，采用隔离的 CUDA 12.9 NVRTC runtime 进行编译，不替换 Hammer 所用 CUDA / Torch runtime。

### 最终 D5 证据

原生单环境、单 episode 运行完成：

- task：`stack_bowls`；
- robot：ARX X5；
- joint action；
- 800 actions 到原生 episode 上限；
- result 记录 `eval_time=1`；
- 三路 RGB：head / left wrist / right wrist；
- 每路 801 帧；
- 640×480；
- 25 FPS；
- 首 / 中 / 尾帧可解码；
- 像素范围 0–255，图像标准差正常；
- 人工首帧可见桌面、碗、机械臂和夹爪。

本次 `demo_policy` 输出近零目标，因此：

- success = 0；
- score = 0；

这是预期的基础设施 smoke，**不能解释为 RoboDojo task / VLA / RLT 性能失败**。

当前原生 physics 运行在 CPU，允许的 B300 GPU 主要承担 renderer / CuRobo。这不是并行 GPU physics 吞吐验收。

因此：

> **D5 通过：RoboDojo 官方原生 task 已在当前 B300 节点完成真实 single-episode reset/action/video/result 闭环。**

---

## 11. 当前 RLinf bridge：CPU contract 已预验收，真实 D8 未开始

目前独立 bridge worktree 已有：

- ARX X5 observation/action schema；
- fake observation pack/unpack；
- missing field / wrong shape / NaN 检查；
- RGB array contract；
- CPU transition contract。

当前 schema + transition tests 合计 **24/24 PASS**，其中独立子进程完成 **20/20 mock transition**。

这些测试覆盖：

- episode / transition ID 顺序；
- duplicate response；
- explicit reset；
- terminal observation；
- finite reward；
- buffer deep-copy isolation。

但必须明确：

> **mock transition ≠ D8 真实 transition。**

它没有执行真实机器人动作，也没有真实 reward / timing / physics duration。

---

## 12. 下一步 D6 / D7：Dojo-Eval

第一版 RLinf adapter 只做 frozen reference：

```text
RoboDojo observation
      ↓
XPolicyLab contract
      ↓
RLinf reference adapter
      ↓
robot-specific action conversion
      ↓
RoboDojo
```

第一版禁止同时加入 RLT actor / critic / replay。

### 关键门槛

必须先获得与 **ARX X5 + task** 匹配的 policy / checkpoint / processor / norm。

Hammer / ALOHA 的 14D checkpoint 与 norm **不能**因为维度相同而直接当作正式 RoboDojo reference。

需要对齐：

- three-camera resize / ordering；
- arm measured joint state + gripper command-derived state；
- ARX X5 joint order；
- arm rad + gripper `[0,1]` action semantics；
- task instruction；
- policy action chunk；
- terminal / reward contract。

验收顺序：

1. fake observation unit tests；
2. XPolicyLab debug contract；
3. fixed observation deterministic policy output；
4. one RoboDojo reference episode；
5. fixed seeds multi-run。

只有 D7 后才能写“RLinf reference 已接入 RoboDojo 评测”。

---

## 13. D8 / D9：Dojo-RL

Dojo-RL 必须新增明确 training transition contract：

```text
reset(seed, env_id)
  -> observation, episode_id, info

step(env_id, episode_id, transition_id, action)
  -> next_observation
     reward
     terminated
     truncated
     final_observation
     executed_length
     execution_duration
     success
     info
```

第一版：

- single env；
- `C=1`；
- 20 transitions；
- 先做真实 transition alignment，不接 actor / critic。

必须检查：

- `action_t` 后拿到的是真正 `obs_{t+1}`；
- episode / transition ID 连续；
- terminal transition 不被 auto-reset 首帧覆盖；
- reward / success 来自固定 task code；
- success / timeout / task failure / simulator error 分开；
- 图像 / state / action 不跨进程复用旧 buffer；
- 实际 policy action 对应多少内部 physics steps / duration；
- reset 只由 RLinf 明确触发。

20/20 **真实** transition 对齐后，才接 replay / actor / critic，做 D9 RLT L0 smoke。

---

## 14. 当前与 Universal Physical Token 的关系

RoboDojo 当前贡献的是**第二平台与更强 contact/precision task 的实验基础**，不是 Physical Token 方法收益。

它已经给当前主线带来两个重要接口约束：

1. **measured state 必须按字段定义。** ARX X5 arm joint 是 measured；gripper scalar 仍是 command-derived。不能把一个固定维度 state vector 整体贴上“物理反馈”标签。
2. **executed action 需要真实时间语义。** 一次 policy target 经插值执行，不等价于一个 physics tick；未来 `measured transition` 和 RLT discount 必须对应实际执行时间范围。

这两点会直接进入后续 B1 measured-transition 的跨平台数据合同。

---

## 15. 公开结论边界

目前可以说：

- RoboDojo 固定源码 / 子模块 / assets 已验收；
- 独立原生 runtime 已完成 D5 所需运行路径补齐；
- B300 上最小 headless RGB renderer 实测通过；
- XPolicyLab CPU WebSocket / ARX X5 schema 已验收；
- RoboDojo 原生 `stack_bowls / arx_x5 / joint` single episode 已在当前节点完成；
- 三路 camera 视频真实生成并通过解码 / 人工检查；
- CPU bridge schema / mock transition tests 已通过。

目前不能说：

- RLinf reference 已完成 Dojo-Eval；
- Hammer checkpoint / norm 已适配 ARX X5；
- D5 的零成功说明 VLA / RLT 能力差；
- RoboDojo 已形成在线 `(s,a,r,s')` 接口；
- RLinf / RLT 已能在 RoboDojo online train；
- RoboDojo 已形成算法 baseline；
- B300 已验证所有 Isaac / RoboDojo GPU physics / RTX 功能。

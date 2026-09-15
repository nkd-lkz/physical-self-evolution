# RoboDojo on B300 · Bring-up / RLinf Integration Log

> 定位：第二实验平台 bring-up，不抢占 hammer / Physical Token 主线。  
> 当前状态（2026-09-15）：**D0–D2 与 D4 已完成；D3 renderer gate 待执行；D5–D10 未开始。**
>
> 本页为公开脱敏记录，不保存内部绝对路径、账号、私有 run 标识或不必要的完整命令。

---

## 0. 当前目标

RoboDojo 这条线分成两个明确里程碑：

1. **Dojo-Eval**：让 RLinf 中的 frozen reference / VLA 通过 RoboDojo + XPolicyLab 协议完成可复现 episode；
2. **Dojo-RL**：再补齐 `reset/step/reward/done/final_observation/transition`，接入 replay、learner 和 weight sync。

必须保持：

> **Dojo-Eval 通过 ≠ Dojo-RL 已接通。**

而且动作维度相同也不意味着 checkpoint / norm / robot convention 可以直接复用。

---

## 1. 当前 Gate 总览

| Gate | 工作 | 当前状态 | 通过后能说明什么 |
|---|---|---|---|
| D0 | 固定源码、系统与安装清单 | **已完成** | 版本与系统事实可追溯 |
| D1 | 子模块 + assets + 无 sudo 工具环境 | **已完成** | 源码/资产完整 |
| D2 | 独立 Isaac Sim / Isaac Lab runtime | **已完成** | Python 与 Isaac import 可用 |
| D3 | B300 headless app + 单路 RGB renderer | **待执行** | 才能形成 B300 renderer/device 兼容性判断 |
| D4 | XPolicyLab `demo_policy` CPU closed loop | **已完成** | WebSocket / reset / action schema 可用 |
| D5 | 官方原生 task 单 episode | 待执行 | 环境 reset/step/done/video/result 可用 |
| D6 | 自建 RLinf reference adapter | 未开始 | RLinf policy 可以驱动 RoboDojo |
| D7 | Dojo-Eval multi-seed | 未开始 | reference evaluation 可重复 |
| D8 | RLinf training bridge / transition alignment | 未开始 | 可生成严格 `(s,a,r,s')` |
| D9 | RLT L0 smoke | 未开始 | actor/critic/replay/sync/checkpoint 工程闭环 |
| D10 | 完整 horizon baseline | 未开始 | 才开始讨论 RoboDojo 上算法效果 |

Gate 顺序不能跳过。特别是：D3 失败不进入 D5；D7 未完成不进入 D8；D9 只是工程验收，D10 才是效果基线。

---

## 2. D0 / D1：源码、子模块与资产

### 已核实

- RoboDojo 主仓固定到一个明确 commit；
- XPolicyLab、IsaacLab、CuRobo 三个顶层子模块均按主仓 gitlink 初始化；
- 四类 RoboDojo assets 已落盘并固定版本；
- assets 规模约 66 GB；
- 固定版本 doctor 可枚举 54 个 runnable task config（包括随机化变体）。

### doctor 结果

首次 post-assets doctor：

- 12 PASS；
- 4 WARN；
- 1 FAIL。

唯一 FAIL 来自独立 Conda 环境缺 PyYAML，导致 env-config 引用检查无法执行；不是 task config 或 assets 缺失。

补齐后 D1 最终：

> **13 PASS / 4 WARN / 0 FAIL**

因此 D1 已完成。

---

## 3. D2：独立 runtime

为避免污染 hammer 环境，RoboDojo 使用独立 Python / Conda runtime。

最终验证：

- Python 3.11.x；
- Isaac Sim 5.1；
- Isaac Lab import 成功；
- PyTorch 2.7 + CUDA 12.8 runtime；
- Isaac Sim / Isaac Lab 基础 import 成功。

安装后 doctor：

> **14 PASS / 3 WARN / 0 FAIL**

三项 WARN 来自尚未提供的 policy directory / processor / policy-specific environment，属于后续 D4 / D6 范围，不阻塞 D2。

### 无 sudo 路线

当前服务器账号无 sudo，因此：

- 不依赖 apt；
- 不依赖 Docker daemon；
- 缺失的用户态工具放在独立 Conda 中；
- 若后续 Isaac import / renderer 明确缺系统动态库，再按具体库名向管理员申请，不提前申请整套 root 权限。

---

## 4. D3：B300 renderer gate —— 尚未执行

当前已有：

- Isaac Python import；
- Isaac Lab import。

当前没有：

- B300 headless app 的稳定启动 / 退出证据；
- 真正的 renderer/device 日志；
- `320×240×3` 的非恒定 RGB 图像；
- 官方 RoboDojo task 的真实 GPU episode。

因此不能写：

> “B300 已兼容 RoboDojo / Isaac Sim renderer”。

### D3 最小验收

只做：

```text
headless SimulationApp
    ↓
最小场景 / camera
    ↓
单张 RGB
    ↓
稳定退出
```

通过条件：

- app 正常启动和退出；
- RGB shape 正确；
- 图像非空、非恒定；
- 无 renderer / device hard failure；
- 保存完整 log + 一张 RGB。

若在最小 RGB 路径连续复现明确 RTX / renderer 硬件阻断，则停止 B300 单机仿真路线，切换为：

```text
RTX 环境机：RoboDojo / Isaac Sim
          ⇅
B300：RLinf policy / replay / learner
```

这属于预先定义的有效架构结果，不是项目失败。

当前 hammer Stage1 长程训练占用允许使用的 GPU，因此 2026-09-15 本轮没有额外启动 Isaac GPU 进程。

---

## 5. D4：XPolicyLab CPU protocol 已通过

### 正式结果

`demo_policy` CPU WebSocket closed loop 已完成：

- 10 episodes；
- 每 episode 20 action steps；
- 共 200 action steps；
- reset / single-action / batch-action / message transport 均完成；
- 正式 v2 验收 exit 0。

第一版 wrapper 曾把预期总动作步数错误写成 20，因此产生一次验收 failure；实际协议循环已经跑完 200 步。失败记录保留，正式结论以修复后的 v2 为准。

### ARX X5 joint schema

当前固定：

```text
left arm  6
left EE   1
right arm 6
right EE  1
----------
total    14 float32
```

当前 debug policy action chunk length = 2。

注意：

> **ARX X5 总维度也是 14，并不意味着可以直接复用 RoboTwin / ALOHA 的 14D norm 或 checkpoint。**

关节顺序、范围、控制语义和 EE 定义仍必须逐项审核。

---

## 6. Dependency isolation

实际发现：

- Isaac Sim runtime 需要较旧的 `websockets`；
- XPolicyLab policy 侧要求更高版本。

处理方式：

- Isaac / simulator 使用独立 Conda runtime；
- XPolicyLab policy 使用独立 CPU venv；
- hammer venv 不修改。

这验证了后续 Dojo-RL 更适合沿用“独立 simulator 进程 + RLinf 进程”的 bridge 架构，而不是强行把全部依赖塞进同一个 Python 环境。

---

## 7. RLinf bridge 当前只到 CPU schema

已建立独立 RoboDojo-RLinf bridge 开发分支，复用现有跨 Python bridge 的工程经验。

当前仅完成：

- ARX X5 observation/action schema；
- fake observation pack/unpack；
- missing field / wrong shape / NaN 等错误检查；
- RGB array contract；
- 4/4 CPU tests passed；
- lint / diff check passed。

当前明确未完成：

- 真实 RoboDojo env registration；
- frozen RLinf reference inference；
- real action conversion；
- Dojo-Eval；
- training transition API；
- replay / actor / critic。

因此该状态不能标记为 D6。

---

## 8. 下一步 D5：官方原生 episode

D3 通过后，第一条官方任务 smoke 固定为官方 quickstart 风格的基础组合，例如：

```text
stack_bowls
ARX X5
joint action
single env
single seed
single episode
```

D5 必须保存：

- 实际 instruction；
- camera names / RGB shapes；
- actual robot joint state；
- action dictionary；
- raw reward；
- success / terminated / truncated；
- video；
- client/server log。

D5 只验证原生环境，不在同一次运行里接 RLinf / RLT。

---

## 9. D6 / D7：Dojo-Eval

第一版 RLinf adapter 只做 frozen reference：

```text
RoboDojo observation
      ↓
XPolicyLab contract
      ↓
RLinf reference adapter
      ↓
robot-specific action dictionary
      ↓
RoboDojo
```

第一版禁止同时加入 RLT actor / critic / replay。

验收顺序：

1. fake observation unit tests；
2. XPolicyLab debug contract；
3. fixed observation deterministic policy output；
4. one RoboDojo episode；
5. fixed seeds multi-run。

只有 D7 后才能写“RLinf 已接入 RoboDojo 评测”。

---

## 10. D8 / D9：Dojo-RL

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
     success
     info
```

第一版：

- single env；
- `C=1`；
- 20 transitions；
- 先做 transition alignment，不接 actor/critic。

必须检查：

- `action_t` 后拿到的是真正 `obs_{t+1}`；
- episode / transition ID 连续；
- terminal transition 不被 auto-reset 首帧覆盖；
- reward / success 来自固定 task code；
- 图像 / state / action 不跨进程复用旧 buffer；
- reset 只由 RLinf 明确触发。

20/20 transition 对齐后，才接 replay / actor / critic，做 D9 RLT L0 smoke。

---

## 11. 当前与 hammer 的资源分工

hammer 主线 GPU 长任务运行期间，RoboDojo 可以继续：

- 文档 / schema 审计；
- CPU tests；
- assets / dependency 整理；
- bridge mock。

暂不：

- 抢占正在训练的 GPU；
- 直接跳到完整 benchmark；
- 同时接真实 RLinf actor + Isaac env。

允许使用的 GPU 真正空闲后：

> **D3 RGB gate → D5 native episode → D6/D7 Dojo-Eval → D8/D9 Dojo-RL。**

---

## 12. 公开结论边界

目前可以说：

- RoboDojo 源码 / 固定子模块 / assets 已验收；
- 独立 Isaac runtime 安装与 import 已验收；
- XPolicyLab CPU WebSocket / ARX X5 joint schema 已验收；
- CPU bridge schema 骨架已通过单测。

目前不能说：

- B300 renderer 已兼容；
- official RoboDojo task 已在 B300 成功跑完；
- RLinf reference 已完成 Dojo-Eval；
- RLinf / RLT 已能在 RoboDojo online train；
- RoboDojo 已形成算法 baseline。

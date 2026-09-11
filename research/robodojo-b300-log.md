# RoboDojo on B300 · 每日小任务日志

> 定位：第二实验平台 bring-up。  
> 原则：每天固定少量时间推进，不抢占 RoboTwin2 / RLT 主线。

---

## 0. 为什么用 B300 单独推进？

目标不是立刻跑 Online RL，而是先回答：

1. B300 非 RTX GPU 上当前软件栈是否兼容？
2. Simulator / renderer / CUDA / PyTorch / policy runtime 是否正常？
3. RoboDojo 能否跑官方最小任务？
4. observation / action contract 是否方便接 π0.5 / RLT？
5. Dojo-Eval 能否稳定复现？

---

## 1. 建议推进顺序

### Day A · 系统信息

记录：
- GPU 型号；
- driver；
- CUDA；
- Python；
- PyTorch；
- OS；
- container / conda；
- EGL / Vulkan / rendering 相关信息。

### Day B · 官方安装

记录：
- 安装命令；
- 失败依赖；
- 是否需要 source build；
- B300 特有错误。

### Day C · Simulator Smoke

目标：
- import；
- env create；
- reset；
- step；
- render。

### Day D · Official Task Smoke

目标：
- 官方策略或 scripted baseline；
- 完整 episode；
- video / success。

### Day E · Policy Contract

整理：
- image shape；
- proprio；
- action dim；
- action semantics；
- control frequency；
- horizon；
- reset/termination。

### Day F · Dojo-Eval

接入 π0.5 / RLT inference server，只做 evaluation。

### Day G · Dojo-RL 可行性

最后才研究：
- transition stream；
- reward；
- learner；
- policy weight sync。

---

## 2. 每日记录模板

### 日期

**今日目标**

**环境信息**

**执行命令**

\`\`\`bash
# commands
\`\`\`

**结果**

**错误日志**

\`\`\`text
# error
\`\`\`

**判断**

**下一步**

---

## 3. 完成 Dojo-Eval 的验收标准

- 环境可 reset；
- task 可完整 episode；
- 图像 / proprio 正确；
- policy output 能映射到 action；
- 同 seed 可重复；
- video / metrics 可保存；
- 不依赖手工中途修复。

---

## 4. 当前状态

- [ ] B300 system info
- [ ] RoboDojo dependency install
- [ ] simulator smoke
- [ ] task smoke
- [ ] observation/action contract
- [ ] Dojo-Eval
- [ ] Dojo-RL feasibility

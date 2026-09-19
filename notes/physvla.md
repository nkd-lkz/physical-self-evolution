# PhysVLA：Towards Physically-Grounded VLA for Embodied Robotic Manipulation

> 阅读状态：**专题阅读完成，仍建议补附录/代码审计**  
> 定位：Physical Token 的强 runtime baseline，不是 learned-physical-representation 的同类方法。

## 1. 一句话

PhysVLA 不从数据中学习一个 physical latent；它在 **frozen VLA 的 action 输出之后**，用人工设计的阶段规则和解析动力学残差做 inference-time correction。

## 2. 核心结构

```text
Frozen VLA
   ↓
predicted action
   ↓
Branch A: phase-aware FSM / geometric rules
   +
Branch B: selective Euler–Lagrange gate
   ↓
corrected action
```

因此更准确的归类是：

> **Physics as runtime rule/model**, 而不是 **Physics as learned representation**。

## 3. Branch A：phase-aware FSM

运行时根据 EEF、gripper、object / target 等几何信息判断阶段，例如 approach / grasp / transport / place，再施加不同的动作修正。

关键点：

- 是 rule-based，不是 learned weight；
- 仿真里可以直接读取 object / EEF / contact 等 privileged state；
- 其收益需要和 perception / calibration 的信息来源一起理解。

## 4. Branch B：Euler–Lagrange gate

典型形式：

```math
r_{EL}=M(q)\ddot q+C(q,\dot q)\dot q+G(q)-\tau
```

当 dynamics residual 超过阈值才触发 correction。

这要求较可信的：

- URDF / kinematics；
- inertial parameters；
- torque / controller mapping；
- frame / calibration。

如果底层 controller 不透明，直接使用刚体 residual 很容易把 controller delay、friction、contact modeling error 错归给上层表示。

## 5. 真机 Sim-to-Real 的关键边界

论文真机部分使用 Agilex Piper 做 pick-and-place。需要特别注意：

> **真机实验只启用了 Branch A。**

因此真机结果主要支持的是：

> phase-aware geometric correction 可以迁到一个真实 pick-and-place setup。

它**没有完整证明**仿真里的 Euler–Lagrange Branch B 在真机上同样有效。

此外，真机 section 对 object / target pose 的获取、误差和 calibration 交代有限，这是复现时必须补查的接口。

## 6. 与我们的 Physical Token 区别

### PhysVLA

```text
VLA action
→ hand-designed physics / rules
→ corrected action
```

### Our candidate

```text
action-head feature + execution history
→ learned Physical Token
→ value / policy / WAM / adaptation
```

核心区别：

- PhysVLA：**known physics / hand-designed correction**
- 我们：**learn effective interaction dynamics from executed consequences**

## 7. 对我们最有价值的启发

把 physics 分成两层：

### Known physics

- FK / Jacobian；
- joint / speed / workspace limits；
- 已知 robot model。

这类关系优先使用 analytic layer，不必让 token 重学。

### Unknown / effective physics

- friction；
- compliance；
- backlash；
- payload；
- delay；
- slip / contact response。

这部分更适合通过：

```text
executed action → measured consequence
```

学习 residual representation。

一个更干净的长期形式：

```math
\hat s_{t+1}=f_{known}(s_t,a_t)+f_{residual}(z_t^P,a_t)
```

## 8. 作为 baseline 怎么比较

建议未来至少比较：

1. Base VLA；
2. PhysVLA-style analytic/runtime correction；
3. Physical Token learned consequence；
4. Analytic safety + Physical Token residual。

尤其在 friction / payload / controller gain / delay shift 下，看固定 physics rule 与 interaction-adaptive latent 的差异。

## 9. 当前结论

PhysVLA 不是“仿真 physics label 学到真机”的方法。它主要是 inference-time correction，因此不会直接撞掉“learned action-side physical representation”这个问题；但它是非常重要的简单强 baseline。

## 10. Source

- arXiv: https://arxiv.org/abs/2606.13886

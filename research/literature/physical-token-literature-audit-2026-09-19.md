# Universal Physical Token：125项相关文献与创新重合审查
> 检索截止：2026-09-19。定位：研究选题与防撞工作稿。主表125项，另列补查/灰色文献；不是125篇全部全文精读，也不保证领域无遗漏。

## 如何使用

编号与Excel一致。P0=最近邻优先核验，P1=方法/强基线，P2=背景或后续扩展。每项将“来源支持的方法”与“对项目的分析”分开。作者录用声明不与正式论文集混同；未复核正式会议的条目只按arXiv记录。没有逐仓安装、跑代码或确认复现成功。

## 检索范围与边界

**研究主问题：**动作生成侧紧凑表示＋实际动作后果＋可信物理约束；兼容不同下游learner，不把RLT收敛作为表征探索的唯一前提。

**检索截止：**2026-09-19；记录本轮可访问的公开题录/摘要。arXiv可持续修订，正式写作前应固定版本。

**年份范围：**重点2024–2026；向前追溯2017–2023年的系统辨识、潜空间模型、触觉融合与安全控制代表作。不是历史全领域穷尽。

**会议覆盖：**RSS、CoRL、ICRA、IROS；NeurIPS、ICML、ICLR；CVPR、ICCV、ECCV；相关ICMR另列，不把它等同机器人旗舰会议。

**期刊覆盖：**Nature、Science Robotics、IEEE T-RO、RA-L、T-ASE、IJRR、Annual Review of Control, Robotics, and Autonomous Systems。

**一手来源：**arXiv、PMLR、OpenReview/ICLR/NeurIPS正式页面、CVF、RSS Proceedings、IEEE/SAGE/Science/Nature等出版社、作者机构或项目页。

**关键词族A：**action representation / action-head / physical token / latent action / compact readout / representation alignment / world-action model

**关键词族B：**action-conditioned dynamics / physical consequence / contact-rich / force tactile representation / history adaptation / online system identification

**关键词族C：**physics-informed / kinematic consistency / differentiable trajectory optimization / constraint-aware / safe policy / barrier functions

**关键词族D：**value guidance / frozen policy adaptation / offline-to-online RL / latent steering / self-improvement / failure recovery

**筛选口径：**纳入能对应提取位置、输入、监督、冻结范围、决策使用或泛化验证的工作；不因标题含physical/self-evolving就视为最近邻。

**检索深度：**题录＋摘要筛查，重点条目补看作者说明；不是125篇全文、附录、代码逐项审计。各条记录evidence及caveat。

**出版状态：**只在正式目录/作者接收声明可核对时写会议期刊；作者声明单独标注。仅arXiv条目不推断录用。

**会议年份：**CoRL 2022与PMLR 2023、CoRL 2024与PMLR 2025分别保留会议年/出版年；online-first与卷期年不同不算错误。

**去重原则：**同一arXiv版本迭代不重复计数；DP期刊与会议合并。PAR/PhysGen为关联谱系，两条题录不等于两个独立方向。

**不能保证的覆盖：**没有完成全部WoS/Scopus/IEEE/ACM数据库逐记录导出，也没有审计所有TPAMI/TMLR和2026后续录用；不能宣称完全检索无遗漏。

**下一轮防撞流程：**围绕18条高重合记录补读方法/附录/代码；沿参考文献与被引工作扩展；逐项填写输入/目标/冻参/干预/预算/泛化证据。

**项目状态边界：**不把参考文献作者报告的成功率移植为自己的预期收益；不自动改变真机任务、训练配置或GitHub项目主规范。


## 高重合近邻：18项必须优先补读

### P001 · RLT

已知方法：紧凑VLA读出＋小型在线learner。

不能单独作为创新：仅把RL Token更名Physical Token。

建议补的验证：相同读出容量/输入/learner下，隔离动作后果监督和物理约束的增量。

来源：https://arxiv.org/abs/2604.23073

### P003 · FLARE

已知方法：少量token＋未来潜表示对齐。

不能单独作为创新：加几个token预测future就算新方法。

建议补的验证：比较冻结readout、联合训练、相同future目标；明确你是否读动作侧、保留哪些可迁移信息。

来源：https://proceedings.mlr.press/v305/zheng25a.html

### P002 · Pri4R

已知方法：privileged 4D future监督。

不能单独作为创新：训练期未来几何监督、推理期删除teacher本身。

建议补的验证：加入真实执行时间、物体相对运动与标签有效性；证明不只是future geometry。

来源：https://arxiv.org/abs/2603.01549

### P004 · AGRA

已知方法：world representation到action representation的对齐。

不能单独作为创新：会预测未来就必然有利于控制。

建议补的验证：同时测预测误差、同状态动作排序、闭环效果，检验表征是否可被决策利用。

来源：https://arxiv.org/abs/2606.12217

### P005 · CometVLA

已知方法：紧凑GAP tokens连接物理知识与动作生成。

不能单独作为创新：compact token＋physical understanding的组合命名。

建议补的验证：区分共同预训练的action prior与冻结action head的执行后果读出；使用matched teacher/数据。

来源：https://arxiv.org/abs/2608.30289

### P006 · PAR

已知方法：physical tokens联合视频与动作。

不能单独作为创新：Physical Token命名、视觉动作统一token本身。

建议补的验证：声明该术语已有先例；定义你的token是decision state还是action token，并说明监督差异。

来源：https://arxiv.org/abs/2508.09822

### P014 · DyWA

已知方法：历史辨识、动态世界模型和策略适应。

不能单独作为创新：history＋预测future＋摩擦/质量泛化。

建议补的验证：与history-only dynamics模型比较；验证额外action-head特征和跨head迁移。

来源：https://openaccess.thecvf.com/content/ICCV2025/html/Lyu_DyWA_Dynamics-adaptive_World_Action_Model_for_Generalizable_Non-prehensile_Manipulation_ICCV_2025_paper.html

### P023 · TACO

已知方法：动作序列—未来状态的时序对比表征。

不能单独作为创新：action-conditioned表征及同时服务online/offline RL。

建议补的验证：检验同容量对比目标与measured-transition回归目标，避免仅换loss名字。

来源：https://www.microsoft.com/en-us/research/publication/taco-temporal-latent-action-driven-contrastive-loss-for-visual-reinforcement-learning/?lang=ja

### P040 · RoboPack

已知方法：触觉辅助隐藏动力学推断和控制。

不能单独作为创新：从接触经验形成物理latent并服务决策。

建议补的验证：视觉/本体/触觉输入对齐；区分多传感器融合收益与action-side读出收益。

来源：https://www.roboticsproceedings.org/rss20/p130.html

### P033 · MSDP

已知方法：多模态latent＋actor/critic非对称使用。

不能单独作为创新：给critic更多物理信息。

建议补的验证：额外传感器、融合算子和grounding目标逐一消融。

来源：https://arxiv.org/abs/2511.14427

### P036 · exUMI

已知方法：action-aware、task-agnostic触觉表示。

不能单独作为创新：动作相关且跨任务的物理表示。

建议补的验证：比较task transfer和head transfer，说明可部署模态及监督适用范围。

来源：https://proceedings.mlr.press/v305/xu25e.html

### P010 · Spline Policy

已知方法：跨多种策略的紧凑轨迹接口和约束。

不能单独作为创新：支持diffusion/flow/Transformer就称Universal。

建议补的验证：区分固定接口兼容性与未见head迁移；证明学习的接触响应而非轨迹参数化。

来源：https://arxiv.org/abs/2606.07386

### P055 · LeTO

已知方法：可微轨迹优化层提供约束控制。

不能单独作为创新：把joint/velocity constraints加在输出上。

建议补的验证：解析可行性层是强基线；约束应新增未知响应建模价值而非只复现已知FK。

来源：https://docs.lib.purdue.edu/iepubs/14/

### P086 · V-GPS

已知方法：跨多种冻结策略的价值引导。

不能单独作为创新：冻结基础策略＋外挂评分器/多head下游。

建议补的验证：同候选动作集、同value模型容量下，只替换表征，评估动作排序质量。

来源：https://proceedings.mlr.press/v270/nakamoto25a.html

### P089 · FlowDAgger

已知方法：轻量latent policy适配冻结VLA和WAM。

不能单独作为创新：冻结大模型、少量反馈、支持WAM。

建议补的验证：比较latent-action steering与state physical readout；控制人工介入与学习预算。

来源：https://arxiv.org/abs/2607.08877

### P088 · DSRL

已知方法：潜空间RL引导冻结生成策略。

不能单独作为创新：不更新生成大模型即可在线适应。

建议补的验证：使用同冻结模型和交互预算，检验physics latent是否优于noise latent。

来源：https://proceedings.mlr.press/v305/wagenmaker25a.html

### P123 · HPT

已知方法：异构输入适配到共享Transformer/token。

不能单独作为创新：共享shape＋机器人adapter。

建议补的验证：封存一个head或本体；报告零样本/少样本适配成本而非仅可运行。

来源：https://papers.nips.cc/paper_files/paper/2024/hash/e0f393e7980a24fd12fa6f15adfa25fb-Abstract-Conference.html

### P103 · GeoAAC

已知方法：从去噪轨迹几何判断可靠性并自适应chunk。

不能单独作为创新：head内部信号＋continue/replan。

建议补的验证：固定H/C和计算预算；探针预测提升不能混同于改变执行频率带来的提升。

来源：https://arxiv.org/abs/2609.20776

## 给本项目的判断：不是给 RLT 换名字，而是提出可证伪的接口假设

已有工作已覆盖“物理 token”“少量 token 预测未来”“多传感器物理潜变量”“冻结大策略的小外挂”“跨策略价值引导”“跨动作头轨迹表示”。因此不能以这些词的组合直接宣称空白。本轮没有发现与某个拟议组合完全一致的论文，也不能据此证明该组合新颖；需要全文、附录、代码和具体实验合同的比对。

### 三条仍值得验证的方案

**方案一：真实执行后果读出。** 在冻结基座、固定容量与传感输入下，比较 action-head / backbone / 仅动作数值 / 仅本体历史。用严格时间对齐的观测和实际施加控制命令，预测机器人与物体的相对运动、接触事件、执行误差。最近邻：RLT、FLARE、Pri4R、DyWA、TACO、RoboPack。核心问题不是“能否预测future”，而是“动作侧读出是否提供额外、可迁移且对决策有用的信息”。

**方案二：物理后果表示用于候选动作评价。** 冻结同一个基座和候选动作集合，保持评价头容量一致，仅改变表示及监督。先离线检验同状态动作排序、失败风险校准和分布外拒绝能力，再做闭环选择。最近邻：V-GPS、Q-VGM、FlowDAgger、DSRL、MSDP。RECAP可作为后续学习机制，但不能直接替换为同一个“冻结外挂”而不改变研究设置。

**方案三：跨动作头迁移的物理接口。** 使用相同维度的token、统一的时间/动作/测量契约和轻量适配器，封存一种动作头或本体做迁移；报告零样本与少样本适配代价。最近邻：HPT、Spline Policy、X-DiffVLA、CometVLA、FlowDAgger。多种模型分别训练都能运行，只能证明兼容，不足以证明通用迁移。

### 必须排除的混杂

1. **更多输入的收益**：history-only、proprio-only、同输入无物理loss都要比较。
2. **浅层已知关系**：FK/Jacobian/关节限位带来的约束不等于学会接触、摩擦或隐藏动力学；增加物体相对运动与物理扰动测试。
3. **动作或未来泄漏**：decoder的动作条件应是实际施加的控制命令及明确时间定义；不能把执行结束后的实际关节运动轨迹当成可提前获取的动作输入。未来观测只作标签。
4. **状态token与候选动作token混淆**：若head特征依赖噪声和某个reference动作，必须明确它是参考动作条件表示，还是每个candidate专属表示；不能默认它就是与动作无关的Markov state。
5. **监督没有梯度**：仅在实测标签上计算物理残差不会训练token；损失必须连接预测分支和readout。常量约束值不是学习机制。
6. **外挂改变执行预算**：候选数、采样步数、重规划频率、允许重试次数、额外传感器和实际仿真时长都要匹配。
7. **先验保留和负结果**：若history-only已覆盖全部收益，或head不优于backbone，应调整假设，不用Universal/Physics命名掩盖结果。

### 今天与同事讨论时应形成的输出

不是马上确定整篇论文，而是为上述三条路线分别填清：新增模块、训练对象、监督标签、部署可得性、最强近邻、最小对照、失败即停止的判据。真机同事优先确认可用的q/qdot/夹爪/F-T/触觉/相机时间戳和实际下发控制命令；你负责论文机制与对照合同。第一阶段无需同时开展在线RL、WAM预训练和planner演化。


# 全部125项文献


## A｜动作侧表征与最邻近工作

### P001 · RLT [P0]

**完整题名：**RL Token: Bootstrapping Online RL with Vision-Language-Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**用重建式紧凑读出保留VLA信息，并供轻量actor/critic进行在线学习。

**项目关系（研究分析）：**compact readout + frozen大模型 + 小型RL本身已有；必须对比原RLT，而非把RLT描述成仅有reward监督。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2604.23073

### P002 · Pri4R [P0]

**完整题名：**Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**以训练期未来3D点轨迹监督VLA表示，部署时不需要相同privileged标签。

**项目关系（研究分析）：**未来几何/动力学辅助监督并非新点；需证明action-conditioned、compact readout及控制收益。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2603.01549

### P003 · FLARE [P0]

**完整题名：**FLARE: Robot Learning with Implicit World Modeling

**发表/版本：**CoRL 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**使用少量额外token，将策略内部表示与未来观测潜变量对齐，进行隐式世界建模。

**项目关系（研究分析）：**少量token + future latent prediction与方案高度相邻；必做同容量future-feature监督对照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v305/zheng25a.html

### P004 · AGRA [P0]

**完整题名：**Making Foresight Actionable: Repurposing Representation Alignment in World Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**研究预测世界的特征为何未必适合动作解码，并通过Action-Grounded Representation Alignment改善对齐。

**项目关系（研究分析）：**不能仅以future预测更好推导控制更好；需核验head特征、对齐目标和因果干预实验。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.12217

### P005 · CometVLA [P0]

**完整题名：**CometVLA: Co-Training on an Embodied Data Pyramid towards Physical Understanding

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**用紧凑Global Action Prior tokens连接物理常识、运动规律与动作生成，并进行多层次数据联合训练。

**项目关系（研究分析）：**compact物理信息接口通向action head已有近邻；需区分后读出/冻结外挂与联合预训练。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.30289

### P006 · PAR [P0]

**完整题名：**Physical Autoregressive Model for Robotic Manipulation without Action Pretraining

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**把视频和动作组织成共享physical tokens，借助视频预训练进行连续自回归世界—动作建模。

**项目关系（研究分析）：**Physical Token名称和联合物理token概念已出现，不能声称首创；本项目需区分生成token与控制读出latent。

**核验边界：**与PhysGen具有作者/内容关联，应按关联工作核查，不能将其当作两个完全独立实验证据。

**一手来源：**https://arxiv.org/abs/2508.09822

### P007 · PhysGen [P1]

**完整题名：**Learning Physics from Pretrained Video Models: A Multimodal Continuous and Sequential World Interaction Models for Robotic Manipulation

**发表/版本：**ICMR 2026；主表年份：2026。

**本轮证据：**正式出版记录。

**方法（来源摘要）：**视频与动作共享连续physical tokens，通过视频预训练、因果建模和高效解码学习交互。

**项目关系（研究分析）：**命名与物理latent概念有重合；ICMR是相关多媒体会议，不在此冒充机器人旗舰会议。

**核验边界：**arXiv提示与PAR存在文本关联；题名保留原文语法。两项题录不等于两个独立研究方向。

**一手来源：**https://arxiv.org/abs/2603.00110

**出版补充：**https://doi.org/10.1145/3805622.3810752

### P008 · SA-VLA [P1]

**完整题名：**SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**动作tokenizer/decoder利用机器人状态，缓解脱离当前状态的动作编码问题。

**项目关系（研究分析）：**状态感知action token已有；需要比较状态输入本身与物理监督的独立作用。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.30113

### P009 · ActionPiece [P1]

**完整题名：**ActionPiece: Rethinking Action Tokenization for Autoregressive Vision-Language-Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**物理距离排序一致性监督离散动作表示与量化，保留动作间局部关系。

**项目关系（研究分析）：**动作几何关系不等于接触动力学；但physics-oriented action-token loss已有，必须比较目标语义。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2609.18487

### P010 · Spline Policy [P0]

**完整题名：**Spline Policy: A Structured Representation for Robot Policies

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**用样条参数压缩动作轨迹，支持多种策略架构，并结合结构化轨迹约束。

**项目关系（研究分析）：**多骨干共用紧凑动作接口已有；需把轨迹参数化与隐藏物理状态读出区别清楚。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.07386

### P011 · PhysVLA [P1]

**完整题名：**PhysVLA: Towards Physically-Grounded VLA for Embodied Robotic Manipulation

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**对已有VLA增加物理相关的推理期执行修正。

**项目关系（研究分析）：**物理外挂/不改骨干本身不足为创新；需与output-only修正和约束投影比较。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.13886

### P012 · MCF-Proto [P1]

**完整题名：**Beyond World-Frame Action Heads: Motion-Centric Action Frames for Vision-Language-Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**动作头学习SO(3)局部运动坐标系与动作原型，形成紧凑几何组织。

**项目关系（研究分析）：**head结构化和几何泛化已有；需分清坐标改进、动作压缩与动力学适应。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2605.11809

### P013 · X-DiffVLA [P1]

**完整题名：**X-DiffVLA: X-Embodied Diffusion Action Heads for Vision-Language-Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**统一扩散动作头，结合embodiment forcing和形态树，迁移不同末端执行器的数据。

**项目关系（研究分析）：**跨本体动作头不是空白；其共享机器人基座/异构末端条件限制需与自己的transfer协议对齐。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2605.25044

### P014 · DyWA [P0]

**完整题名：**DyWA: Dynamics-adaptive World Action Model for Generalizable Non-prehensile Manipulation

**发表/版本：**ICCV 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**结合历史交互、未来状态预测和动作学习，适应非抓取任务中的质量与摩擦变化。

**项目关系（研究分析）：**history + dynamics + action联合建模是直接近邻；必须纳入推动/摩擦任务的强对照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://openaccess.thecvf.com/content/ICCV2025/html/Lyu_DyWA_Dynamics-adaptive_World_Action_Model_for_Generalizable_Non-prehensile_Manipulation_ICCV_2025_paper.html

### P015 · GAP [P1]

**完整题名：**Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation

**发表/版本：**arXiv 2026；CVPR题录线索；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**融合几何latent、2D语义和proprio，联合预测动作chunk与未来3D latent/pointmap。

**项目关系（研究分析）：**动作和未来几何联合预测已有；重点区分几何预测与接触效果判别。

**核验边界：**arXiv摘要已核验；CVPR日程存在题录线索，本表不据此标为正式论文集全文核验。

**一手来源：**https://arxiv.org/abs/2602.23814

### P016 · VLA物理/空间复审 [P1]

**完整题名：**VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling

**发表/版本：**CVPR 2026；主表年份：2026。

**本轮证据：**正式论文集。

**方法（来源摘要）：**重新分析VLA物理与空间建模的泛化来源。

**项目关系（研究分析）：**失败可能是空间/观测标定而非缺物理；应先排除替代解释。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://openaccess.thecvf.com/content/CVPR2026/html/Li_VLA_Models_Are_More_Generalizable_Than_You_Think_Revisiting_Physical_CVPR_2026_paper.html


## B｜动力学充分表示、历史辨识与表征理论

### P017 · UP-OSI [P1]

**完整题名：**Preparing for the Unknown: Learning a Universal Policy with Online System Identification

**发表/版本：**RSS 2017；主表年份：2017。

**本轮证据：**作者项目与论文。

**方法（来源摘要）：**通过在线系统辨识估计隐藏动力学，再条件化通用策略。

**项目关系（研究分析）：**从执行历史推断物理上下文已有长期先例；必须加入history-only基线。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://faculty.cc.gatech.edu/~turk/paper_pages/2017_learning_universal_policy/index.html

### P018 · RMA [P1]

**完整题名：**RMA: Rapid Motor Adaptation for Legged Robots

**发表/版本：**RSS 2021；主表年份：2021。

**本轮证据：**正式论文集。

**方法（来源摘要）：**训练特权环境编码器，再以历史观测适应模块替代不可见物理参数。

**项目关系（研究分析）：**latent物理适应/privileged teacher并不新；迁移到操作需明确新机制。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.roboticsproceedings.org/rss17/p011.html

### P019 · Manipulator RMA [P1]

**完整题名：**Rapid Motor Adaptation for Robotic Manipulator Arms

**发表/版本：**CVPR 2024；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**利用动作与本体状态历史推断影响机械臂控制的隐藏条件。

**项目关系（研究分析）：**与你的history-aware physical token直接相邻；原始历史加小模型应成为必做对照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://openaccess.thecvf.com/content/CVPR2024/html/Liang_Rapid_Motor_Adaptation_for_Robotic_Manipulator_Arms_CVPR_2024_paper.html

### P020 · DeepMDP [P1]

**完整题名：**DeepMDP: Learning Continuous Latent Space Models for Representation Learning

**发表/版本：**ICML 2019；主表年份：2019。

**本轮证据：**正式论文集。

**方法（来源摘要）：**用奖励和latent状态转移预测约束控制表征，并分析价值保持。

**项目关系（研究分析）：**为“对决策充分”提供理论参照；预测任意物理量不自动等于价值充分。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v97/gelada19a.html

### P021 · DBC [P1]

**完整题名：**Learning Invariant Representations for Reinforcement Learning without Reconstruction

**发表/版本：**ICLR 2021；主表年份：2021。

**本轮证据：**作者机构论文页。

**方法（来源摘要）：**用bisimulation相关度量保留奖励与转移相关信息，而非重建全部视觉细节。

**项目关系（研究分析）：**物理充分表示须保留可控/价值相关差异，也应丢掉无关纹理。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://ai.meta.com/research/publications/learning-invariant-representations-for-reinforcement-learning-without-reconstruction/

### P022 · SPR [P1]

**完整题名：**Data-Efficient Reinforcement Learning with Self-Predictive Representations

**发表/版本：**arXiv 2020；ICLR版本待逐页核验；主表年份：2020。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**从当前latent和动作预测未来表征，改善数据效率。

**项目关系（研究分析）：**预测未来latent用于RL早已有之；仅增加预测头不构成充分新意。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2007.05929

### P023 · TACO [P0]

**完整题名：**TACO: Temporal Latent Action-Driven Contrastive Loss for Visual Reinforcement Learning

**发表/版本：**NeurIPS 2023；主表年份：2023。

**本轮证据：**作者机构论文页。

**方法（来源摘要）：**用latent动作序列与未来状态的时序对比目标学习控制相关表示。

**项目关系（研究分析）：**action-conditioned、temporal、可接在线/离线RL都已有近邻；需比较真实后果/跨head增量。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.microsoft.com/en-us/research/publication/taco-temporal-latent-action-driven-contrastive-loss-for-visual-reinforcement-learning/?lang=ja

### P024 · TD-MPC [P1]

**完整题名：**Temporal Difference Learning for Model Predictive Control

**发表/版本：**ICML 2022；主表年份：2022。

**本轮证据：**正式论文集。

**方法（来源摘要）：**联合学习task-oriented latent dynamics、价值和短期规划。

**项目关系（研究分析）：**task-oriented latent dynamics是成熟范式；你应证明预训练head信息的不可替代价值。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v162/hansen22a.html

### P025 · TD-MPC2 [P1]

**完整题名：**TD-MPC2: Scalable, Robust World Models for Continuous Control

**发表/版本：**ICLR 2024；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**可扩展latent世界模型与连续控制，关注稳定训练和跨任务容量。

**项目关系（研究分析）：**共享latent + 多任务控制不是空白；以其表征/归一化经验作机制参照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.iclr.cc/paper_files/paper/2024/hash/cf73d57b6dcda32b293df7c2d5341f49-Abstract-Conference.html

### P026 · R3M [P1]

**完整题名：**R3M: A Universal Visual Representation for Robot Manipulation

**发表/版本：**CoRL 2022（论文集2023）；主表年份：2022。

**本轮证据：**正式论文集。

**方法（来源摘要）：**视频时序对比、语言对齐和稀疏性训练冻结视觉表示，服务下游操作学习。

**项目关系（研究分析）：**冻结通用表示+轻量下游是成熟路线；需要区别视觉表征与动作后果表征。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v205/nair23a.html

### P027 · VIP [P1]

**完整题名：**VIP: Towards Universal Visual Reward and Representation via Value-Implicit Pre-Training

**发表/版本：**arXiv 2022；ICLR版本待逐页核验；主表年份：2022。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**从无动作标注的人类视频学习可迁移表示与视觉奖励。

**项目关系（研究分析）：**比较几何预测是否真的优于价值相关表征；注意VIP并非动作条件动力学模型。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2210.00030

### P028 · Offline meta-RL [P2]

**完整题名：**Offline Meta-Reinforcement Learning with Online Self-Supervision

**发表/版本：**ICML 2022；主表年份：2022。

**本轮证据：**正式论文集。

**方法（来源摘要）：**用无奖励在线数据减轻离线meta-RL适应时的分布偏移。

**项目关系（研究分析）：**无奖励执行反馈促进适应已有方法；借鉴离线—部署分布漂移控制。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v162/pong22a.html

### P029 · Situational dynamics [P1]

**完整题名：**Situationally-aware dynamics learning

**发表/版本：**IJRR 2026（online-first）；主表年份：2026。

**本轮证据：**期刊正式记录。

**方法（来源摘要）：**情境感知的自适应动力学学习。

**项目关系（研究分析）：**与历史推断局部系统状态相邻；需要进一步精读辨识变量与更新规则。

**核验边界：**本轮仅核验出版题录与摘要方向；不据此推断已支持VLA或action-head接口。

**一手来源：**https://journals.sagepub.com/doi/abs/10.1177/02783649261431863


## C｜力触觉、接触与多模态物理监督

### P030 · Making Sense [P1]

**完整题名：**Making Sense of Vision and Touch: Learning Multimodal Representations for Contact-Rich Tasks

**发表/版本：**IEEE T-RO 2020；主表年份：2020。

**本轮证据：**期刊正式记录。

**方法（来源摘要）：**自监督融合视觉、触觉/力和机器人状态，学习接触操作表示供控制使用。

**项目关系（研究分析）：**紧凑多感官latent+接触控制并非新概念；应与早期多模态表征学习定位比较。

**核验边界：**与较早会议版本有关，本表以T-RO条目统一记录。

**一手来源：**https://ieeexplore.ieee.org/document/9043710/

**出版补充：**https://arxiv.org/abs/1907.13098

### P031 · FD-VLA [P0]

**完整题名：**FD-VLA: Force-Distilled Vision-Language-Action Model for Contact-Rich Manipulation

**发表/版本：**ICRA 2026（作者录用声明）；主表年份：2026。

**本轮证据：**arXiv摘要与录用声明。

**方法（来源摘要）：**以真实力latent监督视觉/状态条件的learnable query，推理时注入力token而不要求同样力传感器。

**项目关系（研究分析）：**力蒸馏、query token、部署去传感器已做；需证明不同于force surrogate。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2602.02142

### P032 · HapticVLA [P0]

**完整题名：**HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**利用训练期触觉信息塑造VLA，部署时不依赖相同触觉输入。

**项目关系（研究分析）：**训练特权触觉蒸馏不是空白；关注监督位置、teacher以及动作生成方式。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2603.15257

### P033 · MSDP [P0]

**完整题名：**Self-Supervised Multisensory Pretraining for Contact-Rich Robot Reinforcement Learning

**发表/版本：**IEEE RA-L 2026；主表年份：2026。

**本轮证据：**arXiv摘要与正式期刊书目信息。

**方法（来源摘要）：**masked多感官预训练；冻结表示后critic采用动态cross-attention，actor采用稳定pooling。

**项目关系（研究分析）：**多模态latent及actor/critic非对称用法已有；不能把critic用更多物理信息当成独立创新。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2511.14427

**出版补充：**https://doi.org/10.1109/LRA.2026.3681156

### P034 · MuSe [P1]

**完整题名：**Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**将新的力模态纳入已有视觉运动策略，同时考虑原能力保持。

**项目关系（研究分析）：**后加物理模态与持续学习已有；需用旧任务保持和传感器缺失测试区分。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.30988

### P035 · DeCAL [P0]

**完整题名：**DeCAL: Towards Physically-Grounded Dexterous Vision-Language-Action Models via Contact-Aware Latent Co-Imagination

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**contact-aware视觉触觉门控及latent co-imagination，统一理解、预测和动作。

**项目关系（研究分析）：**contact-aware latent world knowledge高度相关；重点比较重型联合模型与小型冻结外挂。

**核验边界：**本轮arXiv页未见CoRL录用信息，因此不沿用此前对CoRL 2026的未经核验归类。

**一手来源：**https://arxiv.org/abs/2609.09119

### P036 · exUMI [P0]

**完整题名：**exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation

**发表/版本：**CoRL 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**动作感知、任务无关的触觉表示学习及可扩展示教系统。

**项目关系（研究分析）：**action-aware/task-agnostic physical representation已有；需要核查时序预测目标与泛化设置。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v305/xu25e.html

### P037 · TacX [P1]

**完整题名：**Tactile Beyond Pixels: Multisensory Touch Representations for Robot Manipulation

**发表/版本：**CoRL 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**跨图像、声音、运动、压力等触觉信号学习多感官表示。

**项目关系（研究分析）：**共享多传感器latent已有；传感器适配与动作head适配应分别验证。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v305/higuera25a.html

### P038 · Sparsh [P1]

**完整题名：**Sparsh: Self-supervised touch representations for vision-based tactile sensing

**发表/版本：**CoRL 2024（论文集2025）；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**跨视觉式触觉传感器的自监督预训练，并建立TacBench。

**项目关系（研究分析）：**触觉通用表示的重要teacher/基线；不能仅以多传感器共享token主张普适。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v270/higuera25a.html

### P039 · UpViTaL [P1]

**完整题名：**UpViTaL: Unpaired Visual-Tactile Self-Supervised Representation Learning for Dexterous Robotic Manipulation

**发表/版本：**ICRA 2025；主表年份：2025。

**本轮证据：**正式出版记录。

**方法（来源摘要）：**不成对的视觉触觉自监督表示学习，用于灵巧操作。

**项目关系（研究分析）：**privileged物理与视觉对齐未必要求逐帧配对；可借鉴降低标注成本。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://ieeexplore.ieee.org/document/11127230/

### P040 · RoboPack [P0]

**完整题名：**RoboPack: Learning Tactile-Informed Dynamics Models for Dense Packing

**发表/版本：**RSS 2024；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**触觉与视觉历史帮助学习物体级动力学模型，用于密集装填控制。

**项目关系（研究分析）：**隐藏物理属性latent→动作后果→MPC是强近邻；需验证token与真实接触响应的对应。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.roboticsproceedings.org/rss20/p130.html

### P041 · See, feel, act [P1]

**完整题名：**See, feel, act: Hierarchical learning for complex manipulation skills with multisensory fusion

**发表/版本：**Science Robotics 2019；主表年份：2019。

**本轮证据：**期刊正式记录。

**方法（来源摘要）：**多感官融合支持复杂接触操作和分层技能学习。

**项目关系（研究分析）：**物理交互、触觉表示与动作决策的历史根基；不是VLA才出现的问题。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://doi.org/10.1126/scirobotics.aav3123

### P042 · Deep Haptic MPC [P1]

**完整题名：**Deep Haptic Model Predictive Control for Robot-Assisted Dressing

**发表/版本：**arXiv 2017；主表年份：2017。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**用历史末端触觉/运动观测和候选动作预测未来受力，再通过MPC减小危险力。

**项目关系（研究分析）：**candidate action→force consequence→control早已有明确实现；可借鉴物理target和闭环设计。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/1709.09735

### P043 · UniTac-NV [P1]

**完整题名：**UniTac-NV: A Unified Tactile Representation For Non-Vision-Based Tactile Sensors

**发表/版本：**IROS 2025（作者接收声明）；主表年份：2025。

**本轮证据：**arXiv摘要＋作者接收声明。

**方法（来源摘要）：**传感器专用编码器与共享潜空间实现非视觉触觉跨传感器迁移。

**项目关系（研究分析）：**shared latent＋specific adapter已有强相关先例；你的通用性须以跨head/机器人迁移证明。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2506.19699


## D｜显式物理模型、可微约束与安全控制

### P044 · PIN-WM [P0]

**完整题名：**PIN-WM: Learning Physics-INformed World Models for Non-Prehensile Manipulation

**发表/版本：**RSS 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**将可微物理与视觉世界模型结合，用于非抓取操作。

**项目关系（研究分析）：**physics-informed world model已有；应证明紧凑读出比完整物理模型更合适，而非只比较无物理模型。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.roboticsproceedings.org/rss21/p153.html

### P045 · DeLaN [P1]

**完整题名：**Deep Lagrangian Networks: Using Physics as Model Prior for Deep Learning

**发表/版本：**arXiv 2019；ICLR版本待逐页核验；主表年份：2019。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**把拉格朗日结构嵌入动力学网络。

**项目关系（研究分析）：**动力学结构约束不能只写方程；必须核查力矩、惯量和实际控制器是否可识别。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/1907.04490

### P046 · ContactNets [P1]

**完整题名：**ContactNets: Learning Discontinuous Contact Dynamics with Smooth, Implicit Representations

**发表/版本：**CoRL 2020（作者录用声明）；主表年份：2020。
**本轮证据：**arXiv摘要与录用声明。

**方法（来源摘要）：**学习signed distance和contact Jacobian，并以互补性、最大耗散结构处理非连续接触。

**项目关系（研究分析）：**连续平滑损失未必适合冲击/粘滑；真正接触物理需要结构或有效事件目标。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2009.11193

### P047 · GNS [P1]

**完整题名：**Learning to Simulate Complex Physics with Graph Networks

**发表/版本：**ICML 2020；主表年份：2020。

**本轮证据：**正式论文集。

**方法（来源摘要）：**图网络学习多类物理系统动力学。

**项目关系（研究分析）：**对象/关系结构是可选物理归纳偏置；需比较结构latent与无结构token。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v119/sanchez-gonzalez20a.html

### P048 · DPI-Net [P1]

**完整题名：**Learning Particle Dynamics for Manipulating Rigid Bodies, Deformable Objects, and Fluids

**发表/版本：**arXiv 2018；ICLR版本待逐页核验；主表年份：2018。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**粒子和交互网络模拟不同材料物体的动态变化。

**项目关系（研究分析）：**表示需随物理对象与接触关系变化；跨刚体/软体不能只靠相同latent维数。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/1810.01566

### P049 · RoboCraft [P1]

**完整题名：**RoboCraft: Learning to see, simulate, and shape elasto-plastic objects in 3D with graph networks

**发表/版本：**IJRR 2024；主表年份：2024。

**本轮证据：**期刊正式记录。

**方法（来源摘要）：**视觉粒子化、图动力学与规划结合，实现弹塑性物体形状操作。

**项目关系（研究分析）：**已有action-conditioned consequence→planner闭环；区别控制读出与完整物理模拟。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://journals.sagepub.com/doi/10.1177/02783649231219020

### P050 · SAM-RL [P1]

**完整题名：**SAM-RL: Sensing-Aware Model-Based Reinforcement Learning via Differentiable Physics-Based Simulation and Rendering

**发表/版本：**RSS 2023；主表年份：2023。

**本轮证据：**正式论文集。

**方法（来源摘要）：**可微物理仿真和渲染参与模型式RL与感知适配。

**项目关系（研究分析）：**仿真特权监督/可微物理已有；需要校准real-to-sim与部署输入边界。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://roboticsproceedings.org/rss19/p040.html

### P051 · PROMPT [P2]

**完整题名：**Ab Initio Particle-based Object Manipulation

**发表/版本：**RSS 2021；主表年份：2021。

**本轮证据：**正式论文集。

**方法（来源摘要）：**粒子式对象表示支持操作推理与控制。

**项目关系（研究分析）：**对象物理表示+操作决策的早期参照；用于回溯引用，不是直接VLA竞品。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://roboticsproceedings.org/rss17/p071.html

### P052 · One-Shot Real-to-Sim [P1]

**完整题名：**One-Shot Real-to-Sim via End-to-End Differentiable Simulation and Rendering

**发表/版本：**IEEE RA-L 2025；主表年份：2025。

**本轮证据：**正式出版记录。

**方法（来源摘要）：**通过可微仿真与渲染从现实观测辨识仿真属性。

**项目关系（研究分析）：**隐藏属性辨识可显式做，也可latent做；应对比辨识误差与控制用途。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://ieeexplore.ieee.org/document/10982102/

**出版补充：**https://doi.org/10.1109/LRA.2025.3566623

### P053 · PhysDreamer [P1]

**完整题名：**PhysDreamer: Physics-Based Interaction with 3D Objects via Video Generation

**发表/版本：**ECCV 2024（作者项目页）；主表年份：2024。

**本轮证据：**作者项目与论文。

**方法（来源摘要）：**视频生成先验为可微物理物体交互提供监督。

**项目关系（研究分析）：**从视频提取物理先验已有；生成像真的运动不等于经过真实动作干预检验的因果模型。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://physdreamer.github.io/

### P054 · PhysMani [P1]

**完整题名：**PhysMani: Physics-principled 3D World Model for Dynamic Object Manipulation

**发表/版本：**ECCV 2026（作者声明）；主表年份：2026。

**本轮证据：**arXiv摘要与会议声明。

**方法（来源摘要）：**物理约束3D Gaussian速度场预测动态场景，learnable token cross-attention向策略注入未来信息。

**项目关系（研究分析）：**物理世界模型+token注入策略是直接邻居；需与action-head后读出区分并检验额外计算。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.01938

### P055 · LeTO [P0]

**完整题名：**LeTO: Learning Constrained Visuomotor Policy with Differentiable Trajectory Optimization

**发表/版本：**IEEE T-ASE（2024作者接受稿）；主表年份：2024。

**本轮证据：**作者机构接受稿与DOI。

**方法（来源摘要）：**把可微轨迹优化层放进视觉运动策略，联合动作拟合、平滑与约束。

**项目关系（研究分析）：**可微物理/运动学约束的动作外挂已有；应与解析投影而非只有无约束策略比较。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://docs.lib.purdue.edu/iepubs/14/

**出版补充：**https://doi.org/10.1109/TASE.2024.3486542

### P056 · DDAT [P1]

**完整题名：**DDAT: Diffusion Policies Enforcing Dynamically Admissible Robot Trajectories

**发表/版本：**RSS 2025；主表年份：2025。

**本轮证据：**作者项目与论文。

**方法（来源摘要）：**训练与推理中将扩散轨迹投影到动力学可实现集合。

**项目关系（研究分析）：**物理可行轨迹生成已有强基线；不要把joint-limit penalty等价于更强安全保证。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://iconlab.negarmehr.com/DDAT/

### P057 · DPCC [P1]

**完整题名：**Diffusion Predictive Control with Constraints

**发表/版本：**arXiv 2024；主表年份：2024。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**约束收紧和模型投影进入扩散采样，处理训练时未见的状态/动作约束。

**项目关系（研究分析）：**测试时新物理约束适应已有；需检验learned token对比显式投影的额外价值。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2412.09342

### P058 · MDOC [P2]

**完整题名：**Model-Based Diffusion Optimal Control for Multi-Robot Motion Planning

**发表/版本：**RSS 2026；主表年份：2026。

**本轮证据：**正式论文集。

**方法（来源摘要）：**已知动力学与CBF投影结合扩散控制，并扩展到多机器人规划。

**项目关系（研究分析）：**解析安全与学习物理表示应分层；此类保证依赖其明确模型假设。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.roboticsproceedings.org/rss22/p041.html

### P059 · Learned CBF [P1]

**完整题名：**Learning Control Barrier Functions from Expert Demonstrations

**发表/版本：**arXiv 2020；正式会议信息待逐页核验；主表年份：2020。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**由专家示范学习控制障碍函数。

**项目关系（研究分析）：**安全约束学习与任务表示学习不同；比较硬控制保护和soft物理loss。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2004.03315

### P060 · Safe Learning review [P1]

**完整题名：**Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning

**发表/版本：**Annual Review of Control, Robotics, and Autonomous Systems 2022；主表年份：2022。

**本轮证据：**正式综述。

**方法（来源摘要）：**综述学习控制、安全RL及保证成立所需假设。

**项目关系（研究分析）：**用于给安全、鲁棒、约束满足做严格定义；不是一个新算法结果。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.annualreviews.org/content/journals/10.1146/annurev-control-042920-020211

### P061 · Learning-Based MPC review [P1]

**完整题名：**Learning-Based Model Predictive Control: Toward Safe Learning in Control

**发表/版本：**Annual Review of Control, Robotics, and Autonomous Systems 2020；主表年份：2020。

**本轮证据：**正式综述。

**方法（来源摘要）：**综述学习增强MPC、模型误差与安全学习。

**项目关系（研究分析）：**未来physical critic/预测后果引导决策需处理不确定性和模型误差。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://doi.org/10.1146/annurev-control-090419-075625

### P062 · UMI-on-Air [P1]

**完整题名：**UMI-on-Air: Embodiment-Aware Guidance for Embodiment-Agnostic Visuomotor Policies

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**利用下层控制器tracking cost梯度引导扩散策略，适应不同机器人动力学。

**项目关系（研究分析）：**不改预训练策略的跨本体动力学外挂已有；需比较控制器成本指导与物理token。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2510.02614

### P063 · HFVC Preconditions [P1]

**完整题名：**Learning Preconditions of Hybrid Force-Velocity Controllers for Contact-Rich Manipulation

**发表/版本：**CoRL 2022（PMLR 2023）；主表年份：2022。

**本轮证据：**正式论文集。

**方法（来源摘要）：**学习混合力-速度控制器何时可成功的前提条件，并用于接触操作规划。

**项目关系（研究分析）：**operating range/能力边界不是新概念；Physical Token的失败probe要与此类先例对照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v205/liang23a.html

### P064 · Fill the Seam [P2]

**完整题名：**Learning to Fill the Seam by Vision: Sub-millimeter Peg-in-hole on Unseen Shapes in Real World

**发表/版本：**ICRA 2022；主表年份：2022。

**本轮证据：**出版社题录／摘要。

**方法（来源摘要）：**面向未见形状的视觉精细插入，研究亚毫米级装配。

**项目关系（研究分析）：**说明精密任务要看几何与控制协议，不能直接以任务名称推断接触物理难度。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://ieeexplore.ieee.org/document/9812429/

### P065 · Diffused Orientation Fields [P2]

**完整题名：**Object-centric task representation and transfer using diffused orientation fields

**发表/版本：**Science Robotics 2026；主表年份：2026。

**本轮证据：**出版社检索题录。

**方法（来源摘要）：**以物体中心的方向场研究任务表示与迁移。

**项目关系（研究分析）：**几何结构化任务表示的期刊对照；本轮只完成题录级筛查，不声称已精读其动力学机制。

**核验边界：**出版社全文访问受限；仅使用已核验题录与公开摘要级信息。

**一手来源：**https://doi.org/10.1126/scirobotics.aea1762

### P066 · Prof. Robot [P1]

**完整题名：**Prof. Robot: Differentiable Robot Rendering Without Static and Self-Collisions

**发表/版本：**CVPR 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**可微机器人渲染与碰撞相关几何模型，为轨迹调整提供梯度。

**项目关系（研究分析）：**碰撞约束外挂属于已有路线；应对照解析/可微几何模块而非只对照原始VLA。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://openaccess.thecvf.com/content/CVPR2025/html/Ruan_Prof._Robot_Differentiable_Robot_Rendering_Without_Static_and_Self-Collisions_CVPR_2025_paper.html


## E｜世界—动作模型与潜空间未来预测

### P067 · RepWAM [P1]

**完整题名：**RepWAM: World Action Modeling with Representation Visual-Action Tokenizers

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**表示层视觉—动作tokenization与世界动作联合建模。

**项目关系（研究分析）：**共享视觉动作latent不是空白；需区分生成模型token和下游通用物理读出。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.13674

### P068 · OA-WAM [P1]

**完整题名：**OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**可寻址对象/机器人结构参与世界与动作建模。

**项目关系（研究分析）：**结构化object/contact token的参考；不能把人为分成几个token本身当贡献。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2605.06481

### P069 · Riemann-1.0 [P1]

**完整题名：**Riemann-1.0: An Embodied World Action Model for Physical AI

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**统一观测、状态与动作的世界动作模型。

**项目关系（研究分析）：**WAM扩展需明确究竟读动作模块还是视频模块，而不是把任何视频模型当action head。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.27033

### P070 · WAM-RL [P1]

**完整题名：**WAM-RL: World-Action Model Reinforcement Learning with Reconstruction Rewards and Online Video SFT

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**重建奖励与在线视频监督服务世界动作模型的强化学习。

**项目关系（研究分析）：**WAM和RL耦合已有；需要分离表征改进、奖励改变和模型更新三个变量。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.17906

### P071 · RISE [P1]

**完整题名：**RISE: Self-Improving Robot Policy with Compositional World Model

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**组合动力学与价值模型，在想象环境中改进机器人策略。

**项目关系（研究分析）：**后果预测必须转化为更好的动作评价/策略，不能只报预测loss。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2602.11075

### P072 · Motus2 [P1]

**完整题名：**Motus2: A Self-Evolving General World Model for Dexterous Manipulation

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**世界动作、动作条件预测和价值评估形成策略改进回路，并考虑触觉等信息。

**项目关系（研究分析）：**action→consequence→value整个故事已有；小型外挂的效率和可迁移性必须实测。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.30237

### P073 · CauVA [P1]

**完整题名：**Causal World Modeling for Robot Control

**发表/版本：**RSS 2026；主表年份：2026。

**本轮证据：**正式论文集。

**方法（来源摘要）：**因果信息流下建模视频与动作，为机器人控制提供世界预测。

**项目关系（研究分析）：**训练期未来信息泄漏需要明确屏蔽；causal mask本身也已有研究。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.roboticsproceedings.org/rss22/p016.html

### P074 · DINO-WM [P1]

**完整题名：**DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning

**发表/版本：**ICML 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**基于冻结DINO视觉特征学习动作条件latent动力学，实现零样本规划。

**项目关系（研究分析）：**冻结表征 + 小预测模型 + 不改策略规划是重要对照；并非必须action-head才能做到。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v267/zhou25t.html

### P075 · V-JEPA 2 [P1]

**完整题名：**V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**视频latent预测预训练，并引入动作条件学习服务规划。

**项目关系（研究分析）：**要证明动作head读出是否优于通用视频预测特征；视觉世界模型是必须面对的基线。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2506.09985

### P076 · DreamerV3 [P1]

**完整题名：**Mastering diverse control tasks through world models

**发表/版本：**Nature 2025；主表年份：2025。

**本轮证据：**期刊正式记录。

**方法（来源摘要）：**在latent世界模型想象中进行跨多任务的策略价值学习。

**项目关系（研究分析）：**通用latent控制与稳定训练有成熟先例；真实机器人上的证据仍须独立检验。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://www.nature.com/articles/s41586-025-08744-2

### P077 · Human-video structured WM [P1]

**完整题名：**Structured World Models from Human Videos

**发表/版本：**RSS 2023；主表年份：2023。

**本轮证据：**正式论文集。

**方法（来源摘要）：**从人类视频学习结构化世界模型服务控制。

**项目关系（研究分析）：**跨数据来源的world prior可借鉴，但human-video动态不自动等于机器人action-conditioned反馈。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://roboticsproceedings.org/rss19/p012.html

### P078 · DiWA [P1]

**完整题名：**DiWA: Diffusion Policy Adaptation with World Models

**发表/版本：**CoRL 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**在离线学得的世界模型内用RL适配扩散策略，减少额外真实交互。

**项目关系（研究分析）：**绕开昂贵online交互已有直接方案；需比较模型偏差及BC保持，不应预设离线必稳。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v305/chandra25a.html

### P079 · EgoWAM [P1]

**完整题名：**EgoWAM: World Action Models Beyond Pixels with In-the-Wild Egocentric Human Data

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**研究像素以外的world-action表示及真实第一视角数据。

**项目关系（研究分析）：**不同future target的对比很适合物理token；人类数据迁移和机器人标签作用应拆开。

**核验边界：**作者页曾标Under Review；本表不将其升级为CoRL已录用。

**一手来源：**https://arxiv.org/abs/2607.08436

### P080 · GlanceWAM [P1]

**完整题名：**GlanceWAM: Sparse Test-Time Imagination for World-Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**慢速异步未来想象与快速latent动作解码解耦，处理预测陈旧性。

**项目关系（研究分析）：**WAM对接必须考虑生成时间、observation age与控制延迟，而不只hidden维数。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.23927

### P081 · Video2Act [P1]

**完整题名：**Video2Act: A Dual-System Video Diffusion Policy with Robotic Spatio-Motional Modeling

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**从视频生成的空间/运动特征条件化动作策略。

**项目关系（研究分析）：**视频内部特征→动作接口与action-side读出相邻；需精读接口位置与冻结范围。

**核验边界：**arXiv v3于2026-03更新；本轮核验摘要，后续需检查异步接口与完整消融。

**一手来源：**https://arxiv.org/abs/2512.03044

### P082 · PointWorld [P1]

**完整题名：**PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation

**发表/版本：**CVPR 2026（作者项目页）；主表年份：2026。

**本轮证据：**作者项目与论文。

**方法（来源摘要）：**把机器人动作和场景状态统一为3D点流，跨本体学习动作后果并用于MPC。

**项目关系（研究分析）：**统一物理动作坐标 + consequence + 跨本体已存在；要证明head latent较3D统一空间的价值。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://point-world.github.io/

**出版补充：**https://arxiv.org/abs/2601.03782


## F｜离线／在线RL、价值引导与冻结策略适配

### P083 · RECAP / π*0.6 [P0]

**完整题名：**π*0.6: a VLA That Learns From Experience

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**结合示范、自主经验与纠正，以价值/优势条件化策略进行改进。

**项目关系（研究分析）：**是下游候选而非天然轻量冻结外挂；不能由别处成功率推断一定比你的RLT稳定。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2511.14759

### P084 · LWD [P1]

**完整题名：**Learning While Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**DIVL价值学习与Q-learning via Adjoint Matching服务跨机器人群经验回流和策略后训练。

**项目关系（研究分析）：**经验闭环和value→policy更新已有；需分清representation贡献与learner贡献。

**核验边界：**本轮核验v4；QAM全称为Q-learning via Adjoint Matching，不是泛称advantage matching。

**一手来源：**https://arxiv.org/abs/2605.00416

### P085 · Q-VGM [P0]

**完整题名：**Q-VGM: Q-Guided Value-Gradient Matching for Offline-to-Online RL of Flow-Matching VLA Policies

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**action-sensitive chunk critic与局部速度匹配目标引导flow action expert，避免整段去噪反传。

**项目关系（研究分析）：**可作物理token下游，但会改action expert；应与完全冻结base的主实验分开。

**核验边界：**2026-09-17已有v5，方法描述应绑定版本，不机械沿用早期稿。

**一手来源：**https://arxiv.org/abs/2606.08015

### P086 · V-GPS [P0]

**完整题名：**Steering Your Generalists: Improving Robotic Foundation Models via Value Guidance

**发表/版本：**CoRL 2024（论文集2025）；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**冻结通用策略，用学习的价值函数选择候选动作；验证跨多种策略架构。

**项目关系（研究分析）：**同一个value模块服务多种冻结策略已有；learner-agnostic与多head不能单独当创新。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v270/nakamoto25a.html

### P087 · RedFlow [P1]

**完整题名：**RedFlow: Redirect Failure into Action-Level Corrections for Flow-matching VLA Policy

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**把失败经验转化为动作级纠正监督，改善flow VLA。

**项目关系（研究分析）：**失败轨迹利用并非只有reward；需比较counterfactual/corrective目标与你的物理target。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.27782

### P088 · DSRL [P0]

**完整题名：**Steering Your Diffusion Policy with Latent Space Reinforcement Learning

**发表/版本：**CoRL 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**冻结扩散策略，在噪声latent空间学习引导策略。

**项目关系（研究分析）：**冻结生成策略+小latent learner已有；需要证明physical token比噪声/动作latent更有用。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v305/wagenmaker25a.html

### P089 · FlowDAgger [P0]

**完整题名：**FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**把人工纠正逆映射到生成噪声空间，训练小型latent策略适配冻结生成策略，包含VLA与WAM。

**项目关系（研究分析）：**冻结VLA/WAM + 轻量通用适配的直接竞品；必须精读能否共享learner、哪些参数冻结。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.08877

### P090 · Policy Decorator [P1]

**完整题名：**Policy Decorator: Model-Agnostic Online Refinement for Large Policy Model

**发表/版本：**ICLR 2025（作者项目页）；主表年份：2025。

**本轮证据：**作者项目与论文。

**方法（来源摘要）：**残差策略与受控探索改进冻结的大型模仿策略，覆盖Diffusion/Behavior Transformer。

**项目关系（研究分析）：**多模型小外挂、residual、稳定探索都已有；action correction改名不改变其残差定义。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://policydecorator.github.io/

**出版补充：**https://arxiv.org/abs/2412.13630

### P091 · IQL [P1]

**完整题名：**Offline Reinforcement Learning with Implicit Q-Learning

**发表/版本：**arXiv 2021；ICLR版本待逐页核验；主表年份：2021。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**expectile状态价值回归、数据内Q备份与优势加权行为克隆。

**项目关系（研究分析）：**可用于稳健价值学习对照；不是explicit regression，也不保证任意数据覆盖下成功。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2110.06169

### P092 · CQL [P1]

**完整题名：**Conservative Q-Learning for Offline Reinforcement Learning

**发表/版本：**NeurIPS 2020；主表年份：2020。

**本轮证据：**正式论文集。

**方法（来源摘要）：**抑制数据分布外动作价值过估计。

**项目关系（研究分析）：**物理critic也会在未覆盖动作上失真；必须与保守价值学习区分。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.neurips.cc/paper/2020/hash/0d2b2061826a5df3221116a5085a6052-Abstract.html

### P093 · Cal-QL [P1]

**完整题名：**Cal-QL: Calibrated Offline RL Pre-Training for Efficient Online Fine-Tuning

**发表/版本：**NeurIPS 2023；主表年份：2023。

**本轮证据：**正式论文集。

**方法（来源摘要）：**校准离线价值学习，使在线微调的尺度与初始化更合理。

**项目关系（研究分析）：**表征失效与Q校准错误是不同问题；应保留learner稳定性诊断。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.neurips.cc/paper_files/paper/2023/hash/c44a04289beaf0a7d968a94066a1d696-Abstract-Conference.html

### P094 · RLPD [P1]

**完整题名：**Efficient Online Reinforcement Learning with Offline Data

**发表/版本：**ICML 2023；主表年份：2023。

**本轮证据：**正式论文集。

**方法（来源摘要）：**用少量关键设计使off-policy RL有效使用离线数据。

**项目关系（研究分析）：**数据混合、更新比和critic设计可影响结果；不要把其工程改进误判为物理表示收益。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v202/ball23a.html

### P095 · DPPO [P1]

**完整题名：**Diffusion Policy Policy Optimization

**发表/版本：**ICLR 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**把多步扩散采样纳入策略优化结构，微调扩散策略。

**项目关系（研究分析）：**直接优化生成策略是一条不同backend；必须匹配交互和算力预算。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.iclr.cc/paper_files/paper/2025/hash/c0749c39aaff9e9e4c91f7118bf21b1e-Abstract-Conference.html

### P096 · FQL [P1]

**完整题名：**Flow Q-Learning

**发表/版本：**ICML 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**把flow行为先验与Q引导的一步策略提取结合。

**项目关系（研究分析）：**可作为离线/在线learner候选；不能与物理token同时换算法后归因给表示。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v267/park25f.html

### P097 · ConRFT [P1]

**完整题名：**ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**离线BC/Q学习后，以consistency policy及人工干预进行在线微调。

**项目关系（研究分析）：**接触任务稳定改进的候选；需区分完整VLA微调与小外挂的参数预算。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2502.05450

### P098 · HIL-SERL [P1]

**完整题名：**Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning

**发表/版本：**Science Robotics 2025；主表年份：2025。

**本轮证据：**作者项目与正式期刊记录。

**方法（来源摘要）：**人类介入、视觉RL和系统工程支持精密操作学习。

**项目关系（研究分析）：**真实接触学习强基线；要报告人类成本、reset、感知输入与交互预算。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://hil-serl.github.io/

**出版补充：**https://doi.org/10.1126/scirobotics.ads5033

### P099 · D2PPO [P1]

**完整题名：**D2PPO: Diffusion Policy Policy Optimization with Dispersive Loss

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**以dispersive表示正则缓解扩散策略RL中的特征坍缩。

**项目关系（研究分析）：**hidden-feature改进可能来自通用正则而非物理；应加同容量非物理辅助loss对照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2508.02644


## G｜执行时序、失败恢复与非参数自进化

### P100 · SmoothRL [P1]

**完整题名：**SmoothRL: Online Reinforcement Learning During Asynchronous Execution

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**区分承诺、实际执行与丢弃动作区段，对齐异步执行与RL学习。

**项目关系（研究分析）：**proposed/executed差异已有直接研究；需要报告真实执行区间，而不只chunk长度。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.29768

### P101 · VLA-Corrector [P1]

**完整题名：**VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**比较预测与实测变化，检测偏离并修正/截断陈旧动作。

**项目关系（研究分析）：**failure-onset及adaptive-horizon是强对照；不能凭增加监控头就称物理表示创新。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.01804

### P102 · BCP [P1]

**完整题名：**Continue or Replan? Bernoulli-Continuation Policy Learning for Adaptive Horizon Execution

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**学习继续执行或重规划的控制决策。

**项目关系（研究分析）：**二值continuation head已有；如果你的下游也是replan，应匹配此类基线。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.03483

### P103 · GeoAAC [P0]

**完整题名：**GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**从flow去噪轨迹几何估计前缀可靠性，自适应选执行horizon，无额外训练。

**项目关系（研究分析）：**动作生成过程特征可直接提供不确定性；对照能检验你是否只是重学去噪可靠性。

**核验边界：**2026-09-17新增预印本；本轮只核验摘要，需优先跟进全文与代码。

**一手来源：**https://arxiv.org/abs/2609.20776

### P104 · RL²-VLA [P1]

**完整题名：**RL²-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**通过latent RL steering与测试时计算改善VLA执行。

**项目关系（研究分析）：**latent steering与failure条件下介入已有；需证明physical监督带来新的可转移信息。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.26991

### P105 · FailSafe [P2]

**完整题名：**FailSafe: Reasoning and Recovery from Failures in Vision-Language-Action Models

**发表/版本：**IROS 2026（作者接收声明）；主表年份：2026。

**本轮证据：**arXiv摘要＋作者接收声明。

**方法（来源摘要）：**失败识别、解释和恢复服务VLA。

**项目关系（研究分析）：**错误恢复能力并不等同于物理机制识别；可作failure taxonomy参照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2510.01642

### P106 · Zeva [P0]

**完整题名：**Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**从动作和状态变化抽取交互信号，写入多时间尺度记忆以适配冻结策略。

**项目关系（研究分析）：**action-effect经验已有；memory中的描述不等于actor-side可迁移latent，且causal措辞需实验支撑。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.30880

### P107 · Harness VLA [P1]

**完整题名：**Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**通过Agent、解析primitive和记忆改善冻结VLA的局部调用。
**项目关系（研究分析）：**系统层恢复是不同贡献；operating-range相关probe可借鉴，但不直接验证你的token。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.08448

### P108 · SHAPER [P1]

**完整题名：**Self-Evolving Embodied Agents via Skill-Harness Evolution

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**冻结模型，利用执行反馈演化skill指导和context-code harness。

**项目关系（研究分析）：**系统提示/上下文变化能提高结果，必须与表示变化分开归因。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.11350

### P109 · ASPIRE [P1]

**完整题名：**ASPIRE: Agentic /Skills Discovery for Robotics

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**执行trace驱动控制程序诊断、修复和可复用技能积累。

**项目关系（研究分析）：**主要借鉴细粒度失败证据与验证流程，不把代码自进化误记为policy物理表征学习。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2607.00272

### P110 · ENPIRE [P1]

**完整题名：**ENPIRE: Agentic Robot Policy Self-Improvement in the Real World

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**将真机实验、验证和策略/算法改进组织为agentic闭环。

**项目关系（研究分析）：**实验自动化与算法表征是不同层；注意single-shot与多次重试指标。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2606.19980

### P111 · Zetta ζ [P1]

**完整题名：**Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**执行critic、恢复候选和validation-gated技能更新构成系统闭环。

**项目关系（研究分析）：**runtime critic不一定是RL Q；需区分监督、权限和更新对象。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.16590

### P112 · AGM [P2]

**完整题名：**AGM: Achievement-Grounded Memory for Closed-Loop Agents with Frozen VLA Policies

**发表/版本：**arXiv 2026；主表年份：2026。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**以实际完成结果组织记忆，改善冻结策略的闭环Agent。

**项目关系（研究分析）：**成功判定与记忆更新是系统层对照，不作为actor-side物理收益。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2608.29537

### P113 · ForeAct [P1]

**完整题名：**ForeAct: Steering Your VLA with Efficient Visual Foresight Planning

**发表/版本：**CVPR 2026；主表年份：2026。

**本轮证据：**正式论文集。

**方法（来源摘要）：**用未来图像与子任务描述引导VLA，接口可通过视觉输入对接。

**项目关系（研究分析）：**世界预测外挂可不读action head；是检验额外观测/规划解释的强对照。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_ForeAct_Steering_Your_VLA_with_Efficient_Visual_Foresight_Planning_CVPR_2026_paper.html

### P114 · SEAM [P2]

**完整题名：**Rethinking Intermediate Representation for VLM-based Robot Manipulation

**发表/版本：**CVPR 2026（作者机构声明）；主表年份：2026。

**本轮证据：**作者机构项目页／会议声明。

**方法（来源摘要）：**以操作词汇和语法构成可泛化的语义中间表示。

**项目关系（研究分析）：**不是低层动力学token；用于清楚区分semantic interface与physical interface。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://ri.cuhk.edu.hk/en/research/projects/rethinking-intermediate-representation-for-vlm-based-robot-manipulation


## H｜通用动作头、动作tokenizer与跨本体底座

### P115 · π0 [P1]

**完整题名：**π0: A Vision-Language-Action Flow Model for General Robot Control

**发表/版本：**RSS 2025（作者接收声明）；主表年份：2025。

**本轮证据：**arXiv摘要＋作者接收声明。

**方法（来源摘要）：**预训练视觉语言模型结合flow-matching动作专家生成连续动作块。

**项目关系（研究分析）：**第一种head family；抽取位置、采样时刻、噪声条件必须固定。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2410.24164

### P116 · π0.5 [P1]

**完整题名：**π0.5: a Vision-Language-Action Model with Open-World Generalization

**发表/版本：**arXiv 2025；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**联合多源数据和层级推理/动作学习，提升开放世界泛化。

**项目关系（研究分析）：**当前π0.5底座；不要把原任务语义适应与物理token增益混算。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2504.16054

### P117 · OpenVLA [P1]

**完整题名：**OpenVLA: An Open-Source Vision-Language-Action Model

**发表/版本：**arXiv 2024（本表未复核会议版）；主表年份：2024。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**开放的视觉语言动作模型，以离散动作token自回归生成控制。

**项目关系（研究分析）：**可作为AR动作头对照；teacher forcing隐藏态不得泄漏未来示范动作。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2406.09246

### P118 · FAST [P1]

**完整题名：**FAST: Efficient Action Tokenization for Vision-Language-Action Models

**发表/版本：**arXiv 2025（本表未复核会议版）；主表年份：2025。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**利用频域压缩构建高效的动作序列tokenizer。

**项目关系（研究分析）：**压缩动作序列≠物理状态表示；必须区分action token与你的Physical Token。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2501.09747

### P119 · Diffusion Policy [P1]

**完整题名：**Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

**发表/版本：**IJRR 2025；早期版本 RSS 2023；主表年份：2025。

**本轮证据：**出版社题录＋arXiv摘要。

**方法（来源摘要）：**条件迭代去噪生成动作块，采用滚动时域执行。

**项目关系（研究分析）：**连续生成头重要底座；采样步序号与物理时间不是同一个维度。

**核验边界：**期刊在线首发与正式卷期年份不同；RSS/期刊为同一工作谱系，不重复计两篇。

**一手来源：**https://journals.sagepub.com/doi/10.1177/02783649241273668

**出版补充：**https://arxiv.org/abs/2303.04137

### P120 · ACT [P1]

**完整题名：**Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

**发表/版本：**arXiv 2023（本表未复核会议版）；主表年份：2023。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**低成本双臂遥操作结合变分模型与Transformer动作分块。

**项目关系（研究分析）：**回归/块级动作基线；temporal ensembling与执行时域必须和token变量分开。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2304.13705

### P121 · Octo [P1]

**完整题名：**Octo: An Open-Source Generalist Robot Policy

**发表/版本：**arXiv 2024（本表未复核会议版）；主表年份：2024。

**本轮证据：**arXiv摘要。

**方法（来源摘要）：**可适配不同观测和动作空间的通用机器人策略。

**项目关系（研究分析）：**跨本体输入输出适配已有工作；统一接口不能单独证明泛化。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2405.12213

### P122 · OpenVLA-OFT [P1]

**完整题名：**Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success

**发表/版本：**RSS 2025（作者接收声明）；主表年份：2025。

**本轮证据：**arXiv摘要＋作者接收声明。

**方法（来源摘要）：**比较连续动作、并行解码、动作分块和微调配置。

**项目关系（研究分析）：**较便宜的连续回归头对照；不能把整套工程优化的收益算成token收益。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://arxiv.org/abs/2502.19645

### P123 · HPT [P0]

**完整题名：**Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers

**发表/版本：**NeurIPS 2024；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**异构机器人输入经过适配后形成共享Transformer表示。

**项目关系（研究分析）：**共享token、机器人专用适配器与跨本体学习已有人做；需证明动作后果目标的新增价值。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://papers.nips.cc/paper_files/paper/2024/hash/e0f393e7980a24fd12fa6f15adfa25fb-Abstract-Conference.html

### P124 · LAPA [P1]

**完整题名：**Latent Action Pretraining from Videos

**发表/版本：**ICLR 2025；主表年份：2025。

**本轮证据：**正式论文集。

**方法（来源摘要）：**从视频学习潜在动作，再迁移到真实控制动作。

**项目关系（研究分析）：**从变化中提取潜在动作的先例；与actor-side后果状态表示区分。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.iclr.cc/paper_files/paper/2025/hash/45d74e190008c7bff2845ffc8e3facd3-Abstract-Conference.html

### P125 · VQ-BeT [P1]

**完整题名：**Behavior Generation with Latent Actions

**发表/版本：**ICML 2024；主表年份：2024。

**本轮证据：**正式论文集。

**方法（来源摘要）：**利用离散潜动作与Transformer建模多模态行为。

**项目关系（研究分析）：**动作压缩潜变量与物理上下文潜变量不能仅靠名字区分。

**核验边界：**本轮为题录与摘要筛查，方法细节、消融和代码仍需逐篇精读。

**一手来源：**https://proceedings.mlr.press/v235/lee24y.html


# 灰色文献、版本纠错和待补查项

## Kinematic Forcing: Physics-Grounded Representation Alignment for Video-Action World Models

状态：TU Delft硕士论文

处理：题名与本项目高度相关；作为灰色文献查阅，不能标成顶会/期刊论文。

来源：https://repository.tudelft.nl/record/uuid%3A81a6ca75-de23-4cb3-899a-34651dc59b25

## Semantic-Geometric-Physical-Driven Robot Manipulation Skill Transfer via Skill Library and Tactile Representation

状态：IROS 2025题录线索；本轮未取得足够一手方法内容

处理：仅作补查线索，不计入125项主表，也不凭标题判断方法相同。

来源：https://doi.org/10.1109/IROS60139.2025.11246218

## DeCAL的CoRL 2026录用说法

状态：本轮仅核验arXiv

处理：撤回此前未核实的CoRL录用标签；保留论文，不用会议级别背书。

来源：https://arxiv.org/abs/2609.09119

## HPT / DINO-WM / Sparsh发表地点

状态：本輪已区分

处理：HPT为NeurIPS 2024；DINO-WM为ICML 2025；Sparsh为CoRL 2024（PMLR 2025）。


## 经典文献的正式会议版本

状态：部分主表仅按arXiv收录

处理：SPR、VIP、DeLaN、DPI-Net、IQL、ACT、Octo、FAST、OpenVLA等不凭记忆补录接受信息；写正式参考文献前继续核对官方版本。


## 代码公开性与可复现性

状态：本轮未逐仓安装

处理：论文链接不是可运行承诺。后续补充commit、许可证、权重、数据、依赖与硬件验收，不能凭项目页宣布已可复现。



# 下一轮检索如何减少漏检

以18项高重合论文为种子，分别追溯参考文献和查找后续引用；对每个新条目继续记录论文版本、发表证据、传感输入、特征读出位置、监督目标、冻结/更新范围、动作与物理时间语义、部署时特权信息、下游控制方式和跨域验证。对于只在标题上相近的工作保留线索，不推断机制；对于题名不同但实现相同的工作提高优先级。正式投稿前再按各会议/期刊当期目录补扫，不能把本工作稿当成永久完整库。
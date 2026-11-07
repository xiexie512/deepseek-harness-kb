# 外部设计 Skill 地图

> 同类 Agent Skill 已经有几十个。这一篇做三件事：把真正值得看的挑出来、标清"借什么 / 别借什么"、说明**我们已经吸收了哪些、剩下哪些建议直接装**。
>
> 原则：不 fork、不 vendor 别人的仓库（授权与维护成本都不划算），只吸收机制，其余用链接指路。

## 目录

1. [官方基线](#1-官方基线anthropic)
2. [审美方向类（抗 AI 味）](#2-审美方向类抗-ai-味)
3. [设计系统与 token 类](#3-设计系统与-token-类)
4. [评审与审计类](#4-评审与审计类)
5. [UX 深参考与角色类](#5-ux-深参考与角色类)
6. [工具与 MCP（取真值，不是取品味）](#6-工具与-mcp取真值不是取品味)
7. [怎么组合（按场景）](#7-怎么组合按场景)
8. [整合原则：为什么不 fork](#8-整合原则为什么不-fork)
9. [业界共识，以及我们不同意的三条](#9-业界共识以及我们不同意的三条)

---

## 1. 官方基线（Anthropic）

来源：`github.com/anthropics/skills`（Apache-2.0，仓库根有 LICENSE）。

| Skill | 做什么 | 我们的对应 | 什么时候直接装它 |
|---|---|---|---|
| **frontend-design** | 先定"目的/调性/约束/记忆点"，再写代码；给出 AI 默认审美的显式黑名单 | 见 [SKILL.md](SKILL.md) 的"三个问题"与反 AI 味清单 | 你要**从零做有品牌感的营销页**，且愿意接受它挑的字体与调性 |
| **web-artifacts-builder** | React 18 + TS + Tailwind + shadcn/ui 起手，最后用 Parcel 打成一个 HTML | 无（我们只做静态单文件示例） | 产物需要状态、路由、组件库 |
| **canvas-design** | 出 PNG / PDF 的视觉物料（信息图、海报、社交图） | [surfaces.md](surfaces.md) 第 6 节（海报构图与字号） | 要批量出静态图，且不想手搓 SVG |
| **algorithmic-art** | p5.js 生成艺术 | 无 | 做视觉实验，不是做产品界面 |
| **skill-creator** | 用评测与迭代把流程固化成 Skill | 本仓库自身就是按它写的 | 要把你自己的重复流程变成 Skill |

**它们的共同方法论**（值得抄，已被我们采纳）：

1. 先定方向再写代码——不定方向，模型就回归均值。
2. 显式列出"不要做什么"（负面清单比正面清单有效）。
3. "把大胆用在一个地方"（spend your boldness in one place，出自其设计原则，原话借自 Chanel 的"出门前照镜子，摘掉一件配饰"）。
4. 写完自己截图对照 brief 复核。

---

## 2. 审美方向类（抗 AI 味）

这一类的价值不是"更多规则"，而是**给模型一个可命名的方向**。模型的默认是"所有网站的平均值"，命名方向是唯一有效的解药。

| Skill | 机制 | 借什么 | 别借什么 |
|---|---|---|---|
| **Leonxlnx/taste-skill**（MIT） | 三个 1–10 旋钮：`DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`，默认 8 / 6 / 4 | **旋钮思路**已并入 [SKILL.md](SKILL.md) 步骤 1（我们把默认值按场景下调了，见第 9 节） | 默认 8 档方差对后台、文档是过冲 |
| **pbakaus/impeccable**（Apache-2.0） | 24 个命令（polish / bolder / quieter / critique / audit）+ 一套**不调模型**的确定性"slop 检测" | "检测必须确定性、可重复"这一点，已并入 [interaction.md](interaction.md) 的硬门与本文硬门表 | 它偏营销页语气，后台 UI 会觉得"戏太多" |
| **superdesigndev/superdesign-skill** | 变体探索：一次出多个方向再选 | "一次出 3 个变体再定方向"的工作法 | 它会持续产出变体，容易停在探索阶段 |
| **Ilm-Alan/frontend-design**（MIT） | 8 个美学锚点（Swiss / Industrial / Brutalist / Aurora / Chaotic / Retro-Futuristic / Organic / Lo-Fi），每个锁定 palette + type + texture 的具体 token | "锚点必须落到具体 token"这条纪律 | 8 个锚点都偏强风格，正文类页面用不上 |
| **claudekit frontend-design-pro** | 11 种风格，每种附**可直接读的 HTML/CSS** | 当教学素材读：能看清是哪几行 CSS 产生了这个效果 | 直接拿去做产品界面会过火 |
| **JimLiu/baoyu-design**（中文） | 本地跑"设计稿/原型/幻灯片"，输出自包含 HTML | 中文场景的 prompt 写法 | 它假设你用 Claude 系模型与英文术语 |
| **joeseesun/qiaomu-design**（中文） | 反 AI 味 + "风格试衣间" + 58 个真实站点设计系统 | "从真实站点取设计系统"的数据来源 | 站点风格库会诱导你抄皮肤而非结构 |
| **AnxForever/stylekit** | 149 种网页风格，每种配 prompt + token + 组件配方 | 需要"某个明确风格"时的检索入口 | 同上的抄皮肤风险 |
| **KAOPU-XiaoPu/web-design** | 先出规格（spec）再写代码 | "规格先行"的产出形态 | 规格粒度偏粗，仍需我们的数值表补齐 |

**判断标准**：一个审美类 Skill 好不好，看它**能不能说清"为什么不是另一个方向"**。只给形容词（"高级感""呼吸感"）的，一律不装。

---

## 3. 设计系统与 token 类

我们已有"从种子色生成整套 token"（`scripts/make_tokens.py`）。这一类补的是另外两个方向：**从品牌/站点抽取**，以及**把系统编译成 Agent 可读的约束**。

| 项目 | 机制 | 和我们什么关系 |
|---|---|---|
| **dominikmartn/hue** | 学一个品牌的视觉，产出一套设计系统 | 反向：我们是"给定种子色生成"，它是"从素材推断" |
| **arvindrk/extract-design-system** | 从任意公开站点抽 colors / type / spacing / radius / shadow，输出 JSON + CSS 变量 | 做"竞品对齐"时用；抽完请按 [foundations.md](foundations.md) 的刻度归一，否则会继承对方的不规则值 |
| **Railly/tinte** | 把设计系统编译成 Agent Plugin，直接产出 `SKILL.md` + `tokens.css` | 和本仓库的产物形态几乎一致，可作为交叉校验 |
| **jeremylongshore / modu-ai 的 design-system 类** | tokens + 组件规格 + 品牌演示 | 偏"品牌交付物"，不是"约束" |
| **Figma MCP（含 Code Connect）** | 读真实设计文件的组件、变量、布局；Code Connect 把 Figma 组件映射到你的代码组件 | 这是"取真值"，不是"取品味"，见第 6 节 |

**关键区别**：抽取类工具能拿到**数据**，拿不到**判断**。同一套色板，放在表格里是懂行的，放在落地页首屏是灾难。数据要过我们的刻度与对比度闸门。

---

## 4. 评审与审计类

这一类和我们的 `audit_design.py` 最重叠，也是**吸收最多**的一类。

| Skill | 机制 | 已并入我们的哪条 |
|---|---|---|
| **vercel-labs/agent-skills · web-design-guidelines**（MIT） | 100+ 条规则，覆盖 a11y、焦点、表单、动画（含 reduced-motion）、排版、图片、性能、导航、暗色、触控、i18n | [interaction.md](interaction.md) 第 9 节已覆盖大部分；补了"i18n 与暗色单独过一遍"的意识 |
| **tinh2/design-audit** | 分阶段审计：代码库勘察 → WCAG 2.2 逐条 → 性能 → 主题 → 响应式；要求"给文件行号"、"先验 2–3 条再定稿" | **按影响排序 + 给行号**已并入 [checklist.md](checklist.md) 与脚本输出；"先验证再报"是防误报的关键 |
| **dvy1987/design-review** | 硬门机制：无障碍（APCA）与**欺骗性设计**直接判 FAIL，不与分数平均；一次最多 8 条发现 | 伦理硬门 → [interaction.md](interaction.md) 第 11 节；"最多 8 条"→ 评审模板 |
| **mhassan0000/ui-review** | token 合规清单：禁裸 hex、禁任意 px、阴影用变量、圆角走刻度 | "一轴一值" → [foundations.md](foundations.md) 第 10 节 |
| **bitjaru/styleseed（含 ss-review）** | 79 条视觉规则 + `STYLESEED.md` 锁文件，防跨会话漂移 | "锁文件防漂移"→ 我们用 `tokens.css` + 本文维护约定代替 |
| **TrevorEdris 的 design-review** | 用 Playwright 真跑页面、截图、看 console | 我们没做（脚本是静态分析），见第 6 节 |
| **Impeccable 的 detect** | 61–62 条确定性规则，可在 CI / 浏览器插件里跑 | 同 `audit_design.py` 的定位，可互补 |

**共识**：评审必须"给位置 + 给具体改法"，禁止"看起来不错"。这是我们评审模板存在的理由。

---

## 5. UX 深参考与角色类

| Skill | 结构 | 值得学的地方 |
|---|---|---|
| **szilu/ux-designer-skill** | 297 行 `SKILL.md` + 24 个参考文件（约 1 万行），按需加载 | **渐进披露的教科书**：主文件只放决策树与清单，深内容在 references |
| **naksha-studio** | 30 个角色（PM / 设计师 / 前端 / QA）组成"虚拟设计团队" | 多角色分阶段产出；适合大项目，不适合一次改一屏 |
| **appllama-skills** | 从畅销 App 的模式反推原生移动端界面 | 移动端"模式库"思路，和 [surfaces.md](surfaces.md) 第 2 节互补 |
| **genjutsu** | 动效系统：先给"动效主张"再写代码 | 动效要有主张，不是加动画 |
| **power-design / frontend-slides** | 把"不像 AI 做的幻灯片"变成规则集 | 我们的 [surfaces.md](surfaces.md) 第 4 节（PPT）可对照 |

**借法**：学它们的**文件切分与加载策略**，不是学它们的观点。我们自己的切分（一篇一主题 + `SKILL.md` 只留流程）就是同一套逻辑。

---

## 6. 工具与 MCP（取真值，不是取品味）

Skill 给判断，MCP 给事实。两者不能互替。

| 工具 | 给什么事实 | 用在哪一步 |
|---|---|---|
| **Figma MCP（+ Code Connect）** | 真实组件、变量、布局；把 Figma 组件映射到你代码里的组件 | 设计 → 代码；没有 Code Connect 时产出的是一次性 markup，会立刻和组件库脱节 |
| **Chrome DevTools MCP / Lighthouse** | 性能、console、核心指标 | 交付前性能闸门 |
| **Playwright MCP** | 真跑页面、多视口截图、看交互与 a11y 树 | "截图自查"这一步的唯一可靠做法 |
| **awwwards 类 MCP** | 获奖站点的截图与设计 DNA | 找方向时的参考库，注意别抄皮肤 |

**注意**：MCP 的工具定义在会话开始就进上下文，装两三个常用的即可，不要装一打。

---

## 7. 怎么组合（按场景）

**一次只启用一套审美规则**，两套会互相拉扯（一个要"极简"，一个要"最大主义"）。

| 场景 | 建议组合 |
|---|---|
| 从零做品牌营销页 | 本仓库 `SKILL.md`（约束与验收） + `frontend-design`（定方向）。二选一做方向，另一个做闸门 |
| 后台 / 工具型界面 | **只用本仓库**。审美类 Skill 在信息密度场景普遍过冲；需要额外视角时用 `ui-review` 的 token 合规清单 |
| 已有站点"一看就是 AI 做的" | 先跑 `audit_design.py` 和 `impeccable detect`（确定性规则），再按本仓库反 AI 味清单逐条改 |
| 设计稿转代码 | Figma MCP + Code Connect + 本仓库 [components.md](components.md) 的尺寸规格 |
| 要出 PPT / 海报 | 本仓库 [surfaces.md](surfaces.md) 第 4、6 节；需要模板时看 `power-design` / `canvas-design` |
| 评审别人（或自己的）PR | 本仓库 [checklist.md](checklist.md) 的十组清单 + Playwright 截图；评审报告按 `SKILL.md` 模板 |

---

## 8. 整合原则：为什么不 fork

1. **授权要一条条看**：这一堆里 MIT、Apache-2.0、未声明都有；未声明授权的不能整包搬。
2. **规则会打架**：`taste-skill` 默认方差 8，我们的后台规范要求克制；两套同时生效，模型会摇摆。
3. **维护成本会转移给你**：上游一改，你的 fork 就旧了；链接指路则永远指向最新。
4. **定位不同**：它们是"给方向 + 给命令"，我们是"给数值 + 给可跑的审计"。**数值可以吸收，判断要自己长**。

所以我们只做两件事：把机制并入自己的文档（本文第 4 节那批），其余标注"什么时候该装它"。

---

## 9. 业界共识，以及我们不同意的三条

### 共识（已经写进本仓库）

- AI 的默认输出是**训练分布的均值**，不定方向就会趋同。
- 负面清单比正面清单有效（"不要紫→蓝渐变"比"要高级"可执行）。
- 大胆只能花在一个地方，其余全部收敛。
- 状态不齐、无障碍不过，不算做完了——它们是**硬门**，不与分数平均。
- 设计系统要从"参考文档"变成"强制约束"（token 化 + 可审计）。

### 我们不同意的三条

| 流行说法 | 我们的立场 | 理由 |
|---|---|---|
| "用 APCA 全面替代 WCAG 对比度" | **APCA 当设计工具，WCAG 当合规基线** | 合同、验收、无障碍审计仍以 WCAG 2.2 为准；APCA 更贴近视觉感知，但尚无同等合规地位。两者都跑，冲突时以 WCAG 兜底 |
| "禁用 Inter / Roboto / 系统字体" | **营销页禁，后台与中文正文不禁** | 中文场景下系统字体（PingFang / 思源）在小字号上更稳；后台的阅读效率优先于个性。禁字体是手段，不是目的 |
| "方差旋钮默认 8" | **后台 2–3、文档 3–4、营销页 6–8** | 高方差在信息密集界面等于噪音。把档位和场景绑定，比给一个全局默认更有用 |

**一句话总结**：外部方案解决"方向从哪来"，本仓库解决"方向怎么落地成数值、怎么验收"。两边都要，但不要同时听两个方向。

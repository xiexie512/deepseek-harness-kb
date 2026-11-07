# 设计质量系统（design-quality）

> 一套把「好看」和「好用」拆成可执行约束的规范：间距、字阶、色彩、阴影、组件状态、动效曲线、无障碍指标全部有具体数值，可以直接照着改，而不是靠感觉。
>
> 纯 Markdown，模型可直接抓取；同时可作为 Agent Skill 安装使用。

## 为什么会有这套东西

多数"不好看"不是审美问题，是系统缺失：间距随手写（13px、17px）、字号自成一套、颜色没有层级、状态没做完。这套规范合并了五个来源的硬指标，而不是拼观点：

| 来源 | 拿走的部分 |
|---|---|
| Apple Human Interface Guidelines | 六条设计原则，收成"目标感 → 简洁"的判断顺序 |
| Material Design 3 | 动效时长与缓动（强调 500ms / 进场 400ms / 退场 200ms / 标准 300ms） |
| Nielsen 十原则 | 可用性的检查项，逐条落到设计动作 |
| WCAG 2.2 AA | 对比度 4.5:1 / 3:1、触控 24×24（移动端 44×44）、焦点可见 |
| Refactoring UI | 约束刻度、先灰度后上色、三级文字色、行长 45–75 字符 |
| 2026 设计系统趋势 | 设计系统从"参考文档"变成"强制约束"（token 化） |

## 怎么读

按你现在的任务选路径，不要通读：

| 你要做的事 | 读哪些 |
|---|---|
| 改一个具体页面 / 说"不好看" | [SKILL.md](SKILL.md) 的步骤 0 → 2 → 3，再按问题查 [foundations.md](foundations.md) |
| 从零做站点或 App | [SKILL.md](SKILL.md) 全流程 → [patterns.md](patterns.md) → [components.md](components.md) |
| 做后台 / 仪表盘 | [surfaces.md](surfaces.md) 第 3 节 → [components.md](components.md) 表格与筛选 → [patterns.md](patterns.md) 列表页 |
| 做 PPT / 海报 / 报告 | [surfaces.md](surfaces.md) 第 4–6 节 → [foundations.md](foundations.md) 字阶 |
| 交付前最后一遍 | [checklist.md](checklist.md) |
| 想直接用 token | [tokens.css](tokens.css) 或 `scripts/make_tokens.py` |
| 想机器打分 | `scripts/audit_design.py` |
| 想抄现成的 | [examples/](examples/) 6 个成品页 + [reference.md](examples/reference.md) 参考清单 |
| 想装/选外部 Skill | [ecosystem.md](ecosystem.md)（30+ 个设计类 Skill 的机制对照 + 组合建议） |

## 文件清单

| 文件 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 主流程：模式判断 → 五步（诊断/约束/版式/上色/状态）→ 评分卡 |
| [foundations.md](foundations.md) | 间距刻度、字阶表、色彩系统、阴影、圆角、栅格、图标与图片 |
| [components.md](components.md) | 按钮/输入/表格/卡片/弹窗/导航/提示等 16 类组件的尺寸与状态规格 |
| [patterns.md](patterns.md) | 列表页、表单页、详情页、设置页、空状态、引导、搜索、登录 8 种页面模式 |
| [interaction.md](interaction.md) | 十原则→动作、9 种状态、反馈时限、动效表、表单、导航、WCAG 清单 |
| [surfaces.md](surfaces.md) | 网页 / App / 仪表盘 / PPT / 报告 / 海报 / 图表 七套配方 |
| [checklist.md](checklist.md) | 交付前逐条勾选（通用 + 分场景 + 一致性/伦理硬门） |
| [ecosystem.md](ecosystem.md) | 外部设计 Skill 地图：官方、审美、设计系统、评审、UX 参考、MCP 六类，标"借什么 / 别借什么" |
| [tokens.css](tokens.css) | 亮/暗双主题 token，可直接 `@import` |
| `scripts/make_tokens.py` | 按种子色生成整套 token，自带对比度自检 |
| `scripts/audit_design.py` | 审查 HTML/CSS，出 0–100 分与硬伤清单 |
| [examples/](examples/) | 6 个成品示例（落地页/后台/组件/表单/H5/图表），每个 100/100，可直接复制改 |

## 成品示例

规则读完了不知道长什么样，就先看这几页——都是完整可跑的单文件 HTML，各自 100/100：

| 示例 | 抄什么 |
|---|---|
| [landing.html](examples/landing.html) | 一屏一个主张、真实截图代替插画、功能只做 3 个 |
| [dashboard.html](examples/dashboard.html) | 对齐优先、KPI 层级、状态标签、数字右对齐 |
| [components.html](examples/components.html) | 按钮 3 档 × 5 语义、输入 4 态、骨架/空/错/成功 |
| [form.html](examples/form.html) | 字段级错误写"差什么"、表单级错误定位到第一个 |
| [mobile.html](examples/mobile.html) | 44×44 热区、安全区、底部主操作 + Tab |
| [charts.html](examples/charts.html) | 标题写结论、一条高亮其余转灰、直接标注代替图例 |

另外 [examples/reference.md](examples/reference.md) 列了 15 个成熟方案（Apple HIG / Material 3 / Ant / shadcn / Linear / Stripe …），每条标了"借什么、别借什么"。

生态层面看 [ecosystem.md](ecosystem.md)：30+ 个公开的设计类 Agent Skill（Anthropic 官方、taste-skill、impeccable、Vercel web-design-guidelines、UX Designer、各类审计与抽取工具），标注了哪些机制已并入本规范、哪些建议直接安装、哪些不要叠用。

## 两种用法

**1. 当规范文档读**（任何模型 / 任何终端）

```sh
curl -s https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main/design/checklist.md
curl -s https://cdn.jsdelivr.net/gh/xiexie512/deepseek-harness-kb@main/design/foundations.md   # 大陆网络回退
```

**2. 当 Skill 装**

```sh
git clone https://github.com/xiexie512/deepseek-harness-kb.git
ln -sfn "$PWD/deepseek-harness-kb/design" "$HOME/.agents/skills/design-quality"
```

装好后在对话里说"设计""排版""不好看帮我改""配色""审一下这套设计"即可触发。

## 命令

```sh
# 生成 token（含对比度自检）
python3 design/scripts/make_tokens.py --seed "#0f766e" --mode both --out tokens.css

# 审查页面 / 目录
python3 design/scripts/audit_design.py index.html
python3 design/scripts/audit_design.py ./dist --json
```

两个脚本只用标准库，Python 3.8+ 即可，无第三方依赖。

## 维护约定

- 一篇一主题，文件名用小写连字符，不建子目录（脚本除外）。
- 数值必须可执行：写"24px"而不是"适度留白"。
- 新增规则时同步 [checklist.md](checklist.md)，否则规则会被忘掉。
- 改动 token 刻度后，重跑 `scripts/make_tokens.py` 并 diff `tokens.css`。

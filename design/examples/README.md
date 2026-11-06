# 成品示例（examples/）

6 个可以直接打开、直接复制的成品页面。每个文件都过了 `audit_design.py` 的 **100/100**，但它们真正的作用是给你一个"照着改"的起点，而不是收藏。

| 文件 | 场景 | 主要演示的规则 |
|---|---|---|
| [landing.html](landing.html) | SaaS 落地页 | 一屏一个主张、真实截图代替插画、功能只做 3 个、数字带单位、CTA 收尾重复主按钮 |
| [dashboard.html](dashboard.html) | 后台仪表盘 | 对齐优先、KPI 数字层级、状态用标签、表格数字右对齐 + `tabular-nums`、筛选回显 |
| [components.html](components.html) | 组件陈列 | 按钮 3 档 × 5 语义、输入 4 态、开关/勾选、Tabs/面包屑/分页、骨架/空/错/成功、弹窗 |
| [form.html](form.html) | 登录与表单 | 字段级错误写"差什么"、表单级错误定位到第一个、左侧列结果而非装饰墙、SSO 备选 |
| [mobile.html](mobile.html) | 移动端 H5 | 44×44 热区、`env(safe-area-inset-*)`、底部主操作 + Tab、单屏一个主任务、列表两行截断 |
| [charts.html](charts.html) | 数据图表页 | 标题写结论、只高亮一条其余转灰、直接标注代替图例框、柱从 0 起、表格去多余列 |
| [reference.md](reference.md) | 参考清单 | 15 个成熟设计系统/产品，各自"借什么、别借什么" |

## 怎么用（三步）

1. **换 token**：每个文件顶部 `:root` 里只有一小撮变量，和 [../tokens.css](../tokens.css) 同名同值。把 `--brand-*` 换成你的品牌色即可；需要完整色阶时直接改成 `@import url("../tokens.css")`。
2. **换内容**：所有文案都是真实结构的占位（工单、支付、发票这类具体名词），替换时保持**长度量级**——标题别从 8 字换成 30 字，版式会塌。
3. **删段落**：不需要的 `section` 整段删掉，不要留空壳。落地页从 7 段砍到 4 段通常更好。

## 已知局限

- 示例只做视觉与状态，不含交互 JS：表单校验、弹窗开合、Tab 切换都是"画好的状态"，接逻辑时按 [../interaction.md](../interaction.md) 第 2 节的 9 种状态补齐。
- 图表是手写 SVG，用来演示"去图例、直接标注"的画法；真实项目换成 ECharts 时，把 `grid` 收到 8、`splitLine` 改虚线、分类色压到 5 以内（配置片段见 [../surfaces.md](../surfaces.md) 第 7 节）。
- 全部为静态 HTML + 内联 CSS，没有构建步骤，方便直接丢进任何项目里当起点。

## 自检

```sh
python3 ../scripts/audit_design.py .        # 6 个文件应全为 100/100 A
```

审计只覆盖约 40% 的问题，剩下的（层次、留白、灰度测试、键盘走查）按 [../checklist.md](../checklist.md) 人工过。

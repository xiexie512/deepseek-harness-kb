# 决策与偏好记录

> 来源：由 ask-before-start 技能在开工前问答后追加。只记录会复用的稳定偏好、硬约束与被否决的方案。

## 2026-11-09 17:59 · 开工前确认闸门（ask-before-start）

- 顺序固定为「查知识库 → 建缺口清单 → 决策门 → 回写」，不跳步
- 只在会改变范围/核心方案/交付形态/验收标准/数据来源时才提问；工具与文件名之类自行决定
- 提问一次性用 interaction_ask，1–4 个问题，2–4 个选项，选项写「用户怎么回答」并说明影响
- 两轮问答后仍不确定就按推荐假设开工，并在开场句说明假设
- 只把稳定偏好、硬约束、被否决方案写回 notes/decision-log.md，一次性细节不写
- 否决：开工前先做探索性实现去猜用户意图

## 2026-11-09 18:05 · 知识库写入通道

- github.com:443 在本机不通，raw.githubusercontent.com 与 api.github.com 可达
- 因此写入必须支持 gh api 兜底，不能只依赖 git push

## 2026-11-09 18:15 · 提问形式偏好

- 开工前的确认必须弹出可点击的选项卡片（interaction_ask），用户点按钮作答
- 每个选项需 option_id/label/description 三件套齐全，label 写「用户怎么回答」而非操作措辞
- 禁止在正文用 Markdown 列表列选项让用户回「选 A 还是 B」
- 只有必须由用户提供文件/链接时才用自由输入题

## 2026-11-09 18:16 · Skill 部署范围与提问严格度

- 部署：ask-before-start 同步到 ~/.dsh/skills/ask-before-start，供容器版 DSH 使用
- 严格度：宁可多问一次 —— 只要答案会改变范围/交付形态/验收标准，即便方向已给也要先弹卡片

## 2026-11-09 19:33 · 工作台终端与文件改用自带，并接入 Git

- 决策：右侧工作台的文件树与终端一律用 DSH 自带（ui-sidebar-files / ui-sidebar-terminal）
- 停用：better-sidebar、vscode-workbench、自写 side-workbench 三者全部 disabled（disabled 计数 13→15）
- 未做的事：不自写 side-workbench 的替代实现——它那 2200 行文件/终端逻辑是按 macOS 路径写的，改用自带面板而不是改造它
- Git 落地：新建 /root/work 并 git init（首个提交 7d124d2）；ui-git-graph 行显式 disabled: false，其 /git/* 节点路由已挂载（GET /git/repos 返回 405）
- 遗留：git 图谱 UI 需先把 /root/work 添加为工作区才会显示分支/提交图

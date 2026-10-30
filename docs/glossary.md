# 术语表

> 来源：docs/glossary.zh.md（MIT License）。DeepSeek Harness 领域词汇的规范术语速查。

## 能力

- **seam（能力接缝）**：一种包含三种角色的*可替换能力*——**Service Definition**（拥有自身 `ctx.<key>` 和词汇类型的 Cordis Service）、一个或多个 **Service Provider**、一个或多个注入该服务的 **Consumer**。范例：`dsh-shell`（Definition）+ `dsh-bash-local` / `dsh-bash-sandbox`（Providers）+ `dsh-tool-bash`（Consumer）。

## Agent 作用域

- **scope**：按 agent 划分的注册单位。贡献要么全局，要么带作用域（归属恰好一个 scope key）。只有两层、扁平结构：带作用域的注册不会向下继承给 subagent。
- **scope key**：scope 的不透明标识，按对象同一性比较；约定：活跃 agent 就是其自身 scope 的 key。
- **agent 上下文（`agent.ctx`）**：agent 的带作用域上下文；注册既具备 scope 可见性，生命周期也绑定该 scope。
- **shadowing**：最具体者胜出的名称解析——带作用域的工具/片段/变量仅在该 scope 内替换同名全局项。按 agent 定制 persona / 工具变体的机制。
- **restriction / scope-local 注册**：`tools.restrict` 为单个 scope 过滤全局工具集合；scope-local 注册在过滤后合并。被过滤掉的工具不出现在提示词中，也拒绝执行。
- **setup window**：创建者组装 agent 作用域环境的创建时隙（`CreateAgentOptions.setup`），此时 scope 和 agent 已存在但尚未发布。
- **lineage**：以数据形式携带的父子关系事实（`parentSession`、`delegationDepth`、`subagentDepth`），不影响可见性。

## 目标（Goals）

- **目标**：附着在现有会话上的持久完成目标，带 `active / paused / blocked / complete` 阶段和 Goal Round 上限；`blocked` 保留策略代码与说明。目标是状态，不是调度器。
- **Goal Round**：为当前目标接纳的一次续行周期，具体化为一个由目标触发的轮次。
- **目标激活**：续行消费方接纳下一个 Goal Round 的进程本地权限，`armed` / `disarmed`；不参与持久回放，恢复或 fork 后需经 `/goal` 或模型工具做人类授权的恢复变更。

## 人类命令

- **人类命令**：以 `/` 开头的指令，由面向人类的适配器通过 `ctx.commands` 解释执行，不会成为模型消息。
- **目标命令**：`/goal` 由 `dsh-command-goal` 提供，直接观察或更改当前目标。

## 循环层级

- **轮次（turn）**：会话中一次对已接纳输入的排空过程，模型及其工具停止工作或终止策略介入后结束。
- **步骤（step）**：一次模型请求 + 由响应引发的工具执行；一个轮次包含零个或多个步骤。
- **Round**：承载轮次的外层策略迭代（如 Goal Round、Ralph 尝试）；Round 计数器归策略所有。
- **交互段（exchange）**：连续的轮次，从首个步骤接纳真人输入的轮次起，到下一个这样的轮次为止；通知唤醒的轮次归入前面的交互段。

## Ralph

- **Ralph 循环**：一次面向不可变目标的前台全新 agent 工作流运行，由工作流和 subagent 原语组合而成的面向模型的工具策略。
- **Ralph Round**：Ralph 循环中的一个全新子会话；不接收父会话或此前子会话的对话种子，共享工作区 + 有界 Ralph 交接承载跨 Round 状态。
- **Ralph 交接（handoff）**：从一个仍需继续的 Ralph Round 传给下一个的规范化、有界结构化报告（状态、摘要、证据、后续步骤、阻塞说明）。

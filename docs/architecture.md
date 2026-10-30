# 架构

> 来源：docs/architecture.zh.md（MIT License）。改动 `packages/` 下任何内容前，官方要求先读此文。本文是核心概念的精选整理。

## 底层框架：Cordis

[Cordis](https://github.com/cordiverse/cordis) 是 dsh 底层的插件框架：插件向共享上下文贡献**服务**、**类型化事件**和**可逆的副作用**。产品的每一部分都是插件——模型适配器、工具注册表、会话日志、agent loop 本身——因此每个都可以从配置替换。

不存在需要打补丁的特权内核：扩展 dsh 的方式是把插件挂载到其他插件旁边，各项注册是副作用，会在插件卸载时撤销。

## Profile 与组合包（Bundle）

运行中的 `dsh` 是一棵插件树，由启动时**按序叠加的各层**组合而成。

- **profile**：存放在 Harness home 中的具名组装。列出自己叠放的组合包、存放树外插件、保存用户自己的 `cordis.patch.yml`。随发行版交付模板：`web`、`headless`、`sdk`、`sdk-minimal`、`acp`。
- **组合包（bundle）**：Cordis 配置项及其挂载代码的分发格式，插入的内容始终可被其上各层 patch。
- 两者都在 `package.json` 的 `dsh` 字段声明：`dsh.profile` 列出组合包，`dsh.bundle` 指向 patch 文件。

**分层基准（共享第一层）**：`dsh-base` 提供模型适配器、工具、持久化、沙箱与审批策略、设置、凭据、遥测。在此基础上：
- `dsh-web-app` 增加浏览器应用；
- `dsh-headless` 增加不带服务器的一次性运行器；
- `dsh-sdk-app` 增加 SDK JSON-RPC 服务器；
- `dsh-acp-app` 增加仅用于自动化的 ACP 服务器；
- `dsh-sdk-minimal` 是刻意例外：拥有完整显式 SDK 配置树，**不应用 `dsh-base`**。

**层优先级**：profile 中有序的组合包 → 其 `cordis.patch.yml` → home patch → 最后是 `--patch` overlay。patch 按 id 定位条目并替换其整个 config，或插入新条目；`preset` patch 在目标声明的 `config.plugins` 内应用。

**查看配置树**：

```sh
dsh --profile web --dump-config
```

## 应用启动

受支持的 Node 应用通过具名 profile 启动：`dsh --profile <name>` 或 `dsh <name>`。Python SDK 复用同一架构：运行时 wheel 把 `dsh` CLI 打包为 `deepseek-harness-sdk-runtime-<platform>-<arch>`，客户端默认以显式 Harness home 启动 `dsh --profile sdk`。

## 核心包

| 包 | 职责 | `ctx` 键 |
|---|---|---|
| `core/session` | 仅追加的 `SessionEvent` 日志和内存存储 | `ctx.sessions` |
| `core/system-prompt` | 提示词片段与工具 schema 的组装 | `ctx.systemPrompt` |
| `core/tools` | 作用域化的工具注册表和带把关的执行流水线 | `ctx.tools` |
| `core/agent` | `Agent` 接口、活跃 agent 注册表、`agent/*` 事件 | `ctx.agents` |
| `core/agent-loop` | 默认 agent loop 驱动器 | `ctx.agentLoop` |
| `core/scope` | 按 agent 划分作用域的注册原语 | 库（无 ctx 键） |
| `llm/llm` | 消息与流式词汇表、适配器 seam | `ctx.llm` |

## 事件（扩展点）

事件就是扩展点，选对事件域是大多数改动的第一个决定：

- **会话事件**：追加到日志并通过 `session/event` 广播的持久事实。需要 reload 后仍存在的事实用它。
- **Agent 事件（`agent/*`）**：携带活跃 `Agent`：inbox、步骤、状态、请求、验证、续跑。观察或拦截进行中的工作用它。
- **能力事件**：无需导入循环即可向 seam（`fs/*`、`tools/*`、`telemetry/*`）附加策略和适配器。

## 轮次流程（Turn Flow）

- **步骤（step）**：一次模型请求 + 它调用的工具。
- **轮次（turn）**：零个或多个步骤，领取首条输入时打开，不再欠工作时关闭。

简化流程：`turn/start` → 领取输入 → 组装提示词 + 工具 schema → `agent/pre-step` → `step/start` → `agent/request` → 流式请求（`llm/stream` / `agent/assistant-stream`）→ 工具调用（`tools/*`）→ `step/end` → … → `turn/end`。

关键点：
- `turn/*`、`step/*`、`system/message`、`user/message`、`assistant/message`、`assistant/attempt`、`tool/*` 是**持久会话事件**；其余是实时扩展点。
- `agent/pre-step`、`agent/request`、`llm/stream`、三个 `tools/*` 事件是 **waterfall** 事件，监听器必须调用 `next()` 才能委托下去；`agent/turn-stopping` 是 serial 事件。

## 会话日志

**模型可见即已记录**：每个模型请求都必须能从日志重建。新增模型可见输入需要会话事件。

- `deriveMessages()` 从日志投影出模型历史。
- 每个 `assistant/message` 嵌入其精确压缩的 stream；`assistant/attempt` 保留失败、重试、取消等 attempt，不加入模型历史。
- fork、恢复、transcript、遥测、持久化都从这些持久 settlement 派生。
- 文件格式：JSONL v0 用 `session.jsonl[.zstd]`；v1+ 用 `session.vN.jsonl[.zstd]`。

## 能力 Seam

**seam** 是一项可替换能力，包含三种角色：
1. **Service Definition**（声明接口，拥有自己的 `ctx.<key>` 的 Cordis Service）
2. **Service Provider**（实现它）
3. **Consumer**（使用它，通常是面向模型的工具）

一个包可以合并承担多个角色，但单一角色本身不是 seam；添加一项能力意味着把三者一并设计。

经典范例（shell）：`dsh-shell`（Definition）+ `dsh-bash-local` / `dsh-bash-sandbox`（Providers）+ `dsh-tool-bash`（Consumer）。

**seam 正是替换一个提供方就能改变整个产品的原因**：文件系统与进程提供方共享同一个执行世界，把指向远程沙箱，Bash、PTY、LSP 也一并搬了过去。

## 新行为的归属位置（速查表）

| 目标 | 机制 |
|---|---|
| 添加模型提供方 | 在 `ctx.llm` 上注册适配器 |
| 添加面向模型的能力 | 在 `ctx.tools` 上注册；schema 加入提示词组装 |
| 添加 shell 执行 | 注册 `ctx.shell` 后端 |
| 添加用户命令 | 在 `ctx.commands` 上注册（无需模型轮次即可分派） |
| 管理后台任务 | 在 `ctx.jobs` 上注册 |
| 添加文件系统访问或策略 | 注册 `ctx.fs` 提供方，或监听 `fs/*` 事件 |
| 限制所启动的进程 | 使用 `ctx.sandbox` 后端 |
| 拦截请求、工具或轮次 | 使用 `agent/*` 或 `tools/*` 事件 |
| 添加模型可见上下文 | 调用 `agent.inject()` |
| 生成会话标题 | 注册唯一的 `ctx.sessionTitle` 提供方 |
| 在新后端存储会话 | 实现 `SessionPersistence`（create/open/stat/list/export） |

扩展实操：官方 [extension-cookbook](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/cookbook/extension-cookbook.zh.md) 将功能映射到能力，并索引添加包、工具、LLM 适配器、设置页的分步指南。

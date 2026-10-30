# 插件机制与开发

> 来源：docs/cordis-primer.zh.md、docs/architecture.zh.md（MIT License）。

## Cordis 五个核心概念

1. **插件是实现 Service 的对象**：可以是带可选 `inject` 和 `apply(ctx)` 字段的函数，也可以是 `Service` 子类，生命周期由 Cordis 挂载到当前上下文。
2. **上下文是服务的容器**：一个服务占据稳定的 `ctx.<key>`（如 `ctx.tools`、`ctx.llm`、`ctx.sessions`）；其他插件通过 key 查找服务，而非导入具体实现。
3. **通过 `inject` 声明服务依赖**：插件声明所需服务后等待其就绪再启动；加载顺序用服务依赖表达，而非手动编排。
4. **类型化事件用于通信**：用 TypeScript 声明合并注册事件名，按 `emit` / `waterfall` / `parallel` / `serial` / `bail` 分发。
5. **注册是可逆的副作用**：提示词片段、工具 schema、适配器、提供方、监听器通过 `ctx.effect()` 或 `ctx.on()` 安装，reload 和 teardown 时按预期撤销。

## 事件分发模式

| 模式 | 是否 await | 顺序 | 返回值 |
|---|---|---|---|
| `emit` | 否 | 按注册顺序观察 | 无 |
| `waterfall` | 否 | 按注册顺序观察（包装） | 有 |
| `parallel` | 是 | 所有监听器并行 | 无 |
| `serial` | 是 | 按注册顺序 | 有 |
| `bail` | 否 | 按注册顺序，直到某监听器返回 bail 值 | 有 |

**Waterfall 语义**：`ctx.waterfall` 是环绕中间件。监听器接收 `(...args, next)`，调用 `next()` 执行下游；下游返回值通过 `next()` 返回当前包装层。不调用 `next()` 直接返回则短路。策略监听器在拥有决策权时可以不调用 `next()` 直接返回；仅做标注/观察的监听器必须委托。仅在必须早于普通注册运行时才用 `prepend: true`。

## 实践规则

- 将行为封装为插件：工具流水线事件属于 `ctx.tools`，模型流式输出属于 `ctx.llm`，实时 agent 协调属于 `ctx.agents`。
- 拦截和策略优先用事件；直接能力调用优先用服务方法。
- 每个注册都有对应 disposer：从 `ctx.effect()` 返回一个，或用 Cordis 辅助方法自动处理。teardown 有顺序要求时，把相关工作放进同一个 effect。

## 添加能力的三种常规路径

| 想做什么 | 怎么做 |
|---|---|
| 添加工具 | 在 `ctx.tools` 上注册工具；schema 自动加入提示词组装 |
| 添加 LLM 适配器 | 在 `ctx.llm` 上注册适配器 |
| 添加设置页 | 注册设置卡片（见官方 cookbook `adding-a-settings-card`） |

## 安装 / 分发插件

```sh
dsh plugin --profile web add <package-name>          # 从 registry 安装
dsh plugin --profile web add file:/path/to/plugin     # 从本地目录安装
dsh plugin --profile web remove <package-name>        # 卸载
```

- 插件安装后会记录到该 profile，重启生效。
- 给插件仓库添加 [`dsh-plugin`](https://github.com/topics/dsh-plugin) topic 便于被发现。
- 插件可以用 `dsh.bundle` 字段声明 `cordis.patch.yml` 形式的 patch 层，用 `dsh.client` 字段声明注入的客户端模块（如 `dsh-client-ui-model-selection`）。

## 官方学习资源

- [Cordis 入门](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/cordis-primer.zh.md)
- [Cordis 教程（7 步实操）](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/cordis-tutorial/index.zh.md)：first-plugin → lifecycle → services → events → config → composition/HMR → into-the-harness
- [扩展实操手册](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/cookbook/extension-cookbook.zh.md)

# 模型提供商配置

> 来源：docs/user/guide/providers.zh.md（MIT License）。模型变更在下一次请求时生效，不需要重启服务器。

## 配置 DeepSeek

打开 **设置 → 模型**，DeepSeek 卡片提供 API 密钥字段，输入并保存。密钥只写，存于 `$DSH_HOME/.credentials.yaml`。

## 第三方提供商

「添加模型提供商」→ 选择 dsh 自带提供商（列表显示 provider id）：

- `anthropic`、`openai`、`moonshotai`（Kimi）、`zai`（GLM）等
- 输入 API 密钥并保存；已安装目录会提供端点、协议和模型列表。

密钥留空时：使用已保存凭据 → 或尝试读取列出的环境变量。认证状态有三种提示：绿色（已检测到环境变量）、黄色（未检测到凭据变量）、未确认（读取失败）。

## 自定义模型 API（中转站 / 公司网关 / 自建）

把卡片切换到**自定义模型 API**，填写：

- **Provider ID**（小写，永久标识；重命名需新建并删除旧提供商）
- 基础 URL
- **API 协议**（必须选网关实际使用的）：`OpenAI Chat Completions`、`OpenAI Responses`、`Anthropic Messages`（在 `cordis.patch.yml` 中存为 `openai-completions` / `openai-responses` / `anthropic-messages`）
- 凭据和至少一个模型

**探测模型**：在模型目录选「获取可用模型」询问端点；探测只是便利手段，失败时手动添加模型 ID 效果一样。

## 图片输入

在模型「模型选项」勾选「图片」。Pi-ai 保存为 `input: [text, image]`；DeepSeek 适配器保存为 `inputModalities`。可设路由级回退 `defaultInput: [text, image]`。声明了端点并不提供的图片能力不会被拦下，改由提供商拒绝请求。

## 推理等级（Reasoning）

- 内置提供商模型从已安装目录继承等级；DeepSeek 模型提供 `off`、`low`、`high`、`max`。
- 自定义模型可声明 `reasoningEfforts` 档位，值是该档位在协议上以 `reasoning_effort` 发送的写法。
- 只有 `off` 可以留空（不传参）。「不明确关闭就会思考」的 OpenAI 兼容网关（如 DeepSeek V4）需要 `compat.thinkingFormat: deepseek`。
- DeepSeek 自身路由：`llm-deepseek.reasoningEffort` 设置选择器起始默认值（如 `max`）。

```yaml
- id: llm-deepseek
  config:
    reasoningEffort: max
```

## 请求兼容性（compat）

多数 OpenAI 兼容网关会拒绝 OpenAI 接受的某些东西，两个高频问题：

1. 推理模型的系统提示词以 `role: "developer"` 发出 → 网关拒绝 → 设 `compat.supportsDeveloperRole: false`
2. 输出上限写 `max_completion_tokens` → 只认 `max_tokens` 的服务端拒绝 → 设 `compat.maxTokensField: max_tokens`

```yaml
- id: llm-pi-ai
  config:
    providers:
      my-gateway:
        apiKeyEnv: GATEWAY_API_KEY
        api: openai-completions
        baseURL: https://gateway.example/v1
        compat:
          supportsDeveloperRole: false
          maxTokensField: max_tokens
        models:
          - id: my-model
```

路由的 `compat` 是模型默认值，模型自身逐字段胜出。写下的开关必须给值（冒号后留空会被拒绝）。

## 排错速查

| 错误 / 现象 | 处理 |
|---|---|
| `MISSING_CREDENTIAL` | 存储提供商密钥，或提供被引用的环境变量 |
| `UNKNOWN_MODEL` | 选择已配置的模型，或向自定义提供商添加缺失模型 |
| 获取可用模型 401 | 检查密钥（探测调用 `GET /models`） |
| 密钥地址都对但网关拒绝一切请求 | 设 `compat.supportsDeveloperRole: false` + `compat.maxTokensField: max_tokens` |
| 只有推理模型失败 | 设 `compat.supportsDeveloperRole: false`（developer 角色被拒） |
| `off` 无法让 DeepSeek 停止思考 | 设 `compat.thinkingFormat: deepseek` |
| 图片发送前被拒绝 | 模型未声明图片模态：自定义提供商加 `input: [text, image]` |
| 提供商拒绝带图请求 | 模型声明了端点不提供的图片能力，移除 `image` 并开新会话 |

## DeepSeek 账号模型

已登录 DeepSeek 账号的模型列表来自账号服务，用 `modelOverrides` 调整单个模型：

```yaml
- id: llm-deepseek-account
  config:
    modelOverrides:
      deepseek-flash:
        contextWindow: 524288
        maxTokens: 131072
```

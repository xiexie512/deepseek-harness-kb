# 配置体系

> 来源：docs/architecture.zh.md、docs/user/guide/providers.zh.md（MIT License）。

## Harness Home（`$DSH_HOME`）

- 默认位置：`~/.dsh`。
- 存放内容：`profiles/`（各 profile 目录）、`.credentials.yaml`（凭据，权限 600）、插件、会话、缓存等。
- **隔离**：需要隔离 profile、插件、凭据、设置与会话时，使用新的 home（例如显式 `DSH_HOME=/path/to/home`）。

## profiles 与 cordis.patch.yml

每个 profile 是一个目录（如 `$DSH_HOME/profiles/web/`），核心文件：

- `cordis.patch.yml`：用户的配置覆盖（模型页写入的就是它，也可直接编辑）。
- 已安装的插件（通过 `dsh plugin` 管理）。

**直接编辑 profile patch 示例**：

```yaml
# $DSH_HOME/profiles/web/cordis.patch.yml
- id: llm-pi-ai
  config:
    providers:
      my-gateway:
        apiKeyEnv: GATEWAY_API_KEY
        api: openai-completions
        baseURL: https://gateway.example/v1
        models:
          - id: my-model
```

> 注意：Cordis 配置覆盖会**替换完整条目配置**；编辑已有覆盖项时，请保留其他 provider 和字段。

## Patch 分层顺序

```
profile 中有序的组合包
  → profile 的 cordis.patch.yml
  → home patch
  → --patch overlay（命令行传入，可重复）
```

patch 按 id 定位条目并替换其整个 config，或插入新条目。

## 配置目录（config-catalog）

官方自动生成的[配置目录](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/config-catalog.zh.md)（`config-catalog.zh.md`）列出每个插件的所有受支持字段与默认值，派生自源码，不会落后于适配器实际接受的内容。

## 凭据

- 模型页保存的密钥是**只写**的：页面只收到脱敏描述符，永远收不到明文密钥。
- 密钥存储在 `$DSH_HOME/.credentials.yaml`，settings 只保留凭据引用。
- 密钥留空时使用已保存凭据，或回退读取环境变量（如 `DEEPSEEK_API_KEY`）。

## 常用环境变量

| 变量 | 用途 |
|---|---|
| `DSH_HOME` | Harness home 路径（默认 `~/.dsh`） |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `DEEPSEEK_BASE_URL` | DeepSeek 兼容 endpoint（使用代理时设置） |
| `DSH_SYSTEM_PROMPT` | sdk-minimal 等 profile 的系统提示词覆盖 |
| `DSH_MODEL` | minimal 示例的模型覆盖 |

## 调试工具

```sh
dsh --profile web --dump-config          # 打印组合后的配置树
dsh --profile web --dump-default-config  # 打印不含用户层的配置树
dsh --profile web --dump-config-schema   # 打印 JSON Schema
```

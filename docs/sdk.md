# Python SDK

> 来源：docs/user/guide/python-sdk.zh.md（MIT License）。

## 前置条件

- Python 3.10+
- Git
- Linux x64 / Linux arm64 / macOS 14+ (arm64) / Windows x64
- DeepSeek 兼容的 API endpoint 与凭据
- 隔离的 workspace 与隔离的 Harness home

## 安装

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
python -m venv .venv
. .venv/bin/activate
python -m pip install deepseek-harness-sdk
```

安装内容包含匹配的原生运行时 wheel 与 `dsh` 命令——**普通 SDK 运行不需要系统 Node.js**。

## 运行示例

```sh
export DEEPSEEK_API_KEY=sk-your-key-here
# export DEEPSEEK_BASE_URL=http://127.0.0.1:8000/v1   # 使用兼容代理时

python python/sdk/examples/minimal.py \
  --workspace /absolute/path/to/disposable-workspace \
  --dsh-home /absolute/path/to/example-dsh-home \
  --session-id example-001 \
  "Inspect the repository and fix the failing tests."
```

脚本打印最终 assistant 响应；所选 home 会保存生成的 `sdk-minimal` profile、已安装插件和 `sessions/` 下的未压缩 JSONL 会话日志。**示例与 SDK 绝不会静默读取 `~/.dsh`。**

## 在程序中使用

```python
from pathlib import Path

from deepseek_harness import DeepSeekHarness

workspace = Path("/absolute/path/to/disposable-workspace").resolve()
dsh_home = Path("/absolute/path/to/example-dsh-home").resolve()
with DeepSeekHarness(
    provider="deepseek-official",
    model="deepseek-v4-flash",
    max_tokens=49_152,
    cwd=str(workspace),
    dsh_home=str(dsh_home),
    profile="sdk-minimal",
) as harness:
    result = harness.run(
        "Inspect the repository and fix the failing tests.",
        session_id="example-001",
    )

print(result.final_response)
```

SDK 延迟启动内置的 `dsh --profile sdk-minimal` 进程，并复用到上下文管理器退出。

## 安装 / 定义插件

```sh
export DSH_HOME=/absolute/path/to/example-dsh-home
dsh --profile sdk-minimal --dump-default-config >/dev/null   # 初始化 profile
dsh plugin --profile sdk-minimal add file:/path/to/my-plugin-bundle
```

持久配置项变更编辑 `$DSH_HOME/profiles/sdk-minimal/cordis.patch.yml`；单次启动变更从 Python 传 `patches=(...)`。

### 显式启用 `str_replace_editor`

随附运行时包含该工具但 `sdk-minimal` 默认不挂载。保存 `editor.patch.yml`：

```yaml
- insert:
    - id: tool-str-replace-editor
      name: '@deepseek-ai/dsh-tool-str-replace-editor'
```

构造时传 `patches=("/path/to/editor.patch.yml",)`，或写入 `cordis.patch.yml` 持久保存。

## sdk-minimal profile 速查

| 属性 | 值 |
|---|---|
| 系统提示词 | `DSH_SYSTEM_PROMPT`，未设置时 `You are a helpful software engineer assistant.` |
| 默认模型 | `--model` → `DSH_MODEL` → `deepseek-v4-flash` |
| 面向模型的工具 | 持久 `bash`（Windows 为 `pwsh`）、`read_image`、`working_directory` |
| Shell 超时 | 300 秒 |
| 上下文压缩 | 自动执行（额外请求生成较早历史摘要） |
| 会话持久化 | `<dsh_home>/sessions` 下未压缩 JSONL |
| 权限 | 固定 `danger-full-access`，应使用一次性 checkout 或容器 |

注意：`sdk-minimal` 不包含 `dsh-base`，因此基础 profile 以后新增的工具不会隐式出现；它没有 settings、托管凭据、OTel、Web 工具、subagent 等。默认随 DeepSeek 请求上传未接受的日志事件（`session-log-deepseek`，每次请求最多 8 MiB），可在 profile patch 中 `session-log-deepseek.enabled: false` 关闭。

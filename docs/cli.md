# dsh 命令行参考

> 来源：docs/cli-help.zh.md（官方自动生成，MIT License）。同份帮助只展示一次，列出所有调用方式。

## 主命令

```
dsh [--profile] <name> [options] [app-args...]
dsh plugin --profile <name> <pnpm-args...>
```

**选项**

| 选项 | 说明 |
|---|---|
| `-V, --version` | 输出版本号 |
| `--profile <name>` | 启动 `$DSH_HOME/profiles` 下的 profile |
| `--from-default-profile <name>` | 用随附 profile 模板重建一个自定义 profile |
| `--patch <path>` | 在 profile 层之后追加的 patch 覆盖（可重复） |
| `--dump-config` | 打印组合后的配置树并退出 |
| `--dump-config-schema` | 打印 profile 条目与 patch 的 JSON Schema（不挂载） |
| `--dump-default-config` | 打印不含用户层与 `--patch` 覆盖的配置树 |

**示例**

```sh
dsh web                                   # 启动 web profile（同 dsh --profile web）
dsh rescue --from-default-profile web     # 用 web 模板重建 rescue profile 再启动
dsh headless "run the tests"              # 回答一个任务、打印结果、退出
dsh tui --patch ./extra.yml               # 自定义 profile + 一个额外 overlay
dsh web --help                            # web app 自己的参数与帮助
dsh plugin --profile tui add <package>    # 向 tui profile 安装插件
```

## 随附 profile

| Profile | 作用 |
|---|---|
| `web` | 浏览器 UI（默认 `http://127.0.0.1:3080`） |
| `headless` | 一次性任务运行器：回答一个任务后退出 |
| `sdk` | 通过 stdio JSON-RPC 服务 SDK 客户端 |
| `sdk-minimal` | SDK 客户端（刻意极简，不加载 `dsh-base`） |
| `acp` | 通过 Agent Client Protocol stdio 服务自动化客户端 |
| `plugin` | 管理命令（同名 profile 需用 `--profile plugin` 选择） |

## 各 profile 详情

### `dsh headless`

```
dsh --profile headless [options] [task...]
```

- `task`：任务文本，多词自动以空格连接；`-` 表示从 stdin 读取。
- `--json`：向 stdout 输出换行分隔的运行事件（而非最终消息）。
- `--session-id <id>`：沿用持久化的 Session；未知 id 报错。

```sh
dsh --profile headless "run the tests"                # 答完即退
echo "run the tests" | dsh --profile headless         # 从 stdin 读任务
dsh --profile headless --json "run the tests"         # 机器可读事件
dsh --profile headless --session-id session-… "continue"   # 恢复已有会话
```

### `dsh web`

```
dsh --profile web [options]
```

- `--host <host>`：绑定地址（必须是本机某个具体 IPv4/IPv6 地址，拒绝通配符）
- `--no-open`：不自动打开浏览器
- `--port <port>`：监听端口；`0` 表示让系统分配
- `--public-url <url>`：声明 HTTP(S) 根地址（不授予信任）
- `--trusted-host <authority...>`：额外的 browser-trust 受信 host（可重复）
- `--tls-cert <file>` / `--tls-key <file>`：启用 HTTPS（两个必须同时提供）

```sh
dsh --profile web                          # 组合配置的 host 与 port
dsh --profile web --port 8080              # 换端口
dsh --profile web --host 10.0.0.7          # 绑定指定网卡
dsh --profile web --no-open                # 不开浏览器
```

### `dsh sdk` / `dsh sdk-minimal`

```
dsh --profile sdk [options]                # 服务 SDK 客户端直至断开
dsh --profile sdk-minimal [options]        # 极简 SDK 运行时
```

### `dsh acp`

```
dsh --profile acp [options]                # 服务 ACP 客户端直至断开
```

### `dsh plugin`

```
dsh plugin [--profile <name>] <pnpm-args...>
```

把剩余参数原样转发给 profile 目录下的 pnpm：`add <pkg>`、`remove <pkg>`、`why <pkg>` 等。首次使用会初始化该 profile。

## 查看配置树

```sh
dsh --profile web --dump-config
```

打印出的任何条目都可以被你自己的 patch 替换。

# 快速开始

> 来源：deepseek-ai/deepseek-harness 根 README 与 docs/user/guide（MIT License）。

## 通过 npm 运行

安装 Node.js 后：

```sh
npx @deepseek-ai/dsh web
```

- 默认在 `http://127.0.0.1:3080` 启动 Web UI，本机启动时会用默认浏览器打开页面。
- 通过 SSH 启动时只打印宿主机 URL。
- 传 `--no-open` 只运行服务器不打开浏览器。

## 从源码运行

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

`pnpm run build` 会准备仓库产物；`pnpm dsh web` 直接使用已构建产物，不会重新构建。

## Web UI 使用流程

1. **启动**：`dsh web`（或桌面应用），等服务器运行，命令会打印访问地址。
2. **配置模型**：打开 **设置 → 模型**，输入 [DeepSeek API 密钥](https://platform.deepseek.com/) 并保存。模型路由立即生效，不需要重启服务器。其他提供商与自定义 OpenAI 兼容端点见 [models.md](models.md)。
3. **选择工作区**：点击「选择工作区」，添加启动 `dsh` 时所在的项目目录并选中。选中前会话输入框不可用。
4. **运行任务**：启动会话并发送指令。Agent 可以读写工作区文件、运行命令、委派工作、维护计划；需要审批的操作 Web UI 会先询问。

> 注意：`dsh` 进程会把启动时所在的目录作为默认文件系统位置。

## 安装插件

```sh
# 全局安装 dsh 启动器与 pnpm（已装可跳过）
npm install -g @deepseek-ai/dsh pnpm

# 向指定 profile 安装插件（web 模式用 --profile web）
dsh plugin --profile web add <package-name>
```

装完需要重启 `dsh web` 或桌面应用才生效（运行中的进程持有内存里的旧插件）。

## 常见版本信息

- 当前版本查看：`dsh --version`
- 桌面应用（Electron）与 npm CLI 共享产品数据，但包、启用选择与锁文件相互独立。
- 知识库编写时本机环境：dsh `0.2.1-rc.3`（见 [notes/setup](../notes/setup.md)）。

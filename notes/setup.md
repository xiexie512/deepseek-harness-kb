# 本机环境速查（macOS）

> 更新时间：2026-10-30。dsh 处于开发者预览阶段，版本迭代快，此页需随环境变化更新。

## 版本

| 组件 | 版本 | 说明 |
|---|---|---|
| `dsh`（CLI） | 0.2.1-rc.3 | `dsh --version` |
| DeepSeek Harness 桌面应用 | 0.2.1-rc.3 | `/Applications/DeepSeek Harness.app` |

## 目录布局

| 路径 | 内容 |
|---|---|
| `~/.dsh` | Harness home（默认 `$DSH_HOME`） |
| `~/.dsh/profiles/` | 已初始化的 profile：`desktop`、`headless`、`qqbot`、`web` |
| `~/.dsh/.credentials.yaml` | 凭据（只写，权限 600） |
| `~/.dsh/dsh-pet/` | dsh-pet 插件运行时数据 |
| `~/.dsh/electron/` | dsh-pet 桌面模式下载的 Electron |
| `~/deepseek-harness/` | 官方仓库源码克隆（含完整 docs） |
| `~/Documents/deepseek-harness/` | dsh 默认工作区（default-workspace） |
| `~/Desktop/DeepSeek/` | 个人项目集（dsh-pet / dsh-phone / qqbot / douyin-bot / workspace-sync / zhipu-label） |

## 安装方式（本机）

- 桌面应用（Electron）安装，自带签名 dsh 生产运行时（`$DSH_HOME/profiles/desktop`）。
- 全局 npm CLI：`npm install -g @deepseek-ai/dsh pnpm`。
- 源码克隆：`~/deepseek-harness`（`pnpm install` / `pnpm run build` / `pnpm dsh web`）。

## 常用命令

```sh
dsh --version                         # 版本
dsh --profile web --dump-config       # 查看组合配置树
dsh plugin --profile web add <pkg>    # 安装插件（装完重启生效）
dsh web                               # 启动 Web UI（默认 127.0.0.1:3080）
```

## 备份习惯

`~/.dsh` 下保留 `backup-plugins-YYYYMMDD-HHMMSS`、`backup-zhipu-label-*`、`backup-pet-*` 等目录——**安装/升级/卸载插件前先备份对应目录**（沿用此习惯）。

## 已知的个人项目依赖关系

- `dsh-pet` 桌面模式依赖 `~/.dsh/electron`（版本 v43.x，npmmirror 镜像下载）。
- `qqbot` 容器挂载 `~/Desktop/DeepSeek` → `/DeepSeek`（实时双向）。
- `douyin-bot` 复用系统 Chrome profile（`chrome-profile/`），登录态持久化。

# dsh-phone：手机远程访问 dsh

> 作者项目（本机：`~/Desktop/DeepSeek/dsh-phone.sh`），一键管理脚本。

## 原理

启动 DeepSeek Harness 自带的 **web profile**（浏览器 UI），绑定到指定网卡，手机通过 **Tailscale / 局域网**访问。首次访问用 URL 里的 token 换取 **30 天有效期的签名 Cookie**，之后直接使用。

## 用法

```sh
./dsh-phone.sh start [ip]        # 启动并打印手机访问 URL（ip 缺省自动选择）
./dsh-phone.sh stop              # 停止服务
./dsh-phone.sh status            # 查看运行状态与访问地址
./dsh-phone.sh url               # 重新打印当前访问 URL（含 token）
./dsh-phone.sh start --lan       # 强制绑定局域网 IP（仅同 Wi-Fi 可访问）
./dsh-phone.sh autostart         # 安装开机自启（登录后自动启动，launchd）
./dsh-phone.sh no-autostart      # 移除开机自启
```

**地址自动选择顺序**：Tailscale IP > 局域网 IP（`--lan` 强制局域网）。

## 实现要点

- 复用桌面应用自带运行时：`/Applications/DeepSeek Harness.app` 内捆绑的 `node` 与 `dsh` 二进制，无需额外安装 Node。
- 端口默认 `3080`（可用环境变量 `DSH_PHONE_PORT` 覆盖）。
- 日志 `~/Desktop/DeepSeek/dsh-phone.log`，PID 文件 `.dsh-phone.pid`。
- 开机自启：`~/Library/LaunchAgents/com.deepseek-harness.phone.plist`。

## 适用场景

- 手机 / 平板通过 Tailscale 组网远程使用 dsh Web UI。
- 不暴露公网端口（走 Tailscale 或局域网），降低暴露面。

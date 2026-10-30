# qqbot：AstrBot + NapCat QQ 机器人

> 作者项目（本机：`~/Desktop/DeepSeek/qqbot`），Docker Compose 组合部署，源自 NapCat 官方 compose 并适配 **Mac arm64**。

## 架构

```
NapCat（QQ 协议端，端口 6099）
  └─ MODE=astrbot 模式，与 AstrBot 联动
AstrBot（机器人框架，端口 6185，管理面板 http://127.0.0.1:6185）
  ├─ ./data            → /AstrBot/data        （AstrBot 数据）
  ├─ ./napcat/config   → /app/napcat/config   （NapCat 配置）
  ├─ ./ntqq            → /app/.config/QQ      （QQ 登录态）
  └─ ../（宿主机 ~/Desktop/DeepSeek）→ /DeepSeek（双向实时挂载）
```

- 镜像走 `m.daocloud.io` 加速源：`mlikiowa/napcat-docker:latest`、`soulter/astrbot:latest`
- 网络：bridge `astrbot_network`；NapCat 固定 MAC `02:42:ac:11:00:02`。

## 启动

```sh
cd ~/Desktop/DeepSeek/qqbot
docker compose up -d
```

## 管理脚本

```sh
./manage.sh start|stop|restart|status|logs|astrbot|napcat|url|换码
```

- `status`：查看两个容器状态
- `url`：打印 AstrBot 面板地址与 NapCat WebUI token（脱敏：口令不写入知识库）
- `换码`：重启 NapCat 等待二维码生成，拷贝 `qrcode.png` 到本地并用系统看图打开——QQ 登录换码流程
- `douyin` 子命令：管理刷抖音服务（见 [douyin-bot.md](douyin-bot.md)）

## 关键点

- 宿主机 `~/Desktop/DeepSeek` 整个文件夹挂载进容器 `/DeepSeek`——**挂载即同步**，任一边改动另一边实时可见，无需复制。
- QQ 登录态持久化在 `./ntqq`；需要重新登录时用「换码」刷新二维码。
- 定时任务 / 触发式能力由 AstrBot 插件实现，回答完调用同步确认服务（见 [workspace-sync.md](workspace-sync.md)）。

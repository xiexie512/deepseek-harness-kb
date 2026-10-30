# workspace-sync：挂载健康确认服务

> 作者项目（本机：`~/Desktop/DeepSeek/workspace-sync/sync_service.py`），FastAPI 服务。

## 背景

宿主机 `~/Desktop/DeepSeek` 已挂载进 astrbot 容器 `/DeepSeek`（**双向实时互通，挂载即同步**，无需 rsync）。本服务提供 `/sync` 做「挂载健康确认 + 触发时间记录」，供 AstrBot 插件在每次回答完后调用。

## 接口

| 接口 | 说明 |
|---|---|
| `GET /sync` | 确认挂载健康并记录触发时间（幂等） |
| `GET /status` | 查看状态 |

## 实现要点

- 健康检查：确认宿主机目录存在且**可写**（创建临时探针文件再删除）。
- 每 12 小时兜底巡检一次挂载健康（`SYNC_INTERVAL = 12 * 3600`）。
- 状态字段：`last_trigger`（最近一次回答后触发时间）、`healthy`、`last_check`、`last_msg`。

## 运行

```sh
<douyin venv>/bin/python sync_service.py
```

## 设计思路

挂载本身是 Docker bind mount，天然实时同步；本服务不做数据复制，只做「健康确认 + 时间戳」两类事实的轻量服务，供上层（AstrBot 插件）在回答后打点，用于排查「改了一边没生效」类问题。

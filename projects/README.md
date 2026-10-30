# 个人项目索引

本目录收录作者（xiexie512）基于 DeepSeek Harness 构建的个人项目文档。所有项目源码位于本机 `~/Desktop/DeepSeek/`。

| 项目 | 一句话说明 | 文档 |
|---|---|---|
| dsh-pet | 住在 DeepSeek Harness 里的桌面宠物（npm 发布、开源） | [dsh-pet.md](dsh-pet.md) |
| dsh-phone | 手机远程访问 dsh Web UI 的一键管理脚本 | [dsh-phone.md](dsh-phone.md) |
| qqbot | AstrBot + NapCat 的 QQ 机器人 Docker 部署 | [qqbot.md](qqbot.md) |
| douyin-bot | Playwright 自动刷抖音 + DeepSeek 决策 + QQ 播报 | [douyin-bot.md](douyin-bot.md) |
| workspace-sync | 容器与宿主机挂载健康确认服务 | [workspace-sync.md](workspace-sync.md) |
| dsh-zhipu-model-label | 智谱模型【免费/付费】标签 DSH 客户端插件 | [zhipu-model-label.md](zhipu-model-label.md) |

## 目录位置

```
~/Desktop/DeepSeek/
├── dsh-pet/                # 桌宠项目（含发布版插件子目录）
├── dsh-phone.sh            # 手机远程访问脚本
├── qqbot/                  # QQ 机器人部署
├── douyin-bot/             # 抖音自动刷服务 + AstrBot 桥
├── workspace-sync/         # 同步确认服务
├── dsh-zhipu-model-label/  # 智谱标签插件
└── dsh-phone.log / .dsh-phone.pid 等运行态文件
```

## 安全说明

> 本项目文档已做脱敏：**任何密钥、口令均不进入本知识库**。项目源码中若仍存在明文凭据（例如旧版脚本中的 API Key），建议迁移到环境变量或 `.credentials.yaml`，并轮换已暴露的密钥。

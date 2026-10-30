# douyin-bot：自动刷抖音 + DeepSeek 决策 + QQ 播报

> 作者项目（本机：`~/Desktop/DeepSeek/douyin-bot`），FastAPI 服务（端口 8787）。

## 架构

```
Playwright（复用系统 Chrome，有头模式，独立 profile 持久化登录态）
  → 每刷一条视频：提取 标题/作者/点赞/评论 纯文本
  → 调 DeepSeek（纯文本 JSON 判断）
  → 动作：点赞 / 评论 / 划走 / 停止
  → 播报文本进 pending 队列
  → AstrBot 插件（astrbot_plugin_douyin_bridge）轮询转发到 QQ
```

## HTTP 接口

| 接口 | 说明 |
|---|---|
| `POST /start?keyword=xxx` | 启动自动刷（可选搜索词） |
| `POST /stop` | 停止 |
| `POST /say?text=xxx` | 手动让机器人评论当前视频 |
| `POST /click_like` | 手动点赞 |
| `GET /status` | 状态 |
| `GET /pending` | 取走待播报（消费式） |

## 实现要点

- `launch_persistent_context` 复用系统 Chrome 与独立 profile（`chrome-profile/`），登录态持久化。
- 深色水印风控规避：下滑间隔随机抖动（6–12 秒），按条数节流点赞/评论（`REPORT_EVERY=5` 等参数可调）。
- 模型：DeepSeek `deepseek-flash`，纯文本 JSON 返回决策。
- 管理入口：`qqbot/manage.sh douyin start|stop|restart|logs`。

## 安全提示（重要）

> 早期版本源码中曾以**明文**写入 DeepSeek API Key。知识库一律脱敏，请将凭据迁移到环境变量（如 `DEEPSEEK_API_KEY`），并**轮换已暴露的密钥**——尤其本目录如果纳入 git 管理，务必确认 `chrome-profile/`、`.env`、日志不包含密钥。

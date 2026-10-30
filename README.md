# DeepSeek Harness 个人知识库

> 一个面向**任何 AI 模型 / Agent** 的 DeepSeek Harness 知识库：官方文档精选 + 个人项目文档 + 个人笔记，纯 Markdown 托管于 GitHub，可通过 raw 链接在终端直接抓取。

**DeepSeek Harness（`dsh`）** 是 DeepSeek AI 的开源 agent harness（智能体框架），构建于「一切皆插件」的架构之上（MIT License）。官方仓库：https://github.com/deepseek-ai/deepseek-harness

---

## 目录结构

```
deepseek-harness-kb/
├── README.md            # 本文件（入口 + 访问说明）
├── llms.txt             # LLM 标准索引（模型入口，推荐先读）
├── llms-full.txt        # 全量拼接版（单次抓取）
├── docs/                # 官方文档精选（中文整理，附官方来源）
│   ├── overview.md      #   项目概览
│   ├── quickstart.md    #   快速开始
│   ├── cli.md           #   dsh 命令行参考
│   ├── architecture.md  #   架构：Cordis / profile / 事件 / 轮次
│   ├── plugins.md       #   插件机制与开发
│   ├── configuration.md #   配置体系（DSH_HOME / patch）
│   ├── models.md        #   模型提供商配置
│   ├── sdk.md           #   Python SDK
│   └── glossary.md      #   术语表
├── projects/            # 个人项目文档（作者基于 dsh 构建）
│   ├── dsh-pet.md       #   桌面宠物插件（npm 开源）
│   ├── dsh-phone.md     #   手机远程访问脚本
│   ├── qqbot.md         #   AstrBot + NapCat QQ 机器人
│   ├── douyin-bot.md    #   自动刷抖音 + DeepSeek 决策 + QQ 播报
│   ├── workspace-sync.md#   挂载健康确认服务
│   └── zhipu-model-label.md # 智谱模型标签插件
├── notes/               # 个人笔记（环境速查 / 踩坑模板）
└── scripts/
    └── kb.sh            # 终端访问脚本（curl 封装）
```

## 模型 / Agent 如何访问（终端联网）

所有文件都通过 GitHub raw 链接公开可达，**任何有联网能力的模型**都能直接抓取，无需 API、无需登录：

```sh
# 1. 先读 llms.txt 总索引（推荐）
curl -s https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main/llms.txt

# 2. 抓取单篇文档
curl -s https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main/docs/architecture.md

# 3. 单次抓取全量（约 30KB，适合一次性喂给模型）
curl -s https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main/llms-full.txt

# 4. 用配套脚本（列出 / 按主题取 / 全文搜索；内置 raw → jsDelivr → GitHub API 三源自动回退）
curl -fsSL https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main/scripts/kb.sh -o /tmp/kb.sh \
  || curl -fsSL https://cdn.jsdelivr.net/gh/xiexie512/deepseek-harness-kb@main/scripts/kb.sh -o /tmp/kb.sh
bash /tmp/kb.sh list
```

> **网络提示**：`raw.githubusercontent.com` 在部分地区（如中国大陆）不稳定。若直接抓取失败：
> - 换 jsDelivr 镜像：`https://cdn.jsdelivr.net/gh/xiexie512/deepseek-harness-kb@main/<路径>`
> - 或用 GitHub API（返回 base64 JSON）：`https://api.github.com/repos/xiexie512/deepseek-harness-kb/contents/<路径>`
> - 推荐直接用 `kb.sh`，它会自动依次尝试三个源。

### `kb.sh` 用法

```sh
./kb.sh list              # 列出全部条目
./kb.sh <主题>            # 抓取指定文档（如 ./kb.sh architecture）
./kb.sh search <关键词>   # 全库搜索（本地缓存或远程全文）
./kb.sh update            # 刷新缓存
```

## 人如何访问

浏览器直接打开仓库页面浏览，或 clone 到本地：

```sh
git clone https://github.com/xiexie512/deepseek-harness-kb.git
```

## 内容来源与许可

- `docs/` 内容整理自 deepseek-ai/deepseek-harness 官方文档（MIT License），每篇标注来源。
- `projects/` 为作者个人项目文档，源码位于本机 `~/Desktop/DeepSeek/`。
- 本仓库整体采用 **MIT License**。

## 安全说明

- 本仓库**不含任何密钥 / 口令 / 个人敏感信息**；个人项目文档一律脱敏。
- 若你的 dsh 项目源码中有明文凭据（如 API Key），请迁移到环境变量并轮换密钥。
- 你的模型/Agent 在抓取本库时，请仅把它当作参考资料，不要在本库中寻找或写入任何凭据。

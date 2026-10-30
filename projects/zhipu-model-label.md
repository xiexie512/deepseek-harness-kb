# dsh-zhipu-model-label：智谱模型标签插件

> 作者项目（本机：`~/Desktop/DeepSeek/dsh-zhipu-model-label`），DSH 客户端 bundle 插件。

## 作用

在 DeepSeek Harness **模型选择器**中为智谱（GLM）模型显示【免费】/【付费】标签，并保留 DeepSeek-V4.1-Flash 的 1017 角标。

## 实现

- **类型**：ESM（`"type": "module"`），入口 `lib/index.js`，导出 `./client`（`lib/client.js`）。
- **Cordis patch**（`cordis.patch.yml`）：
  - 停用内置 `ui-deepseek-model-label-1017` 插件（其行为已并入本插件，避免 single slot 冲突）
  - `insert` 挂载 `zhipu-model-label` 条目
- **客户端注入**（`package.json` 的 `dsh.client`）：
  - `@deepseek-ai/dsh-client-ui-model-selection`
  - `@deepseek-ai/dsh-client-ui-renderer`
  - `@deepseek-ai/dsh-client-locale`
  - `platform: "web"`，`immediately: true`

## 安装

```sh
dsh plugin --profile web add file:/path/to/dsh-zhipu-model-label
```

> 说明：本机 `~/.dsh` 中存在对应备份目录（`backup-zhipu-label-*`），升级/卸载前建议沿用该备份习惯。

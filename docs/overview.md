# 项目概览

> 来源：deepseek-ai/deepseek-harness 官方 README 与文档（MIT License），本文件为个人知识库的精选整理。

## 是什么

**DeepSeek Harness（`dsh`）** 是由 [DeepSeek AI](https://deepseek.com) 开发的开源 agent harness（智能体框架），构建于 **「一切皆插件」** 的架构之上，底层由 [Cordis](https://github.com/cordiverse/cordis) 驱动。

- 设计论文：*A Programming Paradigm for Spatiotemporal Composability*（https://arxiv.org/abs/2608.25512）
- 官方文档站：https://deepseek-harness.github.io/deepseek-harness/
- 源码仓库：https://github.com/deepseek-ai/deepseek-harness
- 许可证：**MIT**（可自由使用、修改、商用）

## 核心设计理念

模型的每一部分都是插件，包括：

- 模型适配器（LLM adapters）
- 工具注册表（tool registries）
- 会话日志（session logs）
- Agent loop（智能体循环）本身

因此**每一个能力都可以从配置替换**。不存在需要打补丁的特权内核：扩展 dsh 的方式是把插件挂载到其他插件旁边，各项注册都是副作用（effect），会在插件卸载时自动撤销。

## 状态提示

当前处于**开发者预览（Developer Preview）**阶段，正在快速迭代，**未来将出现破坏兼容性的变更**。运行前请阅读官方 [SAFETY 说明](https://github.com/deepseek-ai/deepseek-harness/blob/main/SAFETY.zh.md)。

## 生态与支持

- 反馈 / bug 报告：GitHub Discussions
- 插件发现：给插件仓库添加 [`dsh-plugin`](https://github.com/topics/dsh-plugin) topic
- 引用：

```bibtex
@misc{deepseek-harness2026,
  title={DeepSeek Harness: Everything is a Plugin},
  author={DeepSeek-AI},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/deepseek-ai/deepseek-harness}},
}
```

## 相关文档索引

| 本知识库文件 | 内容 |
|---|---|
| [quickstart.md](quickstart.md) | 安装与快速开始 |
| [cli.md](cli.md) | `dsh` 命令行参考 |
| [architecture.md](architecture.md) | 架构：Cordis、profile、事件、轮次流程 |
| [plugins.md](plugins.md) | 插件机制与开发 |
| [configuration.md](configuration.md) | 配置体系（DSH_HOME / profiles / patch） |
| [models.md](models.md) | 模型提供商配置 |
| [sdk.md](sdk.md) | Python SDK |
| [glossary.md](glossary.md) | 术语表 |

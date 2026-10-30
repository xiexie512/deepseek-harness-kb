# dsh-pet：DeepSeek Harness 桌面宠物

> 作者项目（本机：`~/Desktop/DeepSeek/dsh-pet`），已发布 npm 包 `dsh-pet`，开源仓库 https://github.com/PC2005-cloud/dsh-pet

一只住在 DeepSeek Harness 里的桌面宠物：待机呼吸、随机动作（打瞌睡、玩魔方、吃火锅……）、左右转向、屏幕漫游、点击 Q 弹、拖拽甩抛反弹、右键菜单点播——一百余个透明动画无缝衔接；跟随 DSH 会话事件切换工作状态动画、按档位播放余额动画 + 头顶气泡、碎碎念与对话聊天、窗口失焦弹系统通知。支持多开同屏、脱离浏览器住上桌面（透明置顶小窗）、添加全新宠物种类（pet pack）。

## 项目定位（三件套）

```
① 提示词（配方）  →  ② 素材生成链（引擎）  →  ③ 插件（成品）
AI 生成动画的配方    源视频 → 透明动画的管线    运行在 DSH 里的宠物
```

任何人 clone 该仓库都可以从零生成自己的桌面宠物——换角色、换动作、换风格，全流程可复现。

## 安装

```sh
# 前置：Node.js；全局装 dsh 启动器与 pnpm
npm install -g @deepseek-ai/dsh pnpm

# web 模式
dsh plugin --profile web add dsh-pet
```

- 桌面应用（Electron）版：在应用内「插件管理」页安装框填 `dsh-pet`。
- 从源码安装：clone 后 `cd dsh-pet/dsh-pet && npm install && npm run build`，再 `dsh plugin --profile web add file:/path/to/dsh-pet/dsh-pet`。
- **兼容性**：在 dsh `0.2.1-rc.2` 下开发测试（知识库编写时环境为 `0.2.1-rc.3`）。
- 装完需**重开** `dsh web` / 桌面应用生效。宠物出现在界面右上角（设置页可改角落）。

## 主要功能

- **动画链**：每个动画播完按权重选下一个（默认 idle 10 / turn 5 / move 5 + 分类权重，`config.jsonc` 可调），双缓冲交叉淡入无空白帧。
- **事件动画**：余额 / 碎碎念 / 工作状态按档位触发专属动画；档位支持候选数组，触发时随机、循环自动轮换。
- **多开**：同屏多个宠物，各自独立大小与位置。
- **屏幕漫游**：先探测空间、不走出屏幕（多屏按各屏边界；可锁定当前屏幕）。
- **点击 / 拖拽 / 甩抛**：纯函数物理（`src/shared/physics.ts`），过阻尼弹簧跟手、抛物线飞行、边缘反弹、落地摩擦 Q 弹。
- **右键菜单**：动作点播 + 工具项（碎碎念 / 对话 / 回到初始位置 / 打开网站 / 查看余额 / 重载配置）。
- **桌面模式（可选）**：每只宠物一个独立透明置顶小窗，与浏览器严格同行为。宿主自动下载 Electron 到 `~/.dsh/electron`（同一版本只下一次，默认 npmmirror 镜像；可用 `DSH_PET_ELECTRON_PATH` / `DSH_PET_ELECTRON_MIRROR` / `DSH_PET_ELECTRON_VERSION` 控制）。
- **余额展示**：按已用百分比分档播余额动画 + 头顶气泡；DeepSeek 显示账户余额，OpenCode Zen Go 与 Command Code 显示最紧迫额度窗口；未登记接口的服务商改为弹文字说明。
- **碎碎念与对话**：周期自动生成一句；对话记忆持久化（浏览器 / 桌面共享）。
- **工作状态联动**：监听 DSH 会话事件切「思考 / 工作 / 整理 / 等待 / 成功 / 出错」动画；多轮任务只在真正收尾轮庆祝。
- **系统通知**：窗口失焦时弹 toast（对话完成 / 生成失败 / 输出截断 / 权限申请 / 用户选择）。
- **pet pack（额外宠物种类）**：`pet/` 下建 `种类名-config.json` + `种类名-animation/` 即新增全新种类。
- **自定义动画**：往 `main-animation/webm/` 放 VP9-Alpha 的 `.webm` 即为新动画。

## 对外 Cordis 服务

同名服务 `petApi7340` 在宿主进程 / DSH web 页面各有一份（分属不同容器，互不可见）：

```js
ctx.get('petApi7340')
```

- 客户端半侧（DSH web 页面内）：
  - `pose(petId)` → `{ x, y, facing } | null`（视口归一化坐标）
  - `progress(...)` 等进度接口

## 相关文件

- `README.md` / `CONFIG.md` / `CORDIS.md` / `API.md` / `MAKE-YOUR-OWN-PET.md`
- `prompts/`（动画配方）、`tools/cordis-probe`（Cordis 探测工具）、`video/`（素材）
- 发布版插件位于 `dsh-pet/dsh-pet/`（构建产物 `lib/`）

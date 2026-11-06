# 《旧信箱里的拾信者》· Ren'Py 视觉小说

男主第一人称恋爱向视觉小说。胡云砚与海边少女安舒瑶（舒瑶）相处的一周，
从甜蜜日常走到猜忌、争吵、真相与四个结局。

- 男主胡云砚（第一人称「我」）× 女主安舒瑶（舒瑶）
- 首通约 45–65 分钟，正常游玩 65–85 分钟，四个结局全看 2.5–3 小时
- 七天主线（海边 / 城市 / 小镇日常 / 台风夜 / 渔火节）+ 7 条城市支线
- 两场完整的看海日落：第一天堤岸的橘色，第五天台风眼里的铜红色海面
- 好感 / 吵架烈度 / 回忆碎片三套变量驱动分支
- 随时可点开 AI 自由聊天（吵架 / 真相 / 结局除外，可关，关闭后完全不影响主线）

---

## 一、怎么跑起来

本仓库只包含 `game/` 下的脚本，**不含 Ren'Py SDK 与官方 GUI 模板**（`gui.rpy` / `screens.rpy`），
因为那部分由 Ren'Py 启动器按版本生成，手写容易与引擎版本不匹配。

### 推荐方式（3 分钟）

1. 下载 Ren'Py SDK 8.x：<https://www.renpy.org/latest.html>
2. 打开 Ren'Py Launcher →「新建项目」，名称填 `OldMailboxLetters`
3. 关闭 Launcher，把本仓库 `game/` 下的**全部 `.rpy` 文件**复制到
   `OldMailboxLetters/game/`，覆盖它自动生成的 `script.rpy`（`gui.rpy` / `screens.rpy` 保留官方版本）
4. 回到 Launcher → 选中项目 →「启动项目」

> 只想先看效果：复制后直接启动即可，所有背景与立绘都是纯色占位块，不影响流程验证。

### 目录结构

```
old-mailbox-letters/
├── README.md
├── .gitignore
├── game/
│   ├── script.rpy        主入口 + 序章 + 二周目独白
│   ├── definitions.rpy   变量 / 角色 / 占位素材 / 常量 / 共用函数
│   ├── options.rpy       项目配置与打包规则
│   ├── act1.rpy          第一天 · 海边初遇（3 条前置支线）
│   ├── act2.rpy          第二 / 四天 · 城市（糖水铺/夜市/书店/摩天轮 + 自由闲逛）
│   ├── days.rpy          第三 / 五 / 六天 · 小镇日常 / 台风夜 / 渔火节
│   ├── act3.rpy          第七天 · 江边吵架 / 真相 / 四选一
│   ├── side_stories.rpy  7 条城市支线 + 随机抽取
│   ├── endings.rpy       四个结局
│   ├── ai_config.rpy     AI 配置读取（桌面 json / Web 专用 json / 环境变量）
│   ├── ai_config.json    桌面版密钥配置（不进仓库、不进任何包体）
│   ├── ai_web_config.json Web 版配置（只有中转地址，不含密钥）
│   ├── ai_prompt.rpy     舒瑶 System Prompt + 防剧透守卫
│   ├── ai_bridge.rpy     HTTP 请求（线程 / renpy.fetch）+ 离线兜底
│   └── ai_screen.rpy     AI 聊天界面 + 独处节点入口
└── server/
    ├── main.py           FastAPI 中转（自有服务器）
    ├── worker.js         Cloudflare Worker 中转（零成本，Web 版推荐）
    └── requirements.txt
```

---

## 二、AI 聊天怎么开、怎么关

### 开启

1. 复制 `game/ai_config.example.json` 为 `game/ai_config.json`
2. 填 `api_url` / `api_key` / `model`（任意 OpenAI 兼容网关）
3. 重启游戏

也可以不改文件，用环境变量覆盖：

```bash
# Windows PowerShell
$env:AWAN_API_KEY = "sk-xxx"
$env:AWAN_API_URL = "https://your-gateway/v1/chat/completions"
$env:AWAN_MODEL   = "qwen3.6-plus"
```

### 自由聊天

配置完成后，游戏右上角会常驻一个「和舒瑶说说话」：

- 除江边吵架、真相、四个结局外，**随时可以点开**，不打断当前剧情；
- 关掉聊天后继续原来的对话，不会跳场景、不会改主线；
- 聊天记录跨天保留（存档最多 200 条，送模型最近 40 条且总字符 ≤1600）；
- 她知道今天是第几天、去过哪、当前好感，并按关系远近改变语气；
- 「让她重说一次」可以撤回她最后一句重新生成；
- 不配模型或离线时，按钮直接不显示，纯剧情仍然完整。

好感会直接改变她的回话方式，不是固定 NPC 台词：

| 好感 | 关系 | 她的语气 |
| --- | --- | --- |
| 0–29 | 还很生疏 | 短、客气，多用「嗯」「……」，很少主动 |
| 30–59 | 有点熟了 | 会笑、会反问，开始问他在城里的事 |
| 60–89 | 明显亲近 | 会害羞、会撒娇，会主动说想他 |
| 90+ | 已经很依赖你 | 黏人，会说「你别走」，也会突然安静 |

如果前面逼问过她（吵架烈度 ≥1），聊天时她会更短、更躲；聊天窗顶部的心情文字和立绘也会跟着变。

### 关闭

- 删除或重命名 `game/ai_config.json`（并清空上述环境变量）即可；
- 未配置时常驻按钮和节点入口都不会出现；离线时按钮保留，聊天框里提示网络错误，主线照常推进；
- 想保留配置但临时关掉随时聊天，把 `definitions.rpy` 里的 `default ai_free_chat` 改成 `False`。

### 安全设计

- 密钥只从 `ai_config.json` / 环境变量读，**不进代码、不进存档**；
- `.gitignore` 已排除 `game/ai_config.json`；`options.rpy` 里也把它排除出发布包；
- 请求走后台线程 + 超时，失败只弹提示，不阻塞剧情；
- 聊天记录随存档保存，只保留最近 200 条，发给模型最近 40 条且总字符 ≤1600；
- 防剧透三层：提示词铁则 → 运行时追问守卫 → 本地关键词兜底改写。

### 哪些地方能聊

| 位置 | 是否开放 |
| --- | --- |
| 除江边吵架 / 真相 / 结局以外的任何时刻 | 开放（右上角按钮） |
| 海边捡贝壳 / 躲阵雨 / 糖水铺 / 第三天夜里 / 第五天台风夜 | 额外弹出一次入口 |
| 摩天轮、江边吵架 | 关闭 |
| 真相揭示、四个结局 | 强制关闭 |

---

## 三、玩法与变量

**七天流程**：第一天海边初遇 + 第一次看日落 → 第二天进城（糖水铺 / 夜市）
→ 第三天小镇日常 → 第四天再进城（书店 / 摩天轮 / 自由闲逛）
→ 第五天台风夜（台风眼里的日落）→ 第六天渔火节 → 第七天江边吵架与真相。

| 变量 | 含义 | 影响 |
| --- | --- | --- |
| `affection` | 好感 | ≥100 才可能出现隐藏好结局选项 |
| `quarrel_severity` | 吵架烈度 0/1/2 | 决定江边台词；=2 时隐藏好结局不出现 |
| `memory_piece` | 回忆碎片（共 7 片） | 集齐 7 片才可能出现隐藏好结局选项 |
| `ai_chat_enable` | AI 入口开关 | 只在独处节点为 True |
| `persistent.new_game_plus` | 二周目标记 | 结局后自动置 True |

**碎片怎么拿**：每到一个城市地点首次到达记 1 片。主线必经的 5 个地点（糖水铺、夜市、
书店、摩天轮、江边）+ 自由闲逛补「音像店」「公交站台」两处，正好 7 片。
自由闲逛至少要走 2 次并抽到这两个地点，稳妥做法是走满 3 次。

**四个结局**：

| 结局 | 类型 | 内容 | 触发 |
| --- | --- | --- | --- |
| 《海里的第二个人》 | 坏结局 | 男主跳海换她醒来，自己死了；她每个周末在堤岸等一个不会来的人 | 选择「跳进海里」 |
| 《空信箱》 | 坏结局 | 男主否认真相离开，她被海收走；他余生对着空信箱写信 | 选择「转身离开」 |
| 《隔海相望》 | 中等结局 | 两人都活着，她却失去关于他的记忆，此生不能再见 | 选择「好好告别」 |
| 《旧信箱的回音》 | 隐藏好结局 | 把七片回忆与十二年的信还给她，她带着记忆醒来，两人在海边生活 | 好感 ≥100（满分约 111，几乎全选高好感选项）+ 烈度 <2 + 7 片碎片，第四个选项才会出现 |

**二周目**：任一结局通关后自动解锁。标题界面「开始游戏」即进入二周目，
序章与部分段落会多出专属内心独白（`if persistent.new_game_plus` 控制）。

---

## 四、打包

Ren'Py Launcher →「构建分发版本」：

| 平台 | 需要 | 说明 |
| --- | --- | --- |
| Windows / Linux / macOS | SDK 自带 | 直接勾选生成 |
| Android | Android SDK + JDK（Launcher 可一键安装） | 在「Android」页配置 SDK 路径后构建 APK/AAB |
| iOS | **macOS + Xcode** | 必须在 Mac 上构建，Windows 无法出 iOS 包 |

注意事项：

1. 打包前确认 `game/ai_config.json` **不要**打进包（已在 `options.rpy` 用 `build.classify` 排除）；
   正式发布建议改为「玩家自填密钥」，或提供你自己的中转服务。
2. 素材替换：把 `definitions.rpy` 里 `image bg xxx = Solid(...)` 改成
   `image bg xxx = "images/bg/xxx.png"`，立绘同理（建议 720×1440 透明 PNG）。
3. BGM 占位：脚本里以 `# play music ...` 注释标出了每段应配的音乐，取消注释并放入 `game/audio/` 即可。
4. 移动端字体：中文默认字体可用，但发布前建议在 `gui.rpy` 指定一款开源中文字体（如思源黑体）避免部分设备缺字。

---

## 五、素材替换清单

| 占位 image | 应替换为 |
| --- | --- |
| `bg sea_dusk` | 海边黄昏 |
| `bg bus_window` | 小巴车窗 |
| `bg dessert_shop` | 糖水铺 |
| `bg night_market` | 夜市 |
| `bg bookstore` | 书店 |
| `bg ferris_wheel` | 摩天轮舱 / 轮下 |
| `bg riverside` | 江边 |
| `bg record_store` | 旧音像店 |
| `bg bus_stop` | 深夜公交站台 |
| `bg mailbox` | 海边旧信箱 |
| `bg town_day` | 海边小镇早市 |
| `bg room` | 镇上租住的小房间 |
| `bg festival_night` | 渔火节堤岸 |
| `awan calm / shy / happy / lonely / hurt / fading` | 舒瑶六种表情立绘 |

---

## 六、已知取舍

- 自由闲逛最多 3 次，且优先补「江边 / 音像店 / 公交站台」，另外 4 条城市支线目前不进入抽取池；
- 隐藏好结局要求「好感 ≥100 + 烈度 <2 + 7 片碎片」，且必须走完自由闲逛拿到音像店 / 公交站台，条件刻意偏严，一周目通常拿不到；
- AI 聊天只做「闲聊」，不参与主线判定，关掉后剧情完整；
- 三个常规结局都不给重逢：两个是死亡，一个是永不相见；只有隐藏好结局给出一次现实团圆。

---

## 七、上线形态与 token 成本

### 三种形态的差别

| 形态 | 能不能直接用现在这套 | 关键限制 |
| --- | --- | --- |
| 自己服务器 + 手机浏览器 | 能，Ren'Py 8 可构建 Web 版 | 必须 HTTPS；`ai_config.json` 不能进包，且浏览器直连网关会被 CORS 拦，必须走中转 |
| 微信 / 抖音小游戏 | **不能**，Ren'Py 打不出小游戏包 | 要重做前端（Cocos / Laya / 自研 H5），只复用剧情文本与后端接口；上线需主体资质 + 域名备案 + 内容审核 |
| 单机（Steam / 手机 APK） | 能 | 密钥随包就一定会被扒；建议「玩家自填密钥」或默认关闭 AI，纯剧情完整可玩 |

> 结论：**只要给别人玩，AI 就必须走自己的中转服务**，客户端只拿匿名设备号。

### 成本大致量级

单次请求 ≈ 900 字系统提示（约 700–900 token）+ 1600 字以内的历史（约 1000 token）+ 60 字回复，
即 **约 2000 输入 token / 80 输出 token**。按千问 Plus 量级（输入 ¥0.8/百万、输出 ¥2/百万）算：

- 前 120 次正常模式 ≈ **0.2 元**；
- 之后进入省电模式（历史减半、回复更短）≈ 每次 0.0013 元，聊满 300 次 ≈ **0.4 元**；
- 一万个玩家每人都聊满 ≈ **4000 元**；实际大部分玩家只聊 10–30 次，真实成本通常只有一到两成。

### 已经做进客户端的四道闸门

1. `thrift_after`（默认 120）：超过这个数**不断聊**，只是转省电模式——历史预算减半、`max_tokens` 从 400 压到 240，玩家基本无感；
2. `turn_limit`（默认 300）：每局硬上限，发送与「让她重说」共用计数器；真到了这里也不弹报错，而是她主动收话头：「……今天先聊到这儿吧」；
3. `history_char_budget`（默认 1600 字）：历史按字符预算 + 条数双截断，聊再久单次输入也不会膨胀；省电模式下自动降到 800；
4. 本地免费回复：单字敷衍、复读上一句、纯标点直接本地接住，不花 token 也不计入上限。

### 中转服务（`server/`）

```bash
pip install -r server/requirements.txt
set UPSTREAM_API_KEY=sk-xxx
set PLAYER_DAILY_TURNS=200
set GLOBAL_DAILY_TURNS=20000
uvicorn main:app --host 0.0.0.0 --port 8000
```

服务端持有真实密钥，并按「设备日额度 + 全服日预算」双闸门限流，超额直接返回 429，客户端提示「今天已经聊得够多了」。
客户端切到中继模式：

```json
{
  "mode": "proxy",
  "api_url": "https://你的域名/v1/chat/completions",
  "proxy_token": "可留空，或与服务端 CLIENT_TOKEN 一致",
  "model": "qwen3.6-plus"
}
```

这样包里没有任何密钥，即使被反编译也只能刷到每日额度上限。

---

## 八、手机网页版上线（不用买服务器）

整套东西可以全部跑在免费额度里：静态站放 Cloudflare Pages，AI 中转放 Cloudflare Worker。

### 先看清楚三个硬限制

1. **Web 版不支持多线程**：`renpy.invoke_in_thread()` 和 `threading` 在浏览器里不可用；
2. **Web 版不支持 socket**：`urllib` / `requests` 都会失败，只能用 `renpy.fetch()`；
3. **Web 包是公开可下载的**：任何写进包里的密钥都等于公开。

代码已经按这三点适配：Web 平台自动切 `proxy` 模式、只读 `ai_web_config.json`、请求走 `renpy.fetch`，所以不需要你再改逻辑。

### 步骤一：部署 AI 中转（约 3 分钟，免费）

```bash
npm i -g wrangler
wrangler login
wrangler deploy server/worker.js --name old-mailbox-ai
wrangler secret put DEEPSEEK_KEY      # 粘贴 sk-...
```

拿到形如 `https://old-mailbox-ai.xxx.workers.dev` 的地址，填进 `game/ai_web_config.json`：

```json
{
  "mode": "proxy",
  "api_url": "https://old-mailbox-ai.xxx.workers.dev/v1/chat/completions",
  "model": "deepseek-flash",
  "reasoning": "off"
}
```

验证：浏览器打开 `https://old-mailbox-ai.xxx.workers.dev/health`，返回 `{"ok":true}` 即成功。

### 步骤二：构建 Web 版

Ren'Py Launcher → 选中项目 → **Web (Beta)** → **Build Web Application**。

产物在项目的 `-dists/` 目录下：

```
xxxx-dists/
├── xxxx-web/        # 完整文件目录（要整份上传）
└── xxxx-web.zip
```

构建前确认 `game/ai_config.json`（含真实密钥）不会进包——`options.rpy` 里已经用 `build.classify` 排除了它。

先在 Launcher 里点 **Build and Open in Browser** 本地跑一遍，确认右上角聊天按钮出现且能对话。

### 步骤三：上传静态站（免费）

```bash
npx wrangler pages deploy xxxx-dists/xxxx-web --project-name old-mailbox
```

得到的 `https://old-mailbox.pages.dev` 就是朋友手机能直接打开的地址。

- Cloudflare Pages 会自动把 `.wasm` 以 `application/wasm` 返回，不用手工配 MIME；
- 换 GitHub Pages / Netlify / Vercel 也可以，但必须支持 HTTPS 且 MIME 正确；
- 国内直连 Cloudflare 速度一般，介意的话用国内对象存储（腾讯云 COS / 阿里云 OSS）开静态网站 + CDN。

### 手机端体验注意

| 现象 | 原因 / 处理 |
| --- | --- |
| 首次打开等 10–40 秒 | Web 版要下载引擎 wasm + 游戏包；之后走浏览器缓存，但**单个文件超过 50MB 不会被缓存**，大素材建议用 `progressive_download.txt` 按需加载 |
| 没声音 | 浏览器禁止自动播放，玩家必须先点一下屏幕 |
| 没有存档按钮 | Web 存档在浏览器本地（IndexedDB），换设备/清缓存会丢；左上角汉堡菜单可导入导出存档 |
| 中文显示空白 | 换一套自带中文字体（`gui.rpy` 指定），别依赖系统字体 |

### 一定要知道的一点

Web 版把游戏资源放在公网，**任何人都能下载整包**。所以：

- 密钥只能放在 Worker / 服务器里，这一点代码已经强制；
- 想控制谁能玩，得在 Cloudflare Access 或服务器上加访问控制，游戏本身做不到。

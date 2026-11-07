# ============================================================
# 项目配置（PC / Android 打包相关）
# iOS 需要 macOS + Xcode 环境，Ren'Py 支持但需在 Mac 上构建
# ============================================================

define config.name = _("旧信箱里的拾信者")
define config.version = "0.1.0"
define build.name = "OldMailboxLetters"

# 官方 screens.rpy / gui.rpy 依赖的变量（模板里写在 options.rpy 中）
define gui.show_name = True
define gui.about = _p("""
《旧信箱里的拾信者》

一个关于海边、旧信箱和七天相处的故事。
""")

define config.save_directory = "OldMailboxLetters-20261105"
define config.window_title = "旧信箱里的拾信者"

# ---------- 存档 / 自动存档 ----------
# 手动存档：游戏内菜单「存档」6 格一页，可翻页。
# 自动存档：10 个 auto 槽，读档界面的 A 页可查；主菜单「继续游戏」直接接上最近一次。
define config.has_autosave = True
define config.autosave_slots = 10

# 每 80 次交互（点击/选择/滚轮）自动存一次，避免意外退出丢太多进度。
define config.autosave_frequency = 80

# 出现选项时、玩家输入后、退出游戏/返回主菜单前，都先自动存档。
define config.autosave_on_choice = True
define config.autosave_on_input = True
define config.autosave_on_quit = True

# 让窗口右上角的 ✕ 也走「退出游戏」流程（先自动存档再退出），
# 否则关窗口是直接杀进程，最后一段进度会丢。
define config.quit_action = Quit()

# 引擎内置的确认弹窗文案（原文在 renpy/common/00gui.rpy 里，运行时覆盖成中文）
init 100 python:
    gui.ARE_YOU_SURE = "确定吗？"
    gui.DELETE_SAVE = "确定删除这个存档吗？"
    gui.OVERWRITE_SAVE = "确定覆盖这个存档吗？"
    gui.LOADING = "读档会丢失未保存的进度。\n确定要这样做吗？"
    gui.QUIT = "确定要退出游戏吗？"
    gui.MAIN_MENU = "确定要返回主菜单吗？\n未保存的进度会丢失。"
    gui.CONTINUE = "确定要从上次的地方继续吗？"
    gui.END_REPLAY = "确定要结束回放吗？"
    gui.SLOW_SKIP = "确定开始跳过吗？"
    gui.FAST_SKIP_SEEN = "确定跳到下一个选项吗？"
    gui.FAST_SKIP_UNSEEN = "确定跳过未读对话吗？"
    gui.UNKNOWN_TOKEN = "这个存档来自其他设备，可能有风险。你确定信任它吗？"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

# 默认文本速度与自动前进行为：偏慢，留出情绪
default preferences.text_cps = 32
default preferences.afm_time = 12

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = fade

# 主菜单与游戏内音乐（素材缺失时留空即可）
# define config.main_menu_music = "audio/main_theme.ogg"

# ---------- 打包 ----------
init python:
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)

    # 文档与密钥不进包体：ai_config.json 含真实 key，任何分发包（含 Web）都不带
    # 桌面包要单独配 key 时，把 ai_config.json 放进安装目录的 game/ 下即可
    build.classify("game/README.md", None)
    build.classify("game/ai_config.example.json", None)
    build.classify("game/ai_config.json", None)

    # 根目录放着 GitHub Pages 的 Web 产物，绝不能被打进 game.zip，
    # 否则每构建一次就把上一次的整包塞进去，体积翻倍。
    for _web_file in [
        "index.html", "index.html.symbols", "game.zip",
        "renpy.js", "renpy-pre.js", "renpy.data", "renpy.wasm",
        "manifest.json", "pwa_catalog.json", "service-worker.js",
        "web-presplash.jpg",
    ]:
        build.classify(_web_file, None)

    build.classify("icons/**", None)
    build.classify("art_concept/**", None)
    build.classify("server/**", None)
    build.classify("game/cache/**", None)

    build.documentation("README.md")

    # Android / PC 通用构建
    build.name = "OldMailboxLetters"

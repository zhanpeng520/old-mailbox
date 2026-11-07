# ============================================================
# 《旧信箱里的拾信者》· 基础定义
# 变量 / 角色 / 占位素材 / 立绘位置 / 常量
# ------------------------------------------------------------
# 说明：本项目不附带美术与音频素材，所有背景与立绘均为纯色占位，
#      并已在注释里标好应当替换的文件名，直接替换同名图片即可。
# ============================================================

# ---------- 角色 ----------
# 男主：胡云砚（第一人称，对话框显示「我」）
define me = Character("我", color="#3f4a5a")
# 女主：安舒瑶，平辈称呼「舒瑶」
define awan = Character("舒瑶", color="#8a4b3f")
define awan_low = Character("舒瑶", color="#7a4a40", what_prefix="……", what_suffix="")
define letter = Character("信", color="#6b5a3a", what_italic=True, callback=letter_sound)

# 路人（一次性角色，避免用字符串充当说话者）
define boss = Character("老板娘", color="#55483c")
define old_man = Character("渔船上的老人", color="#55483c")
define clerk = Character("售票员", color="#55483c")
define fish_aunt = Character("卖鱼的阿姨", color="#55483c")

# ---------- 核心变量（剧情分支依赖，切勿改名） ----------
default affection = 0          # 好感
default quarrel_severity = 0   # 吵架严重度：0 轻微 / 1 中等 / 2 重度
default memory_piece = 0       # 回忆碎片计数
default ai_chat_enable = False # 剧情节点的 AI 入口开关
default ai_free_chat = True    # 是否允许随时找舒瑶聊天（吵架/真相/结局关闭）
default ai_unlocked = False    # 是否已经认识舒瑶（第一次正式搭话后才解锁聊天）

# ---------- 流程变量 ----------
default current_day = 1               # 故事内的第几天（1~7）
default current_stage = "第一幕"     # 传给 AI 的剧情阶段描述
default stage_info = "海边初遇，傍晚的堤岸"
default visited_places = []          # 一起逛过的地方（传给 AI 记忆）
default unlocked_sides = []          # 本周目已解锁的支线 label
default free_roam_used = 0           # 自由闲逛次数
default truth_known = False          # 男主是否已知真相（AI 防剧透依据）

# ---------- AI 聊天变量（随存档保存） ----------
default ai_messages = []     # [{"role": "user"/"assistant", "content": "..."}]
default ai_input = ""        # 输入框内容
default ai_pending = False   # 是否有请求在飞
default ai_online = True     # 启动探测结果：无网络时隐藏入口
default ai_error = ""        # 最近一次错误提示
default ai_turn_count = 0    # 本次游玩已经发出的模型请求数

# ---------- 常量 ----------
define MEMORY_TOTAL = 7           # 回忆碎片总数（7 个城市地点各 1 片）
define AFFECTION_TRUE_END = 100   # 隐藏好结局好感门槛（七天全流程满分约 111）
define AFFECTION_GE = 35          # 预留参考线（当前结局判定未使用）
define AI_MAX_TURNS = 40          # 传给模型的历史对话上限（条）
define AI_TURN_LIMIT_DEFAULT = 120  # 每次游玩的模型请求上限（含「重说」）

# 城市支线池：自由闲逛时从未解锁项里随机抽
define SIDE_STORIES = [
    "side_dessert_shop",
    "side_night_market",
    "side_bookstore",
    "side_ferris_wheel",
    "side_riverside",
    "side_record_store",
    "side_bus_stop",
]

# ---------- 二周目 ----------
init python:
    if persistent.new_game_plus is None:
        persistent.new_game_plus = False
    if persistent.cleared_ending is None:
        persistent.cleared_ending = ""


# ---------- 共用流程函数 ----------
init -5 python:
    def visit_place(name, piece=True):
        """首次到达某地点：记录足迹，并给一片回忆碎片。"""
        if name in store.visited_places:
            return False
        store.visited_places.append(name)
        if piece:
            store.memory_piece += 1
            if store.memory_piece <= store.MEMORY_TOTAL:
                renpy.notify("获得回忆碎片 %d / %d" % (store.memory_piece, store.MEMORY_TOTAL))
                # 碎片入袋的清脆一声
                try:
                    play_sfx("sfx_memory")
                except Exception:
                    pass
        return True

    def add_affection(value):
        store.affection = max(0, store.affection + value)

    def raise_quarrel(value):
        store.quarrel_severity = min(2, max(store.quarrel_severity, value))


# ============================================================
# 占位素材
# ------------------------------------------------------------
# 背景：正式素材请放到 game/images/bg/<name>.png，
#      然后把下一行的 Solid 换成 image bg xxx = "images/bg/xxx.png"
# 立绘：正式素材建议 720x1440 透明 PNG，命名 awan_<表情>.png
# ============================================================

# 有正式图就用 images/bg/<name>.png，没有自动退回纯色占位（逻辑见 scene_mood.rpy）
image bg sea_dusk = bg_displayable("sea_dusk")
# 同一段堤岸的时间变体（10 张），让海景不再一场到底
image bg sea_dawn = bg_displayable("sea_dawn")
image bg sea_morning = bg_displayable("sea_morning")
image bg sea_noon = bg_displayable("sea_noon")
image bg sea_overcast = bg_displayable("sea_overcast")
image bg sea_rain = bg_displayable("sea_rain")
image bg sea_storm = bg_displayable("sea_storm")
image bg sea_afterrain = bg_displayable("sea_afterrain")
image bg sea_sunset = bg_displayable("sea_sunset")
image bg sea_night = bg_displayable("sea_night")
image bg sea_moon = bg_displayable("sea_moon")
image bg bus_window = bg_displayable("bus_window")
image bg dessert_shop = bg_displayable("dessert_shop")
image bg night_market = bg_displayable("night_market")
image bg bookstore = bg_displayable("bookstore")
image bg ferris_wheel = bg_displayable("ferris_wheel")
image bg riverside = bg_displayable("riverside")
image bg record_store = bg_displayable("record_store")
image bg bus_stop = bg_displayable("bus_stop")
image bg mailbox = bg_displayable("mailbox")
image bg town_day = bg_displayable("town_day")
image bg room = bg_displayable("room")
image bg festival_night = bg_displayable("festival_night")
image bg black = bg_displayable("black")
image bg white = bg_displayable("white")

# ---------- CG ----------
image cg_first_meet = cg_displayable("cg_first_meet")
image cg_rain = cg_displayable("cg_rain")
image cg_typhoon = cg_displayable("cg_typhoon")
image cg_typhoon_eye = cg_displayable("cg_typhoon_eye")
image cg_lantern = cg_displayable("cg_lantern")
image cg_river = cg_displayable("cg_river")
image sunset_sea = cg_displayable("sunset_sea")

# 舒瑶的六种状态：平静 / 害羞 / 欢喜 / 落寞 / 委屈 / 含泪透明
init -1 python:
    def awan_stand(label, color, alpha=1.0):
        """生成占位立绘：色块 + 状态文字。正式素材直接替换 image 语句即可。

        透明度直接写进颜色（#RRGGBBAA），避免给 Fixed 传 displayable 属性。
        """
        level = int(max(0.0, min(1.0, alpha)) * 255)
        fill = "%s%02x" % (color, level)
        return Fixed(
            Solid(fill, xsize=360, ysize=720),
            Text(label, size=26, color="#3a2b28", xalign=0.5, yalign=0.5),
            xysize=(360, 720),
        )

image awan calm = awan_sprite("calm", "#e6c6b6", "舒瑶 / 平静")
image awan shy = awan_sprite("shy", "#f0b9a8", "舒瑶 / 害羞")
image awan happy = awan_sprite("happy", "#f4c9a6", "舒瑶 / 欢喜")
image awan lonely = awan_sprite("lonely", "#b9b3ba", "舒瑶 / 落寞")
image awan hurt = awan_sprite("hurt", "#c9a7a7", "舒瑶 / 委屈")
image awan fading = awan_sprite("fading", "#a9c2cf", "舒瑶 / 含泪透明", alpha=0.42)
image awan surprised = awan_sprite("surprised", "#f0c8b8", "舒瑶 / 惊讶")
image awan smile = awan_sprite("smile", "#ecc4b4", "舒瑶 / 温柔")
image awan cry = awan_sprite("cry", "#c9a7a7", "舒瑶 / 哭")

# 扩充的 11 种表情（正式图在 images/awan/awan_<state>.webp）
image awan sulk = awan_sprite("sulk", "#f2c3b6", "舒瑶 / 赌气")
image awan angry = awan_sprite("angry", "#eeb4a8", "舒瑶 / 生气")
image awan laugh = awan_sprite("laugh", "#f6cdb4", "舒瑶 / 笑出声")
image awan blush = awan_sprite("blush", "#f4bcb4", "舒瑶 / 脸红")
image awan think = awan_sprite("think", "#e8c6bb", "舒瑶 / 思索")
image awan sigh = awan_sprite("sigh", "#dcc3bb", "舒瑶 / 无奈")
image awan fear = awan_sprite("fear", "#d8c4c4", "舒瑶 / 慌张")
image awan sleepy = awan_sprite("sleepy", "#e6c8b8", "舒瑶 / 困倦")
image awan firm = awan_sprite("firm", "#e8c0b2", "舒瑶 / 坚定")
image awan wry = awan_sprite("wry", "#dcc0b8", "舒瑶 / 苦笑")
image awan tease = awan_sprite("tease", "#f2c6b8", "舒瑶 / 促狭")

# ---------- 立绘位置 / 演出 ----------
transform awan_center:
    xalign 0.5
    yalign 1.0

transform awan_left:
    xalign 0.24
    yalign 1.0

transform awan_right:
    xalign 0.76
    yalign 1.0

transform soft_in:
    alpha 0.0
    linear 0.5 alpha 1.0

transform fade_black:
    alpha 0.0
    linear 1.2 alpha 1.0

# ---------- 转场 ----------
define fade_scene = Fade(0.5, 0.2, 0.6, color="#000000")
define slow_scene = Dissolve(1.2)
# 告别段落用的长淡出
define fade_slow = Dissolve(1.6)

# ============================================================
# 场景 / 情绪引擎
# ------------------------------------------------------------
# 目的：让背景和立绘表情跟着「当前剧情 + 聊天内容」走，而不是写死一张脸。
#
# 三层信息来源，优先级从高到低：
#   1) 剧本显式指定（show awan hurt）—— 编剧意图，永远最优先
#   2) 模型在回复末尾附带的 [mood:xxx] 标签
#   3) 本地推断：玩家说了什么 + 她怎么回 + 好感/吵架状态
#
# 背景同理：地点关键词 → 场景名的映射表，改这张表就能改整个游戏的空间感，
# 不需要翻剧本逐句改 scene 语句。
# ============================================================

default awan_emotion = "calm"      # 聊天界面当前表情
default chat_scene = "sea_dusk"    # 当前聊天背景
default chat_scene_vote = ""       # 场景切换投票（避免一句话就闪背景）
default chat_scene_vote_n = 0


init -6 python:

    # ---------------- 表情 ----------------
    MOOD_STATES = ["calm", "shy", "happy", "lonely", "hurt", "fading",
                   "surprised", "smile", "cry",
                   "sulk", "angry", "laugh", "blush", "think", "sigh",
                   "fear", "sleepy", "firm", "wry", "tease",
                   "wave", "giggle", "uneasy", "point", "cry_silent",
                   "teary_smile", "shock", "pout", "doze", "shiver",
                   "resolve", "farewell", "lean", "wind"]

    MOOD_LABELS = {
        "calm": "平静",
        "shy": "害羞",
        "happy": "开心",
        "lonely": "落寞",
        "hurt": "委屈",
        "fading": "含泪将散",
        "surprised": "愣住",
        "smile": "温柔",
        "cry": "哭",
        "sulk": "赌气",
        "angry": "生气",
        "laugh": "笑出声",
        "blush": "脸红",
        "think": "思索",
        "sigh": "无奈",
        "fear": "慌张",
        "sleepy": "困倦",
        "firm": "坚定",
        "wry": "苦笑",
        "tease": "促狭",
        "wave": "招手",
        "giggle": "掩嘴笑",
        "uneasy": "不安",
        "point": "指点",
        "cry_silent": "无声落泪",
        "teary_smile": "含泪微笑",
        "shock": "震惊",
        "pout": "鼓脸",
        "doze": "犯困",
        "shiver": "发抖",
        "resolve": "决意",
        "farewell": "道别",
        "lean": "凑近",
        "wind": "风里",
    }

    # 玩家说的话里出现这些词，就往某个情绪上加分
    PLAYER_MOOD_SIGNALS = [
        ("hurt", 3, ["滚", "烦死", "闭嘴", "讨厌你", "不喜欢你", "别来找我", "受够了"]),
        ("hurt", 2, ["骗我", "瞒着", "撒谎", "为什么不说", "你到底", "是不是在骗"]),
        ("lonely", 2, ["走了", "要离开", "不来了", "再见", "最后一次", "来不及", "留不住"]),
        ("shy", 3, ["喜欢你", "想你", "好看", "可爱", "漂亮", "抱", "牵", "等我"]),
        ("happy", 2, ["一起", "陪你", "带你去", "明天见", "下次", "我请"]),
        ("shy", 2, ["对不起", "抱歉", "我错了", "是我不好"]),
        ("surprised", 3, ["其实我", "我要走", "我早知道", "秘密", "你猜", "我发现"]),
        ("cry", 3, ["不回来", "最后一天", "永远见不到", "别忘了我"]),
        ("smile", 2, ["等你", "记得", "一直在", "陪着你"]),
        ("angry", 2, ["你怎么这样", "太过分", "说好", "明明答应"]),
        ("sulk", 2, ["哼", "才不理你", "随便你", "不要了"]),
        ("blush", 2, ["喜欢你", "牵你", "抱一下", "好看", "可爱"]),
        ("laugh", 2, ["哈哈", "笑死", "好呆", "你真好玩"]),
        ("sigh", 1, ["又来了", "算了", "没办法", "总之"]),
        ("fear", 2, ["台风", "落水", "危险", "别过去", "快跑"]),
        ("sleepy", 1, ["困", "好晚", "睡了", "明天再说"]),
        ("firm", 2, ["我会回来", "一定", "相信我", "不会忘"]),
        ("tease", 1, ["你猜", "才不告诉你", "看出来了"]),
    ]

    # 她的回复里出现这些词，也影响表情
    REPLY_MOOD_SIGNALS = [
        ("hurt", 2, ["不想说", "别问", "算了", "随便", "你别"]),
        ("lonely", 2, ["不知道", "大概", "也许", "以后", "总有一天", "反正"]),
        ("shy", 2, ["讨厌", "才不", "别说了", "……你"]),
        ("happy", 2, ["好呀", "真的", "那好", "嘿嘿", "嗯！", "哈哈"]),
    ]

    def _apply_mood_signals(text, table, acc):
        for mood, weight, words in table:
            for w in words:
                if w in (text or ""):
                    acc[mood] = acc.get(mood, 0) + weight
                    break
        return acc

    def baseline_mood():
        """没有任何文本信号时的默认表情，由状态决定。"""
        if store.quarrel_severity >= 1:
            return "hurt"
        if store.affection >= 90:
            return "happy"
        if store.affection >= 60:
            return "happy"
        if store.affection >= 30:
            return "shy"
        return "calm"

    def infer_mood(player_text="", reply="", tag=""):
        """综合判断她此刻的表情。tag 来自模型，不合法就忽略。"""
        if tag in MOOD_STATES:
            return tag

        scores = {}
        _apply_mood_signals(player_text, PLAYER_MOOD_SIGNALS, scores)
        _apply_mood_signals(reply, REPLY_MOOD_SIGNALS, scores)

        if store.quarrel_severity >= 2:
            scores["hurt"] = scores.get("hurt", 0) + 3
        elif store.quarrel_severity == 1:
            scores["hurt"] = scores.get("hurt", 0) + 1

        if store.affection >= 90:
            scores["happy"] = scores.get("happy", 0) + 2
            scores["shy"] = scores.get("shy", 0) + 1
        elif store.affection >= 60:
            scores["happy"] = scores.get("happy", 0) + 1
        elif store.affection < 30:
            scores["calm"] = scores.get("calm", 0) + 1

        if not scores:
            return baseline_mood()
        return max(scores, key=scores.get)

    def mood_label(state=None):
        return MOOD_LABELS.get(state or store.awan_emotion, "平静")

    def sprite_name(state=None):
        """给 show / add 用的 image 名。"""
        return "awan " + (state or store.awan_emotion)

    # ---------------- 场景 ----------------
    # 关键词 → 背景名。越具体越靠前，先命中先算。
    SCENE_KEYWORDS = [
        ("festival_night", ["渔火", "灯会", "纸灯", "放灯", "灯笼"]),
        ("ferris_wheel", ["摩天轮", "座舱"]),
        ("night_market", ["夜市", "摊位", "小吃街", "烤"]),
        ("dessert_shop", ["糖水", "甜品", "双皮奶", "绿豆沙"]),
        ("bookstore", ["书店", "书架", "书脊"]),
        ("record_store", ["唱片", "磁带", "随身听"]),
        ("riverside", ["江边", "江面", "大桥", "跨江"]),
        ("bus_stop", ["车站", "小巴", "末班", "候车", "站牌"]),
        ("mailbox", ["信箱", "邮筒", "寄信", "信封"]),
        ("room", ["房间", "屋里", "台灯", "泡面", "枕头", "窗台", "床"]),
        ("town_day", ["早市", "镇上", "街口", "巷子", "菜市场"]),
        # 海景的时间变体：信号越具体越靠前，剩下的都归到黄昏
        ("sea_dawn", ["天亮", "拂晓", "黎明", "日出", "天快亮"]),
        ("sea_morning", ["上午", "早上", "清晨的海", "太阳刚出来"]),
        ("sea_noon", ["正午", "中午", "大太阳", "晒得"]),
        ("sea_storm", ["台风", "风暴", "巨浪", "风眼"]),
        ("sea_rain", ["下雨", "雨幕", "淋雨", "雨还没停"]),
        ("sea_afterrain", ["雨后", "彩虹", "放晴", "云隙"]),
        ("sea_overcast", ["阴天", "乌云", "灰蒙蒙", "天阴"]),
        ("sea_sunset", ["夕阳", "落日", "火烧云", "太阳往下掉"]),
        ("sea_moon", ["月亮", "月夜", "月光", "满月"]),
        ("sea_night", ["夜海", "海面很黑的夜", "堤岸上没有灯"]),
        ("sea_dusk", ["海边", "堤岸", "沙滩", "日落", "海风", "浪", "礁石"]),
    ]

    SCENE_NAMES = [name for name, _ in SCENE_KEYWORDS] + ["bus_window", "black", "white"]

    BG_FALLBACK = {
        "sea_dusk": "#233246",
        "sea_dawn": "#3a4252",
        "sea_morning": "#3f5264",
        "sea_noon": "#5a6a72",
        "sea_overcast": "#3c4148",
        "sea_rain": "#333b44",
        "sea_storm": "#2b2a34",
        "sea_afterrain": "#4a5560",
        "sea_sunset": "#4a3428",
        "sea_night": "#151d2c",
        "sea_moon": "#1b2436",
        "bus_window": "#2a3448",
        "dessert_shop": "#3a2f2a",
        "night_market": "#2e2438",
        "bookstore": "#332b22",
        "ferris_wheel": "#1f2c3d",
        "riverside": "#1c2a36",
        "record_store": "#2b2622",
        "bus_stop": "#151b26",
        "mailbox": "#2a2f38",
        "town_day": "#3b3a33",
        "room": "#2a2622",
        "festival_night": "#241d2e",
        "black": "#000000",
        "white": "#ffffff",
    }

    def scene_for_text(text, fallback=None):
        for scene, words in SCENE_KEYWORDS:
            for w in words:
                if w in (text or ""):
                    return scene
        return fallback

    def sync_scene_from_stage():
        """进入聊天前，先按当前剧情地点定一格背景。"""
        found = scene_for_text(store.stage_info)
        if found:
            store.chat_scene = found
        store.chat_scene_vote = ""
        store.chat_scene_vote_n = 0
        try:
            sync_chat_audio()
        except Exception:
            pass

    def note_chat_scene(text):
        """聊天里连续两轮提到同一个地点才切背景，避免一句话就闪。"""
        cand = scene_for_text(text)
        if not cand or cand == store.chat_scene:
            store.chat_scene_vote = ""
            store.chat_scene_vote_n = 0
            return
        if cand == store.chat_scene_vote:
            store.chat_scene_vote_n += 1
        else:
            store.chat_scene_vote = cand
            store.chat_scene_vote_n = 1
        if store.chat_scene_vote_n >= 2:
            store.chat_scene = cand
            store.chat_scene_vote = ""
            store.chat_scene_vote_n = 0
            try:
                sync_chat_audio()
            except Exception:
                pass

    def _cover_image(path):
        """等比放大后居中裁切，铺满屏幕，不变形。"""
        try:
            bw, bh = renpy.image_size(path)
            sw, sh = config.screen_width, config.screen_height
            k = max(sw / float(bw), sh / float(bh))
            return Transform(path, xysize=(int(bw * k), int(bh * k)), xalign=0.5, yalign=0.5)
        except Exception:
            return Transform(path, xysize=(config.screen_width, config.screen_height))

    def _find_image(folder, name):
        """按 webp / jpg / png 的顺序找图，压缩过也不影响加载。"""
        for ext in (".webp", ".jpg", ".png"):
            path = "%s/%s%s" % (folder, name, ext)
            if renpy.loadable(path):
                return path
        return None

    def find_audio(name):
        """音频同理：放哪个格式都行，缺失就跳过，不报错。"""
        for ext in (".ogg", ".opus", ".mp3", ".wav"):
            path = "audio/%s%s" % (name, ext)
            if renpy.loadable(path):
                return path
        return None

    def play_ending_music():
        """片尾曲：优先用 audio/ending_music，没有就用内置的 bgm_ending。"""
        track = find_audio("ending_music") or find_audio("bgm_ending")
        if track:
            renpy.music.play(track, channel="music", fadein=4.0, fadeout=4.0,
                             loop=True, if_changed=True)
            try:
                stop_amb(4.0)
            except Exception:
                pass
        return track

    def bg_displayable(name):
        """有正式图就用图，没有就退回纯色占位，不会白屏。"""
        path = _find_image("images/bg", name)
        if path:
            return _cover_image(path)
        return Solid(BG_FALLBACK.get(name, "#22232a"))

    def cg_displayable(name):
        """CG 放 images/cg/，同样的铺满逻辑。"""
        path = _find_image("images/cg", name)
        if path:
            return _cover_image(path)
        return Solid("#111318")

    CG_LIST = [
        "cg_first_meet",
        "cg_rain",
        "cg_typhoon",
        "cg_typhoon_eye",
        "cg_lantern",
        "cg_river",
        "sunset_sea",
    ]

    def chat_bg_displayable():
        return bg_displayable(store.chat_scene)


# ---------------- 立绘尺寸 ----------------
init -1 python:
    # 立绘统一按 2:3 出图（推荐 1024x1536），这里缩到屏幕内的高度
    SPRITE_W, SPRITE_H = 400, 560

    def awan_sprite(state, fallback_color, label, alpha=1.0):
        """有正式立绘就用 images/awan/awan_<state>.png，否则用占位色块。

        按高度等比缩放：三张立绘尺寸略有出入也不会被拉变形，
        脚底线和头顶线自动对齐。
        """
        path = _find_image("images/awan", "awan_" + state)
        if not path:
            # 没有单独表情图就复用平静态：宁可同一张脸，也不要换脸跳戏
            path = _find_image("images/awan", "awan_calm")
        if path:
            try:
                iw, ih = renpy.image_size(path)
                zoom = SPRITE_H / float(ih)
            except Exception:
                zoom = SPRITE_H / 1536.0
            d = Transform(path, zoom=zoom, xanchor=0.5, yanchor=1.0)
            if alpha < 1.0:
                d = Transform(d, alpha=alpha)
            return d
        return awan_stand(label, fallback_color, alpha)

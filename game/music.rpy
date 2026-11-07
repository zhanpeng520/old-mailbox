# ============================================================
# 音乐 / 音效
# ------------------------------------------------------------
# 设计原则：不改剧本。用 config.scene_callbacks 监听 scene 语句，
# 从「当前背景」反推该放哪首 BGM，再叠加环境音（海浪 / 雨 / 风）。
#
# 所以编剧写 scene bg sea_storm，音乐自动变紧张；
# 写 scene bg sea_rain，自动变伤感 + 雨声。不用逐句 play music。
# ============================================================

init -4 python:

    # ---------- 混音通道 ----------
    # ambient 走 sfx 混音器，玩家在设置里调「音效」就能关掉环境音
    renpy.music.register_channel("ambient", mixer="sfx", loop=True, tight=True)

    # ---------- 场景 → BGM ----------
    SCENE_BGM = {
        # 海
        "sea_dusk": "bgm_sea",
        "sea_dawn": "bgm_sea",
        "sea_morning": "bgm_warm",
        "sea_noon": "bgm_light",
        "sea_overcast": "bgm_sad",
        "sea_rain": "bgm_sad",
        "sea_storm": "bgm_tense",
        "sea_afterrain": "bgm_ending",
        "sea_sunset": "bgm_ending",
        "sea_night": "bgm_night",
        "sea_moon": "bgm_night",
        # 城里
        "bus_window": "bgm_warm",
        "bus_stop": "bgm_night",
        "town_day": "bgm_light",
        "dessert_shop": "bgm_warm",
        "night_market": "bgm_light",
        "bookstore": "bgm_letter",
        "record_store": "bgm_letter",
        "ferris_wheel": "bgm_night",
        "riverside": "bgm_night",
        "festival_night": "bgm_light",
        "mailbox": "bgm_letter",
        "room": "bgm_letter",
    }

    # ---------- CG → BGM ----------
    CG_BGM = {
        "cg_first_meet": "bgm_ending",
        "cg_rain": "bgm_warm",
        "cg_typhoon": "bgm_tense",
        "cg_typhoon_eye": "bgm_tense",
        "cg_lantern": "bgm_night",
        "cg_river": "bgm_night",
        "sunset_sea": "bgm_ending",
    }

    # ---------- 场景 → 环境音 ----------
    SCENE_AMB = {
        "sea_dusk": "sfx_waves",
        "sea_dawn": "sfx_waves",
        "sea_morning": "sfx_waves",
        "sea_noon": "sfx_waves",
        "sea_overcast": "sfx_wind",
        "sea_sunset": "sfx_waves",
        "sea_night": "sfx_waves",
        "sea_moon": "sfx_waves",
        "sea_rain": "sfx_rain",
        "sea_storm": "sfx_wind",
        "riverside": "sfx_waves",
        "bus_stop": "sfx_wind",
        "mailbox": "sfx_waves",
        "ferris_wheel": "sfx_wind",
    }

    def _audio(name):
        """带缓存的路径查找：没有文件就返回 None，不报错。"""
        if not name:
            return None
        cache = getattr(store, "_audio_cache", None)
        if cache is None:
            cache = store._audio_cache = {}
        if name not in cache:
            cache[name] = find_audio(name)
        return cache[name]

    def play_bgm(name, fade=2.5):
        """换 BGM：同曲不重播，切歌时交叉淡入淡出。"""
        path = _audio(name)
        if not path:
            return
        if renpy.music.get_playing("music") == path:
            return
        renpy.music.play(path, channel="music", fadein=fade, fadeout=fade, loop=True)

    def play_amb(name, fade=3.5):
        path = _audio(name)
        if not path:
            return
        if renpy.music.get_playing("ambient") == path:
            return
        renpy.music.play(path, channel="ambient", fadein=fade, fadeout=fade, loop=True)

    def stop_amb(fade=3.0):
        renpy.music.stop(channel="ambient", fadeout=fade)

    def play_sfx(name):
        path = _audio(name)
        if path:
            renpy.sound.play(path, channel="sound")

    # 读信时的翻纸声：连着念很多行时，隔一行响一次就够
    _letter_page = {"n": 0}

    def letter_sound(event, interact=True, **kwargs):
        if event != "show_done" or not interact:
            return
        _letter_page["n"] += 1
        if _letter_page["n"] % 2 == 1:
            play_sfx("sfx_page")

    # ---------- 从当前画面反推音乐 ----------
    def _visual_now(layer="master"):
        """返回当前的主视觉名：背景取属性名，CG 取 tag。"""
        try:
            tags = renpy.get_showing_tags(layer, sort=True)
        except Exception:
            return None
        for tag in tags:
            if tag == "bg":
                try:
                    attrs = renpy.get_attributes("bg", layer)
                except Exception:
                    attrs = None
                if attrs:
                    return attrs[0]
            elif tag in CG_BGM:
                return tag
        return None

    def _bgm_for_visual(vis):
        if not vis:
            return None
        if vis in CG_BGM:
            return CG_BGM[vis]
        if vis in ("black", "white"):
            return None
        track = SCENE_BGM.get(vis)
        # 吵架越重，海边的曲子越沉
        if getattr(store, "quarrel_severity", 0) >= 2 and track in (
                "bgm_sea", "bgm_ending", "bgm_warm", "bgm_night"):
            track = "bgm_sad"
        return track

    def sync_scene_audio(layer="master"):
        """scene 语句执行后调用：对齐 BGM 与环境音。"""
        vis = _visual_now(layer)
        if not vis or vis in ("black", "white"):
            return
        play_bgm(_bgm_for_visual(vis))
        amb = SCENE_AMB.get(vis)
        if amb:
            play_amb(amb)
        else:
            stop_amb()
        if vis == "sea_storm":
            play_sfx("sfx_thunder")

    def _scene_audio_callback(layer="master"):
        sync_scene_audio(layer)

    if _scene_audio_callback not in config.scene_callbacks:
        config.scene_callbacks.append(_scene_audio_callback)

    def _resume_audio_callback():
        """读档 / 从菜单回来时音乐通道是空的，这里补一次。
        正在播放就完全不动，避免和聊天页的配乐抢。"""
        try:
            if renpy.music.get_playing("music"):
                return
        except Exception:
            return
        sync_scene_audio("master")

    if _resume_audio_callback not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_resume_audio_callback)


# ---------- 聊天界面的背景也跟着换 ----------
init -3 python:

    def sync_chat_audio():
        """聊天页背景切换时同步换 BGM（聊天是 screen，不触发 scene 回调）。"""
        vis = getattr(store, "chat_scene", None) or "sea_dusk"
        play_bgm(_bgm_for_visual(vis), fade=2.0)
        amb = SCENE_AMB.get(vis)
        if amb:
            play_amb(amb)
        else:
            stop_amb()


# ---------- 按钮音效 ----------
init 100 python:
    for _st in (style.button, style.navigation_button, style.quick_button,
                style.choice_button, style.slot_button):
        try:
            _st.activate_sound = "audio/sfx_click.ogg"
        except Exception:
            pass

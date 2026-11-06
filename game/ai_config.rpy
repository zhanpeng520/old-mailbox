# ============================================================
# AI 聊天配置
# ------------------------------------------------------------
# 密钥不进代码、不进存档、不进发布包：
#   1) 桌面 / 安卓：读 game/ai_config.json（本地私有文件，随 .gitignore 忽略）
#   2) Web 版：只读 game/ai_web_config.json（不含密钥，强制 proxy 中转）
#   3) 其次读环境变量 AWAN_API_KEY / AWAN_API_URL / AWAN_MODEL
#   4) 都没有 → ai_is_configured() 为 False，AI 入口自动隐藏，主线照常可玩
# ============================================================

init -10 python:
    import os
    import json
    import random

    # 默认接 OpenAI 兼容网关（可换成任意兼容服务）
    # mode:
    #   direct —— 客户端直连模型网关，api_key 必须写在本地配置里（只适合自己玩）
    #   proxy  —— 客户端只连自己的中转服务，密钥留在服务器（上线 / 小游戏必须用这个）
    AI_CONFIG = {
        "mode": "direct",
        "api_url": "https://aigw.telecomjs.com/v1/chat/completions",
        "api_key": "",
        "proxy_token": "",          # proxy 模式下的弱校验口令，留空则不校验
        "tracking_id": "",          # 部分网关要求的调用方标识，可留空
        "reasoning": "",            # off / low / high / max：off 关闭思考链，闲聊更便宜
        "allow_web_key": False,     # 显式允许在网页包里直连（key 会公开，仅自用/小范围分享）
        "model": "qwen3.6-plus",
        "temperature": 0.9,
        "top_p": 0.95,
        "presence_penalty": 0.3,
        "frequency_penalty": 0.4,
        "max_tokens": 400,
        "timeout": 30,
        "turn_limit": 300,          # 每局硬上限（发送 + 重说共用），正常玩到不了
        "thrift_after": 120,        # 超过这次数转「省电模式」：历史减半、回复更短，但对话不断
        "history_char_budget": 1600,  # 发给模型的历史对话总字符预算
    }

    def _ai_is_web():
        """Web 版没有 socket、也不支持 threading，只能 fetch 走中转。"""
        return bool(getattr(renpy, "emscripten", False))

    def _ai_load_config():
        cfg = dict(AI_CONFIG)
        # Web 包是公开可下载的，只认不含密钥的 ai_web_config.json
        name = "ai_web_config.json" if _ai_is_web() else "ai_config.json"

        fp = None
        try:
            fp = renpy.open_file(name, "utf-8")   # 归档内 / 磁盘都能读
        except Exception:
            path = os.path.join(config.gamedir, name)
            if os.path.exists(path):
                try:
                    fp = open(path, "r", encoding="utf-8")
                except Exception:
                    fp = None

        loaded = fp is not None
        if loaded:
            try:
                data = json.load(fp)
                for key in cfg:
                    if key in data and data[key] not in (None, ""):
                        cfg[key] = data[key]
            except Exception as exc:
                renpy.log("[ai] 读取 %s 失败：%s" % (name, exc))
            finally:
                fp.close()

        cfg["api_key"] = os.environ.get("AWAN_API_KEY", cfg.get("api_key", ""))
        cfg["api_url"] = os.environ.get("AWAN_API_URL", cfg.get("api_url", ""))
        cfg["model"] = os.environ.get("AWAN_MODEL", cfg.get("model", ""))

        if _ai_is_web():
            # 默认强制中转；只有显式 allow_web_key 才允许浏览器直连（key 会随包公开）
            direct_ok = (
                bool(cfg.get("allow_web_key"))
                and str(cfg.get("mode", "")).strip().lower() == "direct"
            )
            if not direct_ok:
                cfg["mode"] = "proxy"
                cfg["api_key"] = ""
            if not loaded:
                cfg["api_url"] = ""
        return cfg

    AI_CONFIG = _ai_load_config()

    def ai_is_proxy():
        return str(AI_CONFIG.get("mode", "direct")).strip().lower() == "proxy"

    def ai_player_id():
        """每台设备一个匿名 ID：服务端用它做每日额度，不涉及个人信息。"""
        pid = getattr(persistent, "ai_player_id", "") or ""
        if not pid:
            pid = "%08x%08x" % (random.getrandbits(32), random.getrandbits(32))
            persistent.ai_player_id = pid
        return pid

    def ai_is_configured():
        """地址齐了就算可用；direct 模式还必须有密钥，proxy 模式交给服务端。"""
        if not AI_CONFIG.get("api_url"):
            return False
        if ai_is_proxy():
            return True
        return bool(AI_CONFIG.get("api_key"))

    def ai_status_text():
        if not ai_is_configured():
            return "未配置模型"
        if not store.ai_online:
            return "离线"
        return "在线"

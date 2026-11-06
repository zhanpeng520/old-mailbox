# ============================================================
# AI 桥接：HTTP 请求 + 后台线程 + 离线兜底
# ------------------------------------------------------------
# 设计要点：
#   - 桌面 / 安卓：标准库 urllib + 后台线程，不额外装依赖，界面不卡；
#   - Web 版：浏览器没有 socket 也没有 threading，改用 renpy.fetch 同步请求；
#   - 返回后 restart_interaction 刷新；
#   - 任何异常都只提示、不抛错，绝不影响主线推进。
# ============================================================

init -8 python:
    import json
    import time

    # Web (Emscripten) 里没有 _ssl / socket，这里必须容错，
    # 否则整个游戏在浏览器里会直接崩在 import 上。
    try:
        import ssl
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError, URLError
    except ImportError:
        ssl = None
        Request = None
        urlopen = None
        # 用内置 OSError 顶替，保证 `except URLError` 不会在运行时炸掉
        HTTPError = OSError
        URLError = OSError

    def _ai_open(req, timeout):
        """带证书回退的 urlopen。

        公司代理 / 杀毒软件常用自签根证书做 SSL 拦截，Ren'Py 自带的 CA 库
        不认它，会直接抛 CERTIFICATE_VERIFY_FAILED。这种情况下退回不校验
        的上下文再发一次，保证聊天能通（仅影响本机到模型网关的这一跳）。
        """
        if urlopen is None:
            raise OSError("当前环境不支持 urllib（Web 版请走 renpy.fetch）")

        try:
            return urlopen(req, timeout=timeout)
        except URLError as exc:
            reason = getattr(exc, "reason", exc)
            text = str(reason)
            if "CERTIFICATE_VERIFY_FAILED" in text or isinstance(reason, ssl.SSLError):
                renpy.log("[ai] 证书链不被信任，改用宽松校验重试")
                return urlopen(req, timeout=timeout, context=ssl._create_unverified_context())
            raise

    def _ai_chat_url():
        url = (AI_CONFIG.get("api_url") or "").strip()
        if url.endswith("/chat/completions"):
            return url
        return url.rstrip("/") + "/chat/completions"

    def _ai_models_url():
        base = _ai_chat_url()
        return base[: -len("/chat/completions")] + "/models"

    def _ai_headers():
        headers = {"Content-Type": "application/json"}
        tracking = str(AI_CONFIG.get("tracking_id", "") or "").strip()
        if tracking:
            headers["X-Tracking-Id"] = tracking
        if ai_is_proxy():
            # 只带匿名设备号与弱口令，真实密钥不出服务器
            headers["X-Player-Id"] = ai_player_id()
            token = AI_CONFIG.get("proxy_token") or ""
            if token:
                headers["X-Client-Token"] = token
        else:
            headers["Authorization"] = "Bearer " + AI_CONFIG.get("api_key", "")
        return headers

    def _ai_post(payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = Request(_ai_chat_url(), data=data, headers=_ai_headers())
        with _ai_open(req, int(AI_CONFIG.get("timeout", 30))) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _ai_request(payload):
        """唯一的出网入口：Web 用 renpy.fetch，其他平台用 urllib。"""
        if _ai_is_web():
            return renpy.fetch(
                _ai_chat_url(),
                json=payload,
                headers=_ai_headers(),
                timeout=int(AI_CONFIG.get("timeout", 30)),
                result="json",
            )
        return _ai_post(payload)

    def _ai_dispatch():
        """Web 不能开线程，只能当场同步发（DeepSeek 实测 0.2~0.3 秒）。"""
        if _ai_is_web():
            ai_request_worker()
        else:
            renpy.invoke_in_thread(ai_request_worker)

    def _ai_extract_text(data):
        """兼容 content 为字符串 / 内容块数组两种返回形态。"""
        try:
            message = data["choices"][0]["message"]
        except (KeyError, IndexError, TypeError):
            return ""
        content = message.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(str(block.get("text", "")))
            return "".join(parts).strip()
        return ""

    def ai_probe_online():
        """启动探活：网关可达即视为在线（/models 不支持也不算离线）。"""
        if not ai_is_configured():
            store.ai_online = False
            return
        if ai_is_proxy():
            # 中转服务不实现 /models，直接放行，省掉一次开机请求
            store.ai_online = True
            return

        def worker():
            try:
                req = Request(_ai_models_url(), headers=_ai_headers())
                with _ai_open(req, 6) as resp:
                    resp.read()
                store.ai_online = True
            except HTTPError:
                # 能拿到 HTTP 状态码说明网络是通的，只是端点不被支持
                store.ai_online = True
            except Exception:
                store.ai_online = False
            finally:
                renpy.restart_interaction()

        renpy.invoke_in_thread(worker)

    def ai_turn_limit():
        """每局硬上限（保底闸门，正常游玩到不了）。"""
        try:
            return max(0, int(AI_CONFIG.get("turn_limit", 300)))
        except (TypeError, ValueError):
            return 300

    def ai_thrift_after():
        """超过这个次数进入省电模式：对话不中断，只是每次更便宜。"""
        try:
            return max(0, int(AI_CONFIG.get("thrift_after", 120)))
        except (TypeError, ValueError):
            return 120

    def ai_is_thrifty():
        return store.ai_turn_count >= ai_thrift_after()

    def ai_turns_left():
        return max(0, ai_turn_limit() - store.ai_turn_count)

    def ai_max_tokens():
        """省电模式下把回复长度压一半，60 字以内照样够说话。"""
        try:
            cap = int(AI_CONFIG.get("max_tokens", 400))
        except (TypeError, ValueError):
            cap = 400
        return min(cap, 240) if ai_is_thrifty() else cap

    def ai_history_messages():
        """双重截断：条数上限 + 字符预算，保证最近一轮一定带上。"""
        try:
            budget = max(200, int(AI_CONFIG.get("history_char_budget", 1600)))
        except (TypeError, ValueError):
            budget = 1600
        if ai_is_thrifty():
            budget = max(400, budget // 2)

        picked = []
        used = 0
        for item in reversed(store.ai_messages[-AI_MAX_TURNS:]):
            cost = len(item.get("content", "")) + 8
            if picked and used + cost > budget:
                break
            picked.append(item)
            used += cost
        picked.reverse()

        # 只留到最后一轮 user 为止，避免「她刚说完就重说」带半截上下文
        while picked and picked[-1]["role"] != "user":
            picked.pop()
        return picked

    def ai_send():
        """界面「发送」按钮：先入列，再丢后台线程请求。"""
        text = (store.ai_input or "").strip()[:300]
        text = text.replace("{", "｛").replace("}", "｝")
        if not text or store.ai_pending:
            return

        # 敷衍 / 复读 / 纯标点：本地接住，不产生请求，也不计入上限
        quick = ai_quick_reply(text)
        if quick:
            store.ai_input = ""
            store.ai_error = ""
            store.ai_messages.append({"role": "user", "content": text})
            store.ai_messages.append({"role": "assistant", "content": quick})
            store.awan_emotion = infer_mood(text, quick, "")
            note_chat_scene(text)
            renpy.restart_interaction()
            return

        if not ai_is_configured():
            store.ai_error = "还没有配置模型密钥（game/ai_config.json）"
            return
        if store.ai_turn_count >= ai_turn_limit():
            # 不是报错，是她自己把话收住，保持沉浸
            store.ai_input = ""
            store.ai_messages.append({"role": "user", "content": text})
            ai_close_chat()
            renpy.restart_interaction()
            return

        store.ai_input = ""
        store.ai_error = ""
        store.ai_messages.append({"role": "user", "content": text})

        # 她一听到这句话就有反应：表情先动，回复再慢慢回来
        store.awan_emotion = infer_mood(text, "", "")
        note_chat_scene(text)

        store.ai_pending = True
        store.ai_turn_count += 1
        renpy.restart_interaction()
        _ai_dispatch()

    def ai_request_worker():
        try:
            messages = [{"role": "system", "content": build_awan_system_prompt()}]
            last_user = ""
            for item in ai_history_messages():
                if item["role"] == "user":
                    last_user = item["content"]
                messages.append({"role": item["role"], "content": item["content"]})

            # 运行时防剧透守卫：玩家在追问核心秘密
            if last_user and ai_guard_triggered(last_user):
                messages.insert(1, {"role": "system", "content": AWAN_GUARD_PROMPT})

            payload = {
                "model": AI_CONFIG.get("model"),
                "messages": messages,
                "temperature": float(AI_CONFIG.get("temperature", 0.9)),
                "top_p": float(AI_CONFIG.get("top_p", 0.95)),
                "presence_penalty": float(AI_CONFIG.get("presence_penalty", 0.3)),
                "frequency_penalty": float(AI_CONFIG.get("frequency_penalty", 0.4)),
                "max_tokens": ai_max_tokens(),
                "stream": False,
            }

            # 闲聊不需要思考链：关掉后输出 token 少一半以上、延迟也低
            reasoning = str(AI_CONFIG.get("reasoning", "")).strip().lower()
            if reasoning == "off":
                payload["thinking"] = {"type": "disabled"}
            elif reasoning in ("low", "high", "max"):
                payload["reasoning_effort"] = reasoning

            data = _ai_request(payload)

            reply = _ai_extract_text(data)
            if not reply:
                reply = "（她张了张嘴，最后什么也没说。）"

            # 剥出情绪标记，台词保持干净；标记缺失时由本地规则推断
            reply, mood_tag = ai_split_mood(reply)
            if not reply:
                reply = "（她张了张嘴，最后什么也没说。）"
            store.awan_emotion = infer_mood(last_user, reply, mood_tag)

            # 像真人一样，让「正在想」多停留一会儿（Web 阻塞主线程，跳过）
            if not _ai_is_web():
                time.sleep(0.45 + min(1.2, len(reply) * 0.015))

            store.ai_messages.append({"role": "assistant", "content": ai_sanitize_reply(reply)})
            # 存档里只保留最近 200 条，避免越聊越大
            if len(store.ai_messages) > 200:
                store.ai_messages = store.ai_messages[-200:]
            store.ai_online = True
        except HTTPError as exc:
            if exc.code == 429:
                store.ai_error = "今天已经聊得够多了，改天再来找她吧。"
            elif ai_is_proxy():
                store.ai_error = "中转服务暂时不可用（HTTP %d），先继续主线吧。" % exc.code
            else:
                store.ai_error = "请求被拒绝（HTTP %d），检查密钥与模型名是否正确。" % exc.code
        except URLError:
            store.ai_online = False
            store.ai_error = "连不上舒瑶……网络好像断了，主线仍可继续。"
        except Exception as exc:
            store.ai_online = False
            if _ai_is_web():
                store.ai_error = "连不上舒瑶……中转服务没开跨域？主线仍可继续。"
            else:
                store.ai_error = "出了点问题（%s），先继续主线吧。" % exc.__class__.__name__
        finally:
            store.ai_pending = False
            renpy.restart_interaction()

    def ai_chat_ready():
        """随时聊天入口是否可用：配置齐全，且不在吵架/真相/结局。

        不断言在线：网络抖动时仍然保留入口，让玩家在聊天框里看到具体错误。
        """
        return bool(store.ai_unlocked) and bool(store.ai_free_chat) and ai_is_configured()

    def ai_chat_visible():
        """右上角按钮是否该显示：入口可用，且不在聊天/主菜单/存读档界面。"""
        if not ai_chat_ready():
            return False
        for name in ("ai_chat_screen", "main_menu", "game_menu"):
            if renpy.get_screen(name) is not None:
                return False
        return True

    def ai_open_chat():
        """进入聊天：先把背景对齐到当前剧情地点，再定一个基线表情。"""
        store.ai_error = ""
        sync_scene_from_stage()
        store.awan_emotion = baseline_mood()
        if not store.ai_messages:
            store.ai_messages.append({"role": "assistant", "content": ai_opening_line()})

    def ai_regenerate():
        """把她最后一句撤回，重新生成一次。"""
        if store.ai_pending or not store.ai_messages:
            return
        if store.ai_turn_count >= ai_turn_limit():
            store.ai_error = "……她今天不想再说了，改天吧。"
            renpy.restart_interaction()
            return
        while store.ai_messages and store.ai_messages[-1]["role"] == "assistant":
            store.ai_messages.pop()
        if not store.ai_messages or store.ai_messages[-1]["role"] != "user":
            store.ai_error = "还没有可以重说的一句。"
            renpy.restart_interaction()
            return
        store.ai_error = ""
        store.ai_pending = True
        store.ai_turn_count += 1
        renpy.restart_interaction()
        _ai_dispatch()

    def ai_reset_chat():
        store.ai_messages = []
        store.ai_input = ""
        store.ai_error = ""
        store.ai_pending = False


# 读档后清掉瞬态状态：若存档时正在等 AI 回复，读回来会一直卡在「正在想……」
init 10 python:

    def _ai_after_load():
        store.ai_pending = False
        store.ai_error = ""
        store.ai_input = ""
        # 老存档没有 ai_unlocked：已经推进过剧情就视为早就认识了
        if not store.ai_unlocked and (store.affection > 0 or store.current_day > 1):
            store.ai_unlocked = True

    if _ai_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_ai_after_load)

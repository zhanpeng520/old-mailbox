# ============================================================
# AI 聊天界面
# ------------------------------------------------------------
# 两种进入方式：
#   1) 剧情独处节点：call screen ai_chat_screen（free_mode=False）
#   2) 右上角常驻按钮：随时 Show 同一个界面（free_mode=True）
# 吵架 / 真相 / 结局段落会把 ai_free_chat 关掉，按钮自动消失。
# 未认识舒瑶之前（ai_unlocked 为 False）也不会出现入口。
# ============================================================

style ai_bubble is frame:
    padding (18, 12)
    xmaximum 480
    background Frame("ui/panel_glass.png", Borders(24, 24, 24, 24), tile=False)

style ai_bubble_text is text:
    size 21
    line_spacing 5
    color "#f2ece4"

style ai_input is input:
    size 21
    color "#f5efe8"


init python:
    # 常驻 HUD：比 show screen 更稳，读档后也不会丢
    if "ai_chat_button" not in config.overlay_screens:
        config.overlay_screens.append("ai_chat_button")


# 右上角常驻入口：配置好、在线、且不在关键剧情时显示
screen ai_chat_button():
    zorder 40

    if ai_chat_visible():
        frame:
            xalign 0.985
            yalign 0.025
            padding (16, 8)
            background Frame("ui/panel_glass.png", Borders(30, 30, 30, 30))

            textbutton "和舒瑶说说话":
                action [Function(ai_open_chat), Show("ai_chat_screen", free_mode=True)]
                text_size 17
                text_color "#efe1d9"
                text_hover_color "#e6b98a"


screen ai_chat_screen(free_mode=False):
    modal True
    zorder 200

    # 离开聊天界面时一定要把浏览器输入框收掉，否则它会残留在剧情画面上
    on "hide" action Function(web_ime_hide)
    on "replace" action Function(web_ime_hide)

    # screen 内先算好文案，避免在文本插值里调用函数
    $ mood_text = mood_label()
    $ subtitle = ("自由聊天 | 她看起来" + mood_text) if free_mode else ("她在这里，看起来" + mood_text + "。")
    $ turns_left = ai_turns_left()
    $ left_hint = (" | 还能聊 %d 句" % turns_left) if turns_left <= 15 else ""
    $ status_line = "第 %d 天 | 好感 %d | %s | %s%s" % (current_day, affection, ai_relation_label(), ai_status_text(), left_hint)
    # 表情由 scene_mood.rpy 推断：她刚说的那句话决定她现在的样子
    $ portrait = sprite_name()

    # Web 端：轮询浏览器原生输入框，接住中文输入法的内容
    if renpy.emscripten:
        timer 0.35 repeat True action Function(web_ime_sync)

    # 背景跟着当前所在地点走，看得见但不抢戏
    add chat_bg_displayable()
    add Solid("#070b1190")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 690
        padding (28, 22)
        background Frame("ui/panel_glass.png", Borders(30, 30, 30, 30), tile=False)

        vbox:
            spacing 10

            # 标题栏
            hbox:
                spacing 14
                add portrait xysize (96, 120)
                vbox:
                    spacing 3
                    text "舒瑶" size 28 color "#f5efe8"
                    text subtitle size 17 color "#e6b98a"
                    text status_line size 15 color "#9aa5ae"

            # 分隔线
            add "ui/hairline.png" xpos 2 ypos 2

            # 对话历史
            frame:
                xsize 744
                ysize 372
                padding (12, 12)
                background Frame("ui/panel_soft.png", Borders(24, 24, 24, 24), tile=False)

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 1.0

                    vbox:
                        spacing 10
                        for m in ai_messages:
                            frame:
                                style "ai_bubble"
                                xalign (1.0 if m["role"] == "user" else 0.0)
                                background (Solid("#e6b98a") if m["role"] == "user" else Frame("ui/panel_glass.png", Borders(24, 24, 24, 24), tile=False))
                                text m["content"] style "ai_bubble_text" color ("#3f2f24" if m["role"] == "user" else "#f2ece4")

                        if ai_pending:
                            text "舒瑶正在想……" size 17 color "#9aa5ae"

            # 输入行
            if renpy.emscripten:
                textbutton "⌨ 用中文输入法（回车发送）":
                    action Function(web_ime_open)
                    text_size 16
                    text_color "#9fb3c4"
                    text_hover_color "#e6b98a"

            hbox:
                spacing 10

                frame:
                    xsize 590
                    ysize 54
                    padding (16, 14)
                    background Frame("ui/panel_soft.png", Borders(24, 24, 24, 24), tile=False)
                    input value VariableInputValue("ai_input") length 200 style "ai_input"

                textbutton "发送":
                    action Function(ai_send)
                    sensitive (not ai_pending)
                    text_size 20
                    text_color "#e6b98a"
                    text_hover_color "#f2d7b8"

            # 状态与退出
            hbox:
                spacing 18

                textbutton "结束聊天":
                    action (Hide("ai_chat_screen") if free_mode else Return())
                    text_size 19
                    text_color "#c9d2dc"
                    text_hover_color "#e6b98a"

                textbutton "让她重说一次":
                    action Function(ai_regenerate)
                    sensitive (not ai_pending and len(ai_messages) > 0 and ai_messages[-1]["role"] == "assistant")
                    text_size 17
                    text_color "#9aa5ae"
                    text_hover_color "#e6b98a"

                if ai_error:
                    text ai_error size 16 color "#e8927f" xmaximum 430

    key "K_ESCAPE" action (Hide("ai_chat_screen") if free_mode else Return())


# 在独处节点调用：有配置且在线才给入口，否则静默跳过
label ai_optional_chat:
    if not ai_chat_enable:
        return
    if not ai_is_configured():
        return
    if not ai_online:
        return

    $ ai_open_chat()
    menu:
        "想和她说说话。":
            call screen ai_chat_screen
        "就这样安静地待一会儿。":
            pass
    return

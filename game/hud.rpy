# ============================================================
# 常驻状态条（左上角：好感 / 回忆碎片）
# ------------------------------------------------------------
# 只在正文里出现，主菜单和存档界面不挡视线。
# 好感条的量程是 100（好结局门槛），超过就满格并变色。
# ============================================================

default show_hud = True


style hud_bar:
    left_bar Solid("#e6b98a")
    right_bar Solid("#ffffff1f")
    thumb None
    ysize 6


screen aff_hud():
    zorder 200

    if show_hud and not main_menu:
        frame:
            background Frame("ui/panel_glass.png", 14, 14)
            xpos 58
            ypos 8
            padding (14, 6, 14, 6)

            hbox:
                spacing 12

                text "好感" size 20 color "#c8ae92" yalign 0.5
                bar value StaticValue(affection, AFFECTION_TRUE_END) style "hud_bar" xsize 104 ysize 7 yalign 0.5
                text "[affection]" size 22 color ("#ffd9a0" if affection >= AFFECTION_TRUE_END else "#f2d6b0") yalign 0.5

                null width 6

                text "碎片" size 19 color "#c8ae92" yalign 0.5
                text "[memory_piece]/[MEMORY_TOTAL]" size 19 color ("#ffd9a0" if memory_piece >= MEMORY_TOTAL else "#f2d6b0") yalign 0.5


init python:
    if "aff_hud" not in config.overlay_screens:
        config.overlay_screens.append("aff_hud")

# ============================================================
# 视觉主题：暮色 · 旧信箱
# ------------------------------------------------------------
# 素材在 game/ui/（暮色渐变背景 / 毛玻璃面板 / 圆角按钮 / 金色名字标签）。
# 本文件只覆盖外观样式，不动任何交互与剧情逻辑。
# 加载顺序在 screens.rpy 之后，同名样式按属性合并覆盖。
# ============================================================

# ---------- 主菜单 ----------
style main_menu_frame:
    background None

style main_menu_title:
    size gui.scale(62)
    color "#f5efe8"

style main_menu_subtitle is main_menu_text:
    size gui.scale(15)
    color "#e6b98a"
    kerning 3.0

style main_menu_version:
    size gui.scale(17)
    color "#c9d2dc"

# ---------- 导航按钮（主菜单 + 各菜单页左侧） ----------
style navigation_button:
    background None
    hover_background Frame("ui/btn_idle.png", Borders(20, 20, 20, 20), tile=False)
    padding (gui.scale(18), gui.scale(7))

style navigation_button_text:
    size gui.scale(24)
    color "#e8e2da"
    hover_color "#e6b98a"
    selected_color "#e6b98a"
    insensitive_color "#7c8894"

# ---------- 对话框：全宽贴底、顶部圆角的毛玻璃卡片 ----------
style window:
    xfill True
    yalign 1.0
    ysize gui.scale(170)
    background Frame("ui/panel_glass_top.png", Borders(30, 30, 30, 0), tile=False)
    padding (gui.scale(60), gui.scale(22))

style namebox:
    xpos gui.scale(64)
    xanchor 0.0
    ypos gui.scale(-18)
    xsize None
    ysize gui.scale(44)
    background Frame("ui/namebox.png", Borders(32, 22, 32, 22), tile=False)
    padding (gui.scale(24), gui.scale(4))

style say_label:
    color "#4a382c"
    size gui.scale(22)
    xalign 0.0
    yalign 0.5

style say_dialogue:
    color "#f5efe8"
    size gui.scale(23)
    line_spacing gui.scale(8)
    xpos gui.scale(60)
    ypos gui.scale(44)
    xsize gui.scale(1160)

# ---------- 选项卡片 ----------
style choice_vbox:
    xalign 0.5
    ypos gui.scale(300)
    yanchor 0.5
    spacing gui.scale(14)

style choice_button:
    xsize gui.scale(780)
    background Frame("ui/panel_glass.png", Borders(30, 30, 30, 30), tile=False)
    hover_background Frame("ui/btn_hover.png", Borders(20, 20, 20, 20), tile=False)
    padding (gui.scale(30), gui.scale(14))

style choice_button_text:
    xalign 0.5
    text_align 0.5
    size gui.scale(24)
    color "#f5efe8"
    hover_color "#3a2f2a"
    insensitive_color "#8a93a0"

# ---------- 快捷菜单：嵌在对话框顶部右侧的一行小字 ----------
style quick_menu:
    xalign 1.0
    xoffset gui.scale(-56)
    ypos gui.scale(560)

style quick_button:
    background None
    hover_background None
    padding (gui.scale(6), gui.scale(2))

style quick_button_text:
    size gui.scale(15)
    color "#c3ccd8"
    hover_color "#e6b98a"
    selected_color "#e6b98a"

# ---------- 菜单页（读档 / 设置 / 历史 / 关于） ----------
style game_menu_outer_frame:
    background Solid("#0d142080")

style game_menu_label_text:
    size gui.scale(44)
    color "#e6b98a"

style slot_button:
    background Frame("ui/slot_idle.png", Borders(22, 22, 22, 22), tile=False)
    hover_background Frame("ui/slot_hover.png", Borders(22, 22, 22, 22), tile=False)
    padding (gui.scale(12), gui.scale(12))

style slot_time_text:
    size gui.scale(16)
    color "#e8e2da"

style slot_name_text:
    size gui.scale(16)
    color "#c9d2dc"

style page_label_text:
    color "#e8e2da"

style page_button_text:
    color "#c9d2dc"
    hover_color "#e6b98a"

# ---------- 设置页按钮 ----------
style radio_button:
    background Frame("ui/btn_idle.png", Borders(20, 20, 20, 20), tile=False)
    hover_background Frame("ui/btn_hover.png", Borders(20, 20, 20, 20), tile=False)
    padding (gui.scale(20), gui.scale(8))

style radio_button_text:
    color "#e8e2da"
    hover_color "#3a2f2a"
    selected_color "#e6b98a"

style check_button:
    background Frame("ui/btn_idle.png", Borders(20, 20, 20, 20), tile=False)
    hover_background Frame("ui/btn_hover.png", Borders(20, 20, 20, 20), tile=False)
    padding (gui.scale(20), gui.scale(8))

style check_button_text:
    color "#e8e2da"
    hover_color "#3a2f2a"
    selected_color "#e6b98a"

style pref_label_text:
    color "#e6b98a"

# ---------- 滚动条 / 滑条 ----------
style bar:
    ysize gui.scale(14)
    left_bar Frame("ui/bar_fill.png", Borders(8, 8, 8, 8), tile=False)
    right_bar Frame("ui/bar_track.png", Borders(8, 8, 8, 8), tile=False)

style vbar:
    xsize gui.scale(14)
    top_bar Frame("ui/vbar_fill.png", Borders(8, 8, 8, 8), tile=False)
    bottom_bar Frame("ui/vbar_track.png", Borders(8, 8, 8, 8), tile=False)

style slider:
    ysize gui.scale(30)
    base_bar Frame("ui/bar_track.png", Borders(8, 8, 8, 8), xalign=0.5, yalign=0.5, tile=False)
    thumb "ui/slider_thumb.png"
    thumb_offset gui.scale(8)

style vslider:
    xsize gui.scale(30)
    base_bar Frame("ui/vbar_track.png", Borders(8, 8, 8, 8), xalign=0.5, yalign=0.5, tile=False)
    thumb "ui/slider_thumb.png"
    thumb_offset gui.scale(8)

style scrollbar:
    base_bar Frame("ui/bar_track.png", Borders(8, 8, 8, 8), tile=False)
    thumb Frame("ui/scroll_thumb.png", Borders(8, 8, 8, 8), tile=False)

style vscrollbar:
    base_bar Frame("ui/vbar_track.png", Borders(8, 8, 8, 8), tile=False)
    thumb Frame("ui/scroll_thumb.png", Borders(8, 8, 8, 8), tile=False)

# ---------- 确认弹窗 / 提示条 ----------
style confirm_frame:
    background Frame("ui/panel_paper.png", Borders(32, 32, 32, 32), tile=False)
    padding (gui.scale(48), gui.scale(34))

style confirm_prompt_text:
    color "#3a2f2a"
    size gui.scale(26)

style confirm_button:
    background Frame("ui/panel_glass.png", Borders(30, 30, 30, 30), tile=False)
    hover_background Frame("ui/btn_hover.png", Borders(20, 20, 20, 20), tile=False)
    padding (gui.scale(26), gui.scale(10))

style confirm_button_text:
    color "#f5efe8"
    hover_color "#3a2f2a"
    size gui.scale(24)
    xalign 0.5

style notify_frame:
    background Frame("ui/panel_glass.png", Borders(30, 30, 30, 30), tile=False)
    padding (gui.scale(28), gui.scale(12))

style notify_text:
    color "#f5efe8"
    size gui.scale(20)

style skip_frame:
    background Frame("ui/panel_glass.png", Borders(30, 30, 30, 30), tile=False)

style skip_text:
    color "#f5efe8"

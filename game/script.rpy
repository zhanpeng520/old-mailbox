# ============================================================
# 《旧信箱里的拾信者》· 主入口与序章
# 结构：序章 → 第一天（海边）→ 第二 / 四天（城市）
#       → 第三 / 五 / 六天（小镇日常）→ 第七天（江边）→ 结局
# ------------------------------------------------------------
# 玩法提示（写进游戏内的说明，不依赖外部文档）：
#   - 好感 affection 决定结局走向
#   - 吵架烈度 quarrel_severity 影响第七天台词与结局
#   - 回忆碎片 memory_piece 集满 7 片才满足隐藏好结局条件
#   - AI 自由聊天只在独处节点出现，吵架/真相/结局强制关闭
# ============================================================

label start:
    # 每局重置（default 变量会随新游戏初始化，这里只做显式兜底）
    $ affection = 0
    $ quarrel_severity = 0
    $ memory_piece = 0
    $ ai_chat_enable = False
    $ ai_free_chat = True
    $ ai_unlocked = False
    $ visited_places = []
    $ unlocked_sides = []
    $ free_roam_used = 0
    $ truth_known = False
    $ current_day = 1
    $ current_stage = "第一幕"
    $ stage_info = "海边初遇，傍晚的堤岸"
    $ ai_messages = []
    $ ai_error = ""
    $ ai_pending = False
    $ ai_turn_count = 0

    # 启动探活：无网络时 AI 入口自动隐藏，主线不受影响
    $ ai_probe_online()

    # 右上角「和舒瑶说说话」由 config.overlay_screens 常驻显示

    scene bg black
    with fade

    # BGM 注释：此处应播「海边留白 · 缓慢钢琴」，素材缺失时保持静音
    # play music "audio/theme_sea.ogg" fadein 2.0

    "我在这座城市上班，做着一份说不上喜欢的工作。"
    "每天挤地铁、改方案、在会议室里点头。"
    "只有周末，我会坐那趟一小时一班的旧小巴，回到海边的镇子。"
    "镇子尽头有一段废弃的堤岸，堤岸上立着一只绿色的旧信箱。"
    "信箱早就没有邮差了。可我还是习惯往里面塞信。"
    "写给一个，我等了很多年的人。"

    if persistent.new_game_plus:
        # 二周目专属独白：玩家已经知道结局，语气更沉
        "——这一次，我知道自己会走到哪里。"
        "所以我想走得慢一点。"
        me "（如果早知道结局，人还会不会开始？）"

    scene bg sea_dusk
    with slow_scene
    "那天傍晚，海面像一块被压暗的玻璃。"
    "我照旧走到堤岸，却发现信箱旁边站着一个人。"

    show awan calm at awan_center
    with dissolve

    "她穿着一件洗得发白的裙子，赤着脚，站在潮湿的石阶上。"
    "风把她的头发吹起来，她却像没感觉似的，一直看着海。"

    awan "……你也来看海？"

    me "（她转过头的时候，我愣了一下。）"
    me "（不是因为她好看，而是因为——这张脸，我好像在哪里见过。）"

    me "嗯。这儿的海，比城里安静。"

    show awan shy at awan_center
    with dissolve

    awan "安静是安静。就是有点太安静了，安静得像……被谁按下了暂停。"

    if persistent.new_game_plus:
        me "（这句话，我上一次也听过。上一次我没有接住。）"

    me "你住在这附近？"

    show awan calm at awan_center
    with dissolve

    awan "算是吧。"
    awan "我在这儿待了很久了。"

    "她说“很久”的时候，语气轻得像在说别人的事。"

    jump act1_start

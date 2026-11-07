# ============================================================
# 第一幕 · 海边初遇
# ------------------------------------------------------------
# 前置可选支线：捡贝壳 / 躲阵雨 / 听渔船故事（最多做 2 个）
# 目标：建立「她只能在海边」的隐线，并完成进城邀约
# ============================================================

default beach_done = []

label act1_start:
    $ current_stage = "第一幕 · 海边"
    $ stage_info = "海边初遇，刚知道她叫舒瑶"

    me "你叫什么？"

    show awan shy at awan_center
    with dissolve

    awan "……安舒瑶。"
    awan "舒服的舒，瑶光的瑶。"

    # 到这儿才算正式认识，右上角的随时聊天从这一刻起才出现
    $ ai_unlocked = True

    me "舒瑶。"

    "我念了一遍，觉得这两个字有点烫。"

    show awan giggle at awan_center
    with dissolve

    awan "你呢？"

    me "胡云砚。"

    awan "胡云砚。"

    awan "……听起来像会在信里写很长句子的人。"

    me "（我笑了一下。）"
    me "你说得挺准。"

    "海风把她的裙角吹得鼓起来。她低下头，用脚尖蹭了蹭石阶上的水。"

    awan "你每个周末都来？"

    me "嗯。往信箱里塞信。"

    show awan shy at awan_center
    with dissolve

    awan "写给谁？"

    me "……一个等不到回信的人。"

    "她没有追问。只是安静地看着我，眼神里有一种我说不清的东西。"
    "像是理解，又像是歉意。"

    jump act1_choose


label act1_choose:
    $ current_stage = "第一幕 · 海边"
    $ stage_info = "在堤岸陪舒瑶，天色还没全暗"

    if len(beach_done) >= 2:
        jump act1_invite

    menu:
        "陪她沿着堤岸捡贝壳。" if "shells" not in beach_done:
            $ beach_done.append("shells")
            call side_beach_shells
            jump act1_choose

        "天上落了几滴雨，找地方躲一躲。" if "rain" not in beach_done:
            $ beach_done.append("rain")
            call side_beach_rain
            jump act1_choose

        "去听堤岸那头渔船上的老人讲故事。" if "boat" not in beach_done:
            $ beach_done.append("boat")
            call side_beach_boat
            jump act1_choose

        "什么都不做，只是陪她站着。":
            me "（我什么都没说。）"
            "我们并肩站着，看太阳一点一点沉进海里。"
            "她的影子被拉得很长，长到几乎要碰到我的鞋尖。"
            $ affection += 3
            jump act1_invite


# ---------- 支线：捡贝壳 ----------
label side_beach_shells:
    $ affection += 5

    me "要不要捡点贝壳？"

    show awan happy at awan_center
    with dissolve

    awan "……可以吗？"

    me "海边的东西，捡了也不算偷。"

    "她蹲下去，很认真地挑。挑了半天，捡起一枚白色的、薄得能透光的扇贝。"

    awan "这个。"

    me "那么小。"

    awan "小的才好。"
    awan "小的，不会被人抢走。"

    "她把贝壳放进我手心，指尖很凉。"

    show awan shy at awan_center
    with dissolve

    awan "你拿着。"
    awan "……等以后我不在了，你看到它，就当我还站在这儿。"

    me "什么叫你不在了？"

    show awan calm at awan_center
    with dissolve

    awan "随口说的。"
    awan "海边的人说话都这样，你别当真。"

    me "（她说得太快了，快得像在补一个漏。）"

    $ ai_chat_enable = True
    call ai_optional_chat
    $ ai_chat_enable = False

    return


# ---------- 支线：躲阵雨 ----------
label side_beach_rain:
    $ affection += 5

    scene bg sea_overcast
    with fade_scene

    "雨来得没道理。前一秒还是黄昏，下一秒就砸下来。"

    me "那边有个废弃的售票亭！"

    scene cg_rain
    with slow_scene

    "我们挤在窄窄的屋檐下。她的肩膀贴着我的手臂，隔着湿掉的衣料，能感觉到凉。"
    "屋檐很窄，雨顺着边沿连成一道线，把外面隔成另一个世界。"
    "檐下有一盏没人管的旧灯，光是暖的，把她的头发照成很浅的白。"

    scene bg sea_rain
    with dissolve

    show awan uneasy at awan_center
    with dissolve

    awan "……你不觉得奇怪吗？"

    me "什么奇怪？"

    awan "雨落到我身上的时候，好像……比落到你身上轻一点。"

    "我低头看她的手臂。雨水顺着她的皮肤滑下去，没有留下水痕。"

    me "（大概是光线的问题。）"
    me "你淋傻了。"

    show awan think at awan_center
    with dissolve

    awan "嗯。大概是吧。"

    "她把脸转开，看着雨幕，很久没说话。"

    $ ai_chat_enable = True
    call ai_optional_chat
    $ ai_chat_enable = False

    return


# ---------- 支线：渔船故事 ----------
label side_beach_boat:
    $ affection += 4

    "堤岸尽头停着一条旧渔船，船头坐着个补网的老人。"

    "老人看见我们，眯着眼笑。"

    old_man "小姑娘又来啦。"
    old_man "你等的那个人，今年也没来？"

    show awan hurt at awan_center
    with dissolve

    awan "……今年还没到日子。"

    me "（她等谁？）"

    "老人摇摇头，继续补网。"

    old_man "海边的人啊，等得久了，就容易把自己也等成一片海。"

    "回去的路上，我问她那句话是什么意思。"

    show awan calm at awan_center
    with dissolve

    awan "老人年纪大了，说话乱七八糟的。"

    me "你等的人，很重要吗？"

    awan "……"
    awan "以前觉得重要。"
    awan "现在觉得，来不来都行。"

    "她说这话的时候，眼睛一直看着海，没有看我。"

    return


# ---------- 邀约 ----------
label act1_invite:
    $ current_stage = "第一天 · 日落"
    $ stage_info = "第一天傍晚，和舒瑶一起看海"

    scene bg sea_dusk
    with slow_scene

    "太阳开始往下掉的时候，海先变了颜色。"
    "先是蓝，后来是青，再后来，整片海面像被人从底下点着，一层一层亮起来。"

    scene cg_first_meet
    with slow_scene

    "我们并排站着，谁也没先开口。"
    "海把最后的光整片摊开，一直铺到我们脚边。"
    "她的影子比我的短一截，边上镶着一圈橘色。"

    scene bg sea_sunset
    with dissolve

    show awan uneasy at awan_center
    with dissolve

    "她坐下来，把脚悬在堤岸外面。"
    "我也坐下，隔着半臂的距离。"

    awan "你看。"

    "她抬手指过去。"
    "海平线上有一条很窄的金线，正一点一点往我们这边推。"

    me "每天都这样？"

    awan "不是每天。"

    awan "要没有云，风又要对。"

    awan "一年里，也遇不上几次。"

    "她说这话的时候，眼睛一直看着海。"
    "夕阳落在她脸上，把她的睫毛照成浅金色。"

    "我忽然觉得，这个傍晚应该被记住。"
    "不是用手机拍下来那种，是很多年以后闭上眼还能看见的那种。"

    "海鸥从我们头顶掠过去，翅膀尖沾了一点橘色。"

    menu:
        "陪她坐到太阳完全沉下去。":
            $ add_affection(5)

            "我没有看时间。"
            "太阳一点一点被海吞掉，最后只剩一条线。"

            show awan happy at awan_center
            with dissolve

            awan "你以前看过吗。"

            me "看过。"

            me "一个人看。"

            awan "一个人看，是什么感觉。"

            me "像在等一件不会发生的事。"

            "她沉默了一会儿，把头轻轻靠在我肩上。"

            awan "那今天不算。"

            me "什么不算。"

            awan "今天不是一个人。"

            "天彻底暗下来之前，海是紫的。"
            "我记住了那个颜色。"

        "怕天黑了不好走，提议看到这里就好。":
            $ add_affection(2)

            me "天快黑了。"

            me "看到这儿，差不多该走了。"

            awan "……嗯。"

            "她站起来，拍了拍裙子上的沙。"

            "太阳还剩最后一点。"
            "她走了几步，又回头看了一眼海。"

            awan "有点可惜。"

            me "明天还有。"

            awan "嗯。"

            awan "明天还有。"

            "她说得很轻。"
            "轻得像我欠了她一个傍晚。"

    show awan farewell at awan_center
    with dissolve

    "天色彻底暗下来的时候，我该走了。"

    me "我明天要回城里。"

    awan "嗯。"

    me "……你要不要一起？"

    show awan shock at awan_center
    with dissolve

    awan "一起？"

    me "就去一天。糖水铺、夜市，随便走走。"

    "她愣了很久，久到我以为她会拒绝。"

    show awan giggle at awan_center
    with dissolve

    awan "我可以吗？"

    me "为什么不可以。"

    awan "……"
    awan "没什么。"

    "她笑起来的时候，眼睛弯成很小的一条缝，像终于被允许做一件想了很久的事。"

    awan "那，明天见。"

    me "明天见。"

    "我走了几步，回头。她还站在原地，冲我挥手。"

    if persistent.new_game_plus:
        me "（上一次，我没有回头。）"
        me "（这一次我回头了，她还在。）"

    scene bg black
    with fade

    "那一晚我睡得很浅。"
    "梦里全是海的声音。"

    jump act1_bus


# ---------- 小巴 ----------
label act1_bus:
    scene bg bus_window
    with slow_scene

    # BGM 注释：小巴段用「摇晃的吉他分解和弦」，音量压低
    # play music "audio/bus_ride.ogg" fadein 1.0

    "第二天的旧小巴，一小时一班。她准时站在站牌下。"

    show awan happy at awan_center
    with dissolve

    awan "我从来没坐过这个。"

    me "很破的。别抱太大期待。"

    awan "破也好。"

    "车开起来，她一直贴着车窗看。"

    "看电线杆一根根退后，看海慢慢被楼房挡住，看天从蓝变成灰。"

    show awan calm at awan_center
    with dissolve

    awan "原来海会不见。"

    me "什么？"

    awan "没什么。"

    "车过隧道的时候，光暗下来。我下意识地去看她。"

    "那一瞬间，她的轮廓好像淡了一下，像一张被水泡过的照片。"

    "灯再亮起来的时候，她又好好的了。"

    me "（……车太晃了吧。）"

    "她把手贴在车窗上，很久都没有放下。"

    awan "云砚。"

    me "嗯？"

    awan "谢谢你带我出来。"

    awan "不管今天怎么样，我都谢谢。"

    "我不知道她为什么要说得像告别。"

    "车到站了。"

    $ current_day = 2

    scene bg black
    with fade
    centered "{size=64}第二天{/size}\n\n{size=26}城市、糖水，和她没见过的灯{/size}"

    jump act2_start

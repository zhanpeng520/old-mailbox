# ============================================================
# 第三幕 · 江边
# ------------------------------------------------------------
# 吵架烈度 quarrel_severity 在此累积（0 轻微 / 1 中等 / 2 重度），
# 不同烈度走不同台词，并影响最终结局。
# 本幕起：AI 聊天全程关闭（不让模型打乱情绪）。
# ============================================================

label act3_start:
    $ current_day = 7
    $ current_stage = "第七天 · 江边"
    $ stage_info = "第七天，江边，心里全是说不通的地方"
    $ ai_chat_enable = False
    $ ai_free_chat = False

    $ visit_place("江边")

    scene bg riverside
    with fade_scene

    # BGM 注释：此处停掉所有旋律，只留风声与环境噪声
    # stop music fadeout 2.0

    "第七天傍晚，我们又进了城。"
    "从车站出来，我们沿着江边走了很久。"

    scene cg_river
    with slow_scene

    "江面很平。远处的大桥排列着一整排灯，像有人把一把尺子横在河上。"
    "她的头发被路灯照得发白，风一吹，边缘就淡下去一点。"

    "我盯着她的轮廓看，看得太久了。"

    scene bg riverside
    with dissolve

    "她一直在说话，说早市、说台风夜的蜡烛、说书店里那本诗集。"

    "可我一个字都没听进去。"

    "我脑子里全是这七天说不通的地方。"

    "店员不看她。售票员不撕第二张票。小孩从她身上穿过去。照片里没有她。她的手会变淡。她说她没有「活下去」这个选项。"

    show awan calm at awan_center
    with dissolve

    awan "云砚？你在听吗？"

    me "舒瑶。"

    awan "嗯？"

    menu:
        "直接问她：你是不是有事瞒着我。":
            $ raise_quarrel(1)
            me "你是不是有事瞒着我。"

            "她的脚步停住了。"

            show awan hurt at awan_center
            with dissolve

            awan "……你为什么这么问。"

            me "这七天，太多地方不对了。"
            me "那些人不是没看见你，是根本看不见你。"

            awan "云砚，你别乱想。"

        "先陪她把这段路走完。":
            me "……没事。"
            me "风有点大。"

            "她看了我一会儿，把手伸过来，想挽我的胳膊。"

            "我下意识地躲了一下。"

            show awan hurt at awan_center
            with dissolve

            "她的手停在半空中，慢慢收了回去。"

            awan "哦。"

            $ raise_quarrel(1)

    "江面上有一艘货船，灯很慢地移过去。"

    show awan lonely at awan_center
    with dissolve

    awan "云砚，我们回去吧。"

    me "你先回答我一个问题。"

    awan "……"

    menu:
        "你到底是谁？":
            $ raise_quarrel(2)
            me "你到底是谁？"

            "她抬起头，眼睛在灯下很亮。"

            awan "我是舒瑶。"

            me "舒瑶是谁？"
            me "你说你在这儿待了很久，多久？你家在哪？你父母呢？你为什么从来不说？"

            "我的声音越来越大。江风把话吹散，又吹回来。"

            awan "云砚，你别这样。"

            me "我别这样？"
            me "我像个傻子一样，带一个连名字都说不清的人逛了一整天。"

            show awan hurt at awan_center
            with dissolve

            awan "不是的……"

            me "那你告诉我啊！"

            "我吼出来的时候，江边有几个路人回过头。"

            "他们看的是我。只有我。"

            awan "……"

        "算了，当我没问。":
            $ raise_quarrel(1)
            me "……算了。"
            me "当我没问。"

            show awan hurt at awan_center
            with dissolve

            awan "你明明很在意。"

            me "我说了算了。"

            awan "云砚。"
            awan "你这样，比骂我还难受。"

            "她低下头，眼泪掉在江边的石栏上，没有留下痕迹。"

    # ---------- 吵架高潮：按烈度分台词 ----------
    if quarrel_severity >= 2:
        me "我真后悔今天带你出来。"

        show awan fading at awan_center
        with dissolve

        awan "……"

        me "我早该发现的。你根本不是——"

        "我没能把那句话说完。"

        "因为她的脸开始变淡。从嘴唇开始，像被水慢慢冲开。"

        awan "云砚。"

        me "舒瑶？"

        awan "别说了。"
        awan "求你。"

        "她的声音已经很远了。"

    elif quarrel_severity == 1:
        me "我只是想知道真相，这很过分吗？"

        show awan hurt at awan_center
        with dissolve

        awan "不过分。"

        me "那你为什么不说？"

        awan "因为说出来，就真的结束了。"

        me "什么结束？"

        "她没有回答。"

        show awan fading at awan_center
        with dissolve

        "江风忽然变大。她的裙角被吹起来，透过那层薄薄的布料，能看见后面的栏杆。"

        awan "云砚，风好大。"

        awan "我有点站不住了。"

    else:
        me "……对不起。"

        show awan hurt at awan_center
        with dissolve

        awan "你为什么要道歉？"

        me "我不知道。"
        me "我就是觉得，我好像一直在逼你。"

        awan "云砚。"

        "她朝我走了一步，又停住。"

        show awan fading at awan_center
        with dissolve

        awan "太晚了。"

        me "什么太晚了？"

        awan "江边的风，比海边的硬。"

    # ---------- 消散 ----------
    show awan fading at awan_center
    with dissolve

    "她抬起手，像是想碰我的脸。"

    "可那只手在半路上就淡了下去，只剩一点轮廓。"

    awan "云砚。"

    me "我在。"

    awan "今天谢谢你。"
    awan "……真的。"

    hide awan
    with fade_slow

    "江边只剩下风。"

    "我伸手去抓，什么也没抓到。"

    "栏杆上有一小片水痕，很快就干了。"

    scene bg black
    with fade

    if persistent.new_game_plus:
        "——这个画面，我在上一次也见过。"
        "只是上一次，我没有跑起来。"

    jump act3_truth


# ============================================================
# 真相：旧信箱里的信
# ============================================================
label act3_truth:
    $ current_stage = "第三幕 · 真相"
    $ stage_info = "已经知道真相，正在海边读信"
    $ truth_known = True

    # 「他还是回来了」计入好感：完美路线需要这 +10 才能摸到 100
    # （旧版是道歉选项 +10，这里改成真相后自动加的固定值，便于结算）
    $ add_affection(10)

    scene bg mailbox
    with slow_scene

    # BGM 注释：单人钢琴，极慢，留白多
    # play music "audio/letter_theme.ogg" fadein 2.0

    "我不知道自己是怎么回到海边的。"

    "等我回过神，人已经站在那只绿色的旧信箱前。"

    "信箱里塞得满满的。"

    "不是我写的那些信。"
    "是别的。一叠，用细麻绳捆着，纸边已经泛黄。"

    letter "「给那个总往信箱里塞信的男生。」"

    "我手抖得厉害，解了三次才解开那根绳子。"

    letter "「你大概不记得我了。」"
    letter "「十二年前，海边修堤岸，我掉进过水里。」"
    letter "「有个穿蓝色外套的男生跳下来，把我推上岸。」"

    "这一行的下面，字迹洇开了一小片，像被水泡过。"

    letter "「他们说你没上来。」"
    letter "「我信了很多年。」"

    "蓝色的外套。"
    "我衣柜最里面，确实挂着一件旧的蓝色外套。"
    "我一直以为那是父亲的。"

    letter "「后来海告诉我，你上来了。」"
    letter "「你只是把那天忘了。」"

    "我摸了摸自己的胸口。"
    "十二年前那个夏天，我一点都想不起来。"
    "我只记得，从那以后，我再没下过水。"

    letter "「我一直没有醒。」"
    letter "「医生说我躺在镇上的病房里，躺了十二年。」"
    letter "「可我还在这儿。海说，只要没有人认出我，我就能一直在这儿。」"
    letter "「我在海边等你，等到自己也不再长大。」"

    "信纸下面还有一张。"

    letter "「今年你终于看见我了。」"
    letter "「我很高兴，也很害怕。」"
    letter "「因为被看见，就意味着要选一个结局。」"

    "我坐在堤岸上，坐到天快亮。"

    "海面很平。远处有早班的渔船，机器声一下一下。"

    "我想起她在糖水铺吃东西时小心翼翼的样子。"
    "想起她在摩天轮上说「让我靠一会儿」。"
    "想起她问「如果我明天不在了，你会不会找我」。"

    "我当时回答「会」。"

    "可我连她是谁都没问清，就先怀疑了她。"

    scene bg sea_dawn
    with slow_scene

    "天亮的时候，她出现了。"

    show awan fading at awan_center
    with dissolve

    "她比昨晚更淡了，像一张反复曝光的照片。"

    awan "你还是来了。"

    me "……舒瑶。"

    awan "你看到信了。"

    me "嗯。"

    "我想说很多话，可一句也说不出来。"

    awan "云砚，你不用觉得对不起我。"
    awan "那些年是我自己要等的。"

    me "可是我刚才——"

    awan "我知道。"
    awan "你只是想知道真相。这没有错。"

    "她笑了一下，很轻。"

    awan "现在你知道了。"

    me "……我在信里，看到你了。"

    awan "嗯。"

    awan "海只肯放一个人走。"

    me "什么意思。"

    awan "要么我回去，要么你留下来。"

    awan "要么，我们两个都被它忘掉。"

    "她说得很轻，像在念一段早就背熟的台词。"

    me "那你想哪一种。"

    awan "我想你活着。"

    awan "可我更想……你记得我。"

    jump act3_choice


# ============================================================
# 最终选择
# ------------------------------------------------------------
# 三个常规选项 = 三个常规结局；
# 第四项为隐藏项，条件不满足时不会出现在菜单里。
#   好感 >= 60、吵架烈度 < 2、回忆碎片集齐 7 片
# ============================================================
label act3_choice:
    $ stage_info = "在海边，必须做出最后的决定"

    menu:
        "跳进海里，抓住她的手，再也不放开。":
            jump ending_path_sea

        "告诉自己这一切都是幻觉，转身离开。":
            jump ending_path_deny

        "留下来，好好跟她告一次别。":
            jump ending_path_farewell

        "把七片回忆，连同十二年的信，一起还给她。" if (affection >= AFFECTION_TRUE_END and quarrel_severity < 2 and memory_piece >= MEMORY_TOTAL):
            jump ending_path_true

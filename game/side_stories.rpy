# ============================================================
# 城市支线（自由闲逛随机解锁）
# ------------------------------------------------------------
# 7 个地点各一条支线，一次只能解锁一部分，剩下的留给二周目。
# 抽取策略：优先抽「主线去不到、只能在自由闲逛里补」的三个地点
#          （江边 / 音像店 / 公交站台），保证 3 次闲逛正好集齐 7 片回忆。
# ============================================================

init -5 python:
    SIDE_PLACE = {
        "side_dessert_shop": "糖水铺",
        "side_night_market": "夜市",
        "side_bookstore": "书店",
        "side_ferris_wheel": "摩天轮",
        "side_riverside": "江边",
        "side_record_store": "音像店",
        "side_bus_stop": "公交站台",
    }

    # 主线不会经过、只能靠自由闲逛补碎片的地点
    SIDE_ONLY = ["side_riverside", "side_record_store", "side_bus_stop"]

    def pick_side_story():
        pool = [name for name in SIDE_STORIES if name not in store.unlocked_sides]
        if not pool:
            return None
        fresh = [name for name in pool if SIDE_PLACE.get(name) not in store.visited_places]
        side_only = [name for name in fresh if name in SIDE_ONLY]
        return renpy.random.choice(side_only or fresh or pool)


label side_story_pick:
    $ chosen = pick_side_story()
    if not chosen:
        "（这条街能走的地方，我们都走过了。）"
        return
    $ unlocked_sides.append(chosen)
    $ renpy.call(chosen)
    return


# ---------- 糖水铺（二次） ----------
label side_dessert_shop:
    $ stage_info = "又回到糖水铺，这次店里没别的客人"
    scene bg dessert_shop
    with fade_scene

    $ visit_place("糖水铺")

    "快打烊了，老板娘在擦桌子。"

    show awan blush at awan_center
    with dissolve

    awan "又是这里。"

    me "你好像很喜欢。"

    awan "嗯。"
    awan "这里的热气，让人觉得时间在动。"

    menu:
        "再点一份双皮奶。":
            $ add_affection(4)
            "老板娘端上来的时候，多放了一把勺子。"

            "她没说话，只是看了我一眼。"

            me "（她是不是……也算看见了？）"

        "问她「时间在动」是什么意思。":
            $ add_affection(3)
            me "什么叫时间在动？"

            show awan uneasy at awan_center
            with dissolve

            awan "就是……会往前走。"
            awan "有些地方，时间是不动的。"

            me "比如？"

            awan "海边。"

            "她说完就低头喝糖水，没有再看我。"

    $ ai_chat_enable = True
    call ai_optional_chat
    $ ai_chat_enable = False
    return


# ---------- 夜市（二次） ----------
label side_night_market:
    $ stage_info = "夜市快收摊了，人少了很多"
    scene bg night_market
    with fade_scene

    $ visit_place("夜市")

    "收摊的摊主在收塑料凳，地上都是纸屑。"

    show awan calm at awan_center
    with dissolve

    awan "热闹散了，原来是这个样子。"

    me "失望？"

    awan "不。"
    awan "散了以后，能看清原来是什么。"

    menu:
        "捡起一张被踩皱的糖纸给她。":
            $ add_affection(4)
            "我把糖纸展平，递给她。上面印着一只褪色的燕子。"

            show awan happy at awan_center
            with dissolve

            awan "……和白天那支一样。"

            "她小心地把糖纸夹进书里。"

        "陪她坐在马路牙子上。":
            $ add_affection(5)
            "我们并肩坐着，看摊主一个个把灯关掉。"

            show awan shy at awan_center
            with dissolve

            awan "云砚。"
            awan "如果我明天不在了，你会不会找我？"

            me "你说什么傻话。"

            awan "你回答我。"

            me "……会。"

            "她低下头，笑了一下，很轻。"

            awan "那就好。"
    return


# ---------- 书店（二次） ----------
label side_bookstore:
    $ stage_info = "深夜书店，只有我们和打瞌睡的店员"
    scene bg bookstore
    with fade_scene

    $ visit_place("书店")

    "书架的影子投在地上，一格一格。"

    show awan calm at awan_center
    with dissolve

    awan "云砚，你相信人会忘记很重要的事吗？"

    me "会吧。人记性都不好。"

    awan "我不是说记性。"

    show awan hurt at awan_center
    with dissolve

    awan "我是说……明明记得，却不敢想。"

    menu:
        "告诉她「那就别想」。":
            $ add_affection(4)
            me "那就别想了。"

            awan "……可以吗？"

            me "有些事不想，也能活下去。"

            "她看着我，很久。"

            awan "你说得对。"
            awan "可是云砚，我好像没有「活下去」这个选项。"

            me "什么意思？"

            awan "……没什么。"

        "告诉她「想不出来也没关系」。":
            $ add_affection(3)
            me "想不出来也没关系。等你想说的时候再说。"

            show awan shy at awan_center
            with dissolve

            awan "你这个人……"
            awan "有时候太温柔了，会让人舍不得。"

    return


# ---------- 摩天轮（二次） ----------
label side_ferris_wheel:
    $ stage_info = "又来到摩天轮下，这次没有上去"
    scene bg ferris_wheel
    with fade_scene

    $ visit_place("摩天轮")

    "摩天轮的灯一圈一圈地转，像一只巨大的、慢慢呼吸的东西。"

    show awan giggle at awan_center
    with dissolve

    awan "我不上去了。"

    me "怕？"

    awan "嗯。"
    awan "在上面的时候，我离海太远了。"

    me "（这句话她说得很认真，不像玩笑。）"

    menu:
        "陪她坐在下面的长椅上。":
            $ add_affection(5)
            "我们坐在长椅上，看轿厢一个个升上去，又落下来。"

            show awan shy at awan_center
            with dissolve

            awan "云砚，你数过吗？"

            me "数什么？"

            awan "数过有多少个轿厢吗？"

            me "没有。"

            awan "我数过。二十四个。"
            awan "每一个转上去，都会落下来。"

            "她说这话的时候，声音很轻，像在说别的东西。"

        "问她为什么怕离海太远。":
            $ raise_quarrel(1)
            me "为什么离海太远，你会怕？"

            show awan hurt at awan_center
            with dissolve

            awan "……"

            me "舒瑶。"

            awan "别问了。"
            awan "有些事，你知道了，就回不去了。"

            "她站起来，往江边走。我站在原地，忽然觉得她的背影很薄。"
    return


# ---------- 江边（二次，重头戏之前） ----------
label side_riverside:
    $ stage_info = "江边步道，风很大"
    scene bg riverside
    with fade_scene

    $ visit_place("江边")

    "江风比海风硬。她把头发别到耳后，露出很白的侧脸。"

    show awan calm at awan_center
    with dissolve

    awan "云砚，你闻。"

    me "闻什么？"

    awan "江里没有海的味道。"
    awan "可是风里有一点点。"

    "我用力闻了闻，只闻到潮湿的水泥味。"

    me "（她说有，那就是有吧。）"

    menu:
        "说「那我以后陪你来看江」。":
            $ add_affection(6)
            me "那我以后常陪你来。"

            show awan think at awan_center
            with dissolve

            awan "以后？"

            me "嗯。以后。"

            "她低下头，很久没说话。再抬起来的时候，眼睛有点红。"

            awan "云砚，你别随便说以后。"

            me "为什么？"

            awan "因为我会当真。"

        "沉默地陪她吹风。":
            $ add_affection(4)
            "我们就那样站着。江面上有货船的灯，很慢地移动。"

            "她的肩膀偶尔碰到我的手臂，凉凉的。"

            awan "这样挺好的。"

            me "嗯。"

            awan "什么都不说，也挺好的。"
    return


# ---------- 音像店 ----------
label side_record_store:
    $ stage_info = "巷子里的旧音像店，老板在听收音机"
    scene bg record_store
    with fade_scene

    $ visit_place("音像店")

    "店面很小，墙上挂满了旧磁带和 CD，空气里有塑料和灰的味道。"

    show awan happy at awan_center
    with dissolve

    awan "这里……"

    "她站在门口，忽然不动了。"

    me "怎么了？"

    awan "我好像来过。"

    me "你不是说你不记得？"

    show awan uneasy at awan_center
    with dissolve

    awan "不是记得。是……身体记得。"

    "她走到最里面那排架子，手指从一盒磁带滑过去，停在一张没有封面的 CD 上。"

    awan "这张。"

    me "上面什么都没写。"

    awan "我知道它是什么。"

    "老板把 CD 放进机器里。音乐响起来的时候，她的眼泪一下就掉了。"

    hide awan
    with dissolve

    "是一段很旧的钢琴，弹到一半就断了，像被谁按停。"

    show awan fading at awan_center
    with dissolve

    awan "云砚，我们走吧。"

    me "你哭了。"

    awan "没有。"
    awan "是灰太大了。"

    menu:
        "买下那张 CD。":
            $ add_affection(6)
            "我把它买了下来。老板说这盘没有标价，随便给。"

            "回去的路上，她一直把 CD 抱在怀里，没有松手。"

            awan "谢谢你。"

        "什么也没买，带她离开。":
            $ add_affection(3)
            "我拉着她出了店门。她的手在抖。"

            me "以后不来了。"

            awan "……嗯。"
            awan "可是云砚，我好像有点想再来一次。"

    return


# ---------- 公交站台 ----------
label side_bus_stop:
    $ stage_info = "深夜公交站台，末班车还没来"
    scene bg bus_stop
    with fade_scene

    $ visit_place("公交站台")

    "站台的灯坏了一盏，明明灭灭。电子屏滚动着末班车的时间。"

    show awan giggle at awan_center
    with dissolve

    awan "云砚，你以前等过末班车吗？"

    me "等过。加班到十一点，站台上就我一个人。"

    awan "那时候在想什么？"

    me "想明天还要上班。"

    "她笑了一声。"

    awan "真好啊。"

    me "哪里好？"

    show awan lonely at awan_center
    with dissolve

    awan "有明天，就好。"

    "电子屏跳了一下，末班车还有十二分钟。"

    menu:
        "问她「你的明天呢」。":
            $ raise_quarrel(1)
            me "那你的明天呢？"

            "她看着电子屏，没有立刻回答。"

            show awan hurt at awan_center
            with dissolve

            awan "我的明天……"
            awan "云砚，车要来了。"

            "她打断了我。"

        "陪她数过往的车。":
            $ add_affection(5)
            "我们数了过去七辆车，没有一辆是末班。"

            show awan happy at awan_center
            with dissolve

            awan "第八辆。"

            me "还没来。"

            awan "我说是就是。"

            "第八辆车拐过街角的时候，车灯把她的脸照亮了一瞬。"

            "我忽然很想记住这个画面。"

    "末班车来了，又走了。我们没有上。"
    return

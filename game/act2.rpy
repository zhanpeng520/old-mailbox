# ============================================================
# 第二幕 · 城市游玩
# ------------------------------------------------------------
# 主线：糖水铺 → 夜市 →（自由闲逛分支）→ 书店 → 摩天轮 → 江边
# 每个地点 2~3 件可选小事；每一次「首次到达」记一片回忆碎片
# 隔阂线索：店员看不见她、没人碰到她、她读得太快
# ============================================================

label act2_start:
    $ current_day = 2
    $ current_stage = "第二天 · 城市"
    $ stage_info = "第二次见面，带她进城，坐在糖水铺里"

    scene bg dessert_shop
    with fade_scene

    # BGM 注释：糖水铺用「轻快的木吉他 + 瓷勺碰撞声」
    # play music "audio/dessert_shop.ogg" fadein 1.0

    "糖水铺开在街角，只有四张桌子。"

    show awan happy at awan_center
    with dissolve

    awan "这里好香。"

    me "双皮奶的味。"

    $ visit_place("糖水铺")

    "老板娘拿着菜单过来，看了我一眼，又看了看我旁边。"

    boss "……一个人？"

    me "两个。"

    "她愣了一下，把菜单放在桌上，转身走了。"
    "从头到尾，她的目光都没有落在舒瑶身上。"

    me "（大概是她低着头，没看见吧。）"

    show awan calm at awan_center
    with dissolve

    awan "她好像……不太高兴。"

    me "这店就是这样，别在意。"

    menu:
        "给她点一份双皮奶。":
            $ add_affection(5)
            me "一份双皮奶，一份绿豆沙。"

            "双皮奶端上来，她拿勺子的手有点抖。"

            show awan shy at awan_center
            with dissolve

            awan "……热的。"
            awan "原来热的甜的东西，是这个味道。"

            me "你没吃过热的甜的？"

            awan "以前……没有人给我买。"

            "她低下头，一口一口吃得很慢，像在把时间拉长。"

        "让她自己选。":
            $ add_affection(3)
            me "你想吃什么，自己点。"

            show awan point at awan_center
            with dissolve

            awan "我……不知道这些名字。"

            "她盯着菜单看了很久，最后指了指最便宜的那一行。"

            awan "这个。"

            me "绿豆沙？"

            awan "嗯。名字听起来，像夏天。"

            "她吃到一半，忽然停下来。"

            awan "云砚，你怎么知道我喜欢甜的？"

            me "我没说。"

            awan "……"

            "她笑了一下，没再问。"

    $ ai_chat_enable = True
    call ai_optional_chat
    $ ai_chat_enable = False

    jump act2_night_market


# ---------- 夜市 ----------
label act2_night_market:
    $ stage_info = "在夜市，人多，她一直跟得很紧"

    scene bg night_market
    with fade_scene

    $ visit_place("夜市")

    "夜市亮得晃眼。烤鱿鱼的烟、糖炒栗子的甜、喇叭里循环的叫卖。"

    show awan happy at awan_center
    with dissolve

    awan "好吵。"

    me "嫌吵？"

    awan "不是。"
    awan "是……很久没听过这么多人的声音了。"

    "人挤人。我下意识地伸手护着她。"

    "可奇怪的是，人流像水一样从她身边分开，没有一个人撞到她，也没有一个人看她。"

    me "（……这么漂亮的女孩子，怎么会没人看？）"

    menu:
        "给她买一支糖画。":
            $ add_affection(5)
            "做糖画的老人舀起一勺糖，在铁板上画了一只鸟。"

            show awan happy at awan_center
            with dissolve

            awan "是燕子。"

            me "你怎么知道？"

            awan "燕子的尾巴是分开的。"

            "她把糖画举起来，对着灯看。糖在灯下像一小片金色的海。"

            awan "……我舍不得吃。"

            me "不吃会化。"

            awan "化了也没关系。"
            awan "反正我记得它长什么样。"

        "陪她玩套圈。":
            $ add_affection(4)
            "十块钱五个圈。她套了三次，一个都没中。"

            show awan blush at awan_center
            with dissolve

            awan "我是不是很笨。"

            me "是挺笨的。"

            "我把剩下的两个圈递给她。"

            "第四次，圈歪歪扭扭地挂在了最边上那个白瓷猫的耳朵上。"

            show awan giggle at awan_center
            with dissolve

            awan "中了！"

            "她抱着那只猫，笑得眼睛都没了。"
            "摊主看了我一眼，又看看那只猫，嘟囔了一句什么。"

        "不买东西，只是慢慢走。":
            $ add_affection(3)
            "我们就一直走。她偶尔停下来看，什么也不买。"
            awan "云砚，你说人为什么要买这么多用不上的东西？"

            me "因为想要。"

            awan "想要，就能买到吗？"

            me "大多数时候能。"

            show awan lonely at awan_center
            with dissolve

            awan "……那真好啊。"

    "人潮散了一点。她忽然停下来，问我："

    awan "云砚，如果我明天不在了，你会不会找我？"

    me "你怎么问这个。"

    awan "你回答我。"

    me "……会。"

    awan "那就好。"

    "她说完，低下头，像是把这句话收进了口袋里。"

    "出了夜市，她忽然拉住我的袖子。"

    show awan calm at awan_center
    with dissolve

    awan "云砚。"
    awan "今天谢谢你。"
    awan "我会记得的。"

    me "记得什么？今天才过了一半。"

    awan "……"

    "她没有回答，只是把手放回身侧。"

    jump act2_after_market


# ---------- 自由闲逛分支 ----------
label act2_after_market:
    $ current_stage = "第二幕 · 岔路"
    $ stage_info = "夜市之后，我该决定要问，还是继续陪她逛"

    "时间还早。"

    menu:
        "那些说不清的事，我想问清楚。":
            $ raise_quarrel(1)
            me "舒瑶。"

            show awan uneasy at awan_center
            with dissolve

            awan "嗯？"

            me "你为什么从来不说你以前的事？"

            "她沉默了一会儿，手指在袖口上绞了绞。"

            awan "……说了，你会不高兴。"

            me "你不说，我才不高兴。"

            show awan hurt at awan_center
            with dissolve

            awan "云砚，别逼我好不好。"

            "她的声音很轻，轻得像怕吵到什么。"

            me "（她在怕什么？）"

            "那一晚，我们之间多了一点什么，又少了一点什么。"

            jump day2_end

        "算了，先陪她随便逛逛。":
            $ add_affection(2)

            "我们沿着夜市外面的马路慢慢走。"
            "收摊的摊主在收灯，一盏一盏，街就暗下去。"
            "她走在我右边，偶尔伸手碰一下路边的栏杆。"

            awan "云砚。"

            me "嗯。"

            awan "今天谢谢你。"

            me "你今天已经谢过了。"

            awan "那就再谢一次。"

            "她说完，把手插回口袋里。"
            "我忽然很想牵她，可手伸到一半，又收了回来。"

            jump day2_end


label act2_free_roam:
    $ stage_info = "第四天，在城里漫无目的地闲逛"

    if free_roam_used >= 3:
        "天快黑了。街上的店一家家亮起灯。"

        show awan calm at awan_center
        with dissolve

        awan "云砚，我们是不是该回去了？"

        me "再走一段吧。"

        jump act2_bookstore

    menu:
        "陪她再去一个地方。":
            call side_story_pick
            $ free_roam_used += 1
            jump act2_free_roam

        "往书店那边走。" if free_roam_used > 0:
            jump act2_bookstore


# ---------- 书店 ----------
label act2_bookstore:
    $ stage_info = "第四天傍晚，在书店，她翻书翻得很快"

    scene bg bookstore
    with fade_scene

    $ visit_place("书店")

    "书店是二十四小时的那种，灯光昏黄，只有店员在柜台后面打瞌睡。"

    show awan calm at awan_center
    with dissolve

    "她走到书架前，抽出一本，翻两页，放回去。再抽一本。"

    "快得不像在读，像在认。"

    me "你看得完吗？"

    awan "看得完。"

    me "这才几分钟。"

    show awan lonely at awan_center
    with dissolve

    awan "……这些书，我好像都读过。"
    awan "可是我想不起来，是什么时候读的。"

    me "（她说「都读过」的时候，语气很确定。）"

    menu:
        "给她挑一本书带走。":
            $ add_affection(5)
            "我在书架上找了半天，抽出一本薄薄的诗集。"

            me "这本。字少，适合你。"

            "她接过去，翻开第一页，念了出来——"

            awan "「我把手伸进海里，捞起一整片黄昏。」"

            "念到一半，她停住了。"

            show awan hurt at awan_center
            with dissolve

            awan "……这句话，我好像说过。"

            me "对谁说的？"

            awan "……"

            "她把书合上，抱在胸前，像是抱住一个不能说出口的东西。"

        "问她记不记得上次来城里。":
            $ raise_quarrel(1)
            me "你以前来过城里吗？"

            awan "……来过吧。"

            me "和谁？"

            show awan shiver at awan_center
            with dissolve

            awan "云砚。"

            me "我在问。"

            awan "我不记得了。真的。"
            awan "有些事，我想记，但是一伸手，就散了。"

            "她说话的时候，指尖在书脊上轻轻发抖。"

            me "（她不像在撒谎。可这比撒谎更让人不安。）"

        "什么也不问，陪她站着。":
            $ add_affection(3)
            "我站在她旁边，看她一本一本地翻。"

            "书店的钟走得很慢。她的侧脸在灯下很安静。"

            "那一刻我忽然想，如果时间能停在这儿也不错。"

            "——这个念头后来被我反复想起。"

    jump act2_ferris_wheel


# ---------- 摩天轮 ----------
label act2_ferris_wheel:
    $ stage_info = "摩天轮上，离海最远的地方"

    scene bg ferris_wheel
    with fade_scene

    $ visit_place("摩天轮")

    "摩天轮在江边，转一圈要十八分钟。"

    "售票的小窗后面，售票员抬头看了看我身后。"

    clerk "几位？"

    me "两位。"

    clerk "……两位？"

    "他探出头，往我身后看了看，皱起眉，最后什么也没说，撕了一张票给我。"

    me "（第二张票，他始终没有撕。）"

    show awan calm at awan_center
    with dissolve

    awan "云砚，我有点怕。"

    me "怕高？"

    awan "不是。"
    awan "是……这里离海，好像很远了。"

    "轿厢一点点升起来。城市的灯在脚下铺开。"

    "升到最高处的时候，她忽然靠在我肩上。"

    show awan fading at awan_center
    with dissolve

    "我低头，看见她的手在灯下变得很淡，能透过她看见轿厢的玻璃。"

    me "舒瑶？"

    awan "……没事。"
    awan "让我靠一会儿。"
    awan "就一会儿。"

    "她的声音很轻，像隔着一层水。"

    menu:
        "握住她的手。":
            $ add_affection(8)
            "我伸手去握她。"
            "她的手很凉，凉得像从海里捞出来的石头。"
            "但我握住了。"

            show awan shy at awan_center
            with dissolve

            awan "……你手心好热。"

            me "你太凉了。"

            awan "嗯。"
            awan "所以你多握一会儿吧。"

        "问她到底怎么了。":
            $ raise_quarrel(1)
            me "你手怎么这么凉？你脸色也不对。"

            show awan hurt at awan_center
            with dissolve

            awan "我没事。"

            me "你从上车开始就不对劲。"

            awan "云砚。"
            awan "你能不能……今天就别问了。"

            "她把头转开，看着窗外。"
            "玻璃上映出她的脸，淡得几乎看不见。"

        "什么也不说，让她靠着。":
            $ add_affection(6)
            "我没有说话。"
            "轿厢慢慢往下走，城市的灯一盏一盏从脚下退回去。"
            "她靠在我肩上，呼吸很轻。"

            "有那么一小会儿，我几乎以为她睡着了。"

    "落地的时候，她的手又恢复了血色。"

    show awan giggle at awan_center
    with dissolve

    awan "云砚，我饿了。"

    me "前两天糖水铺是谁吃了两碗。"

    awan "那是甜的。现在是饿。"

    "她笑起来，和刚才那个透明的人像两个。"

    "我们沿着江边慢慢走，一直走到末班车站。"
    "江风把她的头发吹到我脸上。"

    jump day4_end

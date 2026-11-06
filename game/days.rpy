# ============================================================
# 七天时间轴 · 第二~七天的新增段落
# ------------------------------------------------------------
# 第二天夜里：送她回海边，决定请一周假
# 第三天：小镇早市 / 堤岸 / 泡面
# 第四天：再进城（接回 act2 的书店与摩天轮）
# 第五天：台风、停电、蜡烛
# 第六天：渔火节、纸灯、没有她的照片
# 第七天：江边（接回 act3）
# ============================================================


# ============================================================
# 第二天 · 夜里
# ============================================================
label day2_end:
    $ current_day = 2
    $ stage_info = "第二天夜里，送她回海边"

    scene bg bus_window
    with fade_scene

    "末班小巴上，人很少。"
    "她靠着窗，城市的灯一盏一盏往后退。"

    show awan calm at awan_center
    with dissolve

    awan "云砚。"

    me "嗯。"

    awan "今天走了好多地方。"

    me "累吗。"

    awan "不累。"

    awan "就是有点……舍不得。"

    me "舍不得什么。"

    awan "舍不得天黑。"

    "她说得很轻，像怕被司机听见。"

    scene bg sea_dusk
    with slow_scene

    "车到镇上的时候，已经过了十一点。"
    "堤岸上没有灯，只有海的声音。"

    show awan calm at awan_center
    with dissolve

    awan "送到这儿就行了。"

    me "我看着你回去。"

    awan "……我住得很近。"

    me "那我明天还来。"

    "她愣了一下。"

    awan "明天？"

    me "我请了五天假。"

    me "加上周末，一共七天。"

    show awan shy at awan_center
    with dissolve

    awan "你不用上班吗？"

    me "年假再不用，就过期了。"

    "她低下头，笑了很久。"

    awan "那……明天见。"

    me "明天见。"

    $ add_affection(4)

    "我看着她走到堤岸尽头，走到那只旧信箱旁边。"
    "她没有回头。"
    "可我知道，她一直在听我的脚步声。"

    scene bg black
    with fade

    jump day3_start


# ============================================================
# 第三天 · 海边小镇
# ============================================================
label day3_start:
    $ current_day = 3
    $ current_stage = "第三天 · 海边小镇"
    $ stage_info = "第三天，镇上的早市"

    scene bg black
    with fade
    centered "{size=64}第三天{/size}\n\n{size=26}早市、海风，和一碗泡面{/size}"

    scene bg town_day
    with fade_scene

    "我在镇上租了一间房，在二楼，木地板一到傍晚就响。"
    "一张床，一张桌子，一盏台灯，窗户推开就是海。"
    "墙上还贴着上一任房客留下的日历，停在很多年前，没人撕过。"

    "房东问我住几天，我说七天。"
    "她哦了一声，把钥匙给我，又往我身后看了一眼。"

    "早上七点，镇上的早市已经散了半边。"
    "她站在鱼摊旁边，看得比谁都认真。"

    show awan calm at awan_center
    with dissolve

    awan "原来鱼是这样卖的。"

    me "你以前没见过？"

    awan "见过。"

    awan "只是没这么近。"

    "卖鱼的阿姨抬头看了我一眼。"

    fish_aunt "小伙子，要哪条？"

    me "两个人。"

    "阿姨愣了一下，低头去捞鱼。"

    me "（她还是没看舒瑶。）"

    menu:
        "买两只刚出锅的糖糕，一人一只。":
            $ add_affection(5)

            "糖糕很烫，她两只手倒来倒去。"

            show awan happy at awan_center
            with dissolve

            awan "好烫。"

            me "凉一下再吃。"

            awan "不要。"

            awan "凉了就不是这个味道了。"

            "她小口小口地咬，像在跟时间抢。"

        "让她自己挑点什么。":
            $ add_affection(3)

            me "想要什么，自己挑。"

            "她在摊子之间走了很久，最后停在一个卖发绳的小摊前。"
            "一根红色的发绳，两块钱。"

            show awan shy at awan_center
            with dissolve

            awan "这个。"

            me "就这个？"

            awan "嗯。"

            "她当场把头发扎起来，露出一截很白的脖子。"

            awan "好看吗。"

            me "……好看。"

    "中午我们在堤岸上坐着。"
    "潮水退下去，露出一小片湿的滩涂。"
    "远处的渔船停在海上，像几片没有动的叶子。"

    "她把鞋脱了，踩进浅水里，回头冲我笑。"

    awan "水是温的。"

    me "小心滑。"

    awan "不会。"

    "她弯下腰，从水里捞起一枚小螺，举到太阳底下看。"
    "螺壳里还存着一点水，亮得像一小块海。"

    awan "这个给你。"

    me "又是贝壳。"

    awan "这次是螺。"

    "她把螺塞进我手心，指尖带着海水的凉。"

    "她问我城里的事，问我几点起床、几点下班、周末做什么。"

    me "以前周末就回来，往信箱里塞信。"

    awan "现在呢。"

    me "现在坐在这儿。"

    "她笑了一下。"

    show awan calm at awan_center
    with dissolve

    awan "云砚，你有没有想过，不回城里了。"

    me "想过。"

    me "但我得养活自己。"

    awan "嗯。"

    awan "人是要吃饭的。"

    "她说这话的时候，语气很轻，像在替我难过。"

    scene bg room
    with fade_scene

    "傍晚下起小雨，我们没地方去。"
    "我在租的房间里煮了两碗泡面，加了两颗鸡蛋。"

    show awan calm at awan_center
    with dissolve

    awan "这个好香。"

    me "泡面也香？"

    awan "你煮的。"

    "她坐在窗边，捧着碗，热气把她的脸熏得有点红。"

    $ ai_chat_enable = True
    call ai_optional_chat
    $ ai_chat_enable = False

    "吃到一半，她忽然停下来。"

    awan "云砚。"

    me "嗯。"

    awan "如果有一天我不见了，你会怎么办。"

    me "你怎么又问这个。"

    awan "你回答我。"

    menu:
        "说「那我就一直找，找到为止」。":
            $ add_affection(3)

            me "那我就一直找。"

            me "找到为止。"

            show awan hurt at awan_center
            with dissolve

            awan "如果找不到呢。"

            me "那就一直找。"

            "她低下头，眼泪掉进碗里。"

            awan "你这个人……"

        "说「你不会不见的」。":
            $ add_affection(2)

            me "你不会不见的。"

            "她看了我很久。"

            awan "嗯。"

            awan "你说不会，就不会。"

            "她笑着说完，低头继续吃面。"
            "可我看见她握筷子的手，在轻轻发抖。"

    "窗外雨声很大。"
    "海在雨后面，一声一声。"

    $ add_affection(3)

    scene bg black
    with fade

    jump day4_start


# ============================================================
# 第四天 · 再进城
# ============================================================
label day4_start:
    $ current_day = 4
    $ current_stage = "第四天 · 再进城"
    $ stage_info = "第四天，又坐上了进城的小巴"

    scene bg black
    with fade
    centered "{size=64}第四天{/size}\n\n{size=26}旧音像店、末班车站台，和一整座城{/size}"

    scene bg bus_window
    with slow_scene

    "第四天，我们又进了城。"
    "她说想再去看看。"

    show awan happy at awan_center
    with dissolve

    awan "这次我不怕坐车了。"

    me "上次也没见你怕。"

    awan "上次怕的。"

    awan "怕海不见，也怕你不见。"

    "车过隧道的时候，我下意识地握住她的手。"
    "这一次，她没有变淡。"

    $ add_affection(3)

    "车到站，城市的声音一下子涌上来。"

    jump act2_free_roam


# ============================================================
# 第四天 · 夜里（摩天轮之后）
# ============================================================
label day4_end:
    $ current_day = 4
    $ stage_info = "第四天夜里，摩天轮之后"

    scene bg sea_dusk
    with slow_scene

    "回到镇上的时候，又是夜里。"
    "她走得很慢，手一直很凉。"

    show awan calm at awan_center
    with dissolve

    me "今天走太多了。"

    awan "嗯。"

    awan "可是我很高兴。"

    "她停下来，回头看了一眼海。"

    awan "云砚，你有没有觉得，海在看着我。"

    me "海怎么看人。"

    awan "就是……看着。"

    "她把头靠在我肩上，很轻。"

    $ add_affection(4)

    "那天晚上，我第一次梦见她站在水里，冲我摆手。"
    "梦里我听不见她说什么，只看见她一直在往后退。"

    scene bg black
    with fade

    jump day5_start


# ============================================================
# 第五天 · 台风夜
# ============================================================
label day5_start:
    $ current_day = 5
    $ current_stage = "第五天 · 台风"
    $ stage_info = "第五天，台风把镇子按在了雨里"

    scene bg black
    with fade
    centered "{size=64}第五天{/size}\n\n{size=26}台风、停电，和一支蜡烛{/size}"

    scene bg room
    with fade_scene

    "第五天，台风来了。"
    "雨横着抽在窗上，镇上停了电，房东在楼下喊我别出门。"

    "她坐在窗边，看着外面的海。"

    show awan calm at awan_center
    with dissolve

    awan "今天的海，声音不一样。"

    me "台风天都这样。"

    awan "不是。"

    awan "它在叫我。"

    me "……别吓我。"

    show awan shy at awan_center
    with dissolve

    awan "骗你的。"

    "她笑了一下，可眼睛没有跟着笑。"

    "我点了一支蜡烛，屋里只剩下一点黄光。"
    "她把手伸到火苗旁边，看了很久。"

    awan "原来是这个温度。"

    me "什么？"

    awan "火。"

    awan "我一直以为，火是很烫的。"

    awan "云砚，我好像没有「活下去」这个选项。"

    me "什么意思。"

    "她摇摇头，没有再说。"

    "我握住她的手。她的手比平时更凉。"

    menu:
        "把外套披在她身上，说「冷就靠着我」。":
            $ add_affection(6)

            "我把外套脱下来，披在她肩上。"

            me "冷就靠着我。"

            show awan shy at awan_center
            with dissolve

            awan "……嗯。"

            "她靠过来，隔着衣服，我能感觉到她在发抖。"

            awan "云砚。"

            me "嗯。"

            awan "如果有一天，我连冷都感觉不到了，你还会认得出我吗。"

            me "认得出。"

            me "你化成灰我都认得出。"

            "她笑出了声，笑着笑着，眼泪就下来了。"

        "问她「海为什么会叫你」。":
            $ raise_quarrel(1)
            $ add_affection(3)

            me "海为什么会叫你。"

            "她沉默了很久。"

            show awan hurt at awan_center
            with dissolve

            awan "因为……我本来就该回去。"

            me "回哪儿去。"

            awan "云砚。"

            awan "今天别问了，好不好。"

            "她把脸转开。烛光在她脸上晃，像随时会灭。"

    $ ai_chat_enable = True
    call ai_optional_chat
    $ ai_chat_enable = False

    "临近黄昏的时候，雨忽然停了。"
    "不是变小，是整片雨幕被人一下子收走。"
    "楼下有人喊：别出去，这是台风眼，过一会儿还得来。"

    "她还是站了起来。"

    awan "就一会儿。"

    scene bg sea_dusk
    with slow_scene

    "天是开的。"

    scene cg_typhoon_eye
    with slow_scene

    "整片海被夕阳烧成铜红色。"
    "浪一层一层翻过来，像有人在底下抖一块很重的绸子，每一道浪脊都镶着金边。"
    "远处的防波堤只剩下一个黑影，还歪着。"

    scene bg sea_dusk
    with dissolve

    show awan fading at awan_center
    with dissolve

    "她站在堤岸上，风把她的裙子吹得几乎透明。"

    awan "原来台风里的海，是这个样子。"

    me "怕吗。"

    awan "不怕。"

    awan "就是有点想哭。"

    me "为什么。"

    awan "因为它太漂亮了。"

    "她说得很认真。"
    "我忽然明白，她说的不是海。"

    "太阳沉下去的时候，整片海暗了一瞬。"
    "然后，风又起来了。"

    $ add_affection(4)

    "我们跑回屋里的时候，两个人都湿透了。"
    "她笑得停不下来。"

    scene cg_typhoon
    with slow_scene

    "我重新点了蜡烛。"
    "她坐在床边，头发还在滴水。"
    "烛光只够照亮桌子一圈，其余的地方全退回黑里。"
    "两只泡面桶，一盒我带来的信，还有她被光切开的半张脸。"

    scene bg room
    with dissolve

    show awan calm at awan_center
    with dissolve

    awan "云砚。"

    me "嗯。"

    awan "刚才那个，我会记很久。"

    me "哪个。"

    awan "海。"

    awan "和你看海。"

    "窗外，风声又大起来。"

    "后半夜，雨小了一些。"
    "我醒过来的时候，床边没有人。"

    "她站在窗边，背对着我，看着海。"

    show awan calm at awan_center
    with dissolve

    me "怎么不睡。"

    awan "我不困。"

    awan "云砚，你睡吧。"

    awan "我就在这儿。"

    "我重新躺下，却一直没睡着。"
    "我听见她很小声地说了一句什么。"
    "被雨声盖住了。"

    $ add_affection(3)

    scene bg black
    with fade

    jump day6_start


# ============================================================
# 第六天 · 渔火节
# ============================================================
label day6_start:
    $ current_day = 6
    $ current_stage = "第六天 · 渔火节"
    $ stage_info = "第六天，镇上的渔火节"

    scene bg black
    with fade
    centered "{size=64}第六天{/size}\n\n{size=26}渔火、纸灯，和一张没有她的照片{/size}"

    scene bg festival_night
    with fade_scene

    "第六天，台风走了。"
    "镇上办渔火节，堤岸上挂满了纸灯，海面上漂着一层灯影。"

    show awan happy at awan_center
    with dissolve

    awan "好亮。"

    me "比夜市还亮。"

    awan "不一样。"

    awan "夜市是人的灯。"

    awan "这些是给海的。"

    "她拉着我往人堆里走。"
    "一个小孩从她身上穿过去，跑远了。"

    "我站在原地，后背一点点凉下来。"

    "她回过头，冲我笑。"

    awan "怎么了？"

    me "……没什么。"

    me "人太多了。"

    "我买了两盏纸灯，一人一盏。"
    "摊主说，把想说的话写在灯上，放进海里，海会替你把话带到。"

    "她背对着我写，写得很慢。"

    me "写了什么。"

    awan "不告诉你。"

    "她把灯放进海里，看它漂远。"

    scene cg_lantern
    with slow_scene

    "灯一盏一盏地漂出去，海面被点亮成一条路，一直铺到看不见的地方。"
    "我数不清有多少人在这里许过愿。"
    "她的那盏在最前面，漂得比谁都快。"

    scene bg festival_night
    with dissolve

    "我掏出白天在杂货铺买的拍立得。"

    me "站好，我给你拍一张。"

    show awan shy at awan_center
    with dissolve

    awan "我不上相。"

    me "试试。"

    "咔嚓一声。"
    "照片慢慢显影。"

    "照片里是堤岸、纸灯、海。"
    "她站的位置，只有一团很淡的白。"

    "我盯着照片，手指有点发麻。"

    menu:
        "把照片收起来，装作什么都没发生。":
            $ add_affection(6)

            "我把照片塞进口袋。"

            me "拍糊了。"

            awan "我看看。"

            me "不给。"

            "她伸手来抢，我躲开了。"

            show awan calm at awan_center
            with dissolve

            awan "云砚。"

            awan "你是不是看见了。"

            me "看见什么。"

            awan "……没什么。"

            "她没有再问。"
            "我们并肩站着，看灯一盏一盏漂远。"

            "她忽然说："
            awan "今天是我过得最好的一天。"

            me "明天还有。"

            awan "嗯。"

            awan "明天还有。"

            "她说这句话的时候，声音很轻。"
            "轻得像在替明天道歉。"

        "把照片递给她，问她这是怎么回事。":
            $ raise_quarrel(1)
            $ add_affection(2)

            "我把照片递过去。"

            me "你看看。"

            "她低头看了很久。"

            show awan hurt at awan_center
            with dissolve

            awan "……大概是光太暗了。"

            me "舒瑶。"

            me "这不是光的问题。"

            awan "云砚。"

            awan "今天很好。"

            awan "别在今天问，好不好。"

            "她把照片还给我，转身去看灯。"
            "我跟在后面，隔着半步。"

            "那半步，后来怎么也没能补上。"

    $ add_affection(3)

    scene bg black
    with fade

    "那天晚上，我做了个决定。"
    "明天，我要把话问清楚。"

    jump day7_start


# ============================================================
# 第七天 · 江边
# ============================================================
label day7_start:
    $ current_day = 7
    $ current_stage = "第七天 · 江边"
    $ stage_info = "第七天，她说想去江边"

    scene bg black
    with fade
    centered "{size=64}第七天{/size}\n\n{size=26}江边的风，比海边的硬{/size}"

    scene bg bus_window
    with slow_scene

    "第七天，她说想去江边看看。"

    show awan calm at awan_center
    with dissolve

    awan "城里那条江。"

    me "江有什么好看。"

    awan "海太远了。"

    awan "我想看看，离海远一点的地方，是什么样。"

    "我没听懂这句话。"
    "等听懂的时候，已经太晚了。"

    jump act3_start

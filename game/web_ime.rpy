# ============================================================
# Web 端中文输入
# ------------------------------------------------------------
# 为什么需要这层：
#   Ren'Py 的 Web 运行时（SDL/Emscripten）在 document 上监听 keydown，
#   处理完会 preventDefault。裸塞一个 textarea 进去，按键在冒泡阶段
#   就被吃掉 —— 光标能闪，但一个字也打不出来。
#   对比：Ren'Py 自带的 renpy.input 在 Web 上走 index.html 里的 #inputDiv，
#   它能用正是因为它对 keydown/keyup/keypress 做了 stopPropagation。
#
# 所以这里做三件事：
#   1. 给覆盖层 textarea 加 stopPropagation（关键，不加就打不了字）；
#   2. 按游戏画面（1280x720）算出输入行位置，把原生输入框盖在上面；
#   3. 打开界面自动唤起、发出后自动收回、收到回复自动再唤起。
# 桌面版不受影响，仍然用原来的 Ren'Py input。
# ============================================================

default ai_ime_open = False

init -5 python:

    _OML_IME_SHOW = """
(function(){
  var id = 'oml-ime';
  var el = document.getElementById(id);

  function place(){
    var c = document.getElementById('canvas');
    if(!c || !el){ return; }
    var r = c.getBoundingClientRect();
    var scale = Math.min(r.width / 1280, r.height / 720);
    var offX = r.left + (r.width - 1280 * scale) / 2;
    var offY = r.top + (r.height - 720 * scale) / 2;
    el.style.left = (offX + 268 * scale) + 'px';
    el.style.top = (offY + 563 * scale) + 'px';
    el.style.width = (590 * scale) + 'px';
    el.style.height = Math.max(38, 54 * scale) + 'px';
    el.style.fontSize = Math.max(13, 20 * scale) + 'px';
  }

  if(!el){
    el = document.createElement('textarea');
    el.id = id;
    el.setAttribute('autocomplete', 'off');
    el.setAttribute('autocorrect', 'off');
    el.setAttribute('autocapitalize', 'off');
    el.setAttribute('spellcheck', 'false');
    el.setAttribute('enterkeyhint', 'send');
    el.style.cssText = 'position:fixed;box-sizing:border-box;padding:10px 16px;'
      + 'border-radius:12px;border:1px solid rgba(230,185,138,.55);'
      + 'background:rgba(9,13,19,.96);color:#f2efe9;font-family:inherit;line-height:1.4;'
      + 'resize:none;z-index:2147483647;outline:none;'
      + 'box-shadow:0 10px 34px rgba(0,0,0,.55);';
    el.placeholder = '在这里打字（支持中文输入法），回车发送';

    // ★ 关键：拦住这些事件，别让它们冒泡到 document 被 Ren'Py 的键盘处理 preventDefault
    ['keydown', 'keyup', 'keypress', 'beforeinput', 'input',
     'mousedown', 'mouseup', 'click', 'dblclick',
     'touchstart', 'touchend', 'touchmove', 'wheel'].forEach(function(t){
      el.addEventListener(t, function(e){ e.stopPropagation(); });
    });

    el.addEventListener('keydown', function(e){
      if(e.key === 'Enter' && !e.shiftKey && !e.isComposing && e.keyCode !== 229){
        e.preventDefault();
        e.stopPropagation();
        el.dataset.done = '1';
        el.blur();
      }
    });

    document.body.appendChild(el);
  }

  place();
  window.removeEventListener('resize', window._omlImePlace);
  window._omlImePlace = place;
  window.addEventListener('resize', window._omlImePlace);

  el.dataset.done = '0';
  el.value = '';
  el.style.display = 'block';
  setTimeout(function(){ el.focus(); }, 50);
  setTimeout(function(){ if(document.activeElement !== el){ el.focus(); } }, 260);
})();
"""

    # 只取「回车提交」后的内容（定时轮询用）
    _OML_IME_PULL = """
(function(){
  var t = document.getElementById('oml-ime');
  if(!t || t.dataset.done !== '1') return '';
  t.dataset.done = '0';
  var v = t.value;
  t.value = '';
  t.style.display = 'none';
  return v;
})();
"""

    # 不管有没有回车，直接把当前内容取走（点「发送」按钮用）
    _OML_IME_PULL_ANY = """
(function(){
  var t = document.getElementById('oml-ime');
  if(!t) return '';
  t.dataset.done = '0';
  var v = t.value;
  t.value = '';
  t.style.display = 'none';
  return v;
})();
"""

    _OML_IME_HIDE = """
(function(){var t = document.getElementById('oml-ime'); if(t){t.style.display='none';}})();
"""

    def web_ime_open():
        if not renpy.emscripten:
            return
        import emscripten
        emscripten.run_script(_OML_IME_SHOW)
        store.ai_ime_open = True

    def web_ime_hide():
        store.ai_ime_open = False
        if not renpy.emscripten:
            return
        import emscripten
        emscripten.run_script(_OML_IME_HIDE)

    def web_ime_take(need_enter=True):
        """取浏览器输入框里的文字；need_enter=True 时只认回车提交过的。"""
        if not renpy.emscripten:
            return ""
        import emscripten
        try:
            script = _OML_IME_PULL if need_enter else _OML_IME_PULL_ANY
            val = emscripten.run_script_string(script)
        except Exception:
            return ""
        if not val or val == "undefined" or val == "null":
            return ""
        return val.strip()

    def web_ime_sync():
        """界面定时器：① 没在等回复时把输入框叫回来；② 回车后接住内容发出去。"""
        if not renpy.emscripten:
            return

        if not store.ai_pending and not store.ai_ime_open:
            web_ime_open()
            return

        if store.ai_pending:
            return

        val = web_ime_take(True)
        if not val:
            return
        store.ai_ime_open = False
        store.ai_input = val[:300]
        ai_send()

    def ai_send_web():
        """「发送」按钮：先取浏览器输入框内容，再走原来的发送逻辑。"""
        if renpy.emscripten and not store.ai_pending:
            val = web_ime_take(False)
            if val:
                store.ai_ime_open = False
                store.ai_input = val[:300]
        ai_send()

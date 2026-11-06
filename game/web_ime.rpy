# ============================================================
# Web 端中文输入
# ------------------------------------------------------------
# Ren'Py 的 Web 运行时没有处理输入法（IME）的合成事件，
# 中文输入法在 canvas 里打不出字（只能打英文/数字）。
#
# 这里挂一个浏览器原生 textarea 覆盖在画面上：
#   - 用系统输入法打字，完全没有兼容问题
#   - 回车时标记 done，Ren'Py 定时轮询把文字取回来并发送
# 桌面版不受影响，仍然用原来的 Ren'Py input。
# ============================================================

init -5 python:

    _OML_IME_SHOW = """
(function(){
  var id = 'oml-ime';
  var el = document.getElementById(id);
  if(!el){
    el = document.createElement('textarea');
    el.id = id;
    el.setAttribute('autocomplete', 'off');
    el.style.cssText = 'position:fixed;left:50%;bottom:96px;transform:translateX(-50%);'
      + 'width:58%;max-width:640px;height:54px;padding:12px 16px;border-radius:14px;'
      + 'border:1px solid rgba(255,255,255,.3);background:rgba(9,13,19,.94);'
      + 'color:#f2efe9;font-size:17px;font-family:inherit;line-height:1.4;'
      + 'resize:none;z-index:99999;box-shadow:0 10px 34px rgba(0,0,0,.55);outline:none;';
    el.placeholder = '在这里打字，回车发送';
    el.addEventListener('keydown', function(e){
      if(e.key === 'Enter' && !e.shiftKey && !e.isComposing){
        e.preventDefault();
        el.dataset.done = '1';
        el.blur();
      }
    });
    document.body.appendChild(el);
  }
  el.dataset.done = '0';
  el.value = '';
  el.style.display = 'block';
  setTimeout(function(){ el.focus(); }, 60);
})();
"""

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

    _OML_IME_HIDE = """
(function(){var t = document.getElementById('oml-ime'); if(t){t.style.display='none';}})();
"""

    def web_ime_open():
        if not renpy.emscripten:
            return
        import emscripten
        emscripten.run_script(_OML_IME_SHOW)

    def web_ime_hide():
        if not renpy.emscripten:
            return
        import emscripten
        emscripten.run_script(_OML_IME_HIDE)

    def web_ime_sync():
        """轮询浏览器输入框：回车之后就把它接过来直接发出去。"""
        if not renpy.emscripten or store.ai_pending:
            return
        import emscripten
        try:
            val = emscripten.run_script_string(_OML_IME_PULL)
        except Exception:
            return
        val = (val or "").strip()
        if not val:
            return
        store.ai_input = val[:300]
        ai_send()

"""
旧信箱 · AI 中转服务（上线用）
------------------------------------------------------------
作用：真实模型密钥只存在服务器；客户端只拿到一个匿名设备号。

启动：
    pip install -r requirements.txt
    set UPSTREAM_API_KEY=sk-xxx
    uvicorn main:app --host 0.0.0.0 --port 8000

客户端 ai_config.json 里改成：
    "mode": "proxy",
    "api_url": "https://你的域名/v1/chat/completions"

控费三闸门：
    1) 每设备每天 PLAYER_DAILY_TURNS 次（默认 80）
    2) 全服每天 GLOBAL_DAILY_TURNS 次（默认 20000，超过即熔断）
    3) max_tokens 强制封顶，历史消息长度强制截断
"""

import json
import os
import sqlite3
import time
from contextlib import closing

import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

UPSTREAM_URL = os.environ.get("UPSTREAM_URL", "https://aigw.telecomjs.com/v1/chat/completions")
UPSTREAM_API_KEY = os.environ.get("UPSTREAM_API_KEY", "")
MODEL = os.environ.get("UPSTREAM_MODEL", "qwen3.6-plus")

CLIENT_TOKEN = os.environ.get("CLIENT_TOKEN", "")          # 可留空；留空则不校验
PLAYER_DAILY_TURNS = int(os.environ.get("PLAYER_DAILY_TURNS", "200"))
GLOBAL_DAILY_TURNS = int(os.environ.get("GLOBAL_DAILY_TURNS", "20000"))
MAX_OUTPUT_TOKENS = int(os.environ.get("MAX_OUTPUT_TOKENS", "400"))
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "40"))
MAX_CHARS = int(os.environ.get("MAX_CHARS", "4000"))       # 单次请求全部消息字符上限

DB_PATH = os.environ.get("DB_PATH", "quota.db")
ALLOW_ORIGINS = [o.strip() for o in os.environ.get("ALLOW_ORIGINS", "*").split(",") if o.strip()]

app = FastAPI(title="OldMailbox AI Proxy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _db():
    return closing(sqlite3.connect(DB_PATH, timeout=10))


def _init_db():
    with _db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS usage ("
            " day TEXT NOT NULL, player TEXT NOT NULL, turns INTEGER NOT NULL DEFAULT 0,"
            " tokens INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (day, player))"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS budget ("
            " day TEXT PRIMARY KEY, turns INTEGER NOT NULL DEFAULT 0,"
            " tokens INTEGER NOT NULL DEFAULT 0)"
        )
        conn.commit()


_init_db()


def _today():
    return time.strftime("%Y%m%d")


def _player_used(player):
    with _db() as conn:
        row = conn.execute("SELECT turns FROM usage WHERE day=? AND player=?", (_today(), player)).fetchone()
    return row[0] if row else 0


def _global_used():
    with _db() as conn:
        row = conn.execute("SELECT turns FROM budget WHERE day=?", (_today(),)).fetchone()
    return row[0] if row else 0


def _charge(player, tokens):
    today = _today()
    with _db() as conn:
        conn.execute(
            "INSERT INTO usage (day, player, turns, tokens) VALUES (?, ?, 1, ?)"
            " ON CONFLICT(day, player) DO UPDATE SET turns = turns + 1, tokens = tokens + excluded.tokens",
            (today, player, tokens),
        )
        conn.execute(
            "INSERT INTO budget (day, turns, tokens) VALUES (?, 1, ?)"
            " ON CONFLICT(day) DO UPDATE SET turns = turns + 1, tokens = tokens + excluded.tokens",
            (today, tokens),
        )
        conn.commit()


def _clean_messages(raw):
    """只放行 system/user/assistant 的纯文本，超长直接截断。"""
    messages = []
    for item in raw[-MAX_MESSAGES:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in ("system", "user", "assistant") or not isinstance(content, str):
            continue
        messages.append({"role": role, "content": content[:MAX_CHARS]})

    total = 0
    kept = []
    for item in reversed(messages):
        total += len(item["content"])
        if total > MAX_CHARS:
            break
        kept.append(item)
    kept.reverse()
    return kept


@app.get("/health")
def health():
    return {"ok": True, "day": _today(), "global_used": _global_used(), "global_limit": GLOBAL_DAILY_TURNS}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request, x_player_id: str = Header(default=""), x_client_token: str = Header(default="")):
    if CLIENT_TOKEN and x_client_token != CLIENT_TOKEN:
        raise HTTPException(status_code=403, detail="bad client token")
    if not x_player_id:
        raise HTTPException(status_code=400, detail="missing player id")
    if not UPSTREAM_API_KEY:
        raise HTTPException(status_code=500, detail="server key not configured")

    if _player_used(x_player_id) >= PLAYER_DAILY_TURNS:
        raise HTTPException(status_code=429, detail="daily quota reached")
    if _global_used() >= GLOBAL_DAILY_TURNS:
        raise HTTPException(status_code=429, detail="server budget reached")

    body = await request.json()
    messages = _clean_messages(body.get("messages") or [])
    if not messages:
        raise HTTPException(status_code=400, detail="empty messages")

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": min(1.2, max(0.0, float(body.get("temperature", 0.9)))),
        "top_p": min(1.0, max(0.05, float(body.get("top_p", 0.95)))),
        "presence_penalty": float(body.get("presence_penalty", 0.3)),
        "frequency_penalty": float(body.get("frequency_penalty", 0.4)),
        "max_tokens": min(MAX_OUTPUT_TOKENS, int(body.get("max_tokens", MAX_OUTPUT_TOKENS))),
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=40) as client:
        try:
            resp = await client.post(
                UPSTREAM_URL,
                headers={"Authorization": "Bearer " + UPSTREAM_API_KEY, "Content-Type": "application/json"},
                content=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            )
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="upstream unreachable")

    if resp.status_code >= 400:
        raise HTTPException(status_code=502, detail="upstream error %d" % resp.status_code)

    data = resp.json()
    usage = data.get("usage") or {}
    _charge(x_player_id, int(usage.get("total_tokens", 0) or 0))
    return data

/**
 * 旧信箱 · AI 中转 Worker（Cloudflare Workers）
 * ------------------------------------------------------------
 * 作用：把 DeepSeek 的密钥留在服务端，网页端只知道这个 Worker 的地址。
 * 部署：
 *   1. npm i -g wrangler
 *   2. wrangler login
 *   3. cd server && wrangler secret put DEEPSEEK_KEY   （粘贴 sk-... 那个 key）
 *   4. wrangler deploy
 *   5. 把输出的 https://xxx.workers.dev 填到 game/ai_web_config.json 的 api_url
 *
 * 限流：同一 IP 每天最多 DAILY_LIMIT 次请求，超出返回 429。
 * 前端收到 429 会显示“她今天有点累”，不会崩。
 */

const UPSTREAM = "https://api.deepseek.com/v1/chat/completions";
const DAILY_LIMIT = 300;      // 单 IP 每天条数
const ALLOW_ORIGINS = [
  "https://zhanpeng520.github.io",
  "http://localhost:8787",
  "http://127.0.0.1:8787",
];

// 简单的内存计数（Worker 实例内有效；跨实例不严格，但足够防刷）
const hits = new Map();

function corsHeaders(origin) {
  const allow = ALLOW_ORIGINS.includes(origin) ? origin : ALLOW_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, authorization",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = corsHeaders(origin);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== "POST") {
      return new Response("method not allowed", { status: 405, headers: cors });
    }

    // ---- 限流 ----
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const key = ip + "|" + today();
    const used = hits.get(key) || 0;
    if (used >= DAILY_LIMIT) {
      return new Response(
        JSON.stringify({ error: { message: "daily limit reached" } }),
        { status: 429, headers: { ...cors, "content-type": "application/json" } }
      );
    }
    hits.set(key, used + 1);

    // ---- 转发 ----
    let body;
    try {
      body = await request.text();
    } catch (e) {
      return new Response("bad body", { status: 400, headers: cors });
    }

    const upstream = await fetch(UPSTREAM, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + env.DEEPSEEK_KEY,
      },
      body,
    });

    const text = await upstream.text();
    return new Response(text, {
      status: upstream.status,
      headers: {
        ...cors,
        "content-type": upstream.headers.get("content-type") || "application/json",
      },
    });
  },
};

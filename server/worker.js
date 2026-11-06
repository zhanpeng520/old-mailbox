/**
 * 旧信箱 · Cloudflare Worker 版 AI 中转（零成本方案，免费额度每天 10 万次）
 * ------------------------------------------------------------
 * 作用：
 *   1) 密钥只存在 Worker 的 secret 里，网页包里没有 key；
 *   2) 给浏览器补 CORS 应答（Ren'Py Web 版用 renpy.fetch，跨域必须允许）；
 *   3) 顺手做基础防滥用（条数、长度、max_tokens 封顶）。
 *
 * 部署（3 分钟）：
 *   npm i -g wrangler
 *   wrangler login
 *   wrangler deploy server/worker.js --name old-mailbox-ai
 *   wrangler secret put DEEPSEEK_KEY      # 粘贴 sk-...
 * 可选：
 *   wrangler secret put CLIENT_TOKEN      # 与服务端用的弱口令一致
 *   wrangler secret put ALLOW_ORIGIN      # 默认 *，可填你的站点域名
 *
 * 部署完成后把 https://old-mailbox-ai.你的子域.workers.dev 填进 ai_web_config.json。
 */

const MAX_MESSAGES = 40;
const MAX_CHARS = 6000;
const MAX_OUTPUT_TOKENS = 400;

function corsHeaders(env) {
  return {
    "Access-Control-Allow-Origin": env.ALLOW_ORIGIN || "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Player-Id, X-Client-Token, X-Tracking-Id",
    "Access-Control-Max-Age": "86400",
    "Cache-Control": "no-store",
  };
}

function json(data, status, headers) {
  return new Response(JSON.stringify(data), {
    status,
    headers: Object.assign({ "Content-Type": "application/json; charset=utf-8" }, headers),
  });
}

function cleanMessages(raw) {
  const list = Array.isArray(raw) ? raw.slice(-MAX_MESSAGES) : [];
  const out = [];
  let total = 0;
  for (const item of list) {
    if (!item || typeof item !== "object") continue;
    const role = item.role;
    const content = item.content;
    if (!["system", "user", "assistant"].includes(role) || typeof content !== "string") continue;
    if (total + content.length > MAX_CHARS) break;
    total += content.length;
    out.push({ role, content });
  }
  return out;
}

export default {
  async fetch(request, env) {
    const cors = corsHeaders(env);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    const url = new URL(request.url);
    if (url.pathname.endsWith("/health")) {
      return json({ ok: true, model: env.UPSTREAM_MODEL || "deepseek-flash" }, 200, cors);
    }

    if (request.method !== "POST") {
      return json({ error: "method not allowed" }, 405, cors);
    }

    if (env.CLIENT_TOKEN && request.headers.get("X-Client-Token") !== env.CLIENT_TOKEN) {
      return json({ error: "bad client token" }, 403, cors);
    }

    let body;
    try {
      body = await request.json();
    } catch (e) {
      return json({ error: "bad json" }, 400, cors);
    }

    const messages = cleanMessages(body.messages);
    if (!messages.length) return json({ error: "empty messages" }, 400, cors);

    const payload = {
      model: env.UPSTREAM_MODEL || "deepseek-flash",
      messages,
      temperature: Math.min(1.2, Math.max(0, Number(body.temperature) || 0.9)),
      top_p: Math.min(1, Math.max(0.05, Number(body.top_p) || 0.95)),
      presence_penalty: Number(body.presence_penalty) || 0,
      frequency_penalty: Number(body.frequency_penalty) || 0,
      max_tokens: Math.min(MAX_OUTPUT_TOKENS, Number(body.max_tokens) || MAX_OUTPUT_TOKENS),
      stream: false,
    };

    // 闲聊不思考，省一半以上输出 token
    if (env.REASONING === "off" || env.REASONING === undefined) {
      payload.thinking = { type: "disabled" };
    }

    let upstream;
    try {
      upstream = await fetch(env.UPSTREAM_URL || "https://api.deepseek.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + env.DEEPSEEK_KEY,
        },
        body: JSON.stringify(payload),
      });
    } catch (e) {
      return json({ error: "upstream unreachable" }, 502, cors);
    }

    if (!upstream.ok) {
      const detail = await upstream.text();
      return json({ error: "upstream error", status: upstream.status, detail: detail.slice(0, 300) }, 502, cors);
    }

    const data = await upstream.json();
    return json(data, 200, cors);
  },
};

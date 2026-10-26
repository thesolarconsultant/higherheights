// POST /api/enquiry — validates an enquiry and emails it to the studio via Resend.
//
// Environment variables (Vercel → Settings → Environment Variables):
//   RESEND_API_KEY       required. https://resend.com
//   ENQUIRY_FROM         required for production, e.g. "Higher Heights <enquiries@higherheights.studio>"
//                        (the sending domain must be verified in Resend). Falls back to Resend's onboarding sender.
//   ENQUIRY_TO           optional, defaults to hello@higherheights.studio
//   TURNSTILE_SECRET_KEY optional. When set, a valid Cloudflare Turnstile token is required.
//   TURNSTILE_SITE_KEY   optional, used at build time to render the widget.

const TO = process.env.ENQUIRY_TO || "hello@higherheights.studio";
const FROM = process.env.ENQUIRY_FROM || "Higher Heights <onboarding@resend.dev>";
const MIN_FILL_MS = 2500;
const MAX_PER_HOUR = 5;
const hits = new Map(); // best-effort per-instance limiter; Turnstile is the real backstop

const clean = (v, max) => String(v ?? "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max);
const oneLine = (v, max) => clean(v, max).replace(/[\r\n]+/g, " ");
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function limited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < 3600_000);
  list.push(now);
  hits.set(ip, list);
  if (hits.size > 500) for (const [k, v] of hits) if (!v.some((t) => now - t < 3600_000)) hits.delete(k);
  return list.length > MAX_PER_HOUR;
}

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = [];
  let size = 0;
  for await (const c of req) {
    size += c.length;
    if (size > 50_000) throw new Error("too large");
    chunks.push(c);
  }
  const raw = Buffer.concat(chunks).toString("utf8");
  if ((req.headers["content-type"] || "").includes("application/json")) return JSON.parse(raw || "{}");
  const params = new URLSearchParams(raw);
  const out = {};
  for (const k of new Set(params.keys())) out[k] = k === "services" ? params.getAll(k) : params.get(k);
  return out;
}

export default async function handler(req, res) {
  const wantsJson = (req.headers.accept || "").includes("application/json");
  const fail = (code, error) => {
    if (wantsJson) return res.status(code).json({ ok: false, error });
    res.status(code).setHeader("Content-Type", "text/html; charset=utf-8");
    return res.end(`<!doctype html><meta charset="utf-8"><title>Enquiry</title><body style="font-family:system-ui;padding:2rem;max-width:36rem"><p>${esc(error)}</p><p><a href="/contact">Back to the form</a></p>`);
  };
  const ok = () => {
    if (wantsJson) return res.status(200).json({ ok: true });
    res.statusCode = 303;
    res.setHeader("Location", "/contact?sent=1");
    return res.end();
  };

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return fail(405, "Method not allowed.");
  }

  // Same-site only
  const origin = req.headers.origin;
  if (origin) {
    try {
      if (new URL(origin).host !== req.headers.host) return fail(403, "Forbidden.");
    } catch {
      return fail(403, "Forbidden.");
    }
  }

  let body;
  try {
    body = await readBody(req);
  } catch {
    return fail(400, "That request could not be read.");
  }

  // Spam: honeypot and too-fast submissions look like success to the sender.
  const tooFast = body.t && Date.now() - Number(body.t) < MIN_FILL_MS;
  if (clean(body.website, 200) || tooFast) return ok();

  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return fail(429, "Too many enquiries from this connection. Please email hello@higherheights.studio.");

  const name = oneLine(body.name, 120);
  const email = oneLine(body.email, 200);
  const company = oneLine(body.company, 160);
  const message = clean(body.message, 3000);
  const timing = oneLine(body.timing, 60);
  const budget = oneLine(body.budget, 60);
  const services = (Array.isArray(body.services) ? body.services : body.services ? [body.services] : [])
    .map((s) => oneLine(s, 60))
    .filter(Boolean)
    .slice(0, 10);

  if (!name) return fail(400, "Please tell me your name.");
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return fail(400, "Please enter a valid email address so I can reply.");
  if (message.length < 10) return fail(400, "Tell me a little more about the project (a sentence or two).");

  if (process.env.TURNSTILE_SECRET_KEY) {
    const token = clean(body.token || body["cf-turnstile-response"], 4096);
    const r = token
      ? await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
          method: "POST",
          body: new URLSearchParams({ secret: process.env.TURNSTILE_SECRET_KEY, response: token, remoteip: ip }),
        })
          .then((x) => x.json())
          .catch(() => ({}))
      : {};
    if (!r.success) return fail(400, "The spam check failed. Please try again.");
  }

  if (!process.env.RESEND_API_KEY) {
    console.error("enquiry: RESEND_API_KEY is not set");
    return fail(503, "The form isn't connected yet. Please email hello@higherheights.studio and I'll reply directly.");
  }

  const lines = [
    ["Name", name],
    ["Email", email],
    ["Company", company || "—"],
    ["Services", services.join(", ") || "—"],
    ["Timing", timing || "—"],
    ["Budget", budget || "—"],
  ];
  const text = lines.map(([k, v]) => `${k}: ${v}`).join("\n") + `\n\n${message}\n`;
  const html =
    `<table cellpadding="6" style="font-family:system-ui;font-size:15px">${lines.map(([k, v]) => `<tr><td><b>${k}</b></td><td>${esc(v)}</td></tr>`).join("")}</table>` +
    `<p style="font-family:system-ui;font-size:15px;white-space:pre-wrap">${esc(message)}</p>`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: FROM,
      to: [TO],
      reply_to: email,
      subject: `New enquiry — ${name}${company ? ` (${company})` : ""}`.slice(0, 150),
      text,
      html,
    }),
  }).catch(() => null);

  if (!r || !r.ok) {
    console.error("enquiry: send failed", r && r.status, r && (await r.text().catch(() => "")));
    return fail(502, "That didn't send. Please email hello@higherheights.studio and I'll reply directly.");
  }
  return ok();
}

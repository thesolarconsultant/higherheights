// Static site generator for Higher Heights. No dependencies.
// Reads data/*.json, writes dist/. Edit a project in data/projects.json and rebuild.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dist = path.join(root, "dist");
const site = JSON.parse(fs.readFileSync(path.join(root, "data/site.json"), "utf8"));
const projects = JSON.parse(fs.readFileSync(path.join(root, "data/projects.json"), "utf8"));

const BASE = (
  process.env.SITE_URL ||
  (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : "https://higher-heights.vercel.app")
).replace(/\/$/, "");
const TURNSTILE = process.env.TURNSTILE_SITE_KEY || "";

const esc = (s = "") => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const abs = (p) => (p.startsWith("http") ? p : BASE + p);
const A = (p) => `/assets/${p}`;
const isLand = (p) => p.width > p.height;
const ratio = (p) => `${p.width}/${p.height}`;
const meta = (p) => [p.client, p.tag || p.sector, p.year].filter(Boolean).join(" · ");
const bySlug = (s) => projects.find((p) => p.slug === s);

// ── asset hashing so CSS/JS cache busts on change ────────────
const css = fs.readFileSync(path.join(root, "src/css/site.css"), "utf8");
const js = fs.readFileSync(path.join(root, "src/js/site.js"), "utf8");
const h = (s) => crypto.createHash("md5").update(s).digest("hex").slice(0, 8);
const CSS = `/css/site.css?v=${h(css)}`;
const JS = `/js/site.js?v=${h(js)}`;

// ── shared pieces ────────────────────────────────────────────
const NAV = [
  ["/work", "Work"],
  ["/expertise", "Expertise"],
  ["/studio", "Studio"],
];

function header(cur, theme = "dark") {
  const link = (href, label, cls = "") =>
    `<a href="${href}" class="mono ${cls}"${cur === href ? ' aria-current="page"' : ""}>${label}</a>`;
  return `<header class="head"><div class="wrap head__in">
  <a class="head__logo" href="/" aria-label="Higher Heights — home"><img src="${A(theme === "light" ? "img/hh-navy.svg" : "img/hh-cream.svg")}" alt="" width="38" height="46"><span class="mono">Higher Heights</span></a>
  <button class="head__btn mono" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="head__nav" id="nav" aria-label="Primary">
    ${NAV.map(([href, label]) => link(href, label)).join("\n    ")}
    ${link("/contact", "Start a project", "head__cta")}
  </nav>
</div></header>`;
}

function footer() {
  return `<footer class="wrap foot">
  <div class="foot__brand"><img src="${A("img/wordmark-cream.svg")}" width="1600" height="357" alt="Higher Heights — Film, Aerial, Photography" loading="lazy">
    <p class="mono dim">${esc(site.tagline)}</p></div>
  <nav aria-label="Site" class="mono"><a href="/work">Work</a><a href="/expertise">Expertise</a><a href="/studio">Studio</a><a href="/contact">Contact</a></nav>
  <div class="mono"><a href="mailto:${site.email}">${site.email}</a><br><span class="dim">London · Worldwide · Booking 2026</span></div>
  <div class="mono dim">© 2026 ${esc(site.legalName)}<br>Est. ${site.established} · <a href="/privacy">Privacy</a></div>
</footer>`;
}

function page({ path: p, title, desc, headTheme = "dark", body, ld = [], image, type = "website", noindex = false }) {
  const url = abs(p === "/" ? "/" : p);
  const img = abs(image || A("img/poster-hero.jpg"));
  const fullTitle = p === "/" ? title : `${title} — Higher Heights`;
  const graph = ld.length ? `<script type="application/ld+json">${JSON.stringify(ld.length === 1 ? ld[0] : ld)}</script>` : "";
  return `<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${url}">
${noindex ? '<meta name="robots" content="noindex">' : ""}
<meta name="theme-color" content="#0C0D0C">
<meta property="og:type" content="${type}">
<meta property="og:site_name" content="Higher Heights">
<meta property="og:title" content="${esc(fullTitle)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="${A("img/hh-gold.svg")}" type="image/svg+xml">
<link rel="apple-touch-icon" href="${A("img/icon-180.png")}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;500;600;700&family=DM+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="${CSS}">
<script>document.documentElement.className="js"</script>
${graph}
</head>
<body data-head="${headTheme}">
<a class="skip" href="#main">Skip to content</a>
${header(p, headTheme)}
<main id="main">
${body}
</main>
<script src="${JS}" defer></script>
${TURNSTILE && p === "/contact" ? '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>' : ""}
</body>
</html>
`;
}

// ── components ───────────────────────────────────────────────
function filmTile(p, { idx, cls = "", eager = false } = {}) {
  return `<a class="film ${cls}" href="/work/${p.slug}" aria-label="${esc(p.title)}${p.client ? ", " + esc(p.client) : ""}, ${esc(p.tag || p.sector)}, ${p.year}">
  <div class="film__frame" style="--ar:${ratio(p)}">
    <img src="${A("img/" + p.poster)}" alt="${esc(p.alt)}" width="${p.width}" height="${p.height}" ${eager ? "" : 'loading="lazy"'} decoding="async">
    <video muted loop playsinline preload="none" data-src="${A("vid/" + p.video)}" aria-hidden="true" tabindex="-1"></video>
    ${idx ? `<span class="film__idx mono">${String(idx).padStart(2, "0")}</span>` : ""}
  </div>
  <div class="film__cap"><span class="film__title">${esc(p.title)}</span><span class="film__meta mono dim">${esc(meta(p))}</span></div>
</a>`;
}

function clientsBlock() {
  return `<div class="clients__grid">
${site.clients
  .map(
    (c) =>
      `<div class="client" style="--tint:${c.tint}"><span class="client__mark" role="img" aria-label="${esc(c.name)}" style="width:${c.w}px;height:${c.h}px;-webkit-mask-image:url(${A("img/clients/" + c.file)});mask-image:url(${A("img/clients/" + c.file)})"></span></div>`
  )
  .join("\n")}
</div>`;
}

function closing(title = "Have something<br>worth filming?") {
  return `<section class="dark closing" aria-labelledby="close-h"><div class="wrap">
  <h2 id="close-h" class="d-xxl reveal">${title}</h2>
  <div class="closing__row"><p>A launch, a delivery, a restoration coming off the bench. Tell me what it is and when it happens.</p>
  <a class="btn" href="/contact">Start a project <span aria-hidden="true">→</span></a></div>
  ${footer()}
</div></section>`;
}

const orgLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": BASE + "/#org",
  name: site.legalName,
  alternateName: site.name,
  url: BASE + "/",
  logo: abs(A("img/icon-180.png")),
  email: site.email,
  description: site.description,
  foundingDate: String(site.established),
  areaServed: "Worldwide",
  address: { "@type": "PostalAddress", addressLocality: "London", addressCountry: "GB" },
  founder: { "@type": "Person", name: site.founder, jobTitle: "Director & Photographer" },
};

// ── pages ────────────────────────────────────────────────────
const pages = {};

// HOME
{
  const curated = ["heritage", "styled-by-you", "in-the-case", "rm-69"].map(bySlug);
  const idxOf = (p) => projects.indexOf(p) + 1;
  pages["/"] = page({
    path: "/",
    title: "Higher Heights — Film, aerial and photography studio",
    desc: "Higher Heights is a film and photography studio working across fashion, luxury, automotive and sport. Directed by Morgan. London based, filming worldwide.",
    image: A("img/poster-hero.jpg"),
    ld: [orgLd, { "@context": "https://schema.org", "@type": "WebSite", name: site.name, url: BASE + "/", publisher: { "@id": BASE + "/#org" } }],
    body: `
<section class="dark hero" aria-label="Introduction">
  <div class="hero__stage">
    <img src="${A("img/poster-commercial.jpg")}" alt="" width="1920" height="1080" fetchpriority="high">
    <video id="heroVideo" muted loop playsinline preload="none" data-src="${A("vid/commercial.mp4")}" aria-hidden="true" tabindex="-1"></video>
    <span class="tick tick--tl mono">Reel · Autoplay · Muted</span>
    <span class="tick tick--tr mono" id="tc" aria-hidden="true">00:00:00:00</span>
    <span class="tick tick--bl mono live">Available for commission</span>
    <span class="tick tick--br mono">London · Worldwide</span>
    <h1 class="hero__word d-xxl"><span><i>Higher</i></span><span><i>Heights</i></span></h1>
  </div>
  <div class="hero__foot">
    <p>A film and photography studio for the brands that build things.</p>
    <span class="mono dim">Directed by ${site.founder} · Est. ${site.established}</span>
  </div>
</section>

<section class="paper sect statement" aria-labelledby="st-h"><div class="wrap grid">
  <p class="mono dim eyebrow" style="grid-column:1/-1">The studio</p>
  <h2 id="st-h" class="d-1 reveal">The difference between footage and a film is the decision behind <em>every single frame.</em></h2>
  <div class="text reveal lead">
    <p>Higher Heights is a film and photography studio working across fashion, luxury, automotive and sport — on set with brands, agencies and the occasional very particular private client.</p>
    <p>Every project starts the same way: find the frame that actually says something, then build the story around it.</p>
  </div>
</div></section>

<section class="bone sect" aria-labelledby="wk-h"><div class="wrap">
  <div class="sect-head"><h2 id="wk-h" class="d-2">Selected work</h2><span class="mono dim">2024 — 2026 · ${projects.length} films</span></div>
  <div class="grid curated">
    ${curated.map((p) => filmTile(p, { idx: idxOf(p), cls: "reveal" })).join("\n    ")}
  </div>
  <p style="margin-top:clamp(2.4rem,5vw,4.5rem)"><a class="link mono" href="/work">All ${projects.length} films <span aria-hidden="true">→</span></a></p>
</div></section>

<section class="dark sect" aria-labelledby="ex-h"><div class="wrap grid" style="row-gap:3rem">
  <div class="ex-h"><p class="mono sage eyebrow">Expertise</p><h2 id="ex-h" class="d-2" style="margin-top:1.2rem">Five disciplines, one set of eyes.</h2></div>
  <ol class="index ex-l">
    ${site.expertise
      .map(
        (e, i) => `<li><a href="/expertise#${e.id}"><span class="mono sage">${String(i + 1).padStart(2, "0")}</span><span class="index__name">${esc(e.name)}</span><span class="mono dim" aria-hidden="true">→</span></a></li>`
      )
      .join("\n    ")}
  </ol>
</div></section>

<section class="dark clients" aria-labelledby="cl-h" style="padding-bottom:var(--sect)"><div class="wrap rule" style="padding-top:var(--sect)">
  <div class="sect-head"><h2 id="cl-h" class="mono dim">Selected clients</h2></div>
  ${clientsBlock()}
  <ul class="names mono dim" aria-label="More clients">${site.clientNames.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>
</div></section>

<section class="bone sect" aria-labelledby="fd-h"><div class="wrap grid founder">
  <figure class="founder__img clip"><img src="${A("img/portrait.jpg")}" alt="Morgan, founder of Higher Heights, photographed on a London street" width="564" height="677" loading="lazy" decoding="async"></figure>
  <div class="founder__txt">
    <p class="mono dim eyebrow">Studio</p>
    <h2 id="fd-h" class="d-1">One pair of eyes on the whole thing.</h2>
    <div class="text lead"><p>Higher Heights is run by <strong>Morgan</strong> — a filmmaker and photographer who shoots, directs and edits the majority of the work himself. That means the idea that gets signed off is the idea that gets shot, and the person cutting it was in the room when it was conceived.</p></div>
    <p class="quote">“If it doesn't earn its place in the cut, it doesn't go in.”</p>
    <p><a class="link mono" href="/studio">About the studio <span aria-hidden="true">→</span></a></p>
  </div>
</div></section>

<section class="dark" style="padding-block:clamp(3rem,6vw,6rem)" aria-label="Behind the scenes"><div class="wrap">
  <figure class="bts"><img class="clip" src="${A("img/matchroom-1.jpg")}" alt="Filming ringside at a Matchroom Boxing event" width="1200" height="800" loading="lazy" decoding="async">
  <figcaption><span class="film__title">Matchroom Boxing</span><span class="mono dim">Ringside · Event coverage · 2025</span></figcaption></figure>
</div></section>

${closing()}`,
  });
}

// WORK INDEX
{
  const sectors = [...new Set(projects.map((p) => p.tag || p.sector))];
  pages["/work"] = page({
    path: "/work",
    title: "Work",
    desc: `Selected films and stills by Higher Heights: automotive, luxury, product, sport, brand and event work, 2024 to 2026.`,
    headTheme: "light",
    ld: [{ "@context": "https://schema.org", "@type": "CollectionPage", name: "Work — Higher Heights", url: BASE + "/work" }],
    body: `
<section class="paper pagehead"><div class="wrap">
  <p class="mono dim eyebrow">Selected work · 2024 — 2026</p>
  <h1 class="d-xxl">Eight films,<br>five disciplines.</h1>
  <p class="lead measure dim">Eight films from a wider reel — longer cuts, campaign variants and references for any sector are available on request.</p>
</div></section>
<section class="paper" style="padding-bottom:var(--sect)"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter by discipline">
    <button class="chip mono" type="button" data-filter="all" aria-pressed="true">All</button>
    ${sectors.map((s) => `<button class="chip mono" type="button" data-filter="${esc(s)}" aria-pressed="false">${esc(s)}</button>`).join("\n    ")}
  </div>
  <div class="grid workgrid" id="workgrid">
    ${projects
      .map((p, i) => filmTile(p, { idx: i + 1, cls: `${isLand(p) ? "is-land" : ""} reveal`, eager: i < 2 }).replace('<a class="film', `<a data-cat="${esc(p.tag || p.sector)}" class="film`))
      .join("\n    ")}
    <div class="tail"><span class="mono dim">End of selection</span><p class="lead">Longer cuts, campaign variants and references for any sector are available on request.</p><p><a class="link mono" href="/contact">Request the full reel <span aria-hidden="true">→</span></a></p></div>
  </div>
</div></section>
${closing()}`,
  });
}

// PROJECT PAGES
projects.forEach((p, i) => {
  const next = projects[(i + 1) % projects.length];
  const related = projects
    .filter((o) => o.slug !== p.slug)
    .sort((a, b) => (b.sector === p.sector) - (a.sector === p.sector) || Math.abs(a.year - p.year) - Math.abs(b.year - p.year))
    .slice(0, 3);
  const ogFile = path.join(root, "assets/og", p.slug + ".jpg");
  const image = fs.existsSync(ogFile) ? A(`og/${p.slug}.jpg`) : A("img/" + p.poster);
  const desc = `${p.title} — ${p.tag || p.sector} film${p.client ? " for " + p.client : ""}, ${p.year}. A Higher Heights film.`;
  const facts = [
    p.client && ["Client", p.client],
    ["Sector", p.tag ? `${p.sector} · ${p.tag}` : p.sector],
    ["Year", p.year],
    ["Format", isLand(p) ? "Landscape 16:9" : "Vertical 9:16"],
    p.services.length && ["Services", p.services.join(", ")],
    ...p.credits.map((c) => [c.role, c.name]),
  ].filter(Boolean);
  const metaHtml = `<dl class="meta">${facts.map(([k, v]) => `<div><dt class="mono dim">${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>`;
  const player = `<div class="player" style="--ar:${ratio(p)}" data-player>
    <img src="${A("img/" + p.poster)}" alt="${esc(p.alt)}" width="${p.width}" height="${p.height}" fetchpriority="high">
    <video controls playsinline preload="none" data-src="${A("vid/" + p.video)}" poster="${A("img/" + p.poster)}" aria-label="${esc(p.title)} — film" hidden></video>
    <button class="player__btn" type="button" aria-label="Play ${esc(p.title)}"><span><svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><path d="M8 5l13 8-13 8z" fill="currentColor"/></svg></span></button>
    <span class="tick tick--tl mono">${String(i + 1).padStart(2, "0")} / ${String(projects.length).padStart(2, "0")}</span>
  </div>`;
  pages[`/work/${p.slug}`] = page({
    path: `/work/${p.slug}`,
    title: `${p.title}${p.client ? " — " + p.client : ""}`,
    desc,
    image,
    type: "video.other",
    ld: [
      {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        name: p.title,
        description: desc,
        thumbnailUrl: abs(A("img/" + p.poster)),
        contentUrl: abs(A("vid/" + p.video)),
        uploadDate: String(p.year),
        creator: { "@id": BASE + "/#org" },
      },
      {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Work", item: BASE + "/work" },
          { "@type": "ListItem", position: 2, name: p.title, item: BASE + "/work/" + p.slug },
        ],
      },
    ],
    body: `
<section class="dark proj"><div class="wrap">
  <div class="proj__nav mono"><a href="/work">← Work</a><span class="dim">${String(i + 1).padStart(2, "0")} / ${String(projects.length).padStart(2, "0")}</span><a href="/work/${next.slug}">Next: ${esc(next.title)} →</a></div>
  <h1 class="d-xxl">${esc(p.title)}</h1>
  <div class="proj__sub mono"><span class="sage">${esc(meta(p))}</span><span class="dim">Film${p.gallery.length ? " · Stills" : ""}</span></div>
</div></section>
${
  isLand(p)
    ? `<section class="dark stage"><div class="wrap">${player}</div></section>
<section class="paper sect"><div class="wrap grid"><div style="grid-column:1/span 4">${metaHtml}</div>${
        p.brief ? `<div style="grid-column:6/span 7"><p class="brief">${esc(p.brief)}</p></div>` : ""
      }</div></section>`
    : `<section class="dark stage"><div class="wrap stage--v">${player}<div class="stage__meta">${metaHtml}${
        p.brief ? `<p class="brief" style="margin-top:2rem">${esc(p.brief)}</p>` : ""
      }</div></div></section>`
}
${
  p.gallery.length
    ? `<section class="bone sect" aria-label="Stills"><div class="wrap"><div class="gallery">${p.gallery
        .map((g) => `<img class="clip" src="${A("img/" + g.src)}" alt="${esc(g.alt)}" width="${g.width}" height="${g.height}" loading="lazy" decoding="async">`)
        .join("")}</div></div></section>`
    : ""
}
<section class="dark sect" aria-labelledby="rel-h"><div class="wrap">
  <div class="sect-head"><h2 id="rel-h" class="d-2">More work</h2><a class="link mono" href="/work">All films →</a></div>
  <div class="related">${related.map((r) => filmTile(r, { idx: projects.indexOf(r) + 1 })).join("")}</div>
</div></section>
${closing()}`,
  });
});

// EXPERTISE
{
  const rel = {
    "brand-films": ["styled-by-you", "walking", "face-of-aging", "heritage"],
    aerial: ["highland-road"],
    product: ["rm-69", "in-the-case"],
    events: ["morning-ritual"],
    social: [],
  };
  const relHtml = (id) =>
    rel[id].length
      ? `<p class="mono dim" style="margin-top:2rem">Related work</p><p style="margin-top:.6rem">${rel[id]
          .map((s) => `<a class="link" style="margin:0 1.2rem .6rem 0" href="/work/${s}">${esc(bySlug(s).title)}</a>`)
          .join("")}</p>`
      : "";
  const aerial = [
    ["aerial-cypress.jpg", "Aerial view of a Mediterranean estate at golden hour with a long banquet table running between cypress trees", 1800, 3200, "Estate · Golden hour"],
    ["aerial-villa.jpg", "Top-down aerial of a villa estate with a cypress-lined approach drive", 1800, 1012, "Venue · Approach"],
    ["aerial-night.jpg", "Night aerial of a lit estate with an event set out along the front drive", 1800, 3200, "Event · After dark"],
  ];
  pages["/expertise"] = page({
    path: "/expertise",
    title: "Expertise",
    desc: "Brand films, commercials, aerial, product and stills, event coverage and social cutdowns from Higher Heights, a film and photography studio in London.",
    headTheme: "light",
    ld: [{ "@context": "https://schema.org", "@type": "Service", serviceType: "Film and photography production", provider: { "@id": BASE + "/#org" }, areaServed: "Worldwide" }],
    body: `
<section class="paper pagehead"><div class="wrap">
  <p class="mono dim eyebrow">Expertise</p>
  <h1 class="d-xxl">Five disciplines,<br>one set of eyes.</h1>
  <p class="lead measure dim">The studio moves between brand films, commercials, product, aerial and event coverage. What stays constant is a preference for restraint: fewer setups, better chosen, and a cut that trusts the viewer.</p>
</div></section>
<section class="paper"><div class="wrap">
  <article class="svc" id="brand-films"><div class="svc__h"><p class="mono dim">01</p><h2 class="d-1">Brand films &amp; commercials</h2></div>
    <div class="svc__b text lead"><p>Story-led films for brands, agencies and the occasional very particular private client, across fashion, luxury, automotive and sport.</p>${relHtml("brand-films")}</div></article>

  <article class="svc" id="aerial"><div class="svc__h"><p class="mono dim">02</p><h2 class="d-1">Aerial</h2><p class="mono sage" style="margin-top:1rem">Aerial unit · Shot from above</p></div>
    <div class="svc__b"><div class="text lead"><p>Drone and ground units shooting in tandem — one continuous move from the air to eye level, so the film never has to cut to prove the scale.</p><p>Used for architectural reveals, estate and venue coverage, automotive and landscape work, and event films where the geography is the story.</p></div>
    <dl class="specs mono"><div><dt class="dim">Formats</dt><dd>4K · 6K · Vertical</dd></div><div><dt class="dim">Deployment</dt><dd>UK · Europe · Worldwide</dd></div><div><dt class="dim">Pairing</dt><dd>Aerial + ground</dd></div><div><dt class="dim">Delivery</dt><dd>Graded · Captioned</dd></div></dl>
    ${relHtml("aerial")}</div>
    <div class="strip" style="grid-column:1/-1">${aerial
      .map(([f, alt, w, hh, cap]) => `<figure><img class="clip" src="${A("img/" + f)}" alt="${esc(alt)}" width="${w}" height="${hh}" loading="lazy" decoding="async"><figcaption class="mono dim" style="margin-top:.6rem">${cap}</figcaption></figure>`)
      .join("")}</div></article>

  <article class="svc" id="product"><div class="svc__h"><p class="mono dim">03</p><h2 class="d-1">Product &amp; stills</h2></div>
    <div class="svc__b"><div class="text lead"><p>Movement, up close. Macro and studio work, with stills and product film from the Richard Mille RM 69 shoot.</p></div>${relHtml("product")}</div>
    <div class="strip" style="grid-column:1/-1">${bySlug("rm-69")
      .gallery.slice(0, 4)
      .map((g) => `<img class="clip" src="${A("img/" + g.src)}" alt="${esc(g.alt)}" width="${g.width}" height="${g.height}" loading="lazy" decoding="async">`)
      .join("")}</div></article>

  <article class="svc" id="events"><div class="svc__h"><p class="mono dim">04</p><h2 class="d-1">Events &amp; coverage</h2></div>
    <div class="svc__b"><div class="text lead"><p>Ringside, backstage, after dark. Event films and coverage, delivered with every ratio the campaign needs.</p></div>${relHtml("events")}
    <figure style="margin-top:2rem"><img class="clip" src="${A("img/matchroom-1.jpg")}" alt="Filming ringside at a Matchroom Boxing event" width="1200" height="800" loading="lazy" decoding="async" style="width:100%;height:auto"><figcaption class="mono dim" style="margin-top:.6rem">Matchroom Boxing · Ringside · Event coverage · 2025</figcaption></figure></div></article>

  <article class="svc" id="social"><div class="svc__h"><p class="mono dim">05</p><h2 class="d-1">Social cutdowns</h2></div>
    <div class="svc__b text lead"><p>Master plus every ratio and cutdown the campaign actually needs, edited, graded and captioned.</p></div></article>
</div></section>

<section class="dark sect" aria-labelledby="pr-h"><div class="wrap">
  <div class="sect-head"><h2 id="pr-h" class="d-2">How a project runs</h2><span class="mono dim">Four steps</span></div>
  <ol class="steps">${site.process.map((s) => `<li><span class="mono sage">${s.n}</span><h3>${esc(s.name)}</h3><p>${esc(s.text)}</p></li>`).join("")}</ol>
</div></section>
${closing()}`,
  });
}

// STUDIO
{
  pages["/studio"] = page({
    path: "/studio",
    title: "Studio",
    desc: "Higher Heights is run by Morgan, a filmmaker and photographer who shoots, directs and edits the majority of the work himself. London based, filming worldwide.",
    headTheme: "light",
    ld: [{ "@context": "https://schema.org", "@type": "AboutPage", url: BASE + "/studio", about: { "@id": BASE + "/#org" } }],
    body: `
<section class="paper pagehead"><div class="wrap">
  <p class="mono dim eyebrow">Studio</p>
  <h1 class="d-xxl">One pair of eyes on the whole thing.</h1>
</div></section>
<section class="paper" style="padding-bottom:var(--sect)"><div class="wrap grid founder">
  <figure class="founder__img clip"><img src="${A("img/portrait.jpg")}" alt="Morgan, founder of Higher Heights, photographed on a London street" width="564" height="677" decoding="async"><figcaption class="mono dim" style="margin-top:.7rem">Morgan — Founder · Director</figcaption></figure>
  <div class="founder__txt">
    <div class="text lead"><p>Higher Heights is run by <strong>Morgan</strong> — a filmmaker and photographer who shoots, directs and edits the majority of the work himself. That means the idea that gets signed off is the idea that gets shot, and the person cutting it was in the room when it was conceived.</p>
    <p>The studio moves between brand films, commercials, product, aerial and event coverage. What stays constant is a preference for restraint: fewer setups, better chosen, and a cut that trusts the viewer.</p></div>
    <p class="quote">“If it doesn't earn its place in the cut, it doesn't go in.”</p>
    <div class="tags mono">${["Brand films", "Commercials", "Aerial", "Product", "Events", "Social cutdowns", "Stills"].map((t) => `<span>${t}</span>`).join("")}</div>
  </div>
</div></section>
<section class="dark sect" aria-labelledby="pr-h"><div class="wrap">
  <div class="sect-head"><h2 id="pr-h" class="d-2">How a project runs</h2><span class="mono dim">Four steps</span></div>
  <ol class="steps">${site.process.map((s) => `<li><span class="mono sage">${s.n}</span><h3>${esc(s.name)}</h3><p>${esc(s.text)}</p></li>`).join("")}</ol>
</div></section>
<section class="dark" style="padding-bottom:var(--sect)"><div class="wrap rule" style="padding-top:var(--sect)">
  <div class="sect-head"><h2 class="mono dim">Selected clients</h2></div>
  ${clientsBlock()}
  <ul class="names mono dim" aria-label="More clients">${site.clientNames.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>
</div></section>
<section class="dark" style="padding-bottom:clamp(3rem,6vw,6rem)"><div class="wrap">
  <figure class="bts"><img class="clip" src="${A("img/matchroom-1.jpg")}" alt="Filming ringside at a Matchroom Boxing event" width="1200" height="800" loading="lazy" decoding="async">
  <figcaption><span class="film__title">Matchroom Boxing</span><span class="mono dim">Ringside · Event coverage · 2025</span></figcaption></figure>
</div></section>
${closing()}`,
  });
}

// CONTACT
{
  const opt = (type, name, value, label) =>
    `<label class="opt"><input type="${type}" name="${name}" value="${esc(value)}"><span class="mono">${esc(label || value)}</span></label>`;
  pages["/contact"] = page({
    path: "/contact",
    title: "Contact",
    desc: "Start a project with Higher Heights. Tell Morgan what you are making, when it happens and roughly what you are working with. First reply within a day.",
    ld: [{ "@context": "https://schema.org", "@type": "ContactPage", url: BASE + "/contact", about: { "@id": BASE + "/#org" } }],
    body: `
<section class="dark pagehead"><div class="wrap">
  <p class="mono sage eyebrow">Contact</p>
  <h1 class="d-1" style="max-width:14ch">Have something worth filming?</h1>
</div></section>
<section class="dark" style="padding-bottom:var(--sect)"><div class="wrap grid contact">
  <aside class="contact__info">
    <p class="lead">A launch, a delivery, a restoration coming off the bench. Tell me what it is and when it happens.</p>
    <p style="margin-top:1.6rem"><a class="link" href="mailto:${site.email}">${site.email}</a></p>
    <dl class="facts mono">
      <div><dt class="dim">Based</dt><dd>London</dd></div>
      <div><dt class="dim">Available</dt><dd>Worldwide</dd></div>
      <div><dt class="dim">Booking</dt><dd>2026 — open</dd></div>
      <div><dt class="dim">First reply</dt><dd>From Morgan, within a day</dd></div>
    </dl>
  </aside>
  <div class="contact__form">
    <div class="sent" id="sent" hidden tabindex="-1"><h2 class="d-2">Thank you.</h2><p class="lead" style="margin-top:1rem">Your enquiry has reached the studio. The reply comes from Morgan, not an autoresponder, usually within a day.</p></div>
    <form id="enq" method="post" action="/api/enquiry" novalidate>
      <fieldset class="fs"><legend class="mono sage">1 · What are we making?</legend>
        <div class="opts">
          ${["Brand film", "Commercial", "Automotive", "Aerial", "Product or stills", "Event coverage", "Social cutdowns", "Something else"].map((s) => opt("checkbox", "services", s)).join("\n          ")}
        </div></fieldset>
      <label class="field"><span class="mono sage">2 · Tell me about it</span><textarea name="message" required minlength="10" maxlength="3000" placeholder="What it is, where, and what the film has to do."></textarea></label>
      <fieldset class="fs"><legend class="mono sage">3 · When does it happen?</legend>
        <div class="opts">${["Within a month", "One to three months", "Later this year", "Still deciding"].map((s) => opt("radio", "timing", s)).join("")}</div></fieldset>
      <fieldset class="fs"><legend class="mono sage">4 · Roughly what are you working with?</legend>
        <div class="opts">${["Under £5,000", "£5,000 – £10,000", "£10,000 – £20,000", "£20,000 – £50,000", "£50,000+", "Not sure yet"].map((s) => opt("radio", "budget", s)).join("")}</div>
        <p class="mono dim" style="margin-top:.8rem">A range is enough. It only helps me shape the right approach.</p></fieldset>
      <div class="two">
        <label class="field"><span class="mono sage">Name</span><input name="name" autocomplete="name" required maxlength="120"></label>
        <label class="field"><span class="mono sage">Email</span><input name="email" type="email" autocomplete="email" required maxlength="200" placeholder="you@company.com"></label>
      </div>
      <label class="field"><span class="mono sage">Company or brand <span class="dim">(optional)</span></span><input name="company" autocomplete="organization" maxlength="160"></label>
      <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="t" value="">
      ${TURNSTILE ? `<div class="cf-turnstile" data-sitekey="${esc(TURNSTILE)}" data-theme="dark"></div>` : ""}
      <button class="btn" type="submit" id="send">Send enquiry <span aria-hidden="true">→</span></button>
      <p class="status mono" id="status" role="status" aria-live="polite"></p>
      <noscript><p class="mono dim">JavaScript is off. The form still sends, or email <a href="mailto:${site.email}">${site.email}</a>.</p></noscript>
    </form>
  </div>
</div></section>
<section class="dark" style="padding-top:clamp(3rem,6vw,6rem)"><div class="wrap">${footer()}</div></section>`,
  });
}

// PRIVACY
pages["/privacy"] = page({
  path: "/privacy",
  title: "Privacy",
  desc: "How Higher Heights handles enquiry form submissions and site data.",
  headTheme: "light",
  noindex: false,
  body: `
<section class="paper pagehead"><div class="wrap"><p class="mono dim eyebrow">Privacy</p><h1 class="d-1">Privacy notice</h1></div></section>
<section class="paper" style="padding-bottom:var(--sect)"><div class="wrap"><div class="text measure">
<p>This is a placeholder notice written from what the site does today. It must be reviewed and completed by the studio before launch.</p>
<p><strong>Enquiry form.</strong> When you send an enquiry, the details you enter (name, email, company, project information) are sent by email to ${site.email} so Morgan can reply. They are used only to respond to you.</p>
<p><strong>Spam protection.</strong> The form uses a hidden field and timing checks${TURNSTILE ? " and Cloudflare Turnstile" : ""}. Your IP address may be processed briefly for rate limiting.</p>
<p><strong>Analytics and cookies.</strong> The site sets no cookies and runs no analytics. Fonts load from Google Fonts.</p>
<p><strong>Contact.</strong> Questions about your data: <a href="mailto:${site.email}">${site.email}</a>.</p>
</div></div></section>
<section class="dark" style="padding-top:clamp(3rem,6vw,6rem)"><div class="wrap">${footer()}</div></section>`,
});

// 404
const notFound = page({
  path: "/404",
  title: "Page not found",
  desc: "That page does not exist.",
  noindex: true,
  body: `<section class="dark pagehead" style="min-height:80svh"><div class="wrap"><p class="mono sage eyebrow">404</p><h1 class="d-xxl">Out of frame.</h1><p style="margin-top:2rem"><a class="btn" href="/">Back to the reel</a></p></div></section>
<section class="dark" style="padding-top:clamp(3rem,6vw,6rem)"><div class="wrap">${footer()}</div></section>`,
});

// ── write ────────────────────────────────────────────────────
fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });
const write = (rel, content) => {
  const f = path.join(dist, rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, content);
};
for (const [p, html] of Object.entries(pages)) write(p === "/" ? "index.html" : `${p.slice(1)}/index.html`, html);
write("404.html", notFound);
write("css/site.css", css);
write("js/site.js", js);
if (fs.existsSync(path.join(root, "assets"))) fs.cpSync(path.join(root, "assets"), path.join(dist, "assets"), { recursive: true });

const urls = Object.keys(pages);
write(
  "sitemap.xml",
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${abs(u === "/" ? "/" : u)}</loc></url>`)
    .join("\n")}\n</urlset>\n`
);
write("robots.txt", `User-agent: *\nAllow: /\nSitemap: ${BASE}/sitemap.xml\n`);

console.log(`Built ${urls.length + 1} pages → dist/ (base ${BASE})`);

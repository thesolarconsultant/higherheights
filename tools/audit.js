const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const URL = process.argv[2] || 'http://127.0.0.1:8091/index.html';

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, '../qa/p-audit'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const reqs = [];
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message.slice(0, 80)));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));
  p.on('response', async r => {
    try {
      const h = r.headers();
      reqs.push({
        url: r.url().split('/').slice(-1)[0].slice(0, 42),
        type: r.request().resourceType(),
        bytes: +(h['content-length'] || 0),
        status: r.status(),
      });
    } catch (e) {}
  });

  await p.setViewport({ width: 1440, height: 900 });
  const t0 = Date.now();
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 90000 });
  const loadMs = Date.now() - t0;
  await sleep(2500);

  const metrics = await p.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0] || {};
    const paints = {};
    performance.getEntriesByType('paint').forEach(e => paints[e.name] = Math.round(e.startTime));
    let lcp = 0;
    try {
      const l = performance.getEntriesByType('largest-contentful-paint');
      if (l.length) lcp = Math.round(l[l.length - 1].startTime);
    } catch (e) {}
    return {
      domContentLoaded: Math.round(nav.domContentLoadedEventEnd || 0),
      loadEvent: Math.round(nav.loadEventEnd || 0),
      firstPaint: paints['first-paint'] || null,
      firstContentfulPaint: paints['first-contentful-paint'] || null,
      lcp,
      domNodes: document.querySelectorAll('*').length,
    };
  });

  const struct = await p.evaluate(() => {
    const headings = [...document.querySelectorAll('h1,h2,h3,h4')]
      .map(h => h.tagName + ': ' + h.innerText.trim().replace(/\s+/g, ' ').slice(0, 46));
    const fonts = new Set();
    document.querySelectorAll('*').forEach(e => {
      const f = getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '');
      if (f && f !== 'inherit') fonts.add(f);
    });
    const imgs = [...document.images];
    return {
      headings,
      h1Count: document.querySelectorAll('h1').length,
      fontFamilies: [...fonts],
      sections: document.querySelectorAll('section,header,footer,main').length,
      imgCount: imgs.length,
      imgsNoAlt: imgs.filter(i => !i.hasAttribute('alt')).length,
      imgsNoDims: imgs.filter(i => !i.width || !i.height).length,
      imgsLazy: imgs.filter(i => i.loading === 'lazy').length,
      links: document.querySelectorAll('a').length,
      linksNoText: [...document.querySelectorAll('a')]
        .filter(a => !a.innerText.trim() && !a.getAttribute('aria-label')).length,
      buttons: document.querySelectorAll('button').length,
      buttonsNoLabel: [...document.querySelectorAll('button')]
        .filter(x => !x.innerText.trim() && !x.getAttribute('aria-label')).length,
      videos: document.querySelectorAll('video').length,
      // SEO
      title: document.title,
      titleLen: document.title.length,
      metaDesc: (document.querySelector('meta[name=description]') || {}).content || null,
      og: document.querySelectorAll('meta[property^="og:"]').length,
      jsonLd: document.querySelectorAll('script[type="application/ld+json"]').length,
      canonical: !!document.querySelector('link[rel=canonical]'),
      lang: document.documentElement.lang || null,
      // nav
      internalPages: [...new Set([...document.querySelectorAll('a[href]')]
        .map(a => a.getAttribute('href'))
        .filter(h => h && !h.startsWith('#') && !h.startsWith('mailto') && !h.startsWith('http')))],
    };
  });

  // responsive sweep
  const bp = [];
  for (const [w, h, name] of [[390, 844, 'mobile'], [768, 1024, 'tablet'], [1440, 900, 'desktop'], [1920, 1080, 'wide']]) {
    await p.setViewport({ width: w, height: h });
    await sleep(900);
    const r = await p.evaluate(() => ({
      overflowX: document.documentElement.scrollWidth > window.innerWidth + 2
        ? document.documentElement.scrollWidth - window.innerWidth : 0,
      heroTitlePx: (() => { const t = document.querySelector('.hero__title'); return t ? Math.round(parseFloat(getComputedStyle(t).fontSize)) : null; })(),
      bodyPx: Math.round(parseFloat(getComputedStyle(document.body).fontSize)),
      tinyText: [...document.querySelectorAll('p,span,a,li,dd,dt')]
        .filter(e => e.innerText && e.innerText.trim() && parseFloat(getComputedStyle(e).fontSize) < 11).length,
      smallTargets: [...document.querySelectorAll('a,button')]
        .filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && (b.width < 40 || b.height < 36); }).length,
    }));
    bp.push({ name, w, ...r });
  }

  const byType = {};
  reqs.forEach(r => {
    byType[r.type] = byType[r.type] || { n: 0, bytes: 0 };
    byType[r.type].n++; byType[r.type].bytes += r.bytes;
  });
  const heavy = reqs.filter(r => r.bytes > 120000).sort((a, b) => b.bytes - a.bytes).slice(0, 8);

  console.log(JSON.stringify({
    url: URL, loadMs, metrics, struct,
    responsive: bp,
    requests: { total: reqs.length, byType, heaviest: heavy },
    errors: [...new Set(errs)],
  }, null, 1));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

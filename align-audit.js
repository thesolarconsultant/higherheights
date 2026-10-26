const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-align'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 450) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30));
    }
    window.scrollTo(0, 0);
  });
  await sleep(1000);

  const out = await p.evaluate(() => {
    const visible = e => {
      const s = getComputedStyle(e);
      const r = e.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0.05 &&
             r.width > 0 && r.height > 0 &&
             !/^(SCRIPT|STYLE|META|TITLE|LINK|HEAD|NOSCRIPT)$/.test(e.tagName);
    };

    // ── real rendered font families ──
    const fams = {};
    document.querySelectorAll('*').forEach(e => {
      if (!visible(e) || e.children.length || !e.textContent.trim()) return;
      const f = getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '');
      fams[f] = (fams[f] || 0) + 1;
    });

    // ── alignment: where does each major block actually start? ──
    const edges = {};
    const blocks = [];
    document.querySelectorAll('section, .wrap, .band, .foot__top, .hero__foot, .clients, .marquee').forEach(e => {
      if (!visible(e)) return;
      const r = e.getBoundingClientRect();
      const left = Math.round(r.left);
      const key = (e.tagName + '.' + (e.className || '').toString().split(' ')[0]).slice(0, 34);
      blocks.push({ el: key, left, right: Math.round(window.innerWidth - r.right), w: Math.round(r.width) });
      edges[left] = (edges[left] || 0) + 1;
    });

    // ── text alignment spread ──
    const aligns = {};
    document.querySelectorAll('h1,h2,h3,p,.eyebrow,.mono,.micro').forEach(e => {
      if (!visible(e)) return;
      const a = getComputedStyle(e).textAlign;
      aligns[a] = (aligns[a] || 0) + 1;
    });

    // ── max-width spread: how many different content measures? ──
    const measures = {};
    document.querySelectorAll('p, h2, .band__lede, .foot__tag').forEach(e => {
      if (!visible(e)) return;
      const mw = getComputedStyle(e).maxWidth;
      if (mw && mw !== 'none') measures[mw] = (measures[mw] || 0) + 1;
    });

    return {
      fontFamilies: fams,
      leftEdges: Object.entries(edges).sort((a, b) => b[1] - a[1]),
      blocks: blocks.slice(0, 18),
      textAlign: aligns,
      maxWidths: measures,
    };
  });
  console.log(JSON.stringify(out, null, 1));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

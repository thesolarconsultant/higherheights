const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const URL = process.argv[2] || 'http://127.0.0.1:8092/index.html';

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, '../qa/p-diagnostic'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 90000 });
  await sleep(2500);
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 400) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 28));
    }
    window.scrollTo(0, 0);
  });
  await sleep(1200);

  const d = await p.evaluate(() => {
    const vis = e => {
      const s = getComputedStyle(e), r = e.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > .05 &&
             r.width > 0 && r.height > 0 &&
             !/^(SCRIPT|STYLE|META|TITLE|LINK|HEAD|NOSCRIPT)$/.test(e.tagName);
    };
    const texty = e => vis(e) && e.children.length === 0 && e.textContent.trim();
    const round = n => Math.round(n * 100) / 100;

    // ── TYPE SCALE ──
    const sizes = {}, lh = {}, ls = {}, weights = {};
    document.querySelectorAll('*').forEach(e => {
      if (!texty(e)) return;
      const s = getComputedStyle(e);
      const fs = round(parseFloat(s.fontSize));
      sizes[fs] = (sizes[fs] || 0) + 1;
      const ratio = round(parseFloat(s.lineHeight) / parseFloat(s.fontSize));
      if (!isNaN(ratio)) lh[ratio] = (lh[ratio] || 0) + 1;
      const t = s.letterSpacing === 'normal' ? '0' : round(parseFloat(s.letterSpacing) / parseFloat(s.fontSize) * 1000) / 1000 + 'em';
      ls[t] = (ls[t] || 0) + 1;
      weights[s.fontWeight] = (weights[s.fontWeight] || 0) + 1;
    });

    // ── VERTICAL RHYTHM: gaps between consecutive sections ──
    const secs = [...document.querySelectorAll('section, header.nav, footer, .band, .pin')].filter(vis);
    const gaps = [];
    const pads = {};
    secs.forEach((e, i) => {
      const s = getComputedStyle(e);
      const pt = Math.round(parseFloat(s.paddingTop)), pb = Math.round(parseFloat(s.paddingBottom));
      if (pt) pads[pt] = (pads[pt] || 0) + 1;
      if (pb) pads[pb] = (pads[pb] || 0) + 1;
      if (i) {
        const prev = secs[i - 1].getBoundingClientRect(), cur = e.getBoundingClientRect();
        gaps.push(Math.round(cur.top - prev.bottom));
      }
    });

    // ── LAYOUT: left edges and content measures ──
    const lefts = {}, measures = {};
    document.querySelectorAll('.wrap, section > div, .band, .foot__top').forEach(e => {
      if (!vis(e)) return;
      lefts[Math.round(e.getBoundingClientRect().left)] = 1;
    });
    document.querySelectorAll('p, h1, h2, h3').forEach(e => {
      if (!vis(e)) return;
      const mw = getComputedStyle(e).maxWidth;
      if (mw && mw !== 'none') measures[Math.round(parseFloat(mw))] = (measures[Math.round(parseFloat(mw))] || 0) + 1;
    });

    // ── COLOUR ──
    const inks = {}, grounds = {};
    document.querySelectorAll('*').forEach(e => {
      if (!vis(e)) return;
      const s = getComputedStyle(e);
      if (texty(e)) inks[s.color] = (inks[s.color] || 0) + 1;
      const bg = s.backgroundColor;
      if (bg && !/rgba\(0, 0, 0, 0\)/.test(bg)) grounds[bg] = (grounds[bg] || 0) + 1;
    });

    // ── MOTION INVENTORY ──
    const trans = {}, anims = {}, eases = {};
    document.querySelectorAll('*').forEach(e => {
      if (!vis(e)) return;
      const s = getComputedStyle(e);
      if (s.transitionDuration && s.transitionDuration !== '0s') {
        s.transitionDuration.split(', ').forEach(t => trans[t] = (trans[t] || 0) + 1);
        s.transitionTimingFunction.split(', ').forEach(t => eases[t.slice(0, 40)] = (eases[t.slice(0, 40)] || 0) + 1);
      }
      if (s.animationName && s.animationName !== 'none') {
        s.animationName.split(', ').forEach(a => anims[a] = (anims[a] || 0) + 1);
      }
    });

    return {
      typeScale: Object.entries(sizes).sort((a, b) => b[0] - a[0]),
      lineHeights: Object.entries(lh).sort((a, b) => b[1] - a[1]).slice(0, 8),
      tracking: Object.entries(ls).sort((a, b) => b[1] - a[1]).slice(0, 8),
      weights: Object.entries(weights).sort((a, b) => b[1] - a[1]),
      sectionGaps: gaps,
      sectionPadding: Object.entries(pads).sort((a, b) => b[1] - a[1]).slice(0, 8),
      leftEdges: Object.keys(lefts).map(Number).sort((a, b) => a - b),
      measures: Object.entries(measures).sort((a, b) => b[1] - a[1]),
      inks: Object.entries(inks).sort((a, b) => b[1] - a[1]).slice(0, 8),
      grounds: Object.entries(grounds).sort((a, b) => b[1] - a[1]).slice(0, 8),
      transitions: Object.entries(trans).sort((a, b) => b[1] - a[1]).slice(0, 8),
      easings: Object.entries(eases).sort((a, b) => b[1] - a[1]).slice(0, 6),
      animations: Object.entries(anims).sort((a, b) => b[1] - a[1]),
      docHeight: document.body.scrollHeight,
      sectionCount: secs.length,
    };
  });
  console.log(JSON.stringify(d, null, 1));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

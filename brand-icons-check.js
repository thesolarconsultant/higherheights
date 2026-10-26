const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));

const OUT = path.resolve(__dirname, 'site-brand/assets/img');
const MARK = fs.readFileSync(path.join(OUT, 'hh-gold.svg'), 'utf8');
const NAVY = '#0B1A26';

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-icon'), args: ['--no-first-run', '--hide-scrollbars'],
  });
  const p = await b.newPage();

  for (const size of [16, 32, 48, 180, 512]) {
    // proportional padding — a fixed inset eats the mark at small sizes
    const pad = Math.max(1, Math.round(size * 0.13));
    await p.setViewport({ width: size, height: size, deviceScaleFactor: 1 });
    await p.setContent(`<html><body style="margin:0;width:${size}px;height:${size}px;
      background:${NAVY};display:flex;align-items:center;justify-content:center">
      <div style="width:${size - pad * 2}px;height:${size - pad * 2}px;display:flex;
        align-items:center;justify-content:center">${MARK.replace(/width="\d+"|height="\d+"/g, '')
        .replace('<svg', '<svg style="width:100%;height:100%"')}</div></body></html>`,
      { waitUntil: 'domcontentloaded', timeout: 15000 });
    await sleep(240);
    await p.screenshot({ path: path.join(OUT, `icon-${size}.png`), omitBackground: false });
    console.log('icon-' + size + '.png  pad=' + pad);
  }

  // ── verify the branded site ──
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1600);
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sleep(1200);
  await p.evaluate(() => window.scrollTo(0, 0));
  await sleep(600);

  const r = await p.evaluate(() => {
    const q = s => document.querySelector(s);
    const wmS = q('.hh-wm--studio'), wmC = q('.hh-wm--contact');
    const box = el => { const b = el.getBoundingClientRect(); return { w: Math.round(b.width), h: Math.round(b.height) }; };
    return {
      numeralsInText: (document.body.innerText.match(/\(0\d\)/g) || []).length,
      heroMark: q('.brand__mark') ? q('.brand__mark').getAttribute('src').split('/').pop() : null,
      heroMarkLoaded: q('.brand__mark') ? !!q('.brand__mark').naturalWidth : null,
      footerLogo: q('.footer__logo') ? q('.footer__logo').getAttribute('src').split('/').pop() : null,
      footerLogoLoaded: q('.footer__logo') ? !!q('.footer__logo').naturalWidth : null,
      favicon: q('link[rel=icon]') ? q('link[rel=icon]').getAttribute('href').split('/').pop() : null,
      studioWm: wmS ? { ...box(wmS), op: getComputedStyle(wmS).opacity, src: wmS.querySelector('img').getAttribute('src').split('/').pop(), loaded: !!wmS.querySelector('img').naturalWidth } : null,
      contactWm: wmC ? { ...box(wmC), op: getComputedStyle(wmC).opacity, src: wmC.querySelector('img').getAttribute('src').split('/').pop(), loaded: !!wmC.querySelector('img').naturalWidth } : null,
      studioClips: getComputedStyle(q('.studio')).overflow,
      brokenImgs: [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
    };
  });
  console.log(JSON.stringify({ ...r, errs: [...new Set(errs)] }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

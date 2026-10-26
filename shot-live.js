const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
const URL = 'https://higher-heights.vercel.app/';
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p-live'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [], failed = [];
  p.on('pageerror', e => errs.push('js: ' + e.message));
  p.on('response', r => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url()); });
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3000);
  const info = await p.evaluate(() => ({
    title: document.title,
    h1: getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0],
    body: getComputedStyle(document.body).fontFamily.split(',')[0],
    bodoni: document.fonts.check('400 92px "Bodoni Moda"'),
    heroVideo: (() => { const v = document.querySelector('#heroVideo'); return v ? { ready: v.readyState, w: v.videoWidth, h: v.videoHeight, playing: !v.paused } : null; })(),
    logo: (() => { const l = document.querySelector('.brand__logo'); return l ? { w: Math.round(l.getBoundingClientRect().width), loaded: l.naturalWidth > 0 } : null; })(),
    canonical: document.querySelector('link[rel=canonical]')?.href,
    overflowX: document.documentElement.scrollWidth - innerWidth,
  }));
  await p.screenshot({ path: path.join(OUT, 'v5-live-hero.png') });
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto(URL, { waitUntil: 'networkidle2' });
  await sleep(2200);
  await m.screenshot({ path: path.join(OUT, 'v5-live-mobile.png') });
  console.log(JSON.stringify({ info, errs, failed: [...new Set(failed)].slice(0, 8) }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

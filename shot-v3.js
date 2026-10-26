const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p10'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('js: ' + e.message));
  p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto('http://127.0.0.1:8097/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const info = await p.evaluate(() => {
    const l = document.querySelector('.brand__logo').getBoundingClientRect();
    const f = document.querySelector('.footer__logo');
    const s = document.querySelector('.footer__seal');
    return {
      navLockup: { w: Math.round(l.width), h: Math.round(l.height) },
      brandBox: (() => { const b = document.querySelector('.brand').getBoundingClientRect(); return { w: Math.round(b.width), h: Math.round(b.height) }; })(),
      navH: Math.round(document.querySelector('.nav__inner').getBoundingClientRect().height),
      footerNatural: f ? { w: f.naturalWidth, h: f.naturalHeight, shown: Math.round(f.getBoundingClientRect().width) } : null,
      sealShown: s ? Math.round(s.getBoundingClientRect().width) : null,
      overflowX: document.documentElement.scrollWidth - innerWidth,
      h1Font: getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0],
    };
  });
  await p.screenshot({ path: path.join(OUT, 'v3-hero.png') });
  // nav close-up
  await p.screenshot({ path: path.join(OUT, 'v3-nav.png'), clip: { x: 0, y: 0, width: 900, height: 100 } });
  // footer
  await p.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await sleep(1400);
  const fh = await p.evaluate(() => document.documentElement.scrollHeight);
  await p.screenshot({ path: path.join(OUT, 'v3-footer.png'), clip: { x: 0, y: fh - 300, width: 1600, height: 300 } });
  // mobile
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto('http://127.0.0.1:8097/index.html', { waitUntil: 'networkidle2' });
  await sleep(1800);
  await m.screenshot({ path: path.join(OUT, 'v3-mobile.png') });
  console.log(JSON.stringify({ info, errs: [...new Set(errs)] }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

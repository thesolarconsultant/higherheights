const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p-v6'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('js: ' + e.message));
  p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto('http://127.0.0.1:8080/site-v7/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const info = await p.evaluate(() => ({
    favicon: document.querySelector('link[rel=icon][type="image/svg+xml"]')?.getAttribute('href'),
    icons: Array.from(document.querySelectorAll('link[rel*=icon]')).map(l => l.getAttribute('href')),
    sealGone: !document.querySelector('.footer__seal'),
    footerLogo: (() => { const l = document.querySelector('.footer__logo'); return l ? l.getAttribute('src') : null; })(),
    logoLoaded: (() => { const l = document.querySelector('.brand__logo'); return l && l.complete && l.naturalWidth > 0; })(),
    overflowX: document.documentElement.scrollWidth - innerWidth,
  }));
  await p.screenshot({ path: path.join(OUT, 'v6-hero.png') });
  const totalH = await p.evaluate(() => document.documentElement.scrollHeight);
  await p.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await sleep(1400);
  await p.screenshot({ path: path.join(OUT, 'v6-footer.png'), clip: { x: 0, y: totalH - 300, width: 1600, height: 300 } });
  console.log(JSON.stringify({ info, totalH, errs: [...new Set(errs)] }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

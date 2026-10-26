const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
const URL = 'http://127.0.0.1:8080/site-v4/index.html';
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p11'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('js: ' + e.message));
  p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const info = await p.evaluate(() => ({
    h1: getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0],
    h2: getComputedStyle(document.querySelector('.sect-head h2')).fontFamily.split(',')[0],
    body: getComputedStyle(document.body).fontFamily.split(',')[0],
    bodoni: document.fonts.check('400 92px "Bodoni Moda"'),
    bodoniItalic: document.fonts.check('italic 400 40px "Bodoni Moda"'),
    overflowX: document.documentElement.scrollWidth - innerWidth,
    h2Box: Math.round(document.querySelector('.sect-head h2').getBoundingClientRect().height),
  }));
  await p.screenshot({ path: path.join(OUT, 'v4-hero.png') });
  for (const [sel, name] of [['#work', 'work'], ['#studio', 'studio'], ['#contact', 'contact']]) {
    await p.evaluate(s => document.querySelector(s).scrollIntoView({ behavior: 'instant', block: 'start' }), sel);
    await sleep(1200);
    await p.screenshot({ path: path.join(OUT, 'v4-' + name + '.png') });
  }
  await p.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await sleep(1200);
  await p.screenshot({ path: path.join(OUT, 'v4-footer.png'), clip: { x: 0, y: 700, width: 1600, height: 300 } });
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto(URL, { waitUntil: 'networkidle2' });
  await sleep(1800);
  await m.screenshot({ path: path.join(OUT, 'v4-mobile.png') });
  console.log(JSON.stringify({ info, errs: [...new Set(errs)] }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p5'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('js: ' + e.message));
  p.on('requestfailed', r => errs.push('net: ' + r.url()));
  p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto('http://127.0.0.1:8098/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const info = await p.evaluate(() => ({
    h1Font: getComputedStyle(document.querySelector('h1')).fontFamily,
    h1Size: getComputedStyle(document.querySelector('h1')).fontSize,
    h2Font: getComputedStyle(document.querySelector('.sect-head h2')).fontFamily,
    bodyFont: getComputedStyle(document.body).fontFamily,
    monoFont: getComputedStyle(document.querySelector('.eyebrow__num')).fontFamily,
    monoWeight: getComputedStyle(document.querySelector('.eyebrow__num')).fontWeight,
    fontsReady: document.fonts.status,
    markW: document.querySelector('.brand__mark').getBoundingClientRect().width,
    navH: document.querySelector('.nav__inner')?.getBoundingClientRect().height,
    overflowX: document.documentElement.scrollWidth - window.innerWidth,
  }));
  await p.screenshot({ path: path.join(OUT, 'v2-hero.png') });
  for (const [sel, name] of [['#work', 'work'], ['#aerial', 'aerial'], ['#studio', 'studio'], ['#contact', 'contact']]) {
    await p.evaluate(s => document.querySelector(s).scrollIntoView({ behavior: 'instant', block: 'start' }), sel);
    await sleep(1300);
    await p.screenshot({ path: path.join(OUT, 'v2-' + name + '.png') });
  }
  // footer
  await p.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await sleep(1200);
  await p.screenshot({ path: path.join(OUT, 'v2-footer.png') });
  // mobile
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto('http://127.0.0.1:8098/index.html', { waitUntil: 'networkidle2' });
  await sleep(2000);
  await m.screenshot({ path: path.join(OUT, 'v2-mobile-hero.png') });
  const mob = await m.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth }));
  console.log(JSON.stringify({ info, mob, errs: [...new Set(errs)].slice(0, 12) }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

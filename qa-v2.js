const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(__dirname, 'qa/p8'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('js: ' + e.message));
  p.on('requestfailed', r => errs.push('net: ' + r.url()));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto('http://127.0.0.1:8080/site-v4/index.html', { waitUntil: 'networkidle2' });
  await sleep(2000);
  const R = {};
  // modal flow
  await p.evaluate(() => document.querySelector('#work').scrollIntoView({ behavior: 'instant' }));
  await sleep(700);
  await p.click('.film'); await sleep(1400);
  R.modalOpen = await p.evaluate(() => { const m = document.querySelector('.screen'); return { open: m.classList.contains('is-open'), idx: m.querySelector('.screen__count')?.textContent.trim(), fontTitle: (()=>{const t=m.querySelector('h3,.screen__title,h2');return t?getComputedStyle(t).fontFamily.split(',')[0]:null;})() }; });
  await p.keyboard.press('ArrowRight'); await sleep(1000);
  R.modalNext = await p.evaluate(() => document.querySelector('.screen__count').textContent.trim());
  await p.keyboard.press('Escape'); await sleep(600);
  R.modalClosed = await p.evaluate(() => !document.querySelector('.screen').classList.contains('is-open'));
  // nav + links
  R.anchors = await p.evaluate(() => Array.from(document.querySelectorAll('a[href^="#"]')).map(a => a.getAttribute('href')).filter((v, i, a) => a.indexOf(v) === i).every(h => !!document.querySelector(h)));
  R.favicon = await p.evaluate(() => document.querySelector('link[rel=icon]').getAttribute('href'));
  // oversized / overflow check
  R.overflowX = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  // any text rendered in a fallback font?
  R.fontsReady = await p.evaluate(() => document.fonts.status);
  R.serifLoaded = await p.evaluate(() => document.fonts.check('400 40px "Instrument Serif"'));
  R.sansLoaded = await p.evaluate(() => document.fonts.check('400 16px "Instrument Sans"'));
  // mobile
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto('http://127.0.0.1:8080/site-v4/index.html', { waitUntil: 'networkidle2' });
  await sleep(1800);
  await m.click('#burger'); await sleep(800);
  R.mobileDrawer = await m.evaluate(() => ({ open: document.querySelector('#nav').classList.contains('is-open'), sw: document.documentElement.scrollWidth, iw: innerWidth }));
  await m.screenshot({ path: path.resolve(__dirname, 'qa/v2-mobile-drawer.png') });
  await m.click('#drawer a'); await sleep(900);
  await m.screenshot({ path: path.resolve(__dirname, 'qa/v2-mobile-work.png') });
  R.errs = [...new Set(errs)];
  console.log(JSON.stringify(R, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

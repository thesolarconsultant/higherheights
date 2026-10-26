const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'http://127.0.0.1:8099/index.html';
const OUT = path.resolve(__dirname, 'qa');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.join(OUT, 'profile3'), args: ['--no-first-run', '--autoplay-policy=no-user-gesture-required', '--window-size=1440,900'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(URL, { waitUntil: 'networkidle2' });
  await sleep(1500);

  const R = {};
  const modal = () => p.evaluate(() => {
    const m = document.querySelector('.screen');
    return m ? { open: m.classList.contains('is-open'), idx: m.querySelector('.screen__count')?.textContent.trim(), title: m.querySelector('h3, .screen__title')?.textContent.trim(), text: m.textContent.replace(/\s+/g, ' ').slice(0, 90) } : null;
  });

  await p.evaluate(() => document.querySelector('#work').scrollIntoView({ behavior: 'instant' }));
  await sleep(600);
  // open first card
  await p.click('.film');
  await sleep(1500);
  R.open = await modal();

  // next via button
  const nextBtn = await p.$('.screen [data-next], .screen .screen__nav--next, .screen button[aria-label*="ext"]');
  if (nextBtn) { await nextBtn.click(); await sleep(1200); }
  R.afterNextBtn = await modal();

  // arrow key
  await p.keyboard.press('ArrowRight'); await sleep(1200);
  R.afterArrowRight = await modal();
  await p.keyboard.press('ArrowLeft'); await sleep(1200);
  R.afterArrowLeft = await modal();

  // esc close
  await p.keyboard.press('Escape'); await sleep(800);
  R.afterEsc = await modal();
  R.bodyLockedAfterEsc = await p.evaluate(() => document.body.className);

  // reopen + close button
  await p.click('.film'); await sleep(1200);
  const closeBtn = await p.$('.screen [data-close], .screen .screen__close');
  if (closeBtn) { await closeBtn.click(); await sleep(700); }
  R.afterCloseBtn = await modal();

  // tab focus behaviour while modal open
  await p.click('.film'); await sleep(1000);
  await p.keyboard.press('Tab'); await sleep(300);
  R.focusAfterTabInModal = await p.evaluate(() => document.activeElement.className || document.activeElement.tagName);
  await p.keyboard.press('Escape'); await sleep(500);

  // mobile drawer
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto(URL, { waitUntil: 'networkidle2' });
  await sleep(1200);
  await m.click('#burger'); await sleep(900);
  R.drawer = await m.evaluate(() => ({ navOpen: document.querySelector('#nav').classList.contains('is-open'), expanded: document.querySelector('#burger').getAttribute('aria-expanded'), bodyLocked: document.body.classList.contains('is-locked'), drawerVisible: (() => { const d = document.querySelector('#drawer'); if (!d) return null; const r = d.getBoundingClientRect(); return r.width > 0 && r.height > 0; })() }));
  await m.screenshot({ path: path.join(OUT, 'mob-drawer.png') });
  // click a drawer link
  const link = await m.$('#drawer a');
  if (link) { await link.click(); await sleep(900); }
  R.drawerAfterNav = await m.evaluate(() => ({ navOpen: document.querySelector('#nav').classList.contains('is-open'), y: Math.round(window.scrollY) }));

  // reduced motion pass
  const rm = await b.newPage();
  await rm.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await rm.setViewport({ width: 1440, height: 900 });
  await rm.goto(URL, { waitUntil: 'networkidle2' });
  await sleep(1200);
  R.reducedMotion = await rm.evaluate(() => ({ revealHidden: Array.from(document.querySelectorAll('[class*="reveal"], [data-reveal]')).filter(e => getComputedStyle(e).opacity === '0').length, scrollY: window.scrollY }));
  await rm.screenshot({ path: path.join(OUT, 'rm-hero.png') });

  R.pageErrors = errs;
  console.log(JSON.stringify(R, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'http://127.0.0.1:8099/index.html';
const OUT = path.resolve(__dirname, 'qa');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.join(OUT, 'profile4'), args: ['--no-first-run', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(URL, { waitUntil: 'networkidle2' });
  await sleep(1200);
  await p.evaluate(() => document.querySelector('#work').scrollIntoView({ behavior: 'instant' }));
  await sleep(500);
  await p.click('.film');
  await sleep(1200);
  const R = {};
  R.scrollLockedBehindModal = await p.evaluate(() => getComputedStyle(document.body).overflow + '/' + getComputedStyle(document.documentElement).overflow);
  const yBefore = await p.evaluate(() => window.scrollY);
  await p.mouse.move(700, 450); await p.mouse.wheel({ deltaY: 900 }); await sleep(500);
  R.scrollYAfterWheel = { before: yBefore, after: await p.evaluate(() => window.scrollY) };
  // tab 6 times: is focus contained?
  const chain = [];
  for (let i = 0; i < 7; i++) {
    await p.keyboard.press('Tab'); await sleep(150);
    chain.push(await p.evaluate(() => {
      const a = document.activeElement;
      return a.tagName + '.' + (a.className || '') + (a.closest('.screen') ? ' [in-modal]' : ' [OUTSIDE]');
    }));
  }
  R.tabChain = chain;
  // backdrop click closes?
  await p.mouse.click(30, 30); await sleep(700);
  R.openAfterBackdropClick = await p.evaluate(() => { const m = document.querySelector('.screen'); return m.classList.contains('is-open'); });
  // video sizing inside modal for vertical films
  await p.evaluate(() => { const m = document.querySelector('.screen'); if (!m.classList.contains('is-open')) return; });
  await p.click('.film:nth-child(2)').catch(() => {});
  await sleep(1200);
  R.verticalModal = await p.evaluate(() => {
    const v = document.querySelector('.screen.is-open video');
    if (!v) return null;
    const r = v.getBoundingClientRect();
    return { w: Math.round(r.width), h: Math.round(r.height), vw: v.videoWidth, vh: v.videoHeight, fitsViewport: r.bottom <= innerHeight + 1 && r.top >= -1 };
  });
  await p.screenshot({ path: path.join(OUT, 'modal-vertical.png') });
  console.log(JSON.stringify(R, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

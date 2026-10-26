const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-wmf'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));

  // desktop
  await p.setViewport({ width: 1440, height: 880 });
  await p.goto('http://127.0.0.1:8083/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1400);
  const who = await p.$('.who');
  await who.scrollIntoView();
  await sleep(700);
  const d = await p.evaluate(() => {
    const wm = document.querySelector('.who__wm');
    const img = wm.querySelector('img');
    const br = document.querySelector('.who__body').getBoundingClientRect();
    const wr = wm.getBoundingClientRect();
    return {
      src: img.getAttribute('src').split('/').pop(),
      loaded: !!img.naturalWidth,
      opacity: getComputedStyle(wm).opacity,
      z: getComputedStyle(wm).zIndex,
      widthPx: Math.round(wr.width),
      bleedR: Math.round(wr.right - br.right),
      bleedB: Math.round(wr.bottom - br.bottom),
    };
  });
  console.log('DESKTOP', JSON.stringify(d));
  await who.screenshot({ path: 'brand/wm-final.jpg', quality: 90, type: 'jpeg' });

  // mobile
  await p.setViewport({ width: 414, height: 896, isMobile: true, hasTouch: true });
  await sleep(900);
  await (await p.$('.who')).scrollIntoView();
  await sleep(800);
  const m = await p.evaluate(() => {
    const wm = document.querySelector('.who__wm');
    const sig = document.querySelector('.who__body .sig').getBoundingClientRect();
    const wr = wm.getBoundingClientRect();
    return {
      opacity: getComputedStyle(wm).opacity,
      widthPx: Math.round(wr.width),
      overlapsSignature: !(wr.top > sig.bottom || wr.bottom < sig.top),
    };
  });
  console.log('MOBILE ', JSON.stringify(m));
  await (await p.$('.who')).screenshot({ path: 'brand/wm-final-mobile.jpg', quality: 88, type: 'jpeg' });
  console.log('errs', [...new Set(errs)]);
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

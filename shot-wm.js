const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));

const VARIANTS = [
  ['hh-outline.svg', 'outline', 0.085],
  ['hh-outline-fine.svg', 'fine', 0.10],
  ['hh-solid.svg', 'solid', 0.055],
  ['hh-duo.svg', 'duo', 0.075],
];

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-wm'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));
  await p.setViewport({ width: 1440, height: 880 });
  await p.goto('http://127.0.0.1:8083/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1500);

  const diag = await p.evaluate(() => {
    const wm = document.querySelector('.who__wm');
    const img = wm && wm.querySelector('img');
    const body = document.querySelector('.who__body');
    const h2 = document.querySelector('.who__body h2');
    if (!wm) return { error: 'no watermark element' };
    const wr = wm.getBoundingClientRect(), br = body.getBoundingClientRect();
    return {
      found: true,
      svgLoaded: !!(img && img.naturalWidth),
      naturalSize: img ? `${img.naturalWidth}x${img.naturalHeight}` : null,
      opacity: getComputedStyle(wm).opacity,
      zIndex: getComputedStyle(wm).zIndex,
      bodyOverflow: getComputedStyle(body).overflow,
      wmWidthPx: Math.round(wr.width),
      wmBleedRight: Math.round(wr.right - br.right),
      wmBleedBottom: Math.round(wr.bottom - br.bottom),
      textAboveMark: getComputedStyle(h2).zIndex,
    };
  });
  console.log('DIAG', JSON.stringify(diag, null, 2));

  const who = await p.$('.who');
  await who.scrollIntoView();
  await sleep(700);

  for (const [file, name, op] of VARIANTS) {
    await p.evaluate((f, o) => {
      const wm = document.querySelector('.who__wm');
      wm.querySelector('img').src = 'assets/img/' + f;
      wm.style.opacity = o;
    }, file, op);
    await sleep(600);
    await who.screenshot({ path: `brand/wm-${name}.jpg`, quality: 88, type: 'jpeg' });
    console.log('shot', name);
  }
  console.log('errs', [...new Set(errs)]);
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

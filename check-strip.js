const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-strip'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2000);

  const r = await p.evaluate(() => {
    const q = s => document.querySelector(s);
    const st = q('.hero__status');
    return {
      clock: q('#ukClock') ? q('#ukClock').textContent : null,
      statusIsLink: st ? st.tagName + ' -> ' + st.getAttribute('href') : null,
      discWords: document.querySelectorAll('.hero__disc i').length,
      discAnim: q('.hero__disc i') ? getComputedStyle(q('.hero__disc i')).animationName : null,
      discDelays: [...document.querySelectorAll('.hero__disc i')]
        .map(e => getComputedStyle(e).animationDelay),
      dotAnim: q('.hero__avail i') ? getComputedStyle(q('.hero__avail i'), '::after').animationName : null,
    };
  });
  console.log('STRIP', JSON.stringify(r, null, 2));

  // prove the disciplines are actually animating
  const op = () => p.evaluate(() => [...document.querySelectorAll('.hero__disc i')]
    .map(e => +getComputedStyle(e).opacity).join(','));
  const a = await op(); await sleep(700); const c = await op();
  console.log('opacity t0:', a);
  console.log('opacity t1:', c, c !== a ? '-> animating' : '-> STATIC');

  // hover changes the status colour
  const before = await p.evaluate(() => getComputedStyle(document.querySelector('.hero__status')).color);
  await p.hover('.hero__status'); await sleep(600);
  const after = await p.evaluate(() => getComputedStyle(document.querySelector('.hero__status')).color);
  console.log('status colour', before, '->', after, before !== after ? '(hover works)' : '(NO hover)');

  await p.screenshot({ path: 'brand/strip-full.jpg', quality: 92, type: 'jpeg' });
  await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2.5 });
  await sleep(600);
  await p.screenshot({ path: 'brand/strip-zoom.jpg', quality: 94, type: 'jpeg',
    clip: { x: 40, y: 92, width: 1360, height: 46 } });
  console.log('errs', [...new Set(errs)]);
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

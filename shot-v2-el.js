const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p7'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1600, height: 1100 });
  await p.goto('http://127.0.0.1:8098/index.html', { waitUntil: 'networkidle2' });
  await sleep(1500);
  // element shots at 2x for crispness in the board
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  await sleep(600);
  const jobs = [['#contact', 'v2-contact-el.png'], ['.footer', 'v2-footer-el.png'], ['#studio', 'v2-studio-el.png']];
  for (const [sel, file] of jobs) {
    await p.evaluate(s => document.querySelector(s).scrollIntoView({ behavior: 'instant', block: 'center' }), sel);
    await sleep(1200);
    const el = await p.$(sel);
    await el.screenshot({ path: path.join(OUT, file) });
  }
  // hero, element-free but cropped to first viewport at 2x
  await p.evaluate(() => window.scrollTo(0, 0));
  await sleep(1500);
  await p.screenshot({ path: path.join(OUT, 'v2-hero-2x.png'), clip: { x: 0, y: 0, width: 1600, height: 1000 } });
  console.log('done');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

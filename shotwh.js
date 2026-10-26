const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
// usage: node shotwh.js <file> <out> <width> <height> [clip|full]
(async () => {
  const file = process.argv[2];
  const out = process.argv[3];
  const w = parseInt(process.argv[4] || '1200', 10);
  const h = parseInt(process.argv[5] || '900', 10);
  const mode = process.argv[6] || 'clip';
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(__dirname, '.pptr'), args: ['--no-first-run', '--hide-scrollbars', '--force-device-scale-factor=1'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('requestfailed', r => errs.push('fail ' + r.url()));
  await p.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
  await p.goto('file:///' + file.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 60000 });
  await sleep(1000);
  const docH = await p.evaluate(() => Math.ceil(document.documentElement.scrollHeight));
  if (mode === 'full') await p.screenshot({ path: out, fullPage: true });
  else await p.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: Math.min(h, docH) } });
  console.log(JSON.stringify({ out, docH, errs }));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

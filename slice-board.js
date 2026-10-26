const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const DIR = path.resolve(__dirname, 'brand');

(async () => {
  const file = path.join(DIR, 'identity.html');
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(__dirname, 'qa/p9'), args: ['--no-first-run', '--hide-scrollbars', '--force-device-scale-factor=1'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1100, height: 1400, deviceScaleFactor: 1 });
  await p.goto('file:///' + file.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 90000 });
  await sleep(1500);
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  const slice = 1900;
  const n = Math.ceil(h / slice);
  const outs = [];
  for (let i = 0; i < n; i++) {
    const y = i * slice;
    const hh = Math.min(slice, h - y);
    const out = path.join(DIR, `board-${i + 1}.png`);
    await p.screenshot({ path: out, clip: { x: 0, y, width: 1100, height: hh } });
    outs.push({ out, y, hh, bytes: fs.statSync(out).size });
  }
  console.log(JSON.stringify({ h, n, outs }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

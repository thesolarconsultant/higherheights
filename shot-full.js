const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
const URL = process.argv[2] || 'https://higher-heights.vercel.app/';
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p-full'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1400, height: 900 });
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  // walk the page so lazy images and videos resolve
  await p.evaluate(async () => {
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 180)); }
    window.scrollTo(0, 0);
  });
  await sleep(1500);
  const out = path.join(OUT, 'site-full.png');
  await p.screenshot({ path: out, fullPage: true });
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  console.log(JSON.stringify({ out, height: h, bytes: fs.statSync(out).size }));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

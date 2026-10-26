const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(__dirname, 'qa/profile4'), args: ['--no-first-run', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8099/index.html', { waitUntil: 'networkidle2' });
  await sleep(1200);
  await p.evaluate(() => document.querySelector('#work').scrollIntoView({ behavior: 'instant' }));
  await sleep(500);
  await p.evaluate(() => document.querySelectorAll('.film')[1].click());
  await sleep(1800);
  const r = await p.evaluate(() => {
    const v = document.querySelector('.screen.is-open video');
    const rr = v.getBoundingClientRect();
    return { w: Math.round(rr.width), h: Math.round(rr.height), vw: v.videoWidth, vh: v.videoHeight, top: Math.round(rr.top), bottom: Math.round(rr.bottom), vh_win: innerHeight, playing: !v.paused };
  });
  console.log(JSON.stringify(r));
  await p.screenshot({ path: path.resolve(__dirname, 'qa/modal-vertical.png') });
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(OUT,'p-v8'), args: ['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8082/', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3500);
  await p.screenshot({ path: path.join(OUT,'v8-reel.png') });
  // step the reel
  await p.keyboard.press('ArrowRight'); await sleep(1500);
  const st = await p.evaluate(() => ({ title: document.getElementById('title').textContent, client: document.getElementById('client').textContent, playing: !document.getElementById('stage').paused, w: document.getElementById('stage').videoWidth }));
  await p.screenshot({ path: path.join(OUT,'v8-reel-2.png') });
  // work panel
  await p.evaluate(() => document.getElementById('work').scrollIntoView({behavior:'instant'}));
  await sleep(1800);
  await p.screenshot({ path: path.join(OUT,'v8-work.png') });
  // who + contact
  await p.evaluate(() => document.getElementById('who').scrollIntoView({behavior:'instant'}));
  await sleep(1200);
  await p.screenshot({ path: path.join(OUT,'v8-who.png') });
  await p.evaluate(() => document.getElementById('contact').scrollIntoView({behavior:'instant'}));
  await sleep(900);
  await p.screenshot({ path: path.join(OUT,'v8-contact.png') });
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await m.goto('http://127.0.0.1:8082/', { waitUntil: 'networkidle2' });
  await sleep(2500);
  await m.screenshot({ path: path.join(OUT,'v8-mobile.png') });
  console.log(JSON.stringify({ st, errs }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

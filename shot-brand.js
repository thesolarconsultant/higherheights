const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-bshot'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1800);

  // wake every reveal so nothing screenshots blank
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 500) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 45));
    }
    window.scrollTo(0, 0);
  });
  await sleep(900);

  await p.screenshot({ path: 'brand/b-hero.jpg', quality: 88, type: 'jpeg' });
  console.log('b-hero.jpg');

  for (const [sel, name] of [['.studio', 'b-studio'], ['.contact', 'b-contact'], ['.footer', 'b-footer']]) {
    const el = await p.$(sel);
    if (!el) { console.log('MISSING ' + sel); continue; }
    await el.scrollIntoView();
    await sleep(800);
    const bb = await el.boundingBox();
    await el.screenshot({ path: `brand/${name}.jpg`, quality: 88, type: 'jpeg' });
    console.log(name + '.jpg  h=' + Math.round(bb.height));
  }
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

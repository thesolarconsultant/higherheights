const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-shots'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2000);
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 400) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 35));
    }
    window.scrollTo(0, 0);
  });
  await sleep(1000);

  const shot = async (sel, name, hover) => {
    const el = await p.$(sel);
    if (!el) { console.log('MISSING ' + sel); return; }
    await el.scrollIntoView(); await sleep(800);
    if (hover) { await p.hover(hover); await sleep(700); }
    await el.screenshot({ path: `brand/${name}.jpg`, quality: 90, type: 'jpeg' });
    console.log(name);
  };

  await shot('.clients', 'x-clients', '.client:nth-child(3) .client__mark');
  await shot('#enquiry', 'x-enq1');

  // walk to the budget step and shoot it
  await p.click('.enq__screen.is-on .enq__opt:nth-child(2) span'); await sleep(700);
  await p.click('.enq__screen.is-on .enq__opt:nth-child(1) span'); await sleep(900);
  await shot('#enquiry', 'x-enq-budget');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

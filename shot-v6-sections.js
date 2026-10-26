const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(OUT, 'p-v6s'), args: ['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1600, height: 1000 });
  await p.goto('http://127.0.0.1:8080/site-v6/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2200);
  for (const [sel, name] of [['.band-cream','statement'], ['#work','work'], ['#studio','studio'], ['#contact','contact']]) {
    await p.evaluate(s => document.querySelector(s).scrollIntoView({ behavior: 'instant', block: 'start' }), sel);
    await sleep(1200);
    await p.screenshot({ path: path.join(OUT, 'v6-' + name + '.png') });
  }
  console.log('ok');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

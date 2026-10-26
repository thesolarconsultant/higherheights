const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-v9s'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 860, deviceScaleFactor: 1 });
  await p.goto('http://127.0.0.1:8083/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2000);
  await p.screenshot({ path: 'brand/v9-reel.jpg', quality: 86, type: 'jpeg' });

  for (const [frac, name] of [[0.18, 'v9-ch1'], [0.55, 'v9-ch2']]) {
    await p.evaluate(f => {
      const t = document.getElementById('work-track');
      window.scrollTo(0, t.offsetTop + (t.offsetHeight - innerHeight) * f);
    }, frac);
    await sleep(1600);
    await p.screenshot({ path: `brand/${name}.jpg`, quality: 86, type: 'jpeg' });
  }
  console.log('shot reel + 2 chapters');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

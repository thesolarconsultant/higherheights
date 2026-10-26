const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(OUT,'p-ch'), args: ['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8082/', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const gate = await p.evaluate(() => {
    const t = document.getElementById('work-track');
    return { trackH: t.offsetHeight, top: t.offsetTop };
  });
  const shots = [];
  for (const frac of [0.05, 0.30, 0.62, 0.92]) {
    await p.evaluate((f) => {
      const t = document.getElementById('work-track');
      const span = t.offsetHeight - innerHeight;
      scrollTo(0, t.offsetTop + span * f);
    }, frac);
    await sleep(1600);
    const st = await p.evaluate(() => ({
      title: document.getElementById('w-title').textContent.trim(),
      idx: document.getElementById('w-idx').textContent.trim(),
      credit: document.getElementById('w-credit').textContent.trim(),
      on: Array.from(document.querySelectorAll('.work__media video')).map(v => ({ on: v.classList.contains('is-on'), src: (v.currentSrc||'').split('/').pop(), playing: !v.paused })),
    }));
    const f = path.join(OUT, 'chapter-' + Math.round(frac*100) + '.png');
    await p.screenshot({ path: f });
    shots.push({ frac, st });
  }
  console.log(JSON.stringify({ gate, shots, errs }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

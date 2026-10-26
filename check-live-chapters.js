const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname,'qa/p-livech'), args: ['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('https://higher-heights.vercel.app/', { waitUntil:'networkidle2', timeout:60000 });
  await sleep(2500);
  await p.evaluate(() => { const t=document.getElementById('work-track'); scrollTo(0, t.offsetTop + (t.offsetHeight-innerHeight)*0.45); });
  await sleep(2000);
  const st = await p.evaluate(() => ({
    title: document.getElementById('w-title').innerText.replace(/\n/g,' '),
    idx: document.getElementById('w-idx').textContent.trim(),
    credit: document.getElementById('w-credit').textContent.trim(),
    playing: Array.from(document.querySelectorAll('.work__media video')).filter(v=>v.classList.contains('is-on')).map(v=>({src:(v.currentSrc||'').split('/').pop(), paused:v.paused, w:v.videoWidth}))
  }));
  await p.screenshot({ path: path.resolve(__dirname,'qa/live-chapter.png') });
  console.log(JSON.stringify({ st, errs }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-v9'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8083/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1500);

  // scroll into the work track so a chapter is live
  await p.evaluate(() => {
    const t = document.getElementById('work-track');
    window.scrollTo(0, t.offsetTop + (t.offsetHeight - innerHeight) * 0.45);
  });
  await sleep(1400);

  const r = await p.evaluate(() => {
    const rail = document.getElementById('w-rail');
    const strip = document.getElementById('strip');
    const live = rail.querySelector('.is-live');
    return {
      railItems: rail.children.length,
      railHasNumerals: /\b0[0-9]\b/.test(rail.textContent),
      railLiveText: live ? live.textContent.trim() : null,
      railLiveTickWidth: live ? getComputedStyle(live.querySelector('i')).width : null,
      railIdleTickWidth: getComputedStyle(rail.children[7].querySelector('i')).width,
      stripFirst: strip.children[0].textContent.trim(),
      stripHasNumerals: /\b0[0-9]\b/.test(strip.textContent),
      idxLine: document.getElementById('w-idx').textContent,
      chapterTitle: document.getElementById('w-title').textContent.trim(),
      credit: document.getElementById('w-credit').textContent,
      bodyHasNumerals: /(?:^|[^\d])0[1-8](?:\s*[—–-]|\s*$)/m.test(document.body.innerText),
    };
  });
  console.log(JSON.stringify({ ...r, errs: [...new Set(errs)] }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

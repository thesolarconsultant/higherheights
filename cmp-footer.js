const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(__dirname, 'qa/p6'), args: ['--no-first-run', '--hide-scrollbars'] });
  const out = {};
  for (const [name, url] of [['v1', 'http://127.0.0.1:8099/index.html'], ['v2', 'http://127.0.0.1:8098/index.html']]) {
    const p = await b.newPage();
    await p.setViewport({ width: 1600, height: 1000 });
    await p.goto(url, { waitUntil: 'networkidle2' });
    await sleep(1500);
    out[name] = await p.evaluate(() => {
      const f = document.querySelector('.footer');
      const g = document.querySelector('.footer__grid');
      const img = document.querySelector('.footer__logo');
      const fr = f.getBoundingClientRect();
      const ir = img.getBoundingClientRect();
      const nav = document.querySelector('.brand').getBoundingClientRect();
      return {
        pageH: document.documentElement.scrollHeight,
        footerH: Math.round(fr.height),
        gridH: Math.round(g.getBoundingClientRect().height),
        imgBox: { w: Math.round(ir.width), h: Math.round(ir.height), bottomGap: Math.round(fr.bottom - ir.bottom) },
        imgNatural: { w: img.naturalWidth, h: img.naturalHeight },
        brandBox: { w: Math.round(nav.width), h: Math.round(nav.height) },
        bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0],
      };
    });
    await p.screenshot({ path: path.resolve(__dirname, 'qa/footer-' + name + '.png'), clip: { x: 0, y: out[name].pageH - 420, width: 1600, height: 420 } }).catch(() => {});
    await p.close();
  }
  console.log(JSON.stringify(out, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

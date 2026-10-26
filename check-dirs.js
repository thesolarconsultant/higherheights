const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-dirs'), args: ['--no-first-run', '--hide-scrollbars'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('requestfailed', r => errs.push('FAIL ' + r.url().split('/').slice(-2).join('/')));
  await p.setViewport({ width: 1180, height: 900 });
  const file = path.resolve(__dirname, 'brand', 'directions.html').split(path.sep).join('/');
  await p.goto('file:///' + file, { waitUntil: 'networkidle0', timeout: 60000 });
  await sleep(1200);
  const r = await p.evaluate(() => {
    const imgs = Array.from(document.images);
    return {
      cards: document.querySelectorAll('.dir').length,
      imgCount: imgs.length,
      broken: imgs.filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
      heroHeights: Array.from(document.querySelectorAll('.hero')).map(h => Math.round(h.getBoundingClientRect().height)),
      iconsPerCard: Array.from(document.querySelectorAll('.icons__row')).map(x => x.children.length),
      colourMixSupported: CSS.supports('background', 'color-mix(in srgb, #000 50%, transparent)'),
      schemes: Array.from(document.querySelectorAll('.dir')).map(d => ({
        bg: getComputedStyle(d).getPropertyValue('--bg').trim(),
        title: getComputedStyle(d.querySelector('.hero__title')).color,
      })),
    };
  });
  console.log(JSON.stringify({ ...r, errs: [...new Set(errs)] }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

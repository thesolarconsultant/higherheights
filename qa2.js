const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'http://127.0.0.1:8099/index.html';
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(__dirname, 'qa/profile2'), args: ['--no-first-run', '--window-size=1440,900'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  // full scroll to trigger lazy loading
  await p.evaluate(async () => {
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y <= H; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 160)); }
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 1200));
  });
  await new Promise(r => setTimeout(r, 1500));
  const res = await p.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    return {
      total: imgs.length,
      notLoaded: imgs.filter(i => i.naturalWidth === 0).map(i => i.getAttribute('src')),
      lazy: imgs.filter(i => i.loading === 'lazy').length,
      sized: imgs.map(i => i.getAttribute('src') + ' ' + i.naturalWidth + 'x' + i.naturalHeight),
      // accessibility quick pass
      noAlt: imgs.filter(i => !i.getAttribute('alt') && i.getAttribute('alt') !== '').map(i => i.getAttribute('src')),
      emptyAlt: imgs.filter(i => i.getAttribute('alt') === '').length,
      btnNoLabel: Array.from(document.querySelectorAll('button')).filter(b => !b.textContent.trim() && !b.getAttribute('aria-label')).length,
      links: Array.from(document.querySelectorAll('a[href]')).map(a => ({ href: a.getAttribute('href'), text: a.textContent.replace(/\s+/g, ' ').trim().slice(0, 40), aria: a.getAttribute('aria-label') })),
      focusable: document.querySelectorAll('a[href],button,[tabindex]:not([tabindex="-1"])').length,
      videosWithSound: Array.from(document.querySelectorAll('video')).map(v => v.getAttribute('muted') !== null),
      metaDesc: document.querySelector('meta[name=description]')?.content.length,
      lang: document.documentElement.lang,
      h1count: document.querySelectorAll('h1').length,
    };
  });
  console.log(JSON.stringify(res, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

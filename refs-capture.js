const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'refs');
fs.mkdirSync(OUT, { recursive: true });

const SITES = [
  ['somesuch', 'https://somesuch.com'],
  ['pulse-films', 'https://www.pulsefilms.com'],
  ['caviar', 'https://www.caviar.tv'],
  ['riff-raff', 'https://www.riffraff.tv'],
  ['iconoclast', 'https://iconoclast.tv'],
  ['partizan', 'https://www.partizan.com'],
  ['biscuit', 'https://biscuitfilmworks.com'],
  ['mjz', 'https://www.mjz.com'],
  ['superprime', 'https://www.superprime.tv'],
  ['prettybird', 'https://prettybird.co'],
  ['division', 'https://division.tv'],
  ['ocean-air', 'https://oceanairmedia.com'],
  ['acquafilms', 'https://www.acquafilms.com'],
  ['yacht-media-crew', 'https://yachtmediacrew.com'],
];

(async () => {
  const b = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    userDataDir: path.resolve(OUT, '.profile'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required',
           '--disable-blink-features=AutomationControlled', '--window-size=1440,900'],
  });
  const manifest = [];
  for (const [slug, url] of SITES) {
    const p = await b.newPage();
    const rec = { slug, url, ok: false };
    try {
      await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
      await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await sleep(6500); // let autoplay video start
      rec.title = await p.title();
      rec.media = await p.evaluate(() => ({
        videos: document.querySelectorAll('video').length,
        canvases: document.querySelectorAll('canvas').length,
        heroImgs: document.querySelectorAll('img').length,
        bodyBg: getComputedStyle(document.body).backgroundColor,
        scrollH: document.documentElement.scrollHeight,
        text: (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 220),
      }));
      const f = path.join(OUT, slug + '.png');
      await p.screenshot({ path: f });
      rec.shot = f;
      rec.ok = true;
      rec.bytes = fs.statSync(f).size;
    } catch (e) {
      rec.error = e.message.slice(0, 80);
    }
    manifest.push(rec);
    console.log(JSON.stringify(rec).slice(0, 300));
    await p.close();
  }
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

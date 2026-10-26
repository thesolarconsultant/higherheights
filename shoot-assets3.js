const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const DIR = path.resolve(__dirname, 'brand');
const ICONS = path.join(DIR, 'icons3');
const SITE_IMG = path.resolve(__dirname, 'site-v5', 'assets', 'img');
fs.mkdirSync(ICONS, { recursive: true });

const HH = fs.readFileSync(path.join(DIR, 'logos2', 'hh-flat-gold.svg'), 'utf8');
const inner = HH.split('</svg>')[0].split('>').slice(1).join('>');
const W = 713, H = 854;

function page(bg, padRatio) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    html,body{margin:0;background:${bg};width:100%;height:100%;display:grid;place-items:center;overflow:hidden}
    svg{display:block;height:calc(100% * ${1 - padRatio * 2});width:auto}
  </style></head><body>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}">${inner}</svg>
  </body></html>`;
}

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.join(DIR, '.pptr-ic2'), args: ['--no-first-run', '--hide-scrollbars', '--force-device-scale-factor=1'] });
  const tmp = path.join(ICONS, '_t.html');
  const out = [];

  for (const size of [16, 32, 48, 180, 512]) {
    fs.writeFileSync(tmp, page('#050936', size <= 32 ? 0.06 : 0.14));
    const p = await b.newPage();
    await p.setViewport({ width: size, height: size });
    await p.goto('file:///' + tmp.replace(/\\/g, '/'), { waitUntil: 'load' });
    await sleep(100);
    const f = path.join(ICONS, `icon-${size}.png`);
    await p.screenshot({ path: f });
    out.push([`icon-${size}`, fs.statSync(f).size]);
    await p.close();
  }
  fs.unlinkSync(tmp);

  // share image: wordmark + flat HH
  const og = await b.newPage();
  await og.setViewport({ width: 1200, height: 630 });
  await og.goto('file:///' + path.join(DIR, 'og3.html').replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
  await sleep(600);
  const ogf = path.join(DIR, 'og-image-v3.png');
  await og.screenshot({ path: ogf, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  out.push(['og', fs.statSync(ogf).size]);
  await og.close();

  // publish into the site
  for (const size of [16, 32, 48, 180]) {
    fs.copyFileSync(path.join(ICONS, `icon-${size}.png`), path.join(SITE_IMG, `icon-${size}.png`));
  }
  fs.copyFileSync(ogf, path.join(SITE_IMG, 'og-image.png'));

  console.log(JSON.stringify(out));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

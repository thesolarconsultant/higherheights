const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const DIR = path.resolve(__dirname, 'brand');
const ICONS = path.join(DIR, 'icons');
fs.mkdirSync(ICONS, { recursive: true });

const HH = fs.readFileSync(path.join(DIR, 'logos', 'seal-mark-gold.svg'), 'utf8');
const inner = HH.split('</svg>')[0].split('>').slice(1).join('>');

function page(bg, pad) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    html,body{margin:0;background:${bg};display:grid;place-items:center;width:100%;height:100%}
    svg{width:calc(100% - ${pad * 2}px);height:calc(100% - ${pad * 2}px);display:block}
  </style></head><body>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 594 609">${inner}</svg>
  </body></html>`;
}

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: path.resolve(DIR, '.pptr-icons'), args: ['--no-first-run', '--hide-scrollbars', '--force-device-scale-factor=1'] });
  const out = [];

  // ── app icons: navy field, gold HH ─────────────────────────────────────
  const tmp = path.join(ICONS, '_icon.html');
  for (const size of [16, 32, 48, 180, 512]) {
    fs.writeFileSync(tmp, page('#0B1A26', Math.max(1, Math.round(size * 0.13))));
    const p = await b.newPage();
    await p.setViewport({ width: size, height: size, deviceScaleFactor: 1 });
    await p.goto('file:///' + tmp.replace(/\\/g, '/'), { waitUntil: 'load' });
    await sleep(120);
    const f = path.join(ICONS, `icon-${size}.png`);
    await p.screenshot({ path: f, omitBackground: false });
    out.push([f, fs.statSync(f).size]);
    await p.close();
  }

  // ── cream tile variant (for light contexts) ────────────────────────────
  
  const creamSrc = fs.readFileSync(path.join(DIR, 'logos', 'seal-mark-navy.svg'), 'utf8');
  fs.writeFileSync(tmp, page('#F4EFE6', 24).replace(/<svg xmlns[\s\S]*<\/svg>\s*<\/body>/, creamSrc.trim() + '</body>'));
  {
    const p = await b.newPage();
    await p.setViewport({ width: 180, height: 180 });
    await p.goto('file:///' + tmp.replace(/\\/g, '/'), { waitUntil: 'load' });
    await sleep(120);
    const f = path.join(ICONS, 'icon-180-cream.png');
    await p.screenshot({ path: f });
    out.push([f, fs.statSync(f).size]);
    await p.close();
  }
  fs.unlinkSync(tmp);

  // ── share image 1200x630 ───────────────────────────────────────────────
  {
    const p = await b.newPage();
    await p.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
    await p.goto('file:///' + path.join(DIR, 'og.html').replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
    await sleep(700);
    const f = path.join(DIR, 'og-image.png');
    await p.screenshot({ path: f, clip: { x: 0, y: 0, width: 1200, height: 630 } });
    out.push([f, fs.statSync(f).size]);
    await p.close();
  }

  console.log(JSON.stringify(out));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

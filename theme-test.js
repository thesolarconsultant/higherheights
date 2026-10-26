const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, 'qa');

const hex2rgb = h => {
  const n = parseInt(h.replace('#', ''), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};

const VARIANTS = [
  { name: 'near-black', bg: '#08080A', ink: '#FFFFFF', rgba: 'rgba(8,8,10,' },
  { name: 'deeper-navy', bg: '#0B1024', ink: '#FFFFFF', rgba: 'rgba(11,16,36,' },
  { name: 'scrim-off-navy', bg: '#050936', ink: '#FFFFFF', rgba: 'rgba(5,9,54,', lightScrim: true },
  { name: 'bone-light', bg: '#F2EFE9', ink: '#0B0B0C', rgba: 'rgba(242,239,233,', light: true },
];

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(OUT, 'p-themes'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });

  for (const v of VARIANTS) {
    const p = await b.newPage();
    await p.setViewport({ width: 1440, height: 900 });
    await p.goto('http://127.0.0.1:8082/', { waitUntil: 'networkidle2', timeout: 60000 });
    await sleep(2600);

    const css = v.light
      ? `
      body,.reel,.contact{background:${v.bg} !important;color:${v.ink} !important}
      .reel__stage::after{background:
        linear-gradient(to top,${v.rgba}.88) 0%,${v.rgba}.34) 34%,${v.rgba}0) 66%),
        linear-gradient(to bottom,${v.rgba}.55) 0%,${v.rgba}0) 26%) !important}
      .strip{background:${v.rgba}.72) !important;border-top-color:rgba(11,11,12,.18) !important}
      .strip button{border-right-color:rgba(11,11,12,.12) !important}
      .strip .t,.strip button.is-live .t{color:${v.ink} !important}
      .strip .n{color:rgba(11,11,12,.55) !important}
      .micra,.micro,.credits .k,.panel__credit{color:rgba(11,11,12,.55) !important}
      .credits .v,.title,.panel__title,.panel__note{color:${v.ink} !important}
      .top::before{background:linear-gradient(to bottom,${v.rgba}.85),transparent) !important}
      .foot{color:rgba(11,11,12,.45) !important}
      `
      : `
      body,.reel,.contact{background:${v.bg} !important}
      .reel__stage::after{background:
        linear-gradient(to top,${v.rgba}.90) 0%,${v.rgba}.42) 30%,${v.rgba}0) 64%),
        linear-gradient(to bottom,${v.rgba}.62) 0%,${v.rgba}0) 24%) !important}
      .strip{background:${v.rgba}.42) !important}
      .top::before{background:linear-gradient(to bottom,${v.rgba}.82),${v.rgba}.28) 55%,${v.rgba}0)) !important}
      .panel{background:${v.bg} !important}
      `;

    await p.evaluate(c => {
      const s = document.createElement('style');
      s.textContent = c;
      document.head.appendChild(s);
    }, css);
    await sleep(900);
    const f = path.join(OUT, 'theme-' + v.name + '.png');
    await p.screenshot({ path: f });
    console.log(v.name, '→', f);
    await p.close();
  }
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));

const DEVICES = [
  { n: 'iPhone 14',      width: 390,  height: 844,  touch: true,  mobile: true  },
  { n: 'iPad portrait',  width: 768,  height: 1024, touch: true,  mobile: true  },
  { n: 'iPad landscape', width: 1024, height: 768,  touch: true,  mobile: true  },
  { n: 'desktop mouse',  width: 1440, height: 900,  touch: false, mobile: false },
];

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: 'new', userDataDir: path.resolve(__dirname, '../qa/p-touch'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });

  for (const d of DEVICES) {
    const p = await b.newPage();
    await p.setCacheEnabled(false);
    await p.setViewport({ width: d.width, height: d.height,
                          hasTouch: d.touch, isMobile: d.mobile, deviceScaleFactor: 2 });
    await p.goto('http://127.0.0.1:8092/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
    await sleep(2200);

    // bring the strip into view
    await p.evaluate(() => {
      const s = document.querySelector('.strip');
      if (s) s.scrollIntoView({ block: 'center' });
    });
    await sleep(900);

    const before = await p.evaluate(() => {
      const s = document.querySelector('.strip');
      const pin = document.querySelector('[data-pin], .pin');
      if (!s) return { err: 'no strip' };
      const cs = getComputedStyle(s);
      return {
        touchAction: cs.touchAction,
        scrollLeft: Math.round(s.scrollLeft),
        scrollable: s.scrollWidth - s.clientWidth,
        pinOff: pin ? pin.classList.contains('pin--off') : null,
        stageePos: pin ? getComputedStyle(pin.querySelector('.pin__stage') || pin).position : null,
      };
    });

    // real touch swipe, or mouse drag on desktop
    let after = before.scrollLeft;
    if (d.touch) {
      const box = await p.evaluate(() => {
        const s = document.querySelector('.strip'); const r = s.getBoundingClientRect();
        return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
      });
      await p.touchscreen.touchStart(box.x + 160, box.y);
      for (let i = 1; i <= 8; i++) await p.touchscreen.touchMove(box.x + 160 - i * 22, box.y);
      await p.touchscreen.touchEnd();
      await sleep(900);
      after = await p.evaluate(() => Math.round(document.querySelector('.strip').scrollLeft));
    } else {
      const box = await p.evaluate(() => {
        const s = document.querySelector('.strip'); const r = s.getBoundingClientRect();
        return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
      });
      await p.mouse.move(box.x + 160, box.y);
      await p.mouse.down();
      for (let i = 1; i <= 8; i++) await p.mouse.move(box.x + 160 - i * 22, box.y);
      await p.mouse.up();
      await sleep(700);
      after = await p.evaluate(() => Math.round(document.querySelector('.strip').scrollLeft));
    }

    const moved = after - before.scrollLeft;
    const verdict = before.scrollable > 0
      ? (moved > 20 ? 'SCROLLS ✓' : 'STUCK ✗')
      : 'nothing to scroll';
    console.log(
      `${d.n.padEnd(15)} touch-action:${String(before.touchAction).padEnd(12)} ` +
      `pin--off:${String(before.pinOff).padEnd(5)} stage:${String(before.stageePos).padEnd(7)} ` +
      `scrollLeft ${before.scrollLeft}->${after} (${moved >= 0 ? '+' : ''}${moved})  ${verdict}`
    );
    await p.close();
  }
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

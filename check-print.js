const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-print'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2200);

  const diag = await p.evaluate(() => {
    const q = s => document.querySelector(s);
    const z = s => { const e = q(s); return e ? getComputedStyle(e).zIndex : null; };
    const g = q('.print__grain');
    const gs = g && getComputedStyle(g);
    return {
      layers: {
        print: !!q('.print'), grain: !!g,
        flick: !!q('.print__flick'), scratches: document.querySelectorAll('.print__scratch').length,
      },
      stack: { media: z('.hero__media'), print: z('.print'), inner: z('.hero__inner'), scrim: z('.hero__scrim') },
      grain: gs && {
        blend: gs.mixBlendMode, opacity: gs.opacity,
        anim: gs.animationName + ' ' + gs.animationDuration,
        tile: gs.backgroundSize,
        hasImage: gs.backgroundImage.startsWith('url("data:image/svg'),
      },
      heroVideoPlaying: (() => { const v = q('#heroVideo'); return v ? !v.paused && v.readyState > 2 : null; })(),
    };
  });
  console.log('DIAG', JSON.stringify(diag, null, 2));

  // prove the grain actually moves: two frames, measure the delta
  const clip = { x: 300, y: 220, width: 320, height: 200 };
  const a = await p.screenshot({ clip, encoding: 'base64' });
  await sleep(420);
  const c = await p.screenshot({ clip, encoding: 'base64' });
  console.log('frames identical?', a === c, '(false = grain is moving)');

  await p.screenshot({ path: 'brand/print-hero.jpg', quality: 92, type: 'jpeg' });
  // a 3x crop so the grain texture is actually visible
  await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 3 });
  await sleep(500);
  await p.screenshot({ path: 'brand/print-zoom.jpg', quality: 94, type: 'jpeg',
    clip: { x: 430, y: 300, width: 300, height: 190 } });
  console.log('errs', [...new Set(errs)]);
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

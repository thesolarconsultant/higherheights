// Live QA: load the Higher Heights site in system Chrome, capture console/network errors, screenshots.
const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const OUT = path.resolve(__dirname, 'qa');
const fs = require('fs');
fs.mkdirSync(OUT, { recursive: true });

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'http://127.0.0.1:8099/index.html';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    userDataDir: path.resolve(OUT, 'profile'),
    args: ['--no-first-run', '--no-default-browser-check', '--autoplay-policy=no-user-gesture-required', '--window-size=1600,1000'],
  });
  const page = await browser.newPage();
  const errors = [], failed = [], consoleMsgs = [];
  page.on('console', m => { if (['error', 'warning'].includes(m.type())) consoleMsgs.push(m.type() + ': ' + m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => failed.push(r.url() + ' :: ' + (r.failure() && r.failure().errorText)));
  page.on('response', r => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url()); });

  await page.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 1 });
  await page.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 2500));

  // structural audit
  const audit = await page.evaluate(() => {
    const q = s => Array.from(document.querySelectorAll(s));
    const vids = q('video').map(v => ({ src: v.currentSrc || v.getAttribute('src'), ready: v.readyState, dur: isFinite(v.duration) ? +v.duration.toFixed(1) : null, w: v.videoWidth, h: v.videoHeight, paused: v.paused }));
    const imgs = q('img').map(i => ({ src: i.getAttribute('src'), nat: i.naturalWidth, shown: i.getBoundingClientRect().width > 0 }));
    return {
      title: document.title,
      height: document.documentElement.scrollHeight,
      sections: q('section').map(s => s.className || s.id),
      videos: vids,
      brokenImgs: imgs.filter(i => i.nat === 0).map(i => i.src),
      hiddenImgs: imgs.filter(i => !i.shown).map(i => i.src),
      h1: q('h1').map(h => h.textContent.trim()),
      h2: q('h2').map(h => h.textContent.replace(/\s+/g, ' ').trim()),
      anchors: q('a[href^="#"]').map(a => a.getAttribute('href')).filter((v, i, a) => a.indexOf(v) === i).map(h => ({ h, ok: !!document.querySelector(h) })),
      filmCards: q('.film').length,
      fonts: document.fonts ? document.fonts.status : 'n/a',
      overflowX: document.documentElement.scrollWidth > window.innerWidth + 1 ? document.documentElement.scrollWidth : 0,
      serviceLinks: Array.from(document.querySelectorAll('a')).map(a => a.getAttribute('href')).filter(h => h && /^https?:/.test(h)),
    };
  });

  await page.screenshot({ path: path.join(OUT, 'live-hero.png') });

  // scroll through and capture each section
  const shots = [];
  const anchors = ['#work', '#aerial', '#product', '#studio', '#contact'];
  for (const a of anchors) {
    await page.evaluate(sel => document.querySelector(sel).scrollIntoView({ behavior: 'instant', block: 'start' }), a);
    await new Promise(r => setTimeout(r, 1200));
    const f = path.join(OUT, 'live' + a.replace('#', '-') + '.png');
    await page.screenshot({ path: f });
    shots.push(f);
    // nudge for lazy stuff
    await page.evaluate(() => window.scrollBy(0, 400));
    await new Promise(r => setTimeout(r, 600));
  }

  // open a film modal (lightbox) if it exists
  let modalInfo = null;
  await page.evaluate(() => document.querySelector('#work').scrollIntoView({ behavior: 'instant' }));
  await new Promise(r => setTimeout(r, 800));
  const card = await page.$('.film');
  if (card) {
    await card.click();
    await new Promise(r => setTimeout(r, 1800));
    modalInfo = await page.evaluate(() => {
      const m = document.querySelector('[class*="modal"], dialog, [role="dialog"]');
      return m ? { cls: m.className, open: getComputedStyle(m).display, text: m.textContent.replace(/\s+/g, ' ').slice(0, 300), vids: Array.from(m.querySelectorAll('video')).map(v => ({ src: v.currentSrc, dur: v.duration, paused: v.paused })) } : null;
    });
    await page.screenshot({ path: path.join(OUT, 'live-modal.png') });
  }

  // mobile
  const mob = await browser.newPage();
  await mob.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await mob.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 2000));
  const mobOverflow = await mob.evaluate(() => ({
    sw: document.documentElement.scrollWidth, iw: window.innerWidth,
    offenders: Array.from(document.querySelectorAll('*')).filter(e => e.getBoundingClientRect().right > window.innerWidth + 2).slice(0, 12).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 40)),
  }));
  await mob.screenshot({ path: path.join(OUT, 'live-mobile-hero.png') });
  await mob.evaluate(() => window.scrollBy(0, 900));
  await new Promise(r => setTimeout(r, 900));
  await mob.screenshot({ path: path.join(OUT, 'live-mobile-2.png') });

  console.log(JSON.stringify({ audit, errors, failed: [...new Set(failed)], consoleMsgs: [...new Set(consoleMsgs)], modalInfo, mobOverflow, shots }, null, 2));
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });

const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-de'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2400);

  // ── structural sanity: did the surgery leave valid nesting? ──
  const dom = await p.evaluate(() => ({
    pin: !!document.querySelector('[data-pin]'),
    pinInsideProduct: !!document.querySelector('#product [data-pin]'),
    stripInsidePin: !!document.querySelector('[data-pin] .pin__row'),
    noteAfterPin: !!document.querySelector('#product .wrap .product__note'),
    band: !!document.querySelector('.band'),
    enqInBand: !!document.querySelector('.band .enq'),
    foot: !!document.querySelector('.foot'),
    oldFooterGone: !document.querySelector('.footer'),
    marqRows: document.querySelectorAll('.marq__row').length,
  }));
  console.log('DOM      ', JSON.stringify(dom));

  // ── pin: does it actually travel? ──
  const pinInfo = await p.evaluate(() => {
    const pin = document.querySelector('[data-pin]');
    return {
      off: pin.classList.contains('pin--off'),
      height: pin.offsetHeight,
      viewport: window.innerHeight,
      sticky: getComputedStyle(pin.querySelector('.pin__stage')).position,
    };
  });
  console.log('PIN      ', JSON.stringify(pinInfo));

  const sample = async frac => {
    await p.evaluate(f => {
      const pin = document.querySelector('[data-pin]');
      const abs = pin.getBoundingClientRect().top + window.scrollY;
      window.scrollTo(0, abs + (pin.offsetHeight - innerHeight) * f);
    }, frac);
    await sleep(500);
    return p.evaluate(() => {
      const row = document.querySelector('.pin__row');
      const bar = document.querySelector('.pin__meter i');
      const r = document.querySelector('.pin__stage').getBoundingClientRect();
      return {
        x: Math.round(new DOMMatrix(getComputedStyle(row).transform).m41),
        bar: bar ? bar.style.transform : null,
        stageTop: Math.round(r.top),
      };
    });
  };
  const a = await sample(0.02), m = await sample(0.5), z = await sample(0.98);
  console.log('pin @2%  ', JSON.stringify(a));
  console.log('pin @50% ', JSON.stringify(m));
  console.log('pin @98% ', JSON.stringify(z));
  console.log('-> travels:', a.x > m.x && m.x > z.x, ' stays pinned:',
    Math.abs(a.stageTop) < 3 && Math.abs(m.stageTop) < 3 && Math.abs(z.stageTop) < 3);

  // ── marquee ──
  const mq = await p.evaluate(() => {
    const rows = [...document.querySelectorAll('.marq__row')];
    return rows.map(r => ({
      kids: r.children.length,
      anim: getComputedStyle(r).animationName,
      dur: getComputedStyle(r).animationDuration,
      dir: getComputedStyle(r).animationDirection,
    }));
  });
  console.log('MARQUEE  ', JSON.stringify(mq));

  // ── footer ──
  await p.evaluate(() => document.querySelector('.foot').scrollIntoView());
  await sleep(1200);
  const f = await p.evaluate(() => {
    const ft = document.querySelector('.foot');
    const img = ft.querySelector('.foot__brand img');
    return {
      cols: ft.querySelectorAll('.foot__col').length,
      links: ft.querySelectorAll('a').length,
      wordmark: !!img && img.naturalWidth > 0,
      wordmarkSrc: img ? img.getAttribute('src').split('/').pop() : null,
      year: ft.querySelector('#year') ? ft.querySelector('#year').textContent : null,
      base: ft.querySelectorAll('.foot__base span').length,
    };
  });
  console.log('FOOTER   ', JSON.stringify(f));
  console.log('errs', [...new Set(errs)]);
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

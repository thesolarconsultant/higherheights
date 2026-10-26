const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-all'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  p.on('requestfailed', r => errs.push('REQ ' + r.url().split('/').pop()));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2200);

  // ── herotype: the masked rise ──
  const rise = await p.evaluate(() => {
    const t = document.querySelector('.hero__title');
    const sp = [...t.querySelectorAll('.rise > span')];
    return {
      up: t.classList.contains('is-up'),
      masks: t.querySelectorAll('.rise').length,
      overflow: getComputedStyle(t.querySelector('.rise')).overflow,
      transforms: sp.map(e => getComputedStyle(e).transform),
    };
  });
  console.log('herotype  ', JSON.stringify(rise));

  // ── softfocus: rack ──
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 400) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 35));
    }
  });
  await sleep(1400);
  const rack = await p.evaluate(() => {
    const all = [...document.querySelectorAll('.rack')];
    const img = all[0] && all[0].querySelector('img');
    return {
      count: all.length,
      withViewfinder: all.filter(e => e.querySelector('.rack__vf')).length,
      stillBlurred: all.filter(e => {
        const i = e.querySelector('img');
        return i && getComputedStyle(i).filter !== 'none';
      }).length,
      sampleFilter: img ? getComputedStyle(img).filter : null,
    };
  });
  console.log('softfocus ', JSON.stringify(rack));

  // ── client wall ──
  const cw = await p.evaluate(() => {
    const marks = [...document.querySelectorAll('.client__mark')];
    return {
      logos: marks.length,
      masked: marks.filter(m => getComputedStyle(m).maskImage !== 'none'
                             || getComputedStyle(m).webkitMaskImage !== 'none').length,
      labelled: marks.filter(m => m.getAttribute('aria-label')).length,
      restColour: marks[0] ? getComputedStyle(marks[0]).backgroundColor : null,
      tints: [...new Set(marks.map(m => m.parentElement.style.getPropertyValue('--tint')))].length,
    };
  });
  console.log('clients   ', JSON.stringify(cw));

  // ── enquiry: walk the whole flow ──
  await p.evaluate(() => document.getElementById('enquiry').scrollIntoView());
  await sleep(900);
  const steps = [];
  const state = () => p.evaluate(() => {
    const on = document.querySelector('.enq__screen.is-on');
    return {
      step: on ? +on.dataset.step : null,
      q: on ? on.querySelector('.enq__q').textContent.trim() : null,
      done: document.querySelectorAll('.enq__rail i.is-done').length,
    };
  });
  steps.push(await state());
  await p.click('.enq__screen.is-on .enq__opt:nth-child(2) span'); await sleep(700);
  steps.push(await state());
  await p.click('.enq__screen.is-on .enq__opt:nth-child(1) span'); await sleep(700);
  steps.push(await state());

  const band = await p.evaluate(() => ({
    money: document.getElementById('enqMoney').textContent,
    band: document.getElementById('enqBand').textContent.slice(0, 40) + '…',
    buys: document.querySelectorAll('.enq__buys li').length,
  }));
  // drag the budget up
  await p.evaluate(() => {
    const r = document.querySelector('.enq__range');
    r.value = 30000; r.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await sleep(400);
  const band2 = await p.evaluate(() => ({
    money: document.getElementById('enqMoney').textContent,
    band: document.getElementById('enqBand').textContent.slice(0, 40) + '…',
  }));
  await p.click('#enqNext'); await sleep(700);
  steps.push(await state());

  console.log('enquiry   ', JSON.stringify(steps));
  console.log('budget @10k', JSON.stringify(band));
  console.log('budget @30k', JSON.stringify(band2));

  // validation must block an empty email
  const blocked = await p.evaluate(async () => {
    document.getElementById('enqNext').click();
    await new Promise(r => setTimeout(r, 500));
    const on = document.querySelector('.enq__screen.is-on');
    return +on.dataset.step;
  });
  console.log('empty email blocked at step', blocked, blocked === 3 ? '(correct)' : '(LEAKED)');

  console.log('errs', [...new Set(errs)]);
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

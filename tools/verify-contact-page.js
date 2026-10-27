// Independent verification of /contact (orchestrator-written, not the builder's).
const pt = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const BASE = 'http://127.0.0.1:8120';
let fails = 0;
const ok = (name, cond, extra = '') => { console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? '  [' + extra + ']' : '')); if (!cond) fails++; };

(async () => {
  const b = await pt.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: 'new',
    userDataDir: path.resolve(__dirname, '../qa/p-orch'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required']
  });
  const errs = [], badReq = [];
  const p = await b.newPage();
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('requestfailed', r => badReq.push(r.url()));
  p.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) badReq.push(r.status() + ' ' + r.url()); });
  await p.setCacheEnabled(false);
  await p.setViewport({ width: 1440, height: 900 });

  const resp = await p.goto(BASE + '/contact', { waitUntil: 'networkidle2', timeout: 60000 });
  ok('/contact returns 200', resp.status() === 200, String(resp.status()));
  await sleep(2600);
  const info = await p.evaluate(() => ({
    h1s: [...document.querySelectorAll('h1')].map(h => h.textContent.replace(/\s+/g, ' ').trim()),
    navContact: [...document.querySelectorAll('.nav a')].map(a => a.getAttribute('href')).filter(h => /contact/i.test(h || '')),
    drawerContact: [...document.querySelectorAll('#drawer a')].map(a => a.getAttribute('href')).filter(h => /contact/i.test(h || '')),
    megaContact: [...document.querySelectorAll('#mega a')].map(a => a.getAttribute('href')).filter(h => /contact/i.test(h || '')),
    watermark: !!document.querySelector('.hh-wm--contact'),
    footer: !!document.querySelector('footer.foot'),
    screens: document.querySelectorAll('.enq__screen').length,
    navH: (() => { const n = document.querySelector('#nav'); return n ? n.getBoundingClientRect().height : 0; })(),
    canonical: (document.querySelector('link[rel=canonical]') || {}).href,
    ogurl: (document.querySelector('meta[property="og:url"]') || {}).content
  }));
  ok('exactly one h1', info.h1s.length === 1, info.h1s.join(' | '));
  ok('h1 reads the ask', /have something/i.test(info.h1s[0] || '') && /filming/i.test(info.h1s[0] || ''));
  ok('nav Contact -> /contact', info.navContact.includes('/contact'), info.navContact.join(','));
  ok('drawer Contact -> /contact', info.drawerContact.includes('/contact'), info.drawerContact.join(','));
  ok('mega Contact -> /contact', info.megaContact.includes('/contact'), info.megaContact.join(','));
  ok('watermark present', info.watermark);
  ok('footer present', info.footer);
  ok('nav has height', info.navH > 10, String(Math.round(info.navH)));
  ok('5 form screens', info.screens === 5, 'screens=' + info.screens);
  ok('canonical is /contact', /\/contact$/.test(info.canonical || ''), info.canonical);
  ok('og:url is /contact', /\/contact$/.test(info.ogurl || ''), info.ogurl);

  // sent=1 landing
  const p2 = await b.newPage();
  await p2.setCacheEnabled(false);
  await p2.setViewport({ width: 1440, height: 900 });
  await p2.goto(BASE + '/contact?sent=1', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const sent = await p2.evaluate(() => {
    const done = document.querySelector('.enq__done'), nav = document.querySelector('.enq__nav');
    const vis = el => el && el.getClientRects().length > 0 && getComputedStyle(el).display !== 'none';
    return { doneShown: vis(done), text: (done ? done.textContent : '').replace(/\s+/g, ' ').trim().slice(0, 70), continueHidden: !vis(nav) };
  });
  ok('?sent=1 shows thank-you', sent.doneShown, sent.text);
  ok('?sent=1 hides Continue/Back', sent.continueHidden);
  await p2.screenshot({ path: path.resolve(__dirname, '../qa/contact/orch-sent.png') });

  // error landing
  const pe = await b.newPage();
  await pe.setCacheEnabled(false);
  await pe.setViewport({ width: 1440, height: 900 });
  await pe.goto(BASE + '/contact?error=1', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const er = await pe.evaluate(() => ({ onStep: (document.querySelector('.enq__screen.is-on') || { dataset: {} }).dataset.step, err: (document.getElementById('enqErr') || {}).textContent }));
  ok('?error returns to the reply step with a message', er.onStep === '3' && /\S/.test(er.err || ''), er.onStep + ' / ' + (er.err || '').slice(0, 40));

  // step flow: a radio choice auto-advances, so do not also click Continue
  const p3 = await b.newPage();
  await p3.setCacheEnabled(false);
  await p3.setViewport({ width: 1440, height: 900 });
  await p3.goto(BASE + '/contact', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const st = () => p3.evaluate(() => ({
    step: (document.querySelector('.enq__screen.is-on') || {}).dataset.step,
    hint: (() => { const h = document.getElementById('enqHint'); return h && !h.hidden ? h.textContent : ''; })(),
    money: (document.getElementById('enqMoney') || {}).textContent
  }));
  ok('starts on step 0', (await st()).step === '0');
  await p3.click('#enqNext');
  await sleep(500);
  let s = await st();
  ok('Continue with nothing chosen does not advance', s.step === '0', s.step);
  ok('and says why', /choose one/i.test(s.hint), s.hint);
  await p3.screenshot({ path: path.resolve(__dirname, '../qa/contact/orch-hint.png') });
  await p3.click('.enq__screen.is-on .enq__opt');
  await sleep(900);
  s = await st();
  ok('picking an option advances to step 1', s.step === '1', s.step);
  ok('hint clears on advance', s.hint === '', s.hint);
  await p3.click('.enq__screen.is-on .enq__opt');
  await sleep(900);
  s = await st();
  ok('advances to the budget step', s.step === '2', s.step);
  ok('no plus below max', !/\+/.test(s.money || ''), s.money);
  await p3.evaluate(() => {
    const r = document.querySelector('.enq__range');
    r.value = r.max;
    r.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await sleep(400);
  const buys = await p3.evaluate(() => ({
    money: (document.getElementById('enqMoney') || {}).textContent,
    band: (document.getElementById('enqBand') || {}).textContent,
    bullets: [...document.querySelectorAll('#enqBuys li')].map(li => li.textContent.trim()),
    back: !!document.querySelector('.enq__back:not([hidden])')
  }));
  ok('max shows the plus', buys.money === '£50,000+', buys.money);
  ok('band copy at max', /season|series/i.test(buys.band || ''), buys.band);
  ok('three bullets at max', buys.bullets.length === 3, buys.bullets.join(' | '));
  ok('BACK offered past step 0', buys.back);
  await p3.screenshot({ path: path.resolve(__dirname, '../qa/contact/orch-budget-max.png') });
  await p3.click('.enq__back');
  await sleep(700);
  s = await st();
  ok('BACK returns to step 1', s.step === '1', s.step);

  // mobile
  const p4 = await b.newPage();
  await p4.setCacheEnabled(false);
  await p4.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true });
  await p4.goto(BASE + '/contact', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const mob = await p4.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
  ok('no horizontal overflow at 390px', mob.sw <= mob.cw + 1, mob.sw + ' vs ' + mob.cw);
  await p4.screenshot({ path: path.resolve(__dirname, '../qa/contact/orch-mobile.png'), fullPage: true });

  // homepage regression
  const p5 = await b.newPage();
  await p5.setCacheEnabled(false);
  await p5.setViewport({ width: 1440, height: 900 });
  await p5.goto(BASE + '/', { waitUntil: 'networkidle2', timeout: 90000 });
  await sleep(2600);
  const home = await p5.evaluate(() => ({
    form: !!document.querySelector('#contact #enqForm'),
    steps: document.querySelectorAll('#contact .enq__screen').length,
    tag: (document.querySelector('#contact-head') || {}).tagName,
    head: (document.querySelector('#contact-head') || {}).textContent.replace(/\s+/g, ' ').trim()
  }));
  ok('homepage keeps its own form', home.form, 'screens=' + home.steps);
  ok('homepage heading still an h2', home.tag === 'H2', home.tag + ' ' + home.head);

  // service page nav still works
  const p6 = await b.newPage();
  await p6.setCacheEnabled(false);
  await p6.setViewport({ width: 1440, height: 900 });
  await p6.goto(BASE + '/corporate-video-production', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2600);
  const svc = await p6.evaluate(() => ({
    contact: [...document.querySelectorAll('.nav a')].map(a => a.getAttribute('href')).filter(h => /contact/i.test(h || '')),
    anchors: [...new Set([...document.querySelectorAll('a[href^="/#"], a[href^="#"]')].map(a => a.getAttribute('href')))],
    soh: document.body.innerHTML.indexOf('\u0001') !== -1
  }));
  ok('service page Contact -> /contact', svc.contact.includes('/contact'), svc.contact.join(','));
  ok('service page has no stray control chars', !svc.soh);
  ok('service page anchors are named', svc.anchors.every(h => /^\/?#[a-z]/i.test(h) || h === '/contact'), svc.anchors.slice(0, 8).join(','));

  ok('no console errors', errs.length === 0, errs.slice(0, 3).join(' || '));
  ok('no failed requests', badReq.length === 0, badReq.slice(0, 3).join(' || '));

  await b.close();
  console.log(fails === 0 ? '\nALL PASS' : '\n' + fails + ' FAILURES');
  process.exit(fails === 0 ? 0 : 1);
})().catch(e => { console.error('FATAL', e.message); process.exit(2); });

// Regression checks after the /contact work: homepage + four service pages.
// Needs `node tools/serve-local.js 8092`. Saves two proof screenshots to qa/contact/.
const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path'), fs = require('fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = path.resolve(__dirname, '../qa/contact');
const BASE = 'http://127.0.0.1:8092';
let fails = 0;
const check = (n, ok, d) => { if (!ok) fails++; console.log((ok ? 'PASS ' : 'FAIL ') + n + (d !== undefined ? '  [' + d + ']' : '')); };

(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, '../qa/p-contact'), args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'] });
  const pages = ['', 'corporate-video-production', 'videographer-london', 'event-videography', 'aerial-drone-filming', 'contact'];
  for (const pg of pages) {
    const p = await b.newPage(); await p.setCacheEnabled(false); await p.setViewport({ width: 1440, height: 900 });
    const bad = [];
    p.on('pageerror', e => bad.push('pageerror ' + e.message.slice(0, 80)));
    p.on('console', m => { if (m.type() === 'error') bad.push('console ' + m.text().slice(0, 80)); });
    p.on('requestfailed', r => bad.push('failed ' + r.url().split('/').pop()));
    p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url().split('/').pop()); });
    await p.goto(`${BASE}/${pg}`, { waitUntil: 'networkidle2', timeout: 60000 });
    await sleep(2800);
    const r = await p.evaluate(() => {
      const rect = e => e ? e.getBoundingClientRect() : { height: 0 };
      const contact = [...document.querySelectorAll('.nav__side a, #drawer a, .mega__a')].filter(a => /^contact/i.test(a.textContent.trim())).map(a => a.getAttribute('href'));
      return { nav: rect(document.querySelector('.nav__inner')).height, foot: rect(document.querySelector('.foot')).height,
        h1: document.querySelectorAll('h1').length, contact,
        // every in-page "#x" link on the page must have a target; every "/#x" link a target on the homepage (checked below)
        deadLocal: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(h.slice(1))),
        homeAnchors: [...document.querySelectorAll('a[href^="/#"]')].map(a => a.getAttribute('href')),
        loader: !!document.getElementById('hhload') };
    });
    const name = pg || 'index';
    check(`${name}: nav + footer render, h1 present`, r.nav > 30 && r.foot > 100 && r.h1 >= 1, `nav ${Math.round(r.nav)} foot ${Math.round(r.foot)} h1 ${r.h1}`);
    check(`${name}: Contact items -> /contact (header, mega, drawer)`, r.contact.length === 3 && r.contact.every(h => h === '/contact'), r.contact.join(','));
    check(`${name}: in-page anchors all have targets`, r.deadLocal.length === 0, r.deadLocal.join(',') || 'none dead');
    check(`${name}: no console errors / failed requests`, bad.length === 0, bad.join(' | ') || 'clean');
    if (pg !== '') {                      // the loader removes itself once dismissed, so read the served HTML
      const html = await (await fetch(`${BASE}/${pg}`)).text();
      check(`${name}: served HTML carries the loader`, html.includes('id="hhload"'));
    }
    // the homepage's /#x links must land on something real
    if (pg === '') {
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 20)); } });
      await sleep(400);
      await p.evaluate(() => { document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in', 'in', 'is-visible')); document.querySelectorAll('[data-gw] span').forEach(s => { s.style.opacity = '1'; s.style.transform = 'none'; }); });
      await p.evaluate(() => document.querySelector('#contact').scrollIntoView({ block: 'start' }));
      await sleep(900);
      await p.screenshot({ path: path.join(OUT, 'regress-home-contact-section-1440.png') });
      // mega-menu "now viewing" still marks Contact as current when the section is on screen (its href is now /contact)
      await p.evaluate(() => document.querySelector('#contact').scrollIntoView({ block: 'center' }));
      await sleep(900);
      const cur = await p.evaluate(() => [...document.querySelectorAll('.mega__a[aria-current="true"]')].map(a => a.getAttribute('href')));
      check('index: scrolling to #contact marks the mega Contact item current', cur.length === 1 && cur[0] === '/contact', cur.join(','));
      await p.evaluate(() => document.querySelector('#aerial').scrollIntoView({ block: 'center' }));
      await sleep(900);
      const cur2 = await p.evaluate(() => [...document.querySelectorAll('.mega__a[aria-current="true"]')].map(a => a.getAttribute('href')));
      check('index: scrolling to #aerial marks the mega Aerial item current', cur2.length === 1 && cur2[0] === '#aerial', cur2.join(','));
      await p.evaluate(() => document.querySelector('#contact').scrollIntoView({ block: 'start' }));
      await sleep(700);
      // jump links on the homepage still reach their sections
      const j = await p.evaluate(() => ['#work', '#aerial', '#product', '#studio', '#enquiry', '#contact'].map(h => [h, !!document.querySelector(h)]));
      check('index: anchors #work #aerial #product #studio #enquiry #contact still exist', j.every(x => x[1]), JSON.stringify(j));
      // in-page "#contact" CTA (link-arrow) and the form still work
      const cta = await p.evaluate(() => { const a = document.querySelector('a.link-arrow[href="#contact"]'); return !!a; });
      check('index: the in-page #contact CTA is untouched', cta);
      const form = await p.evaluate(() => ({ screens: document.querySelectorAll('#enqForm .enq__screen').length, h2: !!document.querySelector('#contact-head') && document.querySelector('#contact-head').tagName }));
      check('index: homepage form intact, heading still an h2', form.screens === 5 && form.h2 === 'H2', JSON.stringify(form));
    }
    if (pg === 'contact') {
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 20)); } });
      await sleep(400);
      await p.evaluate(() => { document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in', 'in', 'is-visible')); });
      await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await sleep(900);
      await p.screenshot({ path: path.join(OUT, 'contact-footer-1440.png') });
    }
    await p.close();
  }
  await b.close();
  console.log(fails ? `\n${fails} FAILED` : '\nall regression checks passed');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error('FATAL', e); process.exit(2); });

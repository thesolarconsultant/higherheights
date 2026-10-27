// QA for /contact: assertions plus the four screenshots, saved to qa/contact/.
// Needs `node tools/serve-local.js 8092` running (it honours vercel.json cleanUrls).
// Usage: node tools/qa-contact.js
const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path'), fs = require('fs'), http = require('http');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const BASE = 'http://127.0.0.1:8092';
const OUT = path.resolve(__dirname, '../qa/contact');
fs.mkdirSync(OUT, { recursive: true });

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: !!ok });
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  [' + detail + ']' : ''));
}
const status = url => new Promise((res, rej) =>
  http.get(url, r => { r.resume(); res({ code: r.statusCode, loc: r.headers.location }); }).on('error', rej));

// Load a page and wait out the loading screen (1.7s beat + 0.9s removal).
async function open(browser, url, vp) {
  const p = await browser.newPage();
  await p.setCacheEnabled(false);
  await p.setViewport(vp || { width: 1440, height: 900 });
  const bad = [];
  p.on('pageerror', e => bad.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') bad.push('console.error: ' + m.text()); });
  p.on('requestfailed', r => bad.push('requestfailed: ' + r.url()));
  p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
  p.bad = bad;
  await p.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2800);
  return p;
}
// Same reveal handling as tools/shot-page.js
async function settle(p) {
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 25)); }
    window.scrollTo(0, 0);
  });
  await sleep(500);
  await p.evaluate(() => {
    document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in', 'in', 'is-visible'));
    document.querySelectorAll('[data-gw] span').forEach(s => { s.style.opacity = '1'; s.style.transform = 'none'; });
  });
  await sleep(900);
}
const pick = (p, name, value) => p.click(`.enq__opt:has(input[name=${name}]${value ? `[value="${value}"]` : ''})`);
const step = p => p.evaluate(() => { const s = document.querySelector('.enq__screen.is-on'); return s ? +s.dataset.step : -1; });
const railDone = p => p.evaluate(() => [...document.querySelectorAll('.enq__rail i')].map(i => i.classList.contains('is-done')));
const money = p => p.evaluate(() => document.getElementById('enqMoney').textContent);
const setRange = (p, v) => p.evaluate(v => {
  const r = document.querySelector('.enq__range');
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(r, String(v));
  r.dispatchEvent(new Event('input', { bubbles: true }));
}, v);

(async () => {
  // ── HTTP level ──────────────────────────────────────────────────────────────
  const s1 = await status(BASE + '/contact');
  check('/contact returns 200', s1.code === 200, s1.code);
  const s2 = await status(BASE + '/contact?sent=1');
  check('/contact?sent=1 returns 200', s2.code === 200, s2.code);
  const s3 = await status(BASE + '/contact.html');
  check('/contact.html redirects to the clean URL (cleanUrls)', s3.code === 308 && s3.loc === '/contact', s3.code + ' ' + s3.loc);

  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, '../qa/p-contact'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });

  // ── structure, load health, screenshot (a) ──────────────────────────────────
  let p = await open(browser, BASE + '/contact');
  check('no console errors / failed requests / 4xx on load', p.bad.length === 0, p.bad.join(' | ') || 'clean');
  const s = await p.evaluate(() => {
    const q = x => document.querySelector(x), r = e => e ? e.getBoundingClientRect() : { height: 0, width: 0 };
    const h1 = document.querySelectorAll('h1');
    const hrefs = sel => [...document.querySelectorAll(sel)].map(a => a.getAttribute('href'));
    return {
      h1n: h1.length, h1t: h1[0] && h1[0].innerText.replace(/\s+/g, ' ').trim(), h1id: h1[0] && h1[0].id,
      h1gw: h1[0] && h1[0].dataset.gw, h1em: h1[0] && (h1[0].querySelector('em') || {}).textContent,
      h1font: h1[0] && getComputedStyle(h1[0]).fontFamily.split(',')[0],
      h1size: h1[0] && getComputedStyle(h1[0]).fontSize,
      h1caps: h1[0] && getComputedStyle(h1[0]).textTransform,
      h2n: document.querySelectorAll('h2').length,
      title: document.title, desc: (q('meta[name=description]') || {}).content,
      canon: (q('link[rel=canonical]') || {}).href, ogurl: (q('meta[property="og:url"]') || {}).content,
      navH: r(q('.nav__inner')).height, footH: r(q('.foot')).height, footN: document.querySelectorAll('footer').length,
      wm: !!q('.hh-wm--contact'), wmShown: r(q('.hh-wm--contact img')).width,
      eyebrow: q('.eyebrow .mono') && q('.eyebrow .mono').textContent.trim(),
      navContact: hrefs('.nav__side a, #drawer a, .mega__a').filter((h, i, a) => /contact/i.test(h)),
      contactLinks: [...document.querySelectorAll('.nav__side a, #drawer a, .mega__a')]
        .filter(a => /^contact/i.test(a.textContent.trim())).map(a => a.getAttribute('href')),
      selfAnchor: !![...document.querySelectorAll('.nav a, #drawer a')].find(a => a.getAttribute('href') === '#contact'),
      footLinks: hrefs('.foot a'),
      footL: Math.round(q('.foot__brand img').getBoundingClientRect().left), formL: Math.round(q('.eyebrow').getBoundingClientRect().left),
      loaderGone: !q('#hhload') || getComputedStyle(q('#hhload')).visibility === 'hidden',
      formSteps: document.querySelectorAll('.enq__screen').length,
      numbered: [...document.querySelectorAll('.contact .mono')].filter(e => /^\s*0?\d{1,2}\s*$/.test(e.textContent)).length,
      overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    };
  });
  check('exactly one <h1>', s.h1n === 1, s.h1n);
  check('h1 text is the contact heading, split-letter + <em>filming?</em> kept',
    /Have something\s+worth\s+filming\?/i.test(s.h1t) && s.h1gw === 'letters' && /filming\?/.test(s.h1em), s.h1t);
  check('h1 is styled as the h2 was (display font, uppercase, clamp size)', /Marcellus/i.test(s.h1font) && s.h1caps === 'uppercase', s.h1font + ' ' + s.h1caps + ' ' + s.h1size);
  check('no <h2> left in the heading slot (page has h1, then step headings only)', s.h2n === 0, 'h2 count ' + s.h2n);
  check('title / description set', s.title === 'Contact — Higher Heights Films' && /Morgan/.test(s.desc) && /within a day/.test(s.desc), s.title);
  check('canonical + og:url are the clean /contact URL', /\/contact$/.test(s.canon) && /\/contact$/.test(s.ogurl), s.canon + ' ' + s.ogurl);
  check('nav renders', s.navH > 30, s.navH + 'px');
  check('footer renders, exactly one', s.footH > 100 && s.footN === 1, s.footH + 'px x' + s.footN);
  check('watermark present and visible', s.wm && s.wmShown > 100, s.wmShown + 'px');
  check('eyebrow reads "Contact", no numbered labels', s.eyebrow === 'Contact' && s.numbered === 0, s.eyebrow + ' / numbered ' + s.numbered);
  check('nav Contact items (header, mega, drawer) all point at /contact, none a self-anchor',
    s.contactLinks.length === 3 && s.contactLinks.every(h => h === '/contact') && !s.selfAnchor, s.contactLinks.join(','));
  check('footer anchors resolve to real places (no bare #work etc.)',
    !s.footLinks.some(h => /^#(work|aerial|product|studio)$/.test(h)) && s.footLinks.includes('#enquiry'), s.footLinks.join(' '));
  check('desktop: footer content aligns with the page gutter', s.footL === s.formL, s.footL + ' vs ' + s.formL);
  check('loading screen dismissed', s.loaderGone);
  check('four form steps + done screen present', s.formSteps === 5, s.formSteps);
  check('no horizontal overflow at 1440', !s.overflowX);
  await settle(p);
  await p.screenshot({ path: path.join(OUT, 'contact-top-1440.png') });

  // ── the form ────────────────────────────────────────────────────────────────
  check('starts on step 0, BACK hidden', (await step(p)) === 0 && await p.$eval('#enqBack', e => e.hidden));
  await p.click('#enqNext'); await sleep(350);
  check('step 0 blocks Continue until a subject is chosen', (await step(p)) === 0);
  await pick(p, 'subject', 'An event'); await sleep(900);
  check('choosing a subject advances to step 1; rail marks 2 of 4', (await step(p)) === 1 && JSON.stringify(await railDone(p)) === '[true,true,false,false]');
  check('BACK is shown on step 1', !(await p.$eval('#enqBack', e => e.hidden)));
  await p.click('#enqNext'); await sleep(350);
  check('step 1 blocks Continue until timing is chosen', (await step(p)) === 1);
  await p.click('#enqBack'); await sleep(450);
  check('BACK returns to step 0 and keeps the answer', (await step(p)) === 0 && await p.$eval('input[value="An event"]', e => e.checked));
  await p.click('#enqNext'); await sleep(450);
  check('Continue on an answered step 0 goes forward', (await step(p)) === 1);
  await pick(p, 'timing', 'One to three months'); await sleep(900);
  check('choosing timing advances to step 2 (budget)', (await step(p)) === 2);

  // budget readout: "+" only at the maximum, at every step of the slider
  const lo = await p.$eval('.enq__range', r => ({ min: +r.min, max: +r.max, step: +r.step }));
  let plusOK = true, seen = [];
  for (let v = lo.min; v <= lo.max; v += lo.step) {
    await setRange(p, v); const m = await money(p);
    const want = '£' + v.toLocaleString('en-GB') + (v === lo.max ? '+' : '');
    if (m !== want) plusOK = false;
    if (m.includes('+') !== (v === lo.max)) plusOK = false;
    seen.push(m);
  }
  check('budget readout shows "+" only at max (' + lo.min + '..' + lo.max + ')', plusOK, seen[0] + ' ... ' + seen[seen.length - 2] + ' | ' + seen[seen.length - 1]);

  // drag the real slider to the maximum with the mouse
  await setRange(p, 10000);
  await p.evaluate(() => document.getElementById('enquiry').scrollIntoView({ block: 'center' }));
  await sleep(500);
  const box = await (await p.$('.enq__range')).boundingBox();
  await p.mouse.move(box.x + box.width * 0.2, box.y + box.height / 2);
  await p.mouse.down(); await p.mouse.move(box.x + box.width * 0.6, box.y + box.height / 2, { steps: 8 });
  await p.mouse.move(box.x + box.width + 40, box.y + box.height / 2, { steps: 8 }); await p.mouse.up();
  await sleep(500);
  const mx = await p.evaluate(() => ({
    money: document.getElementById('enqMoney').textContent, band: document.getElementById('enqBand').textContent,
    buys: [...document.querySelectorAll('#enqBuys li')].map(l => l.textContent) }));
  check('dragging to max reads £50,000+', mx.money === '£50,000+', mx.money);
  check('max band is "A season, or a series." with its three bullets',
    mx.band === 'A season, or a series.' && mx.buys.length === 3 &&
    mx.buys.join('|') === 'Several shoots across the year|A presenter-led episodic format|A library you keep drawing on', mx.band + ' / ' + mx.buys.length);
  await p.screenshot({ path: path.join(OUT, 'contact-form-budget-max-1440.png') });

  await p.click('#enqNext'); await sleep(450);
  check('Continue from budget goes to step 3 (reply); button reads "Send it"', (await step(p)) === 3 && /Send it/.test(await p.$eval('#enqNext', e => e.textContent)));
  await p.click('#enqNext'); await sleep(350);
  check('step 3 blocks Send until name, email and message are valid', (await step(p)) === 3);
  await p.type('input[name=name]', 'QA Tester');
  await p.type('input[name=email]', 'not-an-email');
  await p.type('textarea[name=message]', 'A short film about a launch.');
  await p.click('#enqNext'); await sleep(350);
  check('step 3 rejects an invalid email', (await step(p)) === 3);
  await p.$eval('input[name=email]', e => { e.value = ''; }); await p.type('input[name=email]', 'qa@example.com');

  // Never hit the real endpoint: answer it ourselves, and record what would be sent.
  let sent = null;
  await p.setRequestInterception(true);
  p.on('request', r => {
    if (r.url().endsWith('/api/enquiry')) {
      sent = { method: r.method(), accept: r.headers()['accept'], body: JSON.parse(r.postData() || '{}') };
      return r.respond({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
    }
    r.continue();
  });
  await p.click('#enqNext'); await sleep(900);
  check('submit POSTs /api/enquiry as JSON with the chosen answers',
    sent && sent.method === 'POST' && /json/.test(sent.accept) && sent.body.timing === 'One to three months' &&
    sent.body.services[0] === 'An event' && /£50,000\+/.test(sent.body.budget) && sent.body.email === 'qa@example.com', sent && JSON.stringify(sent.body).slice(0, 140));
  check('success shows the done screen (step 4): rail complete, BACK and Continue hidden',
    (await step(p)) === 4 && (await railDone(p)).every(Boolean) &&
    await p.$eval('#enqBack', e => e.offsetParent === null) && await p.$eval('.enq__nav', e => e.offsetParent === null));
  check('no console errors across the whole form run', p.bad.length === 0, p.bad.join(' | ') || 'clean');
  await p.close();

  // failure path: the server says no -> message shown, button usable again
  p = await open(browser, BASE + '/contact');
  await p.setRequestInterception(true);
  p.on('request', r => r.url().endsWith('/api/enquiry')
    ? r.respond({ status: 503, contentType: 'application/json', body: '{"ok":false,"error":"The form isn\'t connected yet."}' }) : r.continue());
  await pick(p, 'subject'); await sleep(900); await pick(p, 'timing'); await sleep(900);
  await p.click('#enqNext'); await sleep(400);
  await p.type('input[name=name]', 'QA'); await p.type('input[name=email]', 'qa@example.com'); await p.type('textarea[name=message]', 'Ten chars at least.');
  await p.click('#enqNext'); await sleep(700);
  const fe = await p.evaluate(() => ({ at: +document.querySelector('.enq__screen.is-on').dataset.step, err: document.getElementById('enqErr').textContent, dis: document.getElementById('enqNext').disabled }));
  check('server error: stays on step 3, shows the error, re-enables Send', fe.at === 3 && /isn't connected/.test(fe.err) && !fe.dis, fe.err);
  await p.close();

  // ── ?sent=1 landing (c) ─────────────────────────────────────────────────────
  p = await open(browser, BASE + '/contact?sent=1');
  const land = await p.evaluate(() => {
    const on = document.querySelector('.enq__screen.is-on');
    return { step: +on.dataset.step, anim: getComputedStyle(on).animationName, rail: [...document.querySelectorAll('.enq__rail i')].map(i => i.classList.contains('is-done')),
      back: document.getElementById('enqBack').hidden, nav: document.querySelector('.enq__nav').hidden, navShown: document.querySelector('.enq__nav').offsetParent !== null || document.getElementById('enqNext').offsetParent !== null,
      q: on.querySelector('.enq__q').textContent, sum: document.getElementById('enqSummary').hidden,
      onCount: document.querySelectorAll('.enq__screen.is-on').length };
  });
  check('?sent=1 lands on the thank-you straight away', land.step === 4 && land.q === 'Thank you.' && land.onCount === 1, land.q);
  check('?sent=1: rail complete, BACK + Continue hidden, step animation not replayed',
    land.rail.every(Boolean) && land.back && land.nav && land.navShown === false && land.anim === 'none', 'anim=' + land.anim);
  check('?sent=1: no empty summary paragraph left showing', land.sum);
  check('?sent=1: no console errors', p.bad.length === 0, p.bad.join(' | ') || 'clean');
  await settle(p);
  await p.screenshot({ path: path.join(OUT, 'contact-sent-1440.png') });
  await p.close();

  p = await open(browser, BASE + '/contact?error=1');
  const er = await p.evaluate(() => ({ step: +document.querySelector('.enq__screen.is-on').dataset.step, err: document.getElementById('enqErr').textContent }));
  check('?error shows the .enq__err message on the reply step', er.step === 3 && /email hello@higherheights\.uk/.test(er.err), er.err);
  await p.close();

  p = await open(browser, BASE + '/contact');
  check('plain /contact (no query) still starts on step 0', (await step(p)) === 0);
  await p.close();

  // ── mobile (d) ──────────────────────────────────────────────────────────────
  p = await open(browser, BASE + '/contact', { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const mob = await p.evaluate(() => ({ ox: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    burger: getComputedStyle(document.getElementById('burger')).display, h1: document.querySelectorAll('h1').length }));
  check('mobile 390: no horizontal overflow, one h1', !mob.ox && mob.h1 === 1, JSON.stringify(mob));
  const footL = await p.evaluate(() => Math.round(document.querySelector('.foot__brand img').getBoundingClientRect().left));
  check('mobile: footer has the same side padding as the form above it (not flush to the edge)', footL >= 16, footL + 'px');
  check('mobile: no console errors / failed requests', p.bad.length === 0, p.bad.join(' | ') || 'clean');
  await settle(p);
  await p.screenshot({ path: path.join(OUT, 'contact-mobile-390.png') });
  await setRange(p, 50000).catch(() => {});
  await p.evaluate(() => document.getElementById('enquiry').scrollIntoView({ block: 'start' }));
  await sleep(400);
  await p.screenshot({ path: path.join(OUT, 'contact-mobile-form-390.png') });
  await p.close();
  p = await open(browser, BASE + '/contact?sent=1', { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await sleep(600);
  await p.screenshot({ path: path.join(OUT, 'contact-mobile-sent-390.png') });
  const inView = await p.evaluate(() => { const r = document.getElementById('enquiry').getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; });
  check('mobile ?sent=1 scrolls the thank-you into view', inView);
  await p.close();

  await browser.close();
  const fails = results.filter(r => !r.ok);
  console.log('\n' + (results.length - fails.length) + '/' + results.length + ' passed' + (fails.length ? ' -- FAILED: ' + fails.map(f => f.name).join('; ') : ''));
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error('FATAL', e); process.exit(2); });

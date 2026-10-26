const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, 'qa/p-cta'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1500);

  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 450) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40));
    }
  });
  await sleep(1200);

  const r = await p.evaluate(() => {
    const q = s => document.querySelector(s);
    const cs = s => { const e = q(s); return e ? getComputedStyle(e) : null; };
    const main = cs('.cbtn--main'), letter = cs('.letter__a');
    const hidden = [...document.querySelectorAll('.contact .reveal')]
      .filter(e => getComputedStyle(e).opacity === '0').length;
    return {
      lede: !!q('.contact__lede'),
      ledeText: q('.contact__lede') ? q('.contact__lede').textContent.trim().slice(0, 46) + '…' : null,
      buttons: document.querySelectorAll('.contact__actions .cbtn').length,
      primaryBg: main && main.backgroundColor,
      primaryRadius: main && main.borderRadius,
      primaryFont: main && main.fontFamily.split(',')[0],
      letterPresent: !!q('.letter'),
      letterFont: letter && letter.fontFamily.split(',')[0],
      letterRadius: letter && letter.borderRadius,
      byline: q('.letter__by span') ? q('.letter__by span').textContent.trim() : null,
      detailsStillThere: document.querySelectorAll('.contact__side dl > div').length,
      revealsStuckHidden: hidden,
      // the ban list
      bans: {
        gradients: [...document.querySelectorAll('.contact *')]
          .filter(e => /gradient/.test(getComputedStyle(e).backgroundImage)).length,
        rounded: [...document.querySelectorAll('.contact *')]
          .filter(e => parseFloat(getComputedStyle(e).borderRadius) > 2).length,
        blur: [...document.querySelectorAll('.contact *')]
          .filter(e => getComputedStyle(e).backdropFilter !== 'none').length,
        poppins: [...document.querySelectorAll('.contact *')]
          .filter(e => /Poppins/i.test(getComputedStyle(e).fontFamily)).length,
      },
    };
  });
  console.log(JSON.stringify({ ...r, errs: [...new Set(errs)] }, null, 2));

  const el = await p.$('.contact');
  await el.scrollIntoView(); await sleep(700);
  await el.screenshot({ path: 'brand/cta.jpg', quality: 90, type: 'jpeg' });
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

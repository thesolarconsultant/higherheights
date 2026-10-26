const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', userDataDir: path.resolve(__dirname,'qa/p-rev'), args: ['--no-first-run','--hide-scrollbars'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1400, height: 900 });
  await p.goto('https://higher-heights.vercel.app/', { waitUntil: 'networkidle2' });
  await sleep(1500);
  const before = await p.evaluate(() => document.querySelectorAll('.reveal').length);
  // slow, realistic scroll
  await p.evaluate(async () => {
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += 300) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
  });
  await sleep(1500);
  const hidden = await p.evaluate(() => {
    const els = Array.from(document.querySelectorAll('.reveal'));
    return els.filter(e => parseFloat(getComputedStyle(e).opacity) < 0.5)
              .map(e => (e.className || '') + ' | ' + (e.textContent || '').trim().slice(0, 40));
  });
  // find tall empty blocks
  const empties = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('section, .band-cream, .studio, .product, .contact').forEach(s => {
      const r = s.getBoundingClientRect();
      const txt = (s.innerText || '').trim().length;
      if (r.height > 400 && txt < 40) out.push({ cls: s.className || s.tagName, h: Math.round(r.height), text: txt });
    });
    return out;
  });
  console.log(JSON.stringify({ revealCount: before, hiddenAfterScroll: hidden, tallEmptySections: empties }, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

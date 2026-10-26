const puppeteer = require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    userDataDir: path.resolve(__dirname, '../qa/p-car'),
    args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'],
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('JS ' + e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://127.0.0.1:8091/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(1800);

  const strip = await p.$('#strip');
  await strip.scrollIntoView();
  await sleep(900);

  const box = await strip.boundingBox();
  const cy = box.y + box.height / 2;
  const read = () => p.evaluate(() => {
    const t = document.querySelector('#strip');
    const bar = document.querySelector('.carousel__bar');
    return {
      left: Math.round(t.scrollLeft),
      max: Math.round(t.scrollWidth - t.clientWidth),
      dragging: document.querySelector('[data-carousel]').classList.contains('is-dragging'),
      bar: bar ? bar.style.transform : null,
      selected: String(window.getSelection()).length,
    };
  });

  console.log('start      ', JSON.stringify(await read()));

  // ── DRAG 1: a normal drag that ENDS INSIDE the strip ──
  await p.mouse.move(box.x + box.width - 120, cy);
  await p.mouse.down();
  for (let i = 1; i <= 12; i++) { await p.mouse.move(box.x + box.width - 120 - i * 28, cy); await sleep(16); }
  await p.mouse.up();
  await sleep(1100);
  const d1 = await read();
  console.log('after drag ', JSON.stringify(d1));

  // ── DRAG 2: the one that used to lock — release OUTSIDE the strip ──
  const before = (await read()).left;
  await p.mouse.move(box.x + box.width - 150, cy);
  await p.mouse.down();
  for (let i = 1; i <= 10; i++) { await p.mouse.move(box.x + box.width - 150 - i * 30, cy - i * 14); await sleep(16); }
  await p.mouse.move(box.x + 60, box.y - 160);   // leave the element entirely
  await p.mouse.up();                             // release off-target
  await sleep(1100);
  const d2 = await read();
  console.log('after exit ', JSON.stringify(d2));

  // ── can it still be dragged after that? (the lock test) ──
  await p.evaluate(() => { document.querySelector('#strip').scrollLeft = 0; });
  await sleep(500);
  const beforeRecover = (await read()).left;
  await p.mouse.move(box.x + box.width - 120, cy);
  await p.mouse.down();
  for (let i = 1; i <= 10; i++) { await p.mouse.move(box.x + box.width - 120 - i * 30, cy); await sleep(16); }
  await p.mouse.up();
  await sleep(1100);
  const d3 = await read();
  console.log('recovery   ', JSON.stringify(d3));

  // ── arrows ──
  await p.evaluate(() => { document.querySelector('#strip').scrollLeft = 0; });
  await sleep(600);
  const nextBtn = await p.$('.carousel__arrow[data-dir="1"]');
  const prevBtn = await p.$('.carousel__arrow[data-dir="-1"]');
  const beforeArrow = (await read()).left;
  await nextBtn.click(); await sleep(900);
  const afterNext = (await read()).left;
  await prevBtn.click(); await sleep(900);
  const afterPrev = (await read()).left;

  console.log('\n── RESULTS ──');
  console.log('drag moved the strip      :', d1.left !== 0);
  console.log('off-target release moved  :', d2.left !== before);
  console.log('dragging flag cleared     :', d2.dragging === false, '  <-- the lock');
  console.log('still draggable after     :', d3.left !== beforeRecover, '  <-- the lock');
  console.log('no text got selected      :', d1.selected === 0 && d2.selected === 0);
  console.log('next arrow moved          :', afterNext > beforeArrow);
  console.log('prev arrow moved back     :', afterPrev < afterNext);
  console.log('progress bar tracking     :', d3.bar);
  console.log('errs', [...new Set(errs)]);

  await strip.scrollIntoView(); await sleep(400);
  await p.screenshot({ path: 'brand/carousel.jpg', quality: 90, type: 'jpeg' });
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });

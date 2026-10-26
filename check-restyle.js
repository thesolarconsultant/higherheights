const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-rs'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();const errs=[];
  p.on('pageerror',e=>errs.push('JS '+e.message.slice(0,70)));
  p.on('requestfailed',r=>errs.push('REQ '+r.url().split('/').pop()));
  await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(3000);
  const f=await p.evaluate(()=>{
    const fam=new Set();
    document.querySelectorAll('*').forEach(e=>{
      if(e.children.length===0&&e.textContent.trim()){
        fam.add(getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g,''));}});
    return {families:[...fam], heroTop:!!document.querySelector('.hero__top'),
      heroFont:getComputedStyle(document.querySelector('.hero__title')).fontFamily.split(',')[0].replace(/["']/g,''),
      heroWeight:getComputedStyle(document.querySelector('.hero__title')).fontWeight,
      rows:document.querySelectorAll('.marquee__track').length,
      logos:document.querySelectorAll('.client').length,
      dirs:[...document.querySelectorAll('.marquee__track')].map(r=>r.dataset.dir)};
  });
  console.log('TYPE/HERO/MARQUEE', JSON.stringify(f,null,1));
  // marquee motion: sample, scroll, sample again
  const snap=()=>p.evaluate(()=>[...document.querySelectorAll('.marquee__track')]
    .map(r=>Math.round(new DOMMatrix(getComputedStyle(r).transform).m41)));
  const a=await snap(); await sleep(800); const c=await snap();
  await p.evaluate(()=>window.scrollBy(0,1400)); await sleep(500);
  const d=await snap(); await sleep(600); const e2=await snap();
  console.log('drift at rest :',a,'->',c,'  moving:',a[0]!==c[0]);
  console.log('after scroll  :',d,'->',e2);
  console.log('opposite dirs :', (c[0]-a[0])>0 !== (c[1]-a[1])>0 ? 'yes' : 'NO');
  console.log('errs',[...new Set(errs)]);
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

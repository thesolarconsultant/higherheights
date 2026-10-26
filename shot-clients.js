const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-cl'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();const errs=[];
  p.on('pageerror',e=>errs.push('JS '+e.message));
  p.on('requestfailed',r=>errs.push('REQ '+r.url().split('/').pop()));
  await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2000);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,30));}});
  await sleep(1000);
  const cl=await p.$('.clients'); await cl.scrollIntoView(); await sleep(900);
  const d=await p.evaluate(()=>{
    const marks=[...document.querySelectorAll('.client__mark')];
    const loaded=marks.filter(m=>{const u=getComputedStyle(m).maskImage||getComputedStyle(m).webkitMaskImage;return u&&u!=='none';});
    return {total:marks.length, masked:loaded.length,
      rows:document.querySelectorAll('#marqueeTrack').length,
      kidsPerRow:[...document.querySelectorAll('#marqueeTrack')].map(r=>r.children.length),
      labels:marks.slice(0,6).map(m=>m.getAttribute('aria-label')),
      paused:getComputedStyle(document.querySelector('#marqueeTrack')).animationPlayState};
  });
  console.log(JSON.stringify(d,null,1));
  // pause the marquee so the shot is sharp
  await p.evaluate(()=>document.querySelectorAll('#marqueeTrack').forEach(r=>r.style.animationPlayState='paused'));
  await sleep(300);
  await cl.screenshot({path:'brand/clients-now.jpg',quality:92,type:'jpeg'});
  // and a hover shot
  await p.hover('.marquee__track .client:nth-child(5) .client__mark').catch(()=>{});
  await sleep(700);
  await cl.screenshot({path:'brand/clients-hover.jpg',quality:92,type:'jpeg'});
  console.log('errs',[...new Set(errs)]);
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-sc'),args:['--no-first-run','--hide-scrollbars']});
 for(const d of [{n:'iPhone 14',w:390,h:844},{n:'iPad portrait',w:768,h:1024}]){
  const p=await b.newPage();await p.setCacheEnabled(false);
  await p.setViewport({width:d.w,height:d.h,hasTouch:true,isMobile:true,deviceScaleFactor:2});
  await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2000);
  await p.evaluate(()=>document.querySelector('.strip').scrollIntoView({block:'center'}));await sleep(600);
  const r=await p.evaluate(()=>{const s=document.querySelector('.strip');const cs=getComputedStyle(s);
   const max=s.scrollWidth-s.clientWidth;
   s.scrollLeft=200; const moved=Math.round(s.scrollLeft); s.scrollLeft=0;
   return{touchAction:cs.touchAction,overflowX:cs.overflowX,
     scrollWidth:s.scrollWidth,clientWidth:s.clientWidth,maxScroll:max,
     programmatic:moved, canScroll:max>10&&moved>10,
     snap:cs.scrollSnapType, webkitMomentum:cs.webkitOverflowScrolling||'n/a'};});
  console.log(`${d.n.padEnd(14)} ${JSON.stringify(r)}`);
  await p.close();}
 await b.close();})().catch(e=>console.error('FATAL',e.message));

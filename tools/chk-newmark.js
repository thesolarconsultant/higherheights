const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-nm'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900,deviceScaleFactor:2});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(2000);
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}});
 await sleep(800);
 const info=await p.evaluate(()=>[...document.querySelectorAll('.hh-wm')].map(w=>{
  const img=w.querySelector('img');const r=w.getBoundingClientRect();
  return{cls:w.className.split(' ')[1],src:(img.currentSrc||img.src).split('/').pop(),
   loaded:img.naturalWidth>0, natural:img.naturalWidth+'x'+img.naturalHeight,
   w:Math.round(r.width),opacity:getComputedStyle(w).opacity};}));
 console.log(JSON.stringify(info,null,1));
 // boost opacity and shoot one so it is actually visible
 await p.evaluate(()=>{document.querySelectorAll('.hh-wm').forEach(w=>w.style.opacity='1');});
 const el=await p.$('.hh-wm--studio');
 if(el) await el.screenshot({path:path.resolve(__dirname,'../brand/wm-proof.png')});
 console.log('shot');await b.close();})().catch(e=>console.error('FATAL',e.message));

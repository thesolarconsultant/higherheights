const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-fit'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(1800);
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}});
 await sleep(700);
 const r=await p.evaluate(()=>[...document.querySelectorAll('.hh-wm')].map(w=>{
  const img=w.querySelector('img');
  const wr=w.getBoundingClientRect(), ir=img.getBoundingClientRect();
  const cs=getComputedStyle(w), is=getComputedStyle(img);
  return{cls:w.className.split(' ')[1],
   box:`${Math.round(wr.width)}x${Math.round(wr.height)}`,
   img:`${Math.round(ir.width)}x${Math.round(ir.height)}`,
   imgOverflowsY: Math.round(ir.height - wr.height),
   imgOverflowsX: Math.round(ir.width - wr.width),
   wrapOverflow: cs.overflow, maxH:cs.maxHeight, imgMaxH:is.maxHeight, fit:is.objectFit};}));
 console.log(JSON.stringify(r,null,1));await b.close();})().catch(e=>console.error('FATAL',e.message));

const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-w2'),args:['--no-first-run','--hide-scrollbars']});
 for(const pg of ['corporate-video-production.html','aerial-drone-filming.html']){
  const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
  await p.goto(`http://127.0.0.1:8092/${pg}`,{waitUntil:'networkidle2',timeout:60000});await sleep(1500);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}});
  await sleep(700);
  const r=await p.evaluate(()=>[...document.querySelectorAll('.hh-wm--pg')].map(w=>{
   const sec=w.closest('section'),wr=w.getBoundingClientRect(),sr=sec.getBoundingClientRect();
   const ix=Math.max(0,Math.min(wr.right,sr.right)-Math.max(wr.left,sr.left));
   const iy=Math.max(0,Math.min(wr.bottom,sr.bottom)-Math.max(wr.top,sr.top));
   const img=w.querySelector('img');
   return{src:(img.currentSrc||img.src).split('/').pop(),w:Math.round(wr.width),
    vis:Math.round(ix*iy/(wr.width*wr.height)*100)+'%',
    sec:(sec.className||'').toString().slice(0,18),loaded:img.naturalWidth>0};}));
  console.log(pg,JSON.stringify(r));await p.close();}
 await b.close();})().catch(e=>console.error('FATAL',e.message));

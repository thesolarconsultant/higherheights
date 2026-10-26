const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-mk'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/corporate-video-production.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(1500);
 const r=await p.evaluate(()=>{
  const out=[];
  document.querySelectorAll('img,svg,[class*=wm],[class*=mark],[class*=brand]').forEach(e=>{
   const cs=getComputedStyle(e),rc=e.getBoundingClientRect();
   if(rc.width<4) return;
   out.push({tag:e.tagName,cls:(e.className||'').toString().slice(0,26),
     src:(e.getAttribute&&e.getAttribute('src')||'').split('/').pop(),
     w:Math.round(rc.width),h:Math.round(rc.height),op:cs.opacity,
     top:Math.round(rc.top+scrollY)});});
  // also background-images
  document.querySelectorAll('*').forEach(e=>{const bg=getComputedStyle(e).backgroundImage;
   if(bg&&bg!=='none'&&!bg.startsWith('linear')&&!bg.startsWith('radial'))
     out.push({tag:'BG:'+e.tagName,cls:(e.className||'').toString().slice(0,26),src:bg.slice(0,60)});});
  return out;});
 r.forEach(x=>console.log(JSON.stringify(x)));
 await b.close();})().catch(e=>console.error('FATAL',e.message));

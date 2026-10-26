const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-ld'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 for(const pg of ['index.html','corporate-video-production.html']){
  const p=await p0(b);await p.setViewport({width:1440,height:900});
  await p.goto(`http://127.0.0.1:8092/${pg}`,{waitUntil:'domcontentloaded',timeout:60000});
  // early: should be visible and big
  await sleep(260);
  const early=await p.evaluate(()=>{const e=document.getElementById('hhload');
   if(!e)return{err:'missing'};const m=e.querySelector('.hhload__mark');
   const r=m?m.getBoundingClientRect():{width:0,height:0};const cs=getComputedStyle(e);
   return{visible:cs.opacity!=='0'&&cs.visibility!=='hidden',markW:Math.round(r.width),
     markH:Math.round(r.height),bg:cs.backgroundColor,z:cs.zIndex};});
  await sleep(4200);
  const late=await p.evaluate(()=>{const e=document.getElementById('hhload');
   return{removed:!e, blocking:e?getComputedStyle(e).pointerEvents!=='none':false};});
  const clickable=await p.evaluate(()=>{const a=document.querySelector('a[href]');
   if(!a)return'no link';const r=a.getBoundingClientRect();
   const top=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
   return top? (top.closest('#hhload')?'BLOCKED':'reachable'):'offscreen';});
  console.log(`${pg.padEnd(32)} early:${JSON.stringify(early)}`);
  console.log(`${''.padEnd(32)} after4s:${JSON.stringify(late)} links:${clickable}`);
  await p.close();}
 await b.close();})().catch(e=>console.error('FATAL',e.message));
async function p0(b){const p=await b.newPage();await p.setCacheEnabled(false);return p;}

const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-tl'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 for(const pg of ['index.html','corporate-video-production.html']){
  const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
  const t0=Date.now();
  await p.goto(`http://127.0.0.1:8092/${pg}`,{waitUntil:'domcontentloaded',timeout:60000}); let gone=null;
  for(let i=0;i<90;i++){
   const state=await p.evaluate(()=>{const e=document.getElementById('hhload');
    if(!e) return 'removed';
    return e.classList.contains('is-done')?'dismissing':'visible';});
   if(state!=='visible'){gone=Date.now()-t0;break;}
   await sleep(25);
  }
  console.log(`${pg.padEnd(32)} starts dismissing at ${gone}ms from navigation  ${(gone>=1600&&gone<=2300)?'✓ ~1.7s beat':'✗ off target'}`);
  await p.close();}
 await b.close();})().catch(e=>console.error('FATAL',e.message));

const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-live'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 for(const url of ['https://higherheights.uk/','https://higherheights.uk/corporate-video-production']){
  const dcl=[],gone=[];
  for(let i=0;i<3;i++){
   const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
   await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
   const t=await p.evaluate(()=>performance.timing.domContentLoadedEventEnd-performance.timing.navigationStart);
   dcl.push(t);
   // wait for the loader to actually go
   const t0=Date.now();
   try{ await p.waitForFunction(()=>{const e=document.getElementById('hhload');
     return !e||e.classList.contains('is-done');},{timeout:8000,polling:40}); }catch(e){}
   gone.push(t+(Date.now()-t0));
   await p.close();
  }
  console.log(`${url}`);
  console.log(`   DCL             : ${dcl.join(', ')} ms`);
  console.log(`   loader gone at  : ${gone.map(Math.round).join(', ')} ms`);
 }
 await b.close();})().catch(e=>console.error('FATAL',e.message));

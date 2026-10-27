const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-tp'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 for(const pg of ['index.html','corporate-video-production.html']){
  const runs=[];
  for(let i=0;i<3;i++){
   const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
   // record the dismissal time inside the page, no polling overhead
   await p.evaluateOnNewDocument(()=>{window.__t=[];
     new MutationObserver(ms=>{for(const m of ms){
       if(m.target.id==='hhload'&&m.target.classList.contains('is-done'))
         window.__t.push(performance.now());}})
       .observe(document.documentElement,{attributes:true,subtree:true,attributeFilter:['class']});});
   await p.goto(`http://127.0.0.1:8092/${pg}`,{waitUntil:'load',timeout:60000});
   await sleep(5200);
   const r=await p.evaluate(()=>({dismiss:window.__t[0]||null,
     dcl:performance.timing.domContentLoadedEventEnd-performance.timing.navigationStart,
     load:performance.timing.loadEventEnd-performance.timing.navigationStart}));
   runs.push(r); await p.close();
  }
  const ds=runs.map(r=>r.dismiss).filter(Boolean);
  console.log(`${pg}`);
  console.log(`   DOMContentLoaded : ${runs.map(r=>r.dcl).join(', ')} ms`);
  console.log(`   loader dismissed : ${ds.map(d=>Math.round(d)).join(', ')} ms  (avg ${Math.round(ds.reduce((a,c)=>a+c,0)/ds.length)})`);
 }
 await b.close();})().catch(e=>console.error('FATAL',e.message));

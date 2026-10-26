const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-hl'),
  args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();const errs=[];
 p.on('pageerror',e=>errs.push('JS '+e.message.slice(0,60)));
 p.on('requestfailed',r=>errs.push('REQ '+r.url().split('/').pop()));
 await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(4000);
 const r=await p.evaluate(()=>{const v=document.getElementById('heroVideo');
   return {src:(v.currentSrc||'').split('/').pop(), poster:(v.poster||'').split('/').pop(),
     playing:!v.paused&&v.readyState>2, w:v.videoWidth, h:v.videoHeight,
     dur:Math.round(v.duration*10)/10, t:Math.round(v.currentTime*10)/10};});
 console.log('DESKTOP',JSON.stringify(r));
 await p.setViewport({width:414,height:860,isMobile:true});
 await p.reload({waitUntil:'networkidle2'}); await sleep(3500);
 const m=await p.evaluate(()=>{const v=document.getElementById('heroVideo');
   return {src:(v.currentSrc||'').split('/').pop(), w:v.videoWidth};});
 console.log('MOBILE ',JSON.stringify(m));
 console.log('errs',[...new Set(errs)]);
 await p.setViewport({width:1440,height:900}); await p.reload({waitUntil:'networkidle2'}); await sleep(3500);
 await p.screenshot({path:'brand/hero-loop.jpg',quality:90,type:'jpeg'});
 await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

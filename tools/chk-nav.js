const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-nv'),
  args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,60)));
 await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});await sleep(2500);
 for(const y of [0,1500,5200,6400,8200,10500]){
   await p.evaluate(v=>window.scrollTo(0,v),y); await sleep(600);
   const r=await p.evaluate(()=>{const n=document.querySelector('.nav');const i=document.querySelector('.nav__inner');
     const under=document.elementsFromPoint(innerWidth/2,n.getBoundingClientRect().bottom-6)
       .filter(e=>!e.closest('.nav'))[0];
     return {light:n.classList.contains('nav--light'),
       bg:getComputedStyle(i).backgroundColor,
       under:under?(under.tagName+'.'+(under.className||'').toString().split(' ')[0]).slice(0,24):'-'};});
   console.log(String(y).padStart(6),JSON.stringify(r));
 }
 console.log('errs',[...new Set(errs)]);await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

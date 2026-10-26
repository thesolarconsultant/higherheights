const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve('C:/Users/Jordan/Projects/higher-heights/qa/p-cb'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});await sleep(1500);
 const r=await p.evaluate(()=>[...document.querySelectorAll('.hh-wm')].map(w=>{
   let a=w.parentElement,cb=null;
   while(a){const s=getComputedStyle(a);
     if(s.position!=='static'||s.transform!=='none'||s.filter!=='none'){cb=a;break;}
     a=a.parentElement;}
   const sec=w.closest('section');
   return {mark:w.className.replace('hh-wm ',''),
     containingBlock:cb?(cb.tagName+'.'+(cb.className||'').toString().split(' ')[0]):'VIEWPORT',
     cbH:cb?Math.round(cb.getBoundingClientRect().height):'-',
     section:sec?(sec.tagName+'.'+(sec.className||'').toString().split(' ')[0]):'-',
     secPos:sec?getComputedStyle(sec).position:'-',
     secH:sec?Math.round(sec.getBoundingClientRect().height):'-'};}));
 console.log(JSON.stringify(r,null,1));await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-wp'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/corporate-video-production.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(1200);
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}window.scrollTo(0,0);});
 await sleep(900);
 await sleep(700);
 const r=await p.evaluate(()=>{const H=document.body.scrollHeight;
  return{docH:H,marks:[...document.querySelectorAll('.hh-wm--pg')].map(w=>{
   const rc=w.getBoundingClientRect();const top=Math.round(rc.top+scrollY);
   return{cls:w.className.split(' ').pop(),top,pctDown:Math.round(top/H*100)+'%',
     w:Math.round(rc.width),sec:(w.closest('section').className||'').slice(0,16)};})};});
 console.log(JSON.stringify(r,null,1));await b.close();})().catch(e=>console.error('FATAL',e.message));

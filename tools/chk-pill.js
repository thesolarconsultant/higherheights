const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-pill'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(1800);
 await p.evaluate(()=>window.scrollTo(0,1500));await sleep(900);
 const r=await p.evaluate(()=>{const inner=document.querySelector('.nav__inner');
  const kids=[...inner.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>3&&r.height>3;});
  return{light:document.querySelector('.nav').classList.contains('nav--light'),
   items:kids.map(e=>{const cs=getComputedStyle(e);const r=e.getBoundingClientRect();
    return{tag:e.tagName,cls:(e.className||'').toString().slice(0,22),
     src:(e.getAttribute&&e.getAttribute('src')||'').split('/').pop(),
     w:Math.round(r.width),h:Math.round(r.height),
     filter:cs.filter,bg:cs.backgroundColor,color:cs.color};}).slice(0,10)};});
 console.log(JSON.stringify(r,null,1));await b.close();})().catch(e=>console.error('FATAL',e.message));

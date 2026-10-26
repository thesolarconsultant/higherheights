const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-dg'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/corporate-video-production.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(1200);
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}});
 await sleep(900);
 const rv=await p.evaluate(()=>({revealTotal:document.querySelectorAll('.reveal').length,revealOn:document.querySelectorAll('.reveal.is-in,.reveal.in,.reveal.is-visible').length,gwTotal:document.querySelectorAll('[data-gw]').length,gwSpans:document.querySelectorAll('[data-gw] span').length,gwLit:[...document.querySelectorAll('[data-gw] span')].filter(s=>+getComputedStyle(s).opacity>0.5).length}));console.log('REVEAL',JSON.stringify(rv));
 const r=await p.evaluate(()=>{
  const out=[];
  document.querySelectorAll('section').forEach(s=>{
    const cs=getComputedStyle(s), r=s.getBoundingClientRect();
    const txt=[...s.querySelectorAll('p,h1,h2,li,span')].filter(e=>e.textContent.trim());
    const sample=txt.slice(0,3).map(e=>{const c=getComputedStyle(e);
      return {tag:e.tagName,col:c.color,op:c.opacity,
        vis:parseFloat(c.opacity)>0.1, txt:e.textContent.trim().slice(0,22)};});
    out.push({cls:(s.className||'').toString().slice(0,22),
      h:Math.round(r.height), bg:cs.backgroundColor, col:cs.color,
      texts:txt.length, sample});
  });
  return out;});
 r.forEach(s=>{console.log(`\n${s.cls||'(none)'}  h=${s.h}  bg=${s.bg}  col=${s.col}  texts=${s.texts}`);
   s.sample.forEach(x=>console.log(`    ${x.tag} op=${x.op} ${x.col}  "${x.txt}"`));});
 await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

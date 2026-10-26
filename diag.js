const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-diag'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();
  await p.setViewport({width:390,height:844,isMobile:true});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2200);
  const d=await p.evaluate(()=>{
    const tiny=[...document.querySelectorAll('*')].filter(e=>{
      const t=e.children.length===0&&e.textContent.trim();
      return t&&parseFloat(getComputedStyle(e).fontSize)<11;
    }).map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,34),
      px:+getComputedStyle(e).fontSize.replace('px',''),txt:e.textContent.trim().slice(0,22)}));
    const serif=[...document.querySelectorAll('*')].filter(e=>{
      const f=getComputedStyle(e).fontFamily;
      return /Times|Arial/i.test(f)&&e.children.length===0;
    }).map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,30),
      font:getComputedStyle(e).fontFamily.slice(0,40)}));
    const small=[...document.querySelectorAll('a,button')].filter(e=>{
      const r=e.getBoundingClientRect();return r.width>0&&(r.width<40||r.height<36);
    }).map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,30),
      w:Math.round(e.getBoundingClientRect().width),h:Math.round(e.getBoundingClientRect().height),
      txt:(e.innerText||e.getAttribute('aria-label')||'').slice(0,18)}));
    return {tiny,serif:serif.slice(0,6),serifCount:serif.length,small};
  });
  console.log(JSON.stringify(d,null,1));
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

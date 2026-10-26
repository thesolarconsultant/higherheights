const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-ft'),args:['--no-first-run','--hide-scrollbars']});
  const p=await b.newPage();await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2500);
  const r=await p.evaluate(()=>[...document.querySelectorAll('*')]
    .filter(e=>e.children.length===0&&e.textContent.trim()&&/Times|Georgia|serif$/i.test(getComputedStyle(e).fontFamily))
    .map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,40),
      font:getComputedStyle(e).fontFamily.slice(0,52),txt:e.textContent.trim().slice(0,30),
      parent:e.parentElement?e.parentElement.tagName+'.'+(e.parentElement.className||'').toString().slice(0,26):null})));
  console.log(JSON.stringify(r,null,1));
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

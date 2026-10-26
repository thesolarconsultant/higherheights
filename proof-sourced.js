const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const DIR=path.resolve(__dirname,'brand/sourced');
const files=fs.readdirSync(DIR).filter(f=>/\.(svg|png)$/i.test(f));
const cells=files.map(f=>{
  const u='file:///'+path.join(DIR,f).split(path.sep).join('/');
  return `<figure><div class="box"><img src="${u}"></div><figcaption>${f}</figcaption></figure>`;
}).join('');
const html=`<!DOCTYPE html><meta charset="utf-8"><style>
 body{background:#0B1A26;color:#F4EFE6;font:13px/1.5 system-ui;margin:0;padding:26px;
      display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
 figure{margin:0}
 .box{height:120px;display:flex;align-items:center;justify-content:center;
      border:1px solid rgba(201,174,124,.3);background:#0E2130;padding:14px}
 .box img{max-width:100%;max-height:92px;object-fit:contain}
 figcaption{margin-top:9px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#C9AE7C}
 h1{grid-column:1/-1;margin:0 0 6px;font:400 19px/1 Georgia,serif;letter-spacing:.02em}
 p.n{grid-column:1/-1;margin:0 0 10px;color:rgba(244,239,230,.6);font-size:12px}
</style><h1>Sourced client logos</h1>
<p class="n">As downloaded, on the site's navy. Not yet knocked out or balanced.</p>${cells}`;
const out=path.join(DIR,'_proof.html');fs.writeFileSync(out,html);
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-proof'),args:['--no-first-run','--hide-scrollbars','--allow-file-access-from-files']});
  const p=await b.newPage();await p.setViewport({width:900,height:700});
  await p.goto('file:///'+out.split(path.sep).join('/'),{waitUntil:'networkidle0'});
  await sleep(1200);
  const broken=await p.evaluate(()=>[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src.split('/').pop()));
  await p.screenshot({path:'brand/sourced-proof.jpg',quality:92,type:'jpeg',fullPage:true});
  console.log('files:',JSON.stringify(require('fs').readdirSync(DIR).filter(f=>/\.(svg|png)$/i.test(f))));
  console.log('broken:',JSON.stringify(broken));
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

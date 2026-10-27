const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const live=fs.readFileSync(path.resolve(__dirname,'../brand/live-wm.svg'),'utf8');
 const word=fs.readFileSync(path.resolve(__dirname,'../site-brand/assets/img/wordmark-cream.svg'),'utf8');
 const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-pl'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setViewport({width:1000,height:420,deviceScaleFactor:2});
 await p.setContent(`<html><body style="margin:0;display:grid;grid-template-columns:1fr 1fr;background:#070D0B;font:11px ui-monospace;color:#7b8794">
  <div style="display:grid;place-items:center;gap:14px;padding:30px 0">
    <div style="width:230px">${live.replace('<svg','<svg style="width:100%;height:auto"')}</div>
    <div>WATERMARK — live on site</div></div>
  <div style="display:grid;place-items:center;gap:14px;padding:30px 0">
    <div style="width:300px">${word.replace('<svg','<svg style="width:100%;height:auto"')}</div>
    <div>NAV / FOOTER WORDMARK — never updated</div></div>
  </body></html>`,{waitUntil:'load'});
 await sleep(500);
 await p.screenshot({path:path.resolve(__dirname,'../brand/live-compare.jpg'),quality:92,type:'jpeg'});
 console.log('ok');await b.close();})().catch(e=>console.error('FATAL',e.message));

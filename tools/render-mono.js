const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const svg=fs.readFileSync(path.resolve(__dirname,'../brand/hh-mono.svg'),'utf8');
 const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-mono'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setViewport({width:1200,height:640,deviceScaleFactor:2});
 const html=`<html><body style="margin:0;display:grid;grid-template-columns:repeat(4,1fr);font:11px ui-monospace">
 <div style="background:#0B1A26;color:#F4EFE6;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:170px;height:170px"')}</div>
 <div style="background:#F4EFE6;color:#0B1A26;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:170px;height:170px"')}</div>
 <div style="background:#0B1A26;color:#C9AE7C;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:170px;height:170px"')}</div>
 <div style="background:#051C16;color:#E9E5DB;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:170px;height:170px"')}</div>
 <div style="background:#0B1A26;color:#F4EFE6;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:64px;height:64px"')}</div>
 <div style="background:#0B1A26;color:#F4EFE6;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:32px;height:32px"')}</div>
 <div style="background:#0B1A26;color:#F4EFE6;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:16px;height:16px"')}</div>
 <div style="background:#F4EFE6;color:#0B1A26;display:grid;place-items:center;height:320px">${svg.replace('<svg','<svg style="width:16px;height:16px"')}</div>
 </body></html>`;
 await p.setContent(html,{waitUntil:'load'});await sleep(600);
 await p.screenshot({path:path.resolve(__dirname,'../brand/mono-proof.png')});
 console.log('rendered');await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

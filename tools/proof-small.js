const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const rd=f=>fs.readFileSync(path.resolve(__dirname,'../brand/'+f),'utf8');
(async()=>{
 const v={plain:rd('hh-mono.svg'),s32:rd('hh-mono-32.svg'),s24:rd('hh-mono-24.svg'),s16:rd('hh-mono-16.svg')};
 const cell=(svg,px)=>`<div style="background:#0B1A26;color:#F4EFE6;display:grid;place-items:center;height:110px">
   ${svg.replace('<svg',`<svg style="width:${px}px;height:${px}px"`)}</div>`;
 const row=(name,svg)=>`<div style="background:#0B1A26;color:#7b8794;display:grid;place-items:center;height:110px;font:10px ui-monospace">${name}</div>`
   +cell(svg,48)+cell(svg,32)+cell(svg,24)+cell(svg,16);
 const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-sm'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setViewport({width:620,height:560,deviceScaleFactor:3});
 await p.setContent(`<html><body style="margin:0;display:grid;grid-template-columns:90px repeat(4,1fr);font:10px ui-monospace">
   <div style="background:#0B1A26;height:110px"></div>
   ${['48px','32px','24px','16px'].map(l=>`<div style="background:#0B1A26;color:#7b8794;display:grid;place-items:center;height:110px">${l}</div>`).join('')}
   ${row('no stroke',v.plain)}${row('stroke 10',v.s32)}${row('stroke 16',v.s24)}${row('stroke 26',v.s16)}
   </body></html>`,{waitUntil:'load'});
 await sleep(500);
 await p.screenshot({path:path.resolve(__dirname,'../brand/small-proof.png')});
 console.log('ok');await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

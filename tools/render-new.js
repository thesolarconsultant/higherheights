const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const rd=f=>fs.readFileSync(path.resolve(__dirname,'../brand/'+f),'utf8');
(async()=>{
 const hh=rd('clean-hh-white.svg'), ci=rd('clean-circle-white.svg');
 const hhb=rd('clean-hh-black.svg'), cib=rd('clean-circle-black.svg');
 const cell=(svg,bg,px)=>`<div style="background:${bg};display:grid;place-items:center;height:300px">
   ${svg.replace('<svg',`<svg style="width:${px}px;height:${px}px"`)}</div>`;
 const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-new'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setViewport({width:1040,height:620,deviceScaleFactor:2});
 await p.setContent(`<html><body style="margin:0;display:grid;grid-template-columns:repeat(4,1fr);font:10px ui-monospace;color:#888">
  ${cell(hh,'#070D0B',200)}${cell(hhb,'#E9E5DB',200)}${cell(ci,'#070D0B',200)}${cell(cib,'#E9E5DB',200)}
  ${cell(hh,'#070D0B',96)}${cell(hh,'#070D0B',48)}${cell(ci,'#070D0B',96)}${cell(ci,'#070D0B',48)}
  </body></html>`,{waitUntil:'load'});
 await sleep(600);
 await p.screenshot({path:path.resolve(__dirname,'../brand/new-logos.jpg'),quality:92,type:'jpeg'});
 console.log('ok');await b.close();})().catch(e=>console.error('FATAL',e.message));

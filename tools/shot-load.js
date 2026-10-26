const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-sl'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setCacheEnabled(false);
 const c=await p.target().createCDPSession();await c.send('Network.enable');
 await c.send('Network.emulateNetworkConditions',{offline:false,latency:300,downloadThroughput:120*1024,uploadThroughput:60*1024});await p.setViewport({width:1200,height:760,deviceScaleFactor:2});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'domcontentloaded',timeout:60000});
 await sleep(500);
 await p.evaluate(()=>{const e=document.getElementById('hhload');if(e){e.style.animation='none';e.style.opacity='1';e.style.visibility='visible';}});
 await sleep(120);
 await p.screenshot({path:path.resolve(__dirname,'../brand/loader.jpg'),quality:92,type:'jpeg'});
 console.log('ok');await b.close();})().catch(e=>console.error('FATAL',e.message));

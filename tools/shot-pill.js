const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-sp2'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900,deviceScaleFactor:1});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(3000);
 await p.evaluate(()=>window.scrollTo(0,1500));await sleep(1000);
 await p.screenshot({path:path.resolve(__dirname,'../brand/pill-light.jpg'),quality:94,type:'jpeg'});
 await p.evaluate(()=>window.scrollTo(0,5200));await sleep(1000);
 await p.screenshot({path:path.resolve(__dirname,'../brand/pill-dark.jpg'),quality:94,type:'jpeg'});
 console.log('ok');await b.close();})().catch(e=>console.error('FATAL',e.message));

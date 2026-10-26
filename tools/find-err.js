const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-err'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setCacheEnabled(false);
 p.on('pageerror',e=>{console.log('ERROR:',e.message);console.log('STACK:',(e.stack||'').split('\n').slice(0,4).join('\n'));});
 await p.goto('http://127.0.0.1:8092/corporate-video-production.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(2000);await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

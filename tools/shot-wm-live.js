const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-wmv'),
  args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});await sleep(2000);
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}});
 await sleep(800);
 for(const [sel,n] of [['.hh-wm--studio','wm-studio'],['.hh-wm--contact','wm-contact']]){
  const el=await p.$(sel.replace('.hh-wm--','.hh-wm.hh-wm--'));
  const sec=await p.evaluateHandle(s=>document.querySelector(s).closest('section'),sel);
  try{ await sec.asElement().screenshot({path:path.resolve(__dirname,`../brand/${n}.jpg`),quality:80,type:'jpeg'});
       console.log('shot',n);}catch(e){console.log(n,'skip',e.message.slice(0,40));}
 }
 await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

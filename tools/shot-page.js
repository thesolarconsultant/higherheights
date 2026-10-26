const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-sp'),
  args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 const pg=process.argv[2];
 await p.goto(`http://127.0.0.1:8092/${pg}`,{waitUntil:'networkidle2',timeout:60000});
 await sleep(1500);
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,25));}window.scrollTo(0,0);});
 await sleep(700);
 await p.evaluate(()=>{document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in','in','is-visible'));document.querySelectorAll('[data-gw] span').forEach(s=>{s.style.opacity='1';s.style.transform='none';});});
 await sleep(1000);
 await p.screenshot({path:path.resolve(__dirname,`../brand/${process.argv[3]}.jpg`),quality:82,type:'jpeg',fullPage:true});
 console.log('ok');await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

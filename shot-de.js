const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-shotde'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();
  await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2000);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,30));}});
  await sleep(1200);
  // pin mid-travel
  await p.evaluate(()=>{const pin=document.querySelector('[data-pin]');
    const abs=pin.getBoundingClientRect().top+window.scrollY;
    window.scrollTo(0, abs+(pin.offsetHeight-innerHeight)*0.55);});
  await sleep(900);
  await p.screenshot({path:'brand/y-pin.jpg',quality:90,type:'jpeg'});
  // clients marquee
  const cl=await p.$('.clients'); await cl.scrollIntoView(); await sleep(800);
  await cl.screenshot({path:'brand/y-marq.jpg',quality:90,type:'jpeg'});
  // contact band + footer
  const ct=await p.$('.contact'); await ct.scrollIntoView(); await sleep(900);
  await ct.screenshot({path:'brand/y-band.jpg',quality:88,type:'jpeg'});
  console.log('shot 3');
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

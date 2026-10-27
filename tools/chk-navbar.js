const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-nb'),args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 for(const d of [{n:'iPhone',w:390,h:844},{n:'desktop',w:1440,h:900}]){
  const p=await b.newPage();await p.setCacheEnabled(false);
  const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,46)));
  await p.setViewport({width:d.w,height:d.h,hasTouch:d.w<800,isMobile:d.w<800,deviceScaleFactor:2});
  await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2000);
  const top=await p.evaluate(()=>{const n=document.querySelector('.nav');const cs=getComputedStyle(n);
   const bef=getComputedStyle(n,'::before');
   return{pt:cs.paddingTop,beforeBg:bef.backgroundColor,beforeContent:bef.content,
     innerBg:getComputedStyle(document.querySelector('.nav__inner')).backgroundColor};});
  await p.evaluate(()=>window.scrollTo(0,1400));await sleep(800);
  const scrolled=await p.evaluate(()=>{const n=document.querySelector('.nav');
   const bef=getComputedStyle(n,'::before');
   return{light:n.classList.contains('nav--light'),beforeBg:bef.backgroundColor,
     innerBg:getComputedStyle(document.querySelector('.nav__inner')).backgroundColor};});
  console.log(`${d.n.padEnd(8)} top:${JSON.stringify(top)}`);
  console.log(`${''.padEnd(8)} scrolled:${JSON.stringify(scrolled)} errs:${errs.length?errs:'none'}`);
  await p.close();}
 await b.close();})().catch(e=>console.error('FATAL',e.message));

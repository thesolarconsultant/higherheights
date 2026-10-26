const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-nav'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();const errs=[];
  p.on('pageerror',e=>errs.push('JS '+e.message));
  p.on('requestfailed',r=>errs.push('REQ '+r.url().split('/').pop()));
  await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2200);
  const d=await p.evaluate(()=>{
    const wm=document.querySelector('.brand__wm');
    const old=document.querySelector('.brand__mark,.brand__text');
    const r=wm?wm.getBoundingClientRect():null;
    return {present:!!wm, loaded:wm?wm.naturalWidth>0:false,
      src:wm?wm.getAttribute('src').split('/').pop():null,
      w:r?Math.round(r.width):null, h:r?Math.round(r.height):null,
      alt:wm?wm.getAttribute('alt'):null, oldLockupGone:!old,
      navH:Math.round(document.querySelector('.nav__inner').getBoundingClientRect().height)};
  });
  console.log(JSON.stringify(d,null,1));
  await p.screenshot({path:'brand/z-nav.jpg',quality:94,type:'jpeg',clip:{x:0,y:0,width:1440,height:88}});
  // and at mobile
  await p.setViewport({width:414,height:860,isMobile:true});await sleep(800);
  const m=await p.evaluate(()=>{const r=document.querySelector('.brand__wm').getBoundingClientRect();
    return {w:Math.round(r.width),h:Math.round(r.height)};});
  console.log('mobile',JSON.stringify(m));
  console.log('errs',[...new Set(errs)]);
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-hero'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();
  await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(3000);
  await p.screenshot({path:'brand/hero-now.jpg',quality:92,type:'jpeg'});
  const d=await p.evaluate(()=>{
    const t=document.querySelector('.hero__title');
    const cs=e=>e?getComputedStyle(e):null;
    const ti=cs(t);
    return {
      titleFont:ti.fontFamily.split(',')[0], titleSize:ti.fontSize, titleWeight:ti.fontWeight,
      lineHeight:ti.lineHeight, letterSpacing:ti.letterSpacing,
      isUp:t.classList.contains('is-up'),
      riseCount:t.querySelectorAll('.rise').length,
      riseDisplay:cs(t.querySelector('.rise')).display,
      spanTransform:cs(t.querySelector('.rise>span')).transform,
      titleBox:(()=>{const r=t.getBoundingClientRect();return {w:Math.round(r.width),h:Math.round(r.height),top:Math.round(r.top)}})(),
      heroH:Math.round(document.querySelector('.hero').getBoundingClientRect().height),
      sub:document.querySelector('.hero__sub')?document.querySelector('.hero__sub').textContent.trim().slice(0,60):null,
      grainOp:cs(document.querySelector('.print__grain')).opacity,
    };
  });
  console.log(JSON.stringify(d,null,2));
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

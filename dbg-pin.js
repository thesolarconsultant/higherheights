const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-dbg'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();
  await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8091/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2500);
  const geo=await p.evaluate(()=>{
    const pin=document.querySelector('[data-pin]');
    const row=pin.querySelector('.pin__row');
    const abs=pin.getBoundingClientRect().top+window.scrollY;
    return {offsetTop:pin.offsetTop, offsetParent:pin.offsetParent?pin.offsetParent.className||pin.offsetParent.tagName:null,
      absTop:Math.round(abs), pinH:pin.offsetHeight, rowW:row.offsetWidth, rowScrollW:row.scrollWidth,
      pinClientW:pin.clientWidth, docH:document.body.scrollHeight, vh:innerHeight};
  });
  console.log('GEO', JSON.stringify(geo,null,1));
  for(const f of [0.02,0.5,0.98]){
    await p.evaluate((f)=>{
      const pin=document.querySelector('[data-pin]');
      const abs=pin.getBoundingClientRect().top+window.scrollY;
      window.scrollTo(0, abs + (pin.offsetHeight-innerHeight)*f);
    },f);
    await sleep(450);
    const r=await p.evaluate(()=>{
      const pin=document.querySelector('[data-pin]');
      const row=pin.querySelector('.pin__row');
      const bar=pin.querySelector('.pin__meter i');
      return {y:Math.round(scrollY), pinTop:Math.round(pin.getBoundingClientRect().top),
        stageTop:Math.round(pin.querySelector('.pin__stage').getBoundingClientRect().top),
        x:Math.round(new DOMMatrix(getComputedStyle(row).transform).m41), bar:bar.style.transform};
    });
    console.log('f='+f, JSON.stringify(r));
  }
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

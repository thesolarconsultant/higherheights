const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const DIR=path.resolve(__dirname,'brand/sourced');
const svgs=fs.readdirSync(DIR).filter(f=>f.endsWith('.svg'));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-rast2'),
    args:['--no-first-run','--hide-scrollbars','--force-device-scale-factor=1']});
  const p=await b.newPage();
  for(const f of svgs){
    const u='file:///'+path.join(DIR,f).split(path.sep).join('/');
    // navigate straight to the SVG so it is the document, not a subresource
    await p.goto(u,{waitUntil:'load',timeout:30000});
    await sleep(600);
    const dim=await p.evaluate(()=>{
      const s=document.querySelector('svg');
      if(!s) return null;
      const vb=s.getAttribute('viewBox');
      let w=parseFloat(s.getAttribute('width'))||0,h=parseFloat(s.getAttribute('height'))||0;
      if((!w||!h)&&vb){const q=vb.trim().split(/[\s,]+/);w=parseFloat(q[2]);h=parseFloat(q[3]);}
      const r=s.getBoundingClientRect();
      return {w:w||Math.round(r.width),h:h||Math.round(r.height)};
    });
    if(!dim){console.log('NO SVG in',f);continue;}
    const scale=Math.min(8,Math.max(1,1200/Math.max(dim.w,dim.h)));
    const W=Math.round(dim.w*scale),H=Math.round(dim.h*scale);
    await p.setViewport({width:Math.min(3000,W),height:Math.min(3000,H),deviceScaleFactor:1});
    await p.evaluate(()=>{document.documentElement.style.background='#fff';
      document.body&&(document.body.style.margin='0');
      const s=document.querySelector('svg');s.style.width='100%';s.style.height='100%';s.style.display='block';});
    await sleep(400);
    const out=path.join(DIR,f.replace('.svg','.png'));
    await p.screenshot({path:out,omitBackground:false});
    console.log(f,'->',path.basename(out),`${W}x${H}`);
  }
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

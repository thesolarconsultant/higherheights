const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-bb'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setViewport({width:900,height:900});
 for(const f of ['hh-navy.svg','hh-cream.svg']){
  const svg=fs.readFileSync(path.resolve(__dirname,'../site-brand/assets/img/'+f),'utf8');
  await p.setContent(`<html><body style="margin:0">${svg.replace('<svg','<svg id="S" style="width:600px;height:600px"')}</body></html>`,{waitUntil:'load'});
  await sleep(300);
  const r=await p.evaluate(()=>{const s=document.getElementById('S');
   const vb=s.getAttribute('viewBox');
   const g=s.querySelector('g')||s;
   const bb=g.getBBox();
   return{viewBox:vb,bboxX:Math.round(bb.x),bboxY:Math.round(bb.y),
     bboxW:Math.round(bb.width),bboxH:Math.round(bb.height)};});
  const [,,vw,vh]=r.viewBox.split(/\s+/).map(Number);
  console.log(`${f}  viewBox=${r.viewBox}`);
  console.log(`   ink bbox: x=${r.bboxX} y=${r.bboxY} w=${r.bboxW} h=${r.bboxH}`);
  console.log(`   overflows: left=${r.bboxX<0?-r.bboxX:0} top=${r.bboxY<0?-r.bboxY:0} right=${Math.max(0,r.bboxX+r.bboxW-vw)} bottom=${Math.max(0,r.bboxY+r.bboxH-vh)}`);
 }
 await b.close();})().catch(e=>console.error('FATAL',e.message));

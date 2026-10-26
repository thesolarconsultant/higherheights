const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const BR=path.resolve(__dirname,'../brand');
const OUT=path.resolve(__dirname,'../site-brand/assets/img');
const rd=f=>fs.readFileSync(path.join(BR,f),'utf8');
// size -> which weight-compensated cut survives it
const LADDER=[[16,'hh-mono-16.svg'],[32,'hh-mono-24.svg'],[48,'hh-mono-32.svg'],
              [180,'hh-mono.svg'],[512,'hh-mono.svg']];
(async()=>{
 const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-ico'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();
 for(const [size,file] of LADDER){
  const pad=Math.round(size*0.13), inner=size-pad*2;
  const svg=rd(file).replace('<svg',`<svg style="width:${inner}px;height:${inner}px"`);
  await p.setViewport({width:size,height:size,deviceScaleFactor:1});
  await p.setContent(`<html><body style="margin:0;width:${size}px;height:${size}px;background:#0B1A26;
    display:grid;place-items:center;color:#F4EFE6">${svg}</body></html>`,{waitUntil:'load'});
  await sleep(220);
  await p.screenshot({path:path.join(OUT,`icon-${size}.png`),omitBackground:false});
  console.log(`  icon-${size}.png  from ${file}  pad ${pad}px`);
 }
 await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

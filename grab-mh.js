const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const fs=require('fs');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'qa/p-grab'),args:['--no-first-run','--hide-scrollbars']});
  const p=await b.newPage();
  await p.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36');
  await p.goto('https://www.melissahemsley.com/',{waitUntil:'networkidle2',timeout:60000});
  await sleep(3000);
  const r=await p.evaluate(()=>{
    const out={title:document.title,imgs:[],inlineSvg:0,headerText:null};
    document.querySelectorAll('img').forEach(i=>{
      const s=i.currentSrc||i.src||'';
      const ctx=(i.className||'')+' '+(i.alt||'');
      if(/logo|brand|mark/i.test(s+' '+ctx)||i.closest('header,[class*=header],[id*=header],[class*=logo]'))
        out.imgs.push({src:s.slice(0,150),alt:i.alt,w:i.naturalWidth,h:i.naturalHeight});
    });
    out.inlineSvg=document.querySelectorAll('header svg,[class*=logo] svg,[id*=logo] svg').length;
    const h=document.querySelector('header')||document.querySelector('[class*=header]');
    out.headerText=h?h.innerText.trim().slice(0,100):null;
    return out;
  });
  console.log(JSON.stringify(r,null,1));
  // grab the best image if there is one
  if(r.imgs.length){
    const best=r.imgs.sort((a,c)=>(c.w*c.h)-(a.w*a.h))[0];
    const v=await p.goto(best.src,{timeout:30000}).catch(()=>null);
    if(v){const buf=await v.buffer();
      const ext=best.src.includes('.svg')?'.svg':best.src.includes('.png')?'.png':'.jpg';
      fs.writeFileSync(path.resolve(__dirname,'brand/sourced/melissahemsley-0'+ext),buf);
      console.log('saved melissahemsley-0'+ext, buf.length+'b');}
  }
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

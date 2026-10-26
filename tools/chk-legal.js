const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-lg'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/corporate-video-production.html',{waitUntil:'networkidle2',timeout:60000});
 await sleep(1200);
 await p.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));await sleep(800);
 const r=await p.evaluate(()=>{const e=document.querySelector('.foot__legal');
  if(!e)return{err:'missing'};const c=getComputedStyle(e),rc=e.getBoundingClientRect();
  const par=getComputedStyle(e.closest('.foot__base')||e.parentElement);
  // crude contrast
  const px=s=>s.match(/\d+/g).map(Number);
  const L=v=>{const [r,g,bl]=px(v);return (0.2126*r+0.7152*g+0.0722*bl)/255;};
  let bg=par.backgroundColor; let n=e.parentElement;
  while(bg&&/rgba\(0, 0, 0, 0\)/.test(bg)&&n){bg=getComputedStyle(n).backgroundColor;n=n.parentElement;}
  const l1=L(c.color),l2=L(bg||'rgb(7,13,11)');
  const ratio=((Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05)).toFixed(2);
  return{text:e.innerText.trim().slice(0,70),col:c.color,bg,ratio,
    w:Math.round(rc.width),h:Math.round(rc.height),fs:c.fontSize,visible:rc.height>0};});
 console.log(JSON.stringify(r,null,1));await b.close();})().catch(e=>console.error('FATAL',e.message));

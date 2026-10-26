const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-wm'),
  args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage(); await p.setCacheEnabled(false);
 for(const vp of [{width:1440,height:900,n:'desktop'},{width:900,height:800,n:'tablet'},{width:414,height:860,n:'mobile',isMobile:true}]){
  await p.setViewport(vp);
  await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(1500);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}});
  await sleep(600);
  const r=await p.evaluate(()=>{
   return [...document.querySelectorAll('.hh-wm')].map(w=>{
    const sec=w.closest('section');
    const wr=w.getBoundingClientRect(), sr=sec.getBoundingClientRect();
    // intersection of mark with its section box
    const ix=Math.max(0,Math.min(wr.right,sr.right)-Math.max(wr.left,sr.left));
    const iy=Math.max(0,Math.min(wr.bottom,sr.bottom)-Math.max(wr.top,sr.top));
    const visible=(ix*iy)/(wr.width*wr.height);
    // also clipped by the viewport horizontally?
    const vx=Math.max(0,Math.min(wr.right,innerWidth)-Math.max(wr.left,0));
    return {cls:w.className.replace('hh-wm ',''),
      w:Math.round(wr.width),h:Math.round(wr.height),
      inSection:Math.round(visible*100)+'%',
      inViewportX:Math.round(vx/wr.width*100)+'%',
      offL:Math.round(Math.max(0,sr.left-wr.left)),offR:Math.round(Math.max(0,wr.right-sr.right)),
      offT:Math.round(Math.max(0,sr.top-wr.top)),offB:Math.round(Math.max(0,wr.bottom-sr.bottom))};
   });});
  console.log(vp.n.padEnd(8),JSON.stringify(r));
 }
 await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

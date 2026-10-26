const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-sec'),
    args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage();await p.setViewport({width:1440,height:900});
  await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'networkidle2',timeout:60000});
  await sleep(2500);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,28));}window.scrollTo(0,0);});
  await sleep(1200);
  const H=await p.evaluate(()=>document.body.scrollHeight);
  // even slices down the page
  const shots=6;
  for(let i=0;i<shots;i++){
    const y=Math.round(i*(H-900)/(shots-1));
    await p.evaluate(v=>window.scrollTo(0,v),y);
    await sleep(850);
    await p.screenshot({path:`brand/d${i}.jpg`,quality:84,type:'jpeg'});
  }
  console.log('captured',shots,'slices of',H,'px');
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

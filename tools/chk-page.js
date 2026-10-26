const puppeteer=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');
const path=require('path');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const pages=process.argv.slice(2);
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-pg'),
  args:['--no-first-run','--hide-scrollbars','--autoplay-policy=no-user-gesture-required']});
 for(const pg of pages){
  const p=await b.newPage();await p.setCacheEnabled(false);await p.setViewport({width:1440,height:900});
  const errs=[];p.on('pageerror',e=>errs.push('JS '+e.message.slice(0,50)));
  p.on('requestfailed',r=>{const u=r.url();if(!u.startsWith('data:'))errs.push('404 '+u.split('/').pop());});
  await p.goto(`http://127.0.0.1:8092/${pg}`,{waitUntil:'networkidle2',timeout:60000});
  await sleep(1800);
  const r=await p.evaluate(()=>({
    title:document.title.slice(0,62),
    desc:(document.querySelector('meta[name=description]')||{}).content?.slice(0,60),
    h1:[...document.querySelectorAll('h1')].map(h=>h.innerText.trim().slice(0,46)),
    h2n:document.querySelectorAll('h2').length,
    navOK:!!document.querySelector('.nav__inner'),
    footOK:!!document.querySelector('.foot'),
    ld:document.querySelectorAll('script[type="application/ld+json"]').length,
    canon:(document.querySelector('link[rel=canonical]')||{}).href?.split('/').pop(),
    h:document.body.scrollHeight}));
  console.log(`\n── ${pg}`);
  console.log(`   title : ${r.title}`);
  console.log(`   h1    : ${r.h1.join(' | ')}`);
  console.log(`   h2s:${r.h2n}  nav:${r.navOK}  footer:${r.footOK}  ld+json:${r.ld}  height:${r.h}`);
  console.log(`   canon : ${r.canon}`);
  console.log(`   errors: ${errs.length?[...new Set(errs)].slice(0,4):'none'}`);
  await p.close();
 }
 await b.close();})().catch(e=>{console.error('FATAL',e.message);process.exit(1);});

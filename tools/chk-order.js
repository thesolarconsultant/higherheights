const pt=require('C:/Users/Jordan/Projects/goodwork-command/node_modules/puppeteer-core');const path=require('path');
(async()=>{const b=await pt.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
 headless:'new',userDataDir:path.resolve(__dirname,'../qa/p-ord'),args:['--no-first-run','--hide-scrollbars']});
 const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.setViewport({width:1440,height:900});
 await p.goto('http://127.0.0.1:8092/index.html',{waitUntil:'load',timeout:60000});
 const films=await p.evaluate(()=>[...document.querySelectorAll('[data-film]')].map(e=>{
   const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
   const f=e.querySelector('.film__frame');
   return {film:e.dataset.film, cls:e.className.match(/f\d+/)?.[0],
     shape:e.className.match(/film--[wv]/)?.[0],
     w:Math.round(r.width), ar:f?getComputedStyle(f).aspectRatio:'?'};}));
 console.log('  pos film      slot  shape     width   aspect');
 films.forEach((f,i)=>console.log(`  ${String(i+1).padEnd(3)} ${f.film.padEnd(9)} ${String(f.cls).padEnd(5)} ${String(f.shape).padEnd(9)} ${String(f.w).padEnd(7)} ${f.ar}`));
 console.log('  errors:',errs.length?errs:'none');
 await b.close();})().catch(e=>console.error('FATAL',e.message));

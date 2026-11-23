// Usage: node make-pdf.js <deck.html> <out-dir>
// Saves each slide as a 3200x1800 PNG (exactly as it looks in the browser); make-pdf.py then builds the PDF from them.
const {chromium}=require('playwright');
(async()=>{
const [src,out]=process.argv.slice(2);
const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:2});
await p.goto('file://'+require('path').resolve(src));
await p.addStyleTag({content:`body{padding:0!important}.bar{display:none!important}.deck{display:block!important}
.stage{width:1600px!important;height:900px!important;max-width:none!important;aspect-ratio:auto!important}
.slide{border-radius:0!important;transition:none!important}`});
await p.evaluate(()=>document.fonts.ready);
await p.waitForTimeout(1200);
const n=await p.$$eval('.slide',s=>s.length);
for(let i=0;i<n;i++){
  await p.evaluate(k=>{document.querySelectorAll('.slide').forEach((s,j)=>s.classList.toggle('on',j===k))},i);
  await p.waitForTimeout(250);
  await (await p.$('#stage')).screenshot({path:`${out}/s${String(i+1).padStart(2,'0')}.png`});
}
await b.close();})();

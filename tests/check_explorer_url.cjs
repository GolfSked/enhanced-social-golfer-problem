const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={URLSearchParams};vm.createContext(ctx);
vm.runInContext(fs.readFileSync('scripts/explorer-url-roster.js','utf8'),ctx);
const parse=(q)=>ctx.explorerUrlRoster(null,q)?.modelContent;
const sample='?round=Moruya|11:35&round=Narooma|10:00&round=Catalina|11:26|8&round=Moruya|11:00';
const config=parse(sample);
assert.equal(parse('?rounds=Old|10:00'), undefined);
assert.equal(parse('?rounds=Old|10:00&round=New|11:00').roundSettings[0].course, 'New');
assert.equal(config.roundSettings[0].interval,7);
assert.equal(config.roundSettings[2].interval,8);
assert.equal(config.roundSettings[3].start,'11:00');
assert.equal(config.roundSettingsError,'');
for(const q of ['?round=X|25:00','?round=X|10:60','?round=X|10:00|0','?round=X|10:00|','?round=|10:00',sample+'&round=Catalina|10:30']){
 assert(parse(q).roundSettingsError,q);assert.equal(parse(q).roundSettings.length,0);
}
assert.equal(parse('?round=Royal%20Moruya%20%26%20Club%7C11%3A35').roundSettings[0].course,'Royal Moruya & Club');
assert.equal(parse('?players=Bran:Train&round=Moruya|11:35').names[0],'Bran');
assert.equal(parse('?round=8-November%2520Moruya|11:35').roundSettings[0].course,'8-November Moruya');
assert.equal(parse('?round=100%25%2520Golf|11:35').roundSettings[0].course,'100% Golf');
assert.equal(parse('?round=A%257CB%2520Club|11:35').roundSettings[0].course,'A%7CB Club');
class El{
 constructor(tag='div'){this.tag=tag;this.children=[];this.options=[];this.style={setProperty(){}};this.events={};this.value='';this.attrs={};this.classes=new Set();this.classList={toggle:(c,v)=>v?this.classes.add(c):this.classes.delete(c)};this.previousElementSibling={textContent:''};this._text=''}
 get textContent(){return this._text+this.children.map(c=>typeof c==='string'?c:c.textContent).join('')}
 set textContent(s){this._text=String(s);this.children=[]}
 append(...xs){this.children.push(...xs)}replaceChildren(){this.children=[];this._text=''}setAttribute(k,v){this.attrs[k]=v}addEventListener(n,f){this.events[n]=f}
}
function render(modelContent, rounds=4){
 const els={};els.rootEvents={};const root={querySelector(s){return els[s]??=new El()},addEventListener(n,f){els.rootEvents[n]=f}};
 root.querySelector('#ag-r').options=Array.from({length:rounds},()=>({textContent:''}));
 const html=fs.readFileSync(`solutions/${({3:'three',4:'four',5:'five'})[rounds]}-round-schedule-explorer.html`,'utf8');
 // Source fragment script is HTML-escaped in the standalone export.
 const escaped=html.match(/data-srcdoc="([\s\S]*?)"><\/iframe>/)[1];
 const decode=s=>s.replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
 const scripts=[...decode(escaped).matchAll(/<script>([\s\S]*?)<\/script>/g)];
 const source=scripts.find(m=>m[1].includes(`const root=document.getElementById('${({3:'three',4:'all',5:'five'})[rounds]}-golf-grids')`))[1];
 vm.runInNewContext(source,{document:{getElementById(){return root},createElement(tag){return new El(tag)},createTextNode(s){return s}},window:{openai:{widgetState:{modelContent},setWidgetState(){return Promise.resolve()}},addEventListener(){}}});
 return els;
}
let els=render({...config,round:1});
assert(els['#ag-course'].textContent.includes('Moruya · first tee 11:35'));
assert(els['#ag-detail'].textContent.includes('11:56:'));
els['#ag-r'].value=2;els['#ag-r'].events.change();
assert(els['#ag-course'].textContent.includes('Catalina · first tee 11:26 · 8-minute'));
assert(els['#ag-detail'].textContent.includes('11:50:'));
els=render({round:1,roundSettings:[{course:'Late',start:'23:55',interval:7}]});
assert(els['#ag-detail'].textContent.includes('00:02 (+1 day)'));
els=render({});assert.equal(els['#ag-n'].value,16);assert(els['#ag-course'].textContent.includes('10:00'));
const example='?round=8-November%20Moruya|11:35&round=9-November%20Narooma|10:00&round=10-November%20Catalina|11:26&round=11-November%20Moruya|11:00&players=Bran:Train:Chops:Torpey:Gun:Alder:Fedo:Drennan:Godge:Laracy:Penguin:Smith:Clarkey:Klug:Fisk:Tallack';
els=render(parse(example));
assert.equal(els['#ag-course-0'].value,'8-November Moruya');
assert.equal(els['#ag-start-2'].value,'11:26');
assert(els['#ag-detail'].textContent.includes('Tallack'));
els['#ag-course-0'].value='Updated Course';els['#ag-start-0'].value='12:05';els['#ag-interval-0'].value='8';
els['#ag-apply-rounds'].events.click();
assert(els['#ag-course'].textContent.includes('Updated Course · first tee 12:05 · 8-minute'));
assert(els['#ag-detail'].textContent.includes('12:29:'));
const applied=els['#ag-detail'].textContent;
els['#ag-start-1'].value='25:10';els['#ag-apply-rounds'].events.click();
assert.equal(els['#ag-round-error'].hidden,false);assert.equal(els['#ag-detail'].textContent,applied);
console.log('URL settings, exact user example, round editing, validation and midnight rollover passed.');

const fiveQuery=sample+'&round=Catalina|10:30';
const fiveConfig=ctx.explorerUrlRoster(null,fiveQuery,5).modelContent;
assert.equal(fiveConfig.roundSettingsError,'');
assert.equal(fiveConfig.roundSettings.length,5);
for(let n=15;n<=24;n++){
 const e=render({...fiveConfig,players:n},5);
 assert.equal(e['#ag-r'].options.length,5);
 for(let r=0;r<5;r++){e['#ag-r'].value=r;e['#ag-r'].events.change();assert(!e['#ag-detail'].textContent.includes('undefined'))}
 assert(e['#ag-course'].textContent.includes('Catalina · first tee 10:30'));
 assert(e['#ag-c'].children.length>0);
 e['#ag-course-4'].value='Fifth course';e['#ag-start-4'].value='12:00';e['#ag-interval-4'].value='9';e['#ag-apply-rounds'].events.click();
 assert(e['#ag-course'].textContent.includes('Fifth course · first tee 12:00 · 9-minute'));
}
console.log('Five-round URL support, all 50 schedule views, partial C and fifth-round editing passed.');

const threeQuery='?round=Moruya|11:35&round=Narooma|10:00&round=Catalina|11:26|8';
const threeConfig=ctx.explorerUrlRoster(null,threeQuery,3).modelContent;
assert.equal(threeConfig.roundSettingsError,'');
assert(ctx.explorerUrlRoster(null,threeQuery+'&round=Extra|10:00',3).modelContent.roundSettingsError);
for(let n=15;n<=24;n++){
 const e=render({...threeConfig,players:n},3);
 for(let r=0;r<3;r++){e['#ag-r'].value=r;e['#ag-r'].events.change();assert(!e['#ag-detail'].textContent.includes('undefined'))}
 assert(e['#ag-a'].children.length>0);
 assert(e['#ag-course'].textContent.includes('Catalina · first tee 11:26 · 8-minute'));
 e['#ag-course-2'].value='Third course';e['#ag-start-2'].value='12:00';e['#ag-interval-2'].value='9';e['#ag-apply-rounds'].events.click();
 assert(e['#ag-course'].textContent.includes('Third course · first tee 12:00 · 9-minute'));
 e['#ag-names'].value='Alice\nBob';e['#ag-apply'].events.click();assert(e['#ag-detail'].textContent.includes('Alice'));
}
console.log('Three-round URL support, all 30 views, names and third-round editing passed.');
for(const word of ['three','four','five']){
 const html=fs.readFileSync(`solutions/${word}-round-schedule-explorer.html`,'utf8');
 assert(html.includes('id="golf-explorer-theme"'));
 assert(html.includes('id=&quot;golf-explorer-theme&quot;'));
 for(const color of ['#f8f6ef','#173d33','#315b47','#bacd9b','#e8dfca','#e8d8a4'])assert(html.includes(color));
}
console.log('Landing-page palette is embedded in each explorer and its sandboxed frame.');

for(const rounds of [3,4,5]){
 for(const count of [15,18,24]){
  const e=render({},rounds);const entries=Array.from({length:count},(_,i)=>i===3?'':`Name ${i+1}`);
  e['#ag-names'].value=entries.join('\n')+'\n\n';e['#ag-apply'].events.click();
  assert.equal(e['#ag-n'].value,count);assert(e['#ag-name-message'].textContent.includes(`selected ${count}`));assert(e['#ag-detail'].textContent.includes('P4'));
 }
 const e=render({players:18},rounds);
 e['#ag-names'].value='Alice\nBob';e['#ag-apply'].events.click();assert.equal(e['#ag-n'].value,18);
 const previous=e['#ag-detail'].textContent;
 e['#ag-names'].value=Array.from({length:25},(_,i)=>`Too many ${i}`).join('\n');e['#ag-apply'].events.click();
 assert.equal(e['#ag-n'].value,18);assert.equal(e['#ag-detail'].textContent,previous);assert(e['#ag-name-message'].textContent.includes('not applied'));
 for(let n=15;n<=24;n++)for(let round=1;round<=rounds;round++){
  const view=render({players:n,round},rounds);const cells=view['#ag-board'].children.filter(c=>c.tag==='button');assert.equal(cells.length,n);
  const c=cells[0];c.events.pointerenter({pointerType:'mouse'});
  const size=cells.filter(c=>c.classes.has('ag-highlighted')).length;assert(size===3||size===4);
  for(const id of ['#ag-a',...(rounds>=4?['#ag-b']:[]),...(rounds===5?['#ag-c']:[])])assert.equal(view[id].children.filter(c=>c.classes.has('ag-highlighted')).length,size);
  assert.equal(view['#ag-detail'].children.filter(c=>c.classes?.has('ag-highlighted')).length,1);
  c.events.pointerleave();assert.equal(cells.filter(c=>c.classes.has('ag-highlighted')).length,0);
  c.events.click();c.events.pointerleave();assert.equal(cells.filter(c=>c.attrs['aria-pressed']==='true').length,size);
  view.rootEvents.keydown({key:'Escape'});assert.equal(cells.filter(c=>c.classes.has('ag-highlighted')).length,0);
  c.events.focus();assert.equal(cells.filter(c=>c.classes.has('ag-highlighted')).length,size);c.events.blur();
  c.events.click();view['#ag-clear'].events.click();assert.equal(cells.filter(c=>c.classes.has('ag-highlighted')).length,0);
 }
}
const version=fs.readFileSync('web/version.txt','utf8').trim();
for(const word of ['three','four','five']){
 const html=fs.readFileSync(`solutions/${word}-round-schedule-explorer.html`,'utf8');
 assert(html.includes(`<meta name="application-version" content="${version}">`));assert(!html.includes('__EXPLORER_VERSION__'));
}
console.log('All 120 views pass linked hover/focus/pin checks; name counts, blank slots, overflow and release versions verified.');
for(const rounds of [3,4,5]){
 const e=render({roundSettings:[{course:'8-November%20Moruya',start:'11:35',interval:7}]},rounds);
 assert(e['#ag-course'].textContent.includes('8-November Moruya'));
 assert.equal(e['#ag-course-0'].value,'8-November Moruya');
 e['#ag-course-0'].value='100%20Golf';e['#ag-apply-rounds'].events.click();
 assert(e['#ag-course'].textContent.includes('100 Golf'));
}
console.log('Encoded spaces are repaired in URLs, restored labels and round editors; percent signs and separators are preserved.');

// Navigation must work even when activation expires during frame messaging.
for(const word of ['three','four','five']){
 const html=fs.readFileSync(`solutions/${word}-round-schedule-explorer.html`,'utf8');
 assert(html.includes('sandbox="allow-scripts"'));
 const branch=html.slice(html.indexOf('    if (data.type === "open-external") {'),html.indexOf('    if (data.type === "follow-up") {'));
 assert(branch.includes('globalThis.location.assign(href)'));
 for(const [href,expected] of [['https://golfsked.github.io/enhanced-social-golfer-problem/','https://golfsked.github.io/enhanced-social-golfer-problem/'],['https://github.com/GolfSked/enhanced-social-golfer-problem','https://github.com/GolfSked/enhanced-social-golfer-problem'],['javascript:alert(1)',null],['http://example.com/',null],[null,null]]){
  const navigated=[];
  vm.runInNewContext(`(()=>{${branch}})()`,{data:{type:'open-external',href},URL,document:{baseURI:'https://golfsked.github.io/enhanced-social-golfer-problem/'},navigator:{userActivation:{isActive:false}},location:{assign:url=>navigated.push(url)}});
  assert.deepEqual(navigated,expected?[expected]:[]);
 }
}
console.log('All explorer links navigate in the same tab without popup APIs; HTTPS validation is preserved.');
// Best-first numbering and allocation summaries apply to every saved schedule.
for(const [rounds,word] of [[3,'three'],[4,'four'],[5,'five']]){
 const source=fs.readFileSync(`web/explorer-sources/${word}-round.html`,'utf8');
 const data=JSON.parse(source.match(/const data=(.*?);\nconst np=/s)[1]);
 for(let n=15;n<=24;n++){
  const counts=Array.from({length:n},(_,i)=>new Set(data[n].groups[i+1]).size);
  assert.deepEqual(counts,[...counts].sort((a,b)=>b-a));
  const parts=[];
  for(let first=0;first<n;){let last=first;while(last+1<n&&counts[last+1]===counts[first])last++;
   parts.push(`${first===last?'P'+(first+1):'P'+(first+1)+'–P'+(last+1)}: ${counts[first]} distinct tee positions${first===last?'':' each'}`);first=last+1;
  }
  assert(render({players:n},rounds)['#ag-check'].textContent.endsWith(parts.join('; ')));
 }
}
console.log('All 30 saved schedules use best-first player numbering and show complete position-allocation summaries.');

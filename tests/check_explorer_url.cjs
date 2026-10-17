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
class El{
 constructor(){this.children=[];this.options=[];this.style={setProperty(){}};this.events={};this.value='';this.previousElementSibling={textContent:''}}
 append(...xs){this.children.push(...xs)}replaceChildren(){this.children=[]}setAttribute(){}addEventListener(n,f){this.events[n]=f}
}
function render(modelContent, rounds=4){
 const els={};const root={querySelector(s){return els[s]??=new El()}};
 root.querySelector('#ag-r').options=Array.from({length:rounds},()=>({textContent:''}));
 const html=fs.readFileSync(`solutions/${({3:'three',4:'four',5:'five'})[rounds]}-round-schedule-explorer.html`,'utf8');
 // Source fragment script is HTML-escaped in the standalone export.
 const escaped=html.match(/data-srcdoc="([\s\S]*?)"><\/iframe>/)[1];
 const decode=s=>s.replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
 const scripts=[...decode(escaped).matchAll(/<script>([\s\S]*?)<\/script>/g)];
 const source=scripts.find(m=>m[1].includes(`const root=document.getElementById('${({3:'three',4:'all',5:'five'})[rounds]}-golf-grids')`))[1];
 vm.runInNewContext(source,{document:{getElementById(){return root},createElement(){return new El()},createTextNode(s){return s}},window:{openai:{widgetState:{modelContent},setWidgetState(){return Promise.resolve()}},addEventListener(){}}});
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
 for(const color of ['#f8f6ef','#173d33','#315b47','#bacd9b','#d6dcb0','#e8d8a4'])assert(html.includes(color));
}
console.log('Landing-page palette is embedded in each explorer and its sandboxed frame.');

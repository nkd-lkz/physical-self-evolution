/* RLT project hub: evidence remains in current-status/experiments; notes are indexed. */
'use strict';
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const readLink=p=>'reader.html?path='+encodeURIComponent(p);
const safeURL=url=>{try{const u=new URL(url,location.href);return ['http:','https:'].includes(u.protocol)?u.href:'#';}catch{return '#';}};
const state={docs:[],progress:[],days:4,limit:16};
async function loadJSON(path){const r=await fetch(path);if(!r.ok)throw Error(path+' · HTTP '+r.status);return r.json();}
function tags(xs){return xs.map(x=>'<span class="tag">'+esc(x)+'</span>').join('');}
function renderStatus(s){
 $('asOf').textContent='最近记录 '+s.as_of;$('statusDate').textContent=s.as_of+' · 非实时训练监控';
 // Explicit current priorities take precedence; retain the historical fallback.
 const groups=[/Stage 1/,/Stage 2.*评估/,/matched smoke|baseline与FLARE/,/Jev GPU|Jev.*pilot/];
 const selected=s.metrics.filter(m=>m.featured===true);
 const metrics=selected.length?selected.slice(0,4):groups.map(re=>s.metrics.find(m=>re.test(m.label))).filter(Boolean);
 for(const m of s.metrics){if(metrics.length>=4)break;if(!metrics.includes(m))metrics.push(m);}
 $('statusMetrics').innerHTML=metrics.map(m=>'<article class="metric"><strong>'+esc(m.value)+'</strong><p>'+esc(m.label)+'</p></article>').join('');
 $('allEvidence').innerHTML='<div class="evidence-list">'+s.metrics.map(m=>'<p><b>'+esc(m.value)+'</b><br>'+esc(m.label)+'</p>').join('')+'</div>'+s.timeline.map(t=>'<div class="timeline-note"><b>'+esc(t.title)+'</b><p class="muted">'+esc(t.body)+'</p></div>').join('');
 const action=p=>'<div class="next-item"><span class="priority">'+esc(p.priority)+'</span><div><b>'+esc(p.action)+'</b><p>'+esc(p.evidence)+'</p></div></div>';
 $('nextActions').innerHTML=s.plan.slice(0,3).map(action).join('')+(s.plan.length>3?'<details><summary>其余 '+(s.plan.length-3)+' 项后续计划</summary><div>'+s.plan.slice(3).map(action).join('')+'</div></details>':'');
}
function renderIdeas(config){
 $('focus').textContent=config.focus;$('question').textContent=config.question;
 $('ideaGrid').innerHTML=config.ideas.map(i=>'<article class="idea-card"><div class="idea-top"><span class="tag '+(i.stage.includes('待')?'warn':'')+'">'+esc(i.stage)+'</span><span>'+esc(i.tag)+'</span></div><h3>'+esc(i.name)+'</h3><p>'+esc(i.hypothesis)+'</p><dl><dt>实现</dt><dd>'+esc(i.design)+'</dd><dt>对照</dt><dd>'+esc(i.control)+'</dd><dt>判定</dt><dd>'+esc(i.gate)+'</dd></dl><a class="text-link" href="'+readLink(i.path)+'">展开方案与证据 ↗</a></article>').join('');
 $('featuredGrid').innerHTML=config.featured.map(f=>'<a class="featured" href="'+readLink(f.path)+'"><strong>'+esc(f.label)+' ↗</strong><p>'+esc(f.why)+'</p></a>').join('');
}
function renderProgress(){
 const q=$('progressSearch').value.trim().toLowerCase(),date=$('progressDate').value;
 const list=state.progress.filter(p=>(date==='all'||p.date===date)&&(!q||(p.title+' '+p.summary).toLowerCase().includes(q)));
 const dates=[...new Set(list.map(p=>p.date))].sort().reverse();
 $('progressCount').textContent=list.length+' 条记录 · '+dates.length+' 个科研日';
 function entry(p){return '<article class="progress-entry">'+tags((p.topics||[]).slice(0,2))+'<h3>'+esc(p.title)+'</h3><p>'+esc(p.summary)+'</p><a href="'+readLink(p.path)+'">查看详细记录 ↗</a></article>';}
 $('progressFeed').innerHTML=dates.slice(0,state.days).map(day=>{
 const entries=list.filter(p=>p.date===day); const daily=state.docs.find(d=>d.path&&d.path.startsWith('research/progress-'+day));
 return '<div class="day-group"><div class="day-heading"><strong>'+esc(day.slice(5).replace('-','.'))+'</strong><span>'+esc(day.slice(0,4))+' · '+entries.length+' 条</span><a href="'+readLink(daily?.path||'research/experiment-log.md')+'">阅读日报 ↗</a></div><div class="day-entries">'+entries.slice(0,3).map(entry).join('')+(entries.length>3?'<details class="day-older"'+(q?' open':'')+'><summary>展开当天其余 '+(entries.length-3)+' 条记录</summary>'+entries.slice(3).map(entry).join('')+'</details>':'')+'</div></div>';
 }).join('')||'<p class="empty">没有匹配的进度记录，请调整关键词或日期。</p>';
 $('moreProgress').hidden=dates.length<=state.days;
}
function syncFilters(){const url=new URL(location.href);for(const [id,key] of [['librarySearch','q'],['kindFilter','kind'],['topicFilter','topic']]){const v=$(id).value;if(v&&v!=='all')url.searchParams.set(key,v);else url.searchParams.delete(key);}history.replaceState(null,'',url);}
function renderLibrary(updateURL=true){
 const q=$('librarySearch').value.trim().toLowerCase(),kind=$('kindFilter').value,topic=$('topicFilter').value;
 const terms=q.split(/\s+/).filter(Boolean);
 const results=state.docs.filter(d=>(kind==='all'||d.kind===kind)&&(topic==='all'||d.topics.includes(topic))&&terms.every(t=>(d.search+' '+d.topics.join(' ')+' '+d.status).toLowerCase().includes(t)));
 $('libraryCount').textContent='找到 '+results.length+' 项 · 显示 '+Math.min(state.limit,results.length)+' 项';
 $('libraryList').innerHTML=results.slice(0,state.limit).map(d=>{
 const href=d.path?readLink(d.path):safeURL(d.source);
 return '<article class="library-item"><div class="item-meta"><span class="tag '+(!d.path?'warn':'')+'">'+esc(d.kind)+'</span><time>'+esc(d.date||'未建独立笔记')+'</time></div><div><h3><a href="'+href+'">'+esc(d.title)+'</a></h3><p>'+esc(d.summary)+'</p><div class="item-topics">'+tags(d.topics.slice(0,4))+'</div><div class="item-status">'+esc(d.status)+'</div></div><div class="item-action"><a href="'+href+'">'+(d.path?'阅读笔记':'查看原文')+' ↗</a>'+(d.path&&d.source?'<a href="'+safeURL(d.source)+'">原始来源 ↗</a>':'')+'</div></article>';
 }).join('')||'<p class="empty">没有匹配的资料。试试更短的关键词，或清除筛选条件。</p>';
 $('moreLibrary').hidden=results.length<=state.limit;
 if(updateURL)syncFilters();
}
function legacyHash(){const aliases={mainline:'ideas',architecture:'ideas',physical:'ideas',baseline:'status',frontier:'library',literature:'library',reading:'library',papers:'library',perspectives:'library',archive:'library'};const old=location.hash.slice(1);if(aliases[old]){history.replaceState(null,'',location.pathname+location.search+'#'+aliases[old]);document.getElementById(aliases[old])?.scrollIntoView();}}
async function init(){
 const jobs=[['状态','data/current-status.json',renderStatus],['研究方案','data/research-hub.json',renderIdeas],['资料索引','data/knowledge-index.json',index=>{
 state.docs=index.documents;state.progress=index.progress;
 $('libraryStats').innerHTML='<span><b>'+index.stats.project_documents+'</b>项目文档</span><span><b>'+index.stats.reading_ledger+'</b>总账条目（含待读）</span><span><b>'+index.stats.progress_days+'</b>科研记录日</span><span><b>'+index.stats.progress_entries+'</b>进度条目</span>';
 $('progressDate').insertAdjacentHTML('beforeend',[...new Set(state.progress.map(p=>p.date))].sort().reverse().map(d=>'<option>'+esc(d)+'</option>').join(''));
 for(const [id,values] of [['kindFilter',state.docs.map(d=>d.kind)],['topicFilter',state.docs.flatMap(d=>d.topics)]])$(id).insertAdjacentHTML('beforeend',[...new Set(values)].sort().map(v=>'<option>'+esc(v)+'</option>').join(''));
 const params=new URLSearchParams(location.search);for(const[id,key]of[['librarySearch','q'],['kindFilter','kind'],['topicFilter','topic']]){const v=params.get(key);if(v){$(id).value=v;if($(id).tagName==='SELECT'&&!$(id).value)$(id).value='all';}}
 renderProgress();renderLibrary(false);
 }]];
 const results=await Promise.allSettled(jobs.map(async([name,path,render])=>{render(await loadJSON(path));return name;}));
 const errors=results.flatMap((r,i)=>r.status==='rejected'?[jobs[i][0]+'：'+r.reason.message]:[]);
 if(errors.length){$('loadError').hidden=false;$('loadError').textContent='部分内容读取失败，请刷新重试。'+errors.join('；');}
 legacyHash();
}
['progressSearch','progressDate'].forEach(id=>$(id).addEventListener(id==='progressSearch'?'input':'change',()=>{state.days=4;renderProgress();}));
['librarySearch','kindFilter','topicFilter'].forEach(id=>$(id).addEventListener(id==='librarySearch'?'input':'change',()=>{state.limit=16;renderLibrary();}));
$('moreProgress').addEventListener('click',()=>{state.days+=4;renderProgress();});
$('moreLibrary').addEventListener('click',()=>{state.limit+=16;renderLibrary();});
$('clearFilters').addEventListener('click',()=>{$('librarySearch').value='';$('kindFilter').value='all';$('topicFilter').value='all';state.limit=16;renderLibrary();});
window.addEventListener('hashchange',legacyHash);
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();$('library').scrollIntoView();$('librarySearch').focus({preventScroll:true});}});
const nav=[...document.querySelectorAll('.sidebar nav a')];
const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){nav.forEach(a=>{const active=a.hash==='#'+e.target.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}},{rootMargin:'-10% 0px -65% 0px'});
document.querySelectorAll('main>section').forEach(el=>observer.observe(el));
init();

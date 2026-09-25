async function loadJSON(path){const r=await fetch(path);if(!r.ok)throw new Error(path);return r.json()}
async function loadJSONOptional(path){try{return await loadJSON(path)}catch(e){return []}}
function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
let papers=[];
let frontier=[];
async function init(){
  try{
    const [basePapers,latestPapers,baseFrontier,frontierAdds,currentStatus,literatureLedger]=await Promise.all([
      loadJSON('data/papers.json'),
      loadJSONOptional('data/latest-readings.json'),
      loadJSON('data/frontier.json'),
      loadJSONOptional('data/frontier-additions.json'),
      loadJSONOptional('data/current-status.json'),
      loadJSONOptional('data/literature-reading-ledger.json')
    ]);
    papers=[...latestPapers,...basePapers.filter(p=>!latestPapers.some(x=>x.id===p.id))];
    frontier=[...frontierAdds,...baseFrontier.filter(p=>!frontierAdds.some(x=>x.id===p.id))];
    renderPapers();
    renderFrontier();
    renderCurrentStatus(currentStatus);
    renderLiteratureStatus(literatureLedger);
    const logs=await loadJSON('data/experiments.json');
    document.getElementById('experimentList').innerHTML=logs.map(x=>'<div><b>'+esc(x.date)+' · '+esc(x.title)+'</b><p>'+esc(x.summary)+'</p></div>').join('');
  }catch(e){console.error(e)}
}
function renderCurrentStatus(s){
  if(!s||Array.isArray(s)||!s.metrics)return;
  const metricWrap=document.querySelector('#status .metrics');
  if(metricWrap){
    metricWrap.innerHTML=s.metrics.map(x=>'<article class="card"><div class="metric">'+esc(x.value)+'</div><div class="muted">'+esc(x.label)+'</div></article>').join('');
  }
  const timeline=document.querySelector('#status .timeline');
  if(timeline&&Array.isArray(s.timeline)){
    timeline.innerHTML=s.timeline.map(x=>'<div><b>'+esc(x.title)+'</b><p>'+esc(x.body)+'</p></div>').join('');
  }
  const planBody=document.querySelector('#plan tbody');
  if(planBody&&Array.isArray(s.plan)){
    planBody.innerHTML=s.plan.map(x=>'<tr><td>'+esc(x.priority)+'</td><td>'+esc(x.action)+'</td><td>'+esc(x.evidence)+'</td></tr>').join('');
  }
  const statusHeading=document.querySelector('#status h2');
  if(statusHeading&&s.as_of){statusHeading.title='动态状态快照：'+s.as_of;}
}
function renderLiteratureStatus(s){
  if(!s||Array.isArray(s)||!s.status_counts)return;
  const wrap=document.getElementById('literatureMetrics');
  if(!wrap)return;
  const counts=s.status_counts||{};
  const deep=(counts['已精读/已有独立笔记']||0)+(counts['已阅读/已有专题笔记']||0);
  const skim=(counts['已初读/讨论过，待系统精读']||0);
  const unread=(counts['待精读']||0);
  const total=Array.isArray(s.papers)?s.papers.length:(deep+skim+unread);
  wrap.innerHTML=
    '<article class="card"><div class="metric">'+esc(total)+'</div><div class="muted">当前主表文献总数</div></article>'+
    '<article class="card"><div class="metric">18</div><div class="muted">09-19 批次防撞优先</div></article>'+
    '<article class="card"><div class="metric">'+esc(deep)+'</div><div class="muted">已精读 / 专题阅读</div></article>'+
    '<article class="card"><div class="metric">'+esc(unread)+'</div><div class="muted">待系统精读（另有 '+esc(skim)+' 篇已初读）</div></article>';
}
function renderFrontier(){
  const q=(document.getElementById('frontierSearch')?.value||'').toLowerCase();
  const f=document.getElementById('frontierFilter')?.value||'all';
  const grid=document.getElementById('frontierGrid');
  if(!grid)return;
  grid.innerHTML='';
  frontier.filter(w=>{
    const txt=[w.title,w.category,w.layer,w.update,w.feedback,w.timescale,w.summary,w.mechanism,w.evidence,w.borrow,w.boundary].join(' ').toLowerCase();
    return (f==='all'||w.category===f)&&txt.includes(q);
  }).forEach(w=>{
    const a=document.createElement('article');
    a.className='card work-card';
    a.innerHTML=
      '<div class="work-meta">'+esc(w.year)+' · '+esc(w.layer)+' · '+esc(w.status)+'</div>'+
      '<div class="paper-title">'+esc(w.title)+'</div>'+
      '<div class="work-facts"><span>更新：'+esc(w.update)+'</span><span>反馈：'+esc(w.feedback)+'</span><span>尺度：'+esc(w.timescale)+'</span></div>'+
      '<p>'+esc(w.summary)+'</p>'+
      '<p class="paper-relation"><b>机制：</b>'+esc(w.mechanism)+'</p>'+
      '<p class="paper-relation"><b>可借鉴：</b>'+esc(w.borrow)+'</p>'+
      '<p class="paper-relation"><b>边界：</b>'+esc(w.boundary)+'</p>'+
      '<div class="read-more"><a href="'+esc(w.url)+'" target="_blank" rel="noopener">'+esc(w.url_label||'原文 / 项目 ↗')+'</a>'+(w.note&&w.note!==w.url?' · <a href="'+esc(w.note)+'">专题分析 →</a>':'')+'</div>';
    grid.appendChild(a);
  });
}

function renderPapers(){
  const q=(document.getElementById('paperSearch').value||'').toLowerCase();
  const f=document.getElementById('paperFilter').value;
  const grid=document.getElementById('paperGrid');
  grid.innerHTML='';
  papers.filter(p=>{const txt=[p.title,p.layer,p.one,...(p.tags||[])].join(' ').toLowerCase();return (f==='all'||p.theme===f)&&txt.includes(q)}).forEach(p=>{
    const a=document.createElement('a');a.className='card paper-card';a.href=p.note||p.url||'#';
    a.innerHTML='<div class="paper-meta">'+esc(p.year)+' · '+esc(p.layer)+' · '+esc(p.status)+'</div><div class="paper-title">'+esc(p.title)+'</div><p>'+esc(p.one)+'</p><div class="paper-relation"><b>当前主线提示：</b>论文卡保留为知识库；具体项目关系以 Leadership Physical Token Spec 为准。</div><div class="read-more">深入阅读 →</div>';
    grid.appendChild(a);
  });
}
document.addEventListener('DOMContentLoaded',()=>{
  document.getElementById('paperSearch')?.addEventListener('input',renderPapers);
  document.getElementById('paperFilter')?.addEventListener('change',renderPapers);
  document.getElementById('frontierSearch')?.addEventListener('input',renderFrontier);
  document.getElementById('frontierFilter')?.addEventListener('change',renderFrontier);
  init();
});

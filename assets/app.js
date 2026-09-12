async function loadJSON(path){const r=await fetch(path);if(!r.ok)throw new Error(path);return r.json()}
async function loadJSONOptional(path){try{return await loadJSON(path)}catch(e){return []}}
function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
let papers=[];
let frontier=[];
async function init(){
  try{
    const [basePapers,latestPapers,baseFrontier,frontierAdds]=await Promise.all([
      loadJSON('data/papers.json'),
      loadJSONOptional('data/latest-readings.json'),
      loadJSON('data/frontier.json'),
      loadJSONOptional('data/frontier-additions.json')
    ]);
    papers=[...latestPapers,...basePapers.filter(p=>!latestPapers.some(x=>x.id===p.id))];
    frontier=[...frontierAdds,...baseFrontier.filter(p=>!frontierAdds.some(x=>x.id===p.id))];
    renderPapers();
    renderFrontier();
    const logs=await loadJSON('data/experiments.json');
    document.getElementById('experimentList').innerHTML=logs.map(x=>'<div><b>'+esc(x.date)+' · '+esc(x.title)+'</b><p>'+esc(x.summary)+'</p></div>').join('');
  }catch(e){console.error(e)}
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
      '<div class="read-more"><a href="'+esc(w.url)+'" target="_blank" rel="noopener">原文 / 项目 ↗</a></div>';
    grid.appendChild(a);
  });
}

function renderPapers(){
  const q=(document.getElementById('paperSearch').value||'').toLowerCase();
  const f=document.getElementById('paperFilter').value;
  const grid=document.getElementById('paperGrid');
  grid.innerHTML='';
  papers.filter(p=>{const txt=[p.title,p.layer,p.one,p.project,...(p.tags||[])].join(' ').toLowerCase();return (f==='all'||p.theme===f)&&txt.includes(q)}).forEach(p=>{
    const a=document.createElement('a');a.className='card paper-card';a.href=p.note||p.url||'#';
    a.innerHTML='<div class="paper-meta">'+esc(p.year)+' · '+esc(p.layer)+' · '+esc(p.status)+'</div><div class="paper-title">'+esc(p.title)+'</div><p>'+esc(p.one)+'</p><div class="paper-relation"><b>对当前项目：</b>'+esc(p.project)+'</div><div class="read-more">深入阅读 →</div>';
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
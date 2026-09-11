async function loadJSON(path){const r=await fetch(path);if(!r.ok)throw new Error(path);return r.json()}
function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
let papers=[];
async function init(){
  try{
    papers=await loadJSON('data/papers.json');
    renderPapers();
    const logs=await loadJSON('data/experiments.json');
    document.getElementById('experimentList').innerHTML=logs.map(x=>'<div><b>'+esc(x.date)+' · '+esc(x.title)+'</b><p>'+esc(x.summary)+'</p></div>').join('');
  }catch(e){console.error(e)}
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
document.addEventListener('DOMContentLoaded',()=>{document.getElementById('paperSearch').addEventListener('input',renderPapers);document.getElementById('paperFilter').addEventListener('change',renderPapers);init()});
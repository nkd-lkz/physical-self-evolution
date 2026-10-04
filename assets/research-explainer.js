/* Method views explain a proposal. The slider uses measured training data only. */
'use strict';
(() => {
 const root=document.getElementById('understand'); if(!root)return;
 const byId=id=>document.getElementById(id);
 const views={
  zero:{status:'已实现 · 昨晚对照',condition:'64 维全零条件',detail:'actor 看不到历史响应。它仍读取当前特征和 reference。它与响应组使用相同头部容量。'},
  response:{status:'已实现 · 控制收益未证明',condition:'固定响应统计',detail:'读取已完成的命令与关节变化。七个响应斜率和七个支持度补齐为 64 维。这个 reader 不更新参数。'},
  learned:{status:'拟议 · Stage 1B 尚未实现',condition:'学习得到的经验条件',detail:'拟用真实后继监督经验 encoder／reader。首轮在 Stage 2 冻结它们。这是待验证设计，不是昨晚训练的模型。'}
 };
 const steps=[
  '① 读取当前图像、任务和本体观测。冻结 VLA 生成特征与 reference 动作。',
  '② 只读取此前完成的历史。当前动作还没有执行，其后果不能进入条件。',
  '③ 小 actor 生成动作。环境 gate 决定何时切换到 actor。本轮没有 expert。',
  '④ 执行完成后，记录实际命令和真实后继。记录从下一次决策开始可用。'
 ];
 let mode='response',step=0;
 function renderMethod(){
  const v=views[mode];byId('methodStatus').textContent=v.status;byId('conditionName').textContent=v.condition;
  byId('methodDetail').textContent=v.detail;byId('flowDetail').textContent=steps[step];
  root.querySelectorAll('[data-method]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.method===mode)));
  root.querySelectorAll('[data-flow-step]').forEach(n=>n.classList.toggle('active',Number(n.dataset.flowStep)===step));
  byId('advanceFlow').textContent=step===3?'回到下一次决策':'下一步 →';
 }
 root.querySelectorAll('[data-method]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.method;renderMethod();}));
 byId('advanceFlow').addEventListener('click',()=>{step=(step+1)%4;renderMethod();});renderMethod();
 fetch('data/zeva-matched-results-2026-10-04.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json();}).then(data=>{
  const rows=data.common_evaluations,range=byId('checkpointSlider');range.max=rows.length-1;range.value=rows.length-1;
  const x=n=>52+(n-25)/250*428,y=v=>178-v*144;
  function draw(selected){
   let svg='<svg class="ex-chart" viewBox="0 0 520 222" role="img" aria-labelledby="curveTitle curveDesc"><title id="curveTitle">相同训练轮次的成功率</title><desc id="curveDesc">蓝线为零条件，橙线为固定响应。每个点只有八个评估回合；完整数值在下方表格。</desc>';
   for(const n of [0,0.25,0.5,0.75,1])svg+='<line x1="52" x2="480" y1="'+y(n)+'" y2="'+y(n)+'" stroke="#dfe5df"/><text x="43" y="'+(y(n)+4)+'" text-anchor="end" font-size="11" fill="#526259">'+Math.round(n*100)+'%</text>';
   for(const n of [25,75,125,175,225,275])svg+='<text x="'+x(n)+'" y="199" text-anchor="middle" font-size="11" fill="#526259">'+n+'</text>';
   for(const [key,color,dash]of [['zero','#225b96',''],['response','#b76627','5 3']]){
    svg+='<polyline fill="none" stroke="'+color+'" stroke-width="2.5" stroke-dasharray="'+dash+'" points="'+rows.map(r=>x(r.iteration)+','+y(r[key].success_rate)).join(' ')+'"/>';
    svg+='<circle cx="'+x(selected.iteration)+'" cy="'+y(selected[key].success_rate)+'" r="'+(key==='zero'?7:4)+'" fill="'+(key==='zero'?'white':color)+'" stroke="'+color+'" stroke-width="2"/>';
   }
   byId('trainingCurve').innerHTML=svg+'<text x="266" y="220" text-anchor="middle" font-size="11" fill="#526259">已完成的训练轮数</text></svg>';
  }
  function renderResult(){
   const row=rows[Number(range.value)];byId('checkpointLabel').textContent='共同第 '+row.iteration+' 轮';
   for(const key of ['zero','response']){
    const r=row[key];byId(key+'Result').textContent=r.successes+'/'+r.episodes;
    byId(key+'Budget').textContent=r.actor_updates+' 次更新；'+r.recorded_transitions+' 条 replay';
   }
   const delta=row.response.successes-row.zero.successes;
   byId('checkpointInterpretation').textContent=delta===0?'这个保存点的成功数相同。不能据此证明两种方法等价。':'这个保存点相差 '+Math.abs(delta)+' 个成功回合。样本很少，不能据此判断方法胜负。';draw(row);
  }
  range.addEventListener('input',renderResult);renderResult();
  byId('checkpointTable').innerHTML=rows.map(r=>'<tr><td>'+r.iteration+'</td><td>'+r.zero.successes+'/8</td><td>'+r.response.successes+'/8</td><td>'+r.zero.actor_updates+' / '+r.response.actor_updates+'</td></tr>').join('');
  byId('downloadResults').addEventListener('click',()=>{
   const csv=['iteration,zero_successes,response_successes,episodes_each,zero_updates,response_updates',...rows.map(r=>[r.iteration,r.zero.successes,r.response.successes,8,r.zero.actor_updates,r.response.actor_updates].join(','))].join('\n');
   const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='zeva-common-checkpoints-2026-10-04.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
 }).catch(error=>{byId('checkpointInterpretation').textContent='数据暂未加载。请打开下方完整结果文件。';byId('checkpointSlider').disabled=true;byId('downloadResults').disabled=true;console.error(error);});
})();

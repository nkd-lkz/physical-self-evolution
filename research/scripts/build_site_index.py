"""Build the RLT website's document index; never read the separate survey domain.

Run after project notes change. Pages also rebuilds this at deployment, so a new
project Markdown document is discoverable without editing index.html.
"""
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import argparse
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/knowledge-index.json'

def read_json(name):
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())

def clean(text):
    text = re.sub(r'!\[[^]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^]]*)\]\([^)]*\)', r'\1', text)
    return re.sub(r'\s+', ' ', re.sub(r'[`*#>]', '', text)).strip()

def note_path(value):
    if not value:
        return None
    if value.startswith(('notes/', 'research/')):
        return value
    return parse_qs(urlparse(value).query).get('path', [None])[0]

def topics(text):
    text = text.lower()
    patterns = {
        '物理经验 / 接触': r'physic|物理|contact|接触|后果|consequence|force|触觉',
        '强化学习': r'\brl\b|rlt|强化学习|critic|actor|serl',
        '记忆 / 适应': r'memory|记忆|zeva|适应|adapt|历史|遗忘',
        'RSI / Harness': r'rsi|harness|自进化|self.evol|自改|rpent|agent',
        '世界模型': r'world model|世界模型|flare|wam|future|未来|预测',
        '动作 / 决策': r'action|动作|decision|决策|jev|候选',
        '基线 / 工程': r'baseline|基线|复现|工程|smoke|pico|vr|部署',
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]

def doc_kind(path):
    name = path.name.lower()
    if path.parts[0] == 'notes': return '论文笔记'
    if name.startswith('progress-') or name in ('experiment-log.md','robodojo-b300-log.md') or 'audit-2026-09-30' in name: return '实验进度'
    if 'literature' in path.parts or any(w in name for w in ['reading','frontier','source-intake','six-papers','perspective','talk-']): return '调研与观点'
    if any(w in name for w in ['experiment','implementation','ideas','plan','protocol','spec','roadmap','selection','implications']): return '科研方案'
    return '项目资料'

def build():
    ledger=read_json('literature-reading-ledger')
    cards={}
    # Later records intentionally take precedence (the existing publication convention).
    for source in ['frontier','frontier-additions','papers','latest-readings']:
        for row in read_json(source):
            key=row['id']; cards[key]={**cards.get(key,{}),**row}
    by_path={}
    for row in ledger['papers']:
        path=note_path(row.get('note_path'))
        if path: by_path[path]=dict(row)
    for row in cards.values():
        path=note_path(row.get('note'))
        if path: by_path[path]={**by_path.get(path,{}),**row}
    docs=[]
    for folder in ('notes','research'):
        for file in sorted((ROOT/folder).rglob('*.md')):
            path=file.relative_to(ROOT); rel=path.as_posix(); raw=file.read_text()
            title_match=re.search(r'^#\s+(.+)',raw,re.M)
            title=clean(title_match.group(1)) if title_match else file.stem
            row=by_path.get(rel,{})
            paragraphs=[clean(p) for p in re.split(r'\n\s*\n',raw) if p.strip() and not p.lstrip().startswith(('#','|','```','![','<!--'))]
            summary=row.get('one') or row.get('summary') or row.get('method_note') or next((p for p in paragraphs if len(p)>25),'项目记录，打开查看详细内容。')
            git_date=subprocess.run(['git','log','-1','--format=%cs','--',rel],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
            dates=re.findall(r'20\d{2}-\d{2}-\d{2}',file.stem)
            date=max(dates+[git_date]) if dates or git_date else ''
            search=title+' '+summary+' '+' '.join(re.findall(r'^#{2,4}\s+(.+)',raw,re.M))+' '+row.get('project','')
            docs.append({'id':'doc:'+rel,'title':title,'path':rel,'kind':doc_kind(path),'date':date,'summary':summary[:280],
                'topics':topics(title+' '+summary+' '+row.get('layer','')+' '+str(row.get('tags',[]))),
                'status':row.get('status') or row.get('read_status') or '已有项目笔记',
                'source':row.get('url') or row.get('source_url') or '', 'search':search[:3000]})
    used_paths={d['path'] for d in docs}
    used_sources={d['source'].rstrip('/') for d in docs if d['source']}
    def add_external(row,kind):
        path=note_path(row.get('note_path') or row.get('note'))
        source=row.get('source_url') or row.get('url') or ''
        if path in used_paths or (source and source.rstrip('/') in used_sources): return
        summary=row.get('method_note') or row.get('one') or row.get('summary') or ''
        title=row.get('title') or row.get('short_title')
        status=row.get('read_status') or row.get('status') or '待核验'
        if not source: return
        docs.append({'id':kind+':'+row['id'],'title':title,'path':None,'kind':kind,'date':'','summary':summary[:280],
            'topics':topics(title+' '+summary+' '+row.get('category','')+' '+row.get('layer','')),
            'status':status,'source':source,'search':' '.join([title,summary,row.get('project_note',''),row.get('borrow',''),row.get('boundary','')])})
        used_sources.add(source.rstrip('/'))
    for row in ledger['papers']: add_external(row,'阅读清单')
    for row in cards.values(): add_external(row,'前沿条目')
    docs.sort(key=lambda d:(d['date'],bool(d['path']),d['title']),reverse=True)
    progress=read_json('experiments')
    for item in progress:
        # Existing explicit links win; otherwise resolve the matching day's report.
        if item.get('path'): continue
        explicit=re.findall(r'research/[a-zA-Z0-9._/-]+\.md',item['summary'])
        paths=[p for p in explicit if (ROOT/p).is_file()]
        daily=sorted((ROOT/'research').glob('progress-'+item['date']+'*.md'))
        item['path']=paths[0] if paths else (daily[-1].relative_to(ROOT).as_posix() if daily else 'research/experiment-log.md')
        item['topics']=topics(item['title'])
    return {'as_of':read_json('current-status')['as_of'],'stats':{'project_documents':len(used_paths),'reading_ledger':len(ledger['papers']),
        'read_status_counts':ledger['status_counts'],'progress_entries':len(progress),'progress_days':len({p['date'] for p in progress})},'documents':docs,'progress':progress}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Fail if checked-in index is stale')
    args=parser.parse_args()
    payload=json.dumps(build(),ensure_ascii=False,indent=2)+'\n'
    if args.check:
        if not OUT.exists() or OUT.read_text()!=payload: raise SystemExit('Index is stale. Run python research/scripts/build_site_index.py')
    else: OUT.write_text(payload)
    print('Project knowledge index ready; separate survey domain excluded.')

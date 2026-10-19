"""Build the three-round explorer from saved, independently checked schedules."""
import argparse,csv,itertools,json,re
from pathlib import Path
from rank_explorer_players import rank_entry
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('four_round_fragment',type=Path)
parser.add_argument('output_fragment',type=Path)
args=parser.parse_args()
data={};manifest={}
for n in range(15,25):
 folder=Path(f'runs/v2_pilot_20261011/rounds3/n{n}' if n<19 else f'runs/three_round_explorer_20261017/n{n}/n{n}')
 path=folder/'schedule.csv';result=json.loads((folder/'result.json').read_text())
 rows=[list(map(int,row)) for row in csv.reader(path.open()) if row]
 G=max(row[1] for row in rows);rounds=[[None]*G for _ in range(3)]
 for rd,g,*ps in rows:
  assert rounds[rd-1][g-1] is None
  rounds[rd-1][g-1]=ps
 groups={p:[] for p in range(1,n+1)}
 for rd in rounds:
  assert sorted(sum(rd,[]))==list(range(1,n+1))
  triples=(4-n%4)%4
  assert [len(ps) for ps in rd]==[3]*triples+[4]*((n-3*triples)//4)
  for g,ps in enumerate(rd):
   for p in ps:groups[p].append(g)
 pairs=[tuple(sorted(pair)) for rd in rounds for ps in rd for pair in itertools.combinations(ps,2)]
 assert len(pairs)==len(set(pairs))
 fours=[sum(len(rounds[r][groups[p][r]])==4 for r in range(3)) for p in groups]
 assert max(fours)-min(fours)<=1
 grid=[]
 for ps in rounds[0]:
  row=[]
  for qs in rounds[1]:
   common=set(ps)&set(qs);assert len(common)<=1;row.append(next(iter(common),None))
  grid.append(row)
 assert sorted(p for row in grid for p in row if p)==list(range(1,n+1))
 for a,b in itertools.combinations(range(3),2):assert len({(v[a],v[b]) for v in groups.values()})==n
 spans=[len(set(gs)) for gs in groups.values()];score=min(spans),sum(spans)
 assert score==(result['minimum_spread'],result['total_spread'])
 assert result['status']=='OPTIMAL'
 data[n]={'rounds':rounds,'groups':groups,'grid':grid,'minimum':score[0],'total':score[1]}
 manifest[n]={'source':str(path),'minimum_spread':score[0],'total_spread':score[1],'status':result['status']}
 print(n,score)
for n in data:
 data[n],mapping=rank_entry(data[n])
 manifest[n]['old_to_new_player_numbers']=mapping
 manifest[n]['numbering']='descending distinct positions, then original player ID'
s=args.four_round_fragment.read_text()
s=re.sub(r'const data=.*?;\nconst np=', 'const data='+json.dumps(data,separators=(',',':'))+';\nconst np=',s,flags=re.S)
s=s.replace('all-golf-grids','three-golf-grids').replace('Four-round','Three-round').replace('Our four-round schedules','Our three-round schedules')
s=s.replace('width:calc(66.666667% - 7.333333px);margin:24px 0;', 'width:100%;max-width:320px;margin:24px auto;')
s=s.replace('width:calc(66.666667% - 7.333333px);align-items:end', 'width:100%;max-width:320px;margin:0 auto;align-items:end')
s=s.replace('width:calc(66.666667% - 7.333333px);padding-bottom:8px;align-items:start', 'width:100%;max-width:320px;margin:0 auto;padding-bottom:8px;align-items:start')
s=s.replace('<option value="3">Round 4 · partial B</option>','')
s=re.sub(r'<tr><th scope="row">4</th>.*?</tr>','',s)
s=re.sub(r'<section><h3>Partial B.*?</section>','',s)
s=re.sub(r'<section><h3>A \+ B.*?</section>','',s)
s=s.replace('grid-template-columns:repeat(3,minmax(0,1fr))','grid-template-columns:minmax(0,320px);justify-content:center')
s=s.replace('r<4','r<3').replace('state.round<=4','state.round<=3').replace('s.round<=4','s.round<=3')
s=s.replace("['rows','columns','partial A','partial B']", "['rows','columns','partial A']")
s=s.replace("[['ag-a',2,'A'],['ag-b',3,'B']]", "[['ag-a',2,'A']]")
s=s.replace("[['ag-a',2],['ag-b',3],['ag-pairs',4]]", "[['ag-a',2]]")
s=s.replace("kind===4?`${gs[2]+1}·${gs[3]+1}`:gs[kind]+1", "gs[kind]+1").replace('gs===null||kind===4?null:gs[kind]','gs===null?null:gs[kind]')
s=s.replace("kind===4?'group pair':roundTitle(kind)", "roundTitle(kind)")
s=s.replace("kind===4?`${gs[2]+1}, ${gs[3]+1}`:gs[kind]+1", "gs[kind]+1")
s=s.replace('(rd+1)%4','(rd+1)%3')
s=s.replace('width:calc(66.666667% - 7.333333px)}}', 'width:100%;max-width:320px;margin-left:auto;margin-right:auto}}')
args.output_fragment.write_text(s)
Path('solutions/three-round-explorer-sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('All ten optimal schedules independently validated; three-round fragment saved.')

"""Build the five-round fragment from the four-round explorer and audited witnesses."""
import argparse,csv,itertools,json,re
from pathlib import Path
from rank_explorer_players import rank_entry
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('four_round_fragment',type=Path)
parser.add_argument('output_fragment',type=Path)
args=parser.parse_args()
sources={15:'runs/v2_pilot_20261011/rounds5/n15/schedule.csv',16:'runs/n16_r5_ordering_20261011/schedule.csv',17:'runs/n17_r5_ordering_20261011/min4_integer_opt_case0/schedule.csv',18:'runs/n18_via20_ordering_20261011/family_optimal_schedule.csv',19:'runs/n19_via20_ordering_20261011/best_schedule.csv',23:'runs/n23_r5_min5_1200s_20261011/schedule.csv'}
for n in [20,21,22,24]:sources[n]=f'runs/n19_to24_r5_sweep_20261011/run_n{n}/n{n}/schedule.csv'
expected={15:(3,51),16:(2,51),17:(4,76),18:(4,72),19:(4,79),20:(5,100),21:(5,105),22:(5,110),23:(5,115),24:(5,120)}
data={};manifest={}
for n,path in sorted(sources.items()):
 rows=[list(map(int,row)) for row in csv.reader(open(path)) if row]
 G=max(row[1] for row in rows);rounds=[[None]*G for _ in range(5)]
 for rd,g,*ps in rows:
  assert rounds[rd-1][g-1] is None
  rounds[rd-1][g-1]=ps
 groups={p:[] for p in range(1,n+1)}
 for rd in rounds:
  assert sorted(sum(rd,[]))==list(range(1,n+1))
  assert [len(ps) for ps in rd]==[3]*((4-n%4)%4)+[4]*((n-3*((4-n%4)%4))//4)
  for g,ps in enumerate(rd):
   for p in ps:groups[p].append(g)
 pairs=[tuple(sorted(pair)) for rd in rounds for ps in rd for pair in itertools.combinations(ps,2)]
 assert len(pairs)==len(set(pairs))
 triples=[sum(len(rounds[r][groups[p][r]])==3 for r in range(5)) for p in groups]
 assert max(triples)-min(triples)<=1
 grid=[]
 for ps in rounds[0]:
  row=[]
  for qs in rounds[1]:
   common=set(ps)&set(qs);assert len(common)<=1;row.append(next(iter(common),None))
  grid.append(row)
 assert sorted(p for row in grid for p in row if p)==list(range(1,n+1))
 for a,b in itertools.combinations(range(5),2):assert len({(v[a],v[b]) for v in groups.values()})==n
 spans=[len(set(gs)) for gs in groups.values()];score=min(spans),sum(spans)
 assert score==expected[n],(n,score)
 data[n]={'rounds':rounds,'groups':groups,'grid':grid,'minimum':score[0],'total':score[1]}
 manifest[n]={'source':path,'minimum_spread':score[0],'total_spread':score[1]}
 print(n,score)
for n in data:
 data[n],mapping=rank_entry(data[n])
 manifest[n]['old_to_new_player_numbers']=mapping
 manifest[n]['numbering']='descending distinct positions, then original player ID'
s=args.four_round_fragment.read_text()
s=re.sub(r'const data=.*?;\nconst np=', 'const data='+json.dumps(data,separators=(',',':'))+';\nconst np=',s,flags=re.S)
s=s.replace('all-golf-grids','five-golf-grids').replace('Four-round','Five-round')
s=s.replace('Our four-round schedules','Our five-round schedules')
s=s.replace('<option value="3">Round 4 · partial B</option>','<option value="3">Round 4 · partial B</option><option value="4">Round 5 · partial C</option>')
row=re.search(r'<tr><th scope="row">4</th>.*?</tr>',s).group(0)
s=s.replace(row,row+'\n'+row.replace('>4</th>','>5</th>').replace('-3"','-4"').replace('Round 4','Round 5'))
s=s.replace('<section><h3>A + B · group pairs</h3><div id="ag-pairs" class="ag-mini"></div></section>','<section><h3>Partial C · round 5</h3><div id="ag-c" class="ag-mini"></div></section>')
s=s.replace('r<4','r<5').replace('state.round<=4','state.round<=5').replace('s.round<=4','s.round<=5')
s=s.replace("['rows','columns','partial A','partial B']", "['rows','columns','partial A','partial B','partial C']")
s=s.replace("[['ag-a',2,'A'],['ag-b',3,'B']]", "[['ag-a',2,'A'],['ag-b',3,'B'],['ag-c',4,'C']]")
s=s.replace("[['ag-a',2],['ag-b',3],['ag-pairs',4]]", "[['ag-a',2],['ag-b',3],['ag-c',4]]")
s=s.replace("kind===4?`${gs[2]+1}·${gs[3]+1}`:gs[kind]+1", "gs[kind]+1").replace('gs===null||kind===4?null:gs[kind]','gs===null?null:gs[kind]')
s=s.replace("kind===4?'group pair':roundTitle(kind)", "roundTitle(kind)")
s=s.replace("kind===4?`${gs[2]+1}, ${gs[3]+1}`:gs[kind]+1", "gs[kind]+1")
args.output_fragment.write_text(s)
Path('solutions/five-round-explorer-sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert 'ag-pairs' not in s
print('All ten schedules independently validated; five-round fragment saved.')

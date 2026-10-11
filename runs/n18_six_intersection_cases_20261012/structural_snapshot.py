"""Resumable mixed-size structural enumeration, with exact orbit exclusions."""
import hashlib,itertools,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from ordering_snapshot import optimize,save
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
sizes=[3,3,4,4,4]
orders=[a+b for a in itertools.permutations(range(2)) for b in itertools.permutations(range(2,5))]

def names(row):
 mapping={};next_name={3:0,4:2}
 for g in row:
  if g not in mapping:
   size=sizes[g];mapping[g]=next_name[size];next_name[size]+=1
 return tuple(mapping[g] for g in row)

def orbit(schedule):
 result=set()
 for a,b in itertools.permutations(range(5),2):
  columns={p:g for g,members in enumerate(schedule[b]) for p in members}
  for ro in orders:
   for co in orders:
    colmap={old:new for new,old in enumerate(co)}
    mapping={};index=0
    for old in ro:
     for p in sorted(schedule[a][old],key=lambda p:colmap[columns[p]]):
      mapping[p]=index;index+=1
    second=[None]*18
    for p in mapping:second[mapping[p]]=colmap[columns[p]]
    if tuple(second)!=names(second):continue
    remaining=[]
    for r in range(5):
     if r in (a,b):continue
     raw=[None]*18
     for g,members in enumerate(schedule[r]):
      for p in members:raw[mapping[p]]=g
     remaining.append(names(raw))
    result.add(tuple(second)+tuple(v for row in sorted(remaining) for v in row))
 assert result
 return sorted(result)

def lex_le(model,left,right,label):
 prefix=model.NewBoolVar(label+'_prefix0');model.Add(prefix==1)
 for p,(a,b) in enumerate(zip(left,right)):
  model.Add(a<=b).OnlyEnforceIf(prefix)
  equal=model.NewBoolVar(f'{label}_equal{p}')
  model.Add(a==b).OnlyEnforceIf(equal)
  model.Add(a!=b).OnlyEnforceIf(equal.Not())
  nxt=model.NewBoolVar(f'{label}_prefix{p+1}')
  model.Add(nxt<=prefix);model.Add(nxt<=equal);model.Add(nxt>=prefix+equal-1);prefix=nxt

def build(odd=True):
 model=cp_model.CpModel()
 slots=[[model.NewIntVar(0,4,f'g_{r}_{p}') for p in range(18)] for r in range(5)]
 membership={}
 for r in range(5):
  for g,size in enumerate(sizes):
   for p in range(18):
    member=model.NewBoolVar(f'in_{r}_{g}_{p}')
    model.Add(slots[r][p]==g).OnlyEnforceIf(member)
    model.Add(slots[r][p]!=g).OnlyEnforceIf(member.Not());membership[r,g,p]=member
   model.Add(sum(membership[r,g,p] for p in range(18))==size)
  if r:
   for p in range(18):
    for g in (1,3,4):
     model.Add(membership[r,g,p]<=sum(membership[r,g-1,q] for q in range(p)))
 start=0
 for g,size in enumerate(sizes):
  for p in range(start,start+size):model.Add(slots[0][p]==g)
  for p in range(start,start+size-1):model.Add(slots[1][p]<slots[1][p+1])
  start+=size
 for p in range(18):
  model.AddLinearConstraint(sum(membership[r,g,p] for r in range(5) for g in (0,1)),1,2)
 for r,s in itertools.combinations(range(5),2):
  codes=[]
  for p in range(18):
   code=model.NewIntVar(0,24,f'pair_{r}_{s}_{p}')
   model.Add(code==5*slots[r][p]+slots[s][p]);codes.append(code)
  model.AddAllDifferent(codes)
 lex_le(model,slots[2],slots[3],'round23')
 lex_le(model,slots[3],slots[4],'round34')
 if odd:
  edges={}
  for a,b in itertools.combinations(range(10),2):
   edge=model.NewBoolVar(f'edge_{a}_{b}')
   if a//2==b//2:model.Add(edge==1)
   else:
    common=[]
    for p in range(18):
     joint=model.NewBoolVar(f'common_{a}_{b}_{p}')
     model.Add(joint<=membership[a//2,a%2,p]);model.Add(joint<=membership[b//2,b%2,p])
     model.Add(joint>=membership[a//2,a%2,p]+membership[b//2,b%2,p]-1);common.append(joint)
    model.Add(edge==sum(common))
   edges[a,b]=edge
  arcs=[];used=[]
  for v in range(10):
   inactive=model.NewBoolVar(f'inactive_{v}')
   arcs.append((v,v,inactive));used.append(1-inactive)
  for (a,b),edge in edges.items():
   for tail,head in ((a,b),(b,a)):
    arc=model.NewBoolVar(f'arc_{tail}_{head}')
    model.Add(arc<=edge);arcs.append((tail,head,arc))
  model.AddCircuit(arcs)
  half=model.NewIntVar(1,4,'half_length');model.Add(sum(used)==2*half+1)
 assert not model.Validate(),model.Validate()
 return model,slots

def decode(assignment):
 first=[g for g,size in enumerate(sizes) for _ in range(size)]
 rows=[first]+[assignment[i:i+18] for i in range(0,72,18)]
 schedule=[[[p+1 for p in range(18) if row[p]==g] for g in range(5)] for row in rows]
 validate(schedule,18,5)
 return schedule

def bipartite(schedule):
 adjacency={v:set() for v in range(10)}
 for r in range(5):adjacency[2*r].add(2*r+1);adjacency[2*r+1].add(2*r)
 for p in range(1,19):
  triples=[2*r+g for r,row in enumerate(schedule) for g,members in enumerate(row[:2]) if p in members]
  if len(triples)==2:
   a,b=triples;adjacency[a].add(b);adjacency[b].add(a)
 colors={}
 for v in adjacency:
  if v in colors:continue
  colors[v]=0;queue=[v]
  while queue:
   a=queue.pop()
   for b in adjacency[a]:
    if b not in colors:colors[b]=1-colors[a];queue.append(b)
    elif colors[b]==colors[a]:return False
 return True


import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import main,module
from oracle import reference,windows

def measure(repo,tmp):
 w=module(repo,'windower');a=w.parse_args(['toy','--sample_gaps','no'])
 actual=[v.tolist() for v in w.initwindows([1,81,161,241,320],[80]*4,a)]
 control=w.snpdist([[0,80],[1,80],[2,80],[3,80]],80,a)
 mismatches=0
 # Every valid position, both sides of boundaries, sparse and dense tables.
 for n in [2,3,4,8]:
  for positions in [[p] for p in range(1,n*80+1)]+[list(range(1,n*80+1)),[]]:
   got=[v.tolist() for v in w.initwindows(positions,[80]*n,a)]
   mismatches+=got!=windows(positions,[80]*n,80)
 return {'windows':actual,'retained_sites':sum(v[0] for v in actual),'normal_histogram':control,'oracle_mismatches':mismatches}

def verify(before,after,expected):
 assert before['windows']!=expected['windows']
 assert after['windows']==expected['windows']
 assert after['retained_sites']==5 and after['oracle_mismatches']==0
 assert before['windows'][:2]==after['windows'][:2]
 assert before['normal_histogram']==after['normal_histogram']=={0:1,1:1,2:1,3:1}

if __name__=='__main__': main(Path(__file__).parent,measure,reference,verify)

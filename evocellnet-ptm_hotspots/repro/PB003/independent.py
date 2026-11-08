"""Independent stdlib permutation, five-site averages, sample SD, normal survival and Bonferroni."""
import json,pathlib,random,statistics,math
here=pathlib.Path(__file__).resolve().parent
a=json.load(open(here/'before.json'));b=json.load(open(here/'after.json'))
def calculate(n):
 rng=random.Random(0);background=[]
 for trial in range(n):
  columns=[]
  for protein in range(2):
   occupancy=[1,1,1,0,0,0,0,0,0];rng.shuffle(occupancy);columns.append(occupancy)
  background.append([sum(columns[p][j] for p in range(2) for j in range(c-2,c+3))/5 for c in range(2,7)])
 fg=[1.2,1.2,1.2,0.8,0.4];result=[]
 for j in range(5):
  data=[trial[j] for trial in background];mu=statistics.mean(data);sd=statistics.stdev(data)
  z=(fg[j]-mu)/sd if sd else 0
  raw=math.erfc(z/math.sqrt(2))/2 if fg[j]>mu else 1.0
  result.append((raw,min(1,5*raw)))
 return result
for key,n in [('iter2',2),('default100',100)]:
 oracle=calculate(n)
 for row,(p,adj) in zip(b[key],oracle):
  assert math.isclose(row['pvals'],p,rel_tol=1e-10,abs_tol=1e-15),(key,row,p)
  assert math.isclose(row['p_adjust'],adj,rel_tol=1e-10,abs_tol=1e-15)
 assert any(not math.isfinite(x['pvals']) or not math.isclose(x['pvals'],y['pvals'],rel_tol=1e-10) for x,y in zip(a[key],b[key]))
 print(key,'before p:',[r['pvals'] for r in a[key]])
 print(key,'correct=after p:',[r['pvals'] for r in b[key]])
assert all(math.isfinite(r['p_adjust']) for r in b['iter2'])
assert a['normal_empty_ptms']==b['normal_empty_ptms']
assert all(r['pvals']==1 and r['p_adjust']==1 for r in b['normal_empty_ptms'])
for suffix in ['-normal-empty.csv','-normal-dispersed.csv']:
 assert (here/('before.json'+suffix)).read_bytes()==(here/('after.json'+suffix)).read_bytes()
assert a['normal_dispersed_ptms']==b['normal_dispersed_ptms']
assert all(r['pvals']==1 and r['p_adjust']==1 for r in b['normal_dispersed_ptms'])
print('Independent seeded shuffles, sample SD, Gaussian survival and Bonferroni agree.')
print('Normal dispersed nonempty PTMs and empty PTMs, default 100 permutations: all output unchanged.')

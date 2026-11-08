"""Recompute the full requested-power null from recorded draws, without R/package code."""
import csv,pathlib,math
here=pathlib.Path(__file__).resolve().parent
def read(name):return {r['metric']:float(r['value']) for r in csv.DictReader(open(here/name),delimiter='\t')}
def enrichment(selected,power):
 weights={i:(7-i)**power for i in selected}
 total=sum(weights.values());scores=[]
 for cutoff in range(1,7):
  prefix=[i for i in selected if i<=cutoff]
  scores.append(sum(weights[i] for i in prefix)/total-(cutoff-len(prefix))/(6-len(selected)))
 return max(scores,key=abs)
a,b=read('before.tsv'),read('after.tsv')
draws=[list(map(int,line.split())) for line in open(here/'before.tsv.draws')]
assert open(here/'before.tsv.draws').read()==open(here/'after.tsv.draws').read()
observed=enrichment([1,4],2)
expected=sum(enrichment(s,2)>=observed for s in draws)/len(draws)
wrong_null=sum(enrichment(s,1)>=observed for s in draws)/len(draws)
assert math.isclose(observed,a['edge_ES']) and a['edge_ES']==b['edge_ES']
assert math.isclose(a['edge_p'],wrong_null)
assert not math.isclose(a['edge_p'],expected)
assert math.isclose(b['edge_p'],expected),(b,expected)
for key in ['normal_ES','normal_p']:assert a[key]==b[key]
normal_observed=enrichment([1,4],1)
normal_expected=sum(enrichment(s,1)>=normal_observed for s in draws)/len(draws)
assert math.isclose(b['normal_p'],normal_expected)
print(f'Requested power=2 observed ES={observed}; 1000 fixed draws')
print(f"p-value: before={a['edge_p']}, correct=after={b['edge_p']}; wrong p=1 null={wrong_null}")
print('Default p=1 ES and p-value unchanged; both independently recomputed.')

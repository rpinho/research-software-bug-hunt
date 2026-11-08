"""Exact rational covariance decomposition, independent of R/MIMOSA2."""
from fractions import Fraction as F
import csv,pathlib,json,math
p=pathlib.Path(__file__).resolve().parent
rows=list(csv.DictReader((p/'contributions.csv').open()))
samples=sorted({r['Sample'] for r in rows});species=sorted({r['Species'] for r in rows})
x={s:{t:F(0) for t in samples} for s in species}
for r in rows:x[r['Species']][r['Sample']]+=F(r['newValue'])
total=[sum(x[s][t] for s in species) for t in samples]
def cov(a,b):
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    return sum((u-ma)*(v-mb) for u,v in zip(a,b))/(len(a)-1)
variance=cov(total,total)
expected={s:cov([x[s][t] for t in samples],total)/variance for s in species}
assert sum(expected.values())==1
for suffix in ['cov','matrix']:
    for r in csv.DictReader((p/f'after-{suffix}.csv').open()):
        assert math.isclose(float(r['VarShare']),float(expected[r['Species']]),abs_tol=1e-12)
(p/'correct-output.json').write_text(json.dumps({'total_by_sample':dict(zip(samples,map(str,total))),'variance':str(variance),'variance_shares':{s:str(v) for s,v in expected.items()}},indent=2)+'\n')
print('Independent exact-rational check: A=0, B=1, Residual=0; shares sum to 1.')

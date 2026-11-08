"""Second independently written check: exact rational two-node inversion.
This script uses no matrix solver, NumPy, upstream code, or oracle.py.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, sys
case=Path(sys.argv[1]).resolve()
tokens=(case/'input.txt').read_text().split()
n,s=int(tokens[0]),int(tokens[1]);assert n==2
freq=[Q(x) for x in tokens[2:2+2*s]]
d=[Q(x) for x in tokens[2+2*s:4+2*s]]
assert d[0]>0 and d[1]>0
expected=[]
for k in range(s):
    root,child=freq[2*k:2*k+2]
    assert root==1 and 0<=child<=root
    # U=[[1,1],[0,1]]. Invert exactly. This is feasible and has
    # zero residual, the global lower bound of a sum of squares.
    m=[root-child,child]
    assert sum(m)==1 and min(m)>=0
    assert m[0]+m[1]==root and m[1]==child
    expected.extend(m)
for flag in (0,1):
    out=[Q(x) for x in (case/f'after-{flag}.txt').read_text().split()]
    assert abs(out[0])<=Q(1,1000000)
    assert max(abs(a-b) for a,b in zip(out[1:],expected))<Q(3,1000000)
    before=[Q(x) for x in (case/f'before-{flag}.txt').read_text().split()]
    assert before[0]>Q(1,1000000) or max(abs(a-b) for a,b in zip(before[1:],expected))>Q(1,1000)
result={'expected_cost':'0','expected_M_column_major':[str(x) for x in expected], 'reason':'Exact inverse U=[[1,1],[0,1]] is feasible in both modes and attains the nonnegative sum-of-squares lower bound zero. Positive D makes this solution unique.', 'independent_of':'oracle.py and all upstream numerical code'}
(case/'closed-form-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(case.name+': exact rational closed form agrees')

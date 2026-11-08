"""Independent likelihood and Pearson definitions; no masked-array arithmetic.

The nonnegative zero plateau gives p(center)=0 and positive other bins.
An observed count at p=0 makes the likelihood zero and -log(L)=+infinity.
Pearson's positive squared residual divided by zero is likewise +infinity.
When both observed and expected are zero, that bin contributes zero.
The other probabilities are four 0.16's and four 0.09's at this pin's grid.
"""
import json
import math
probabilities=[.16,.09,.16,.09,0.,.09,.16,.09,.16]

def costs(counts, probabilities):
    nll=0.; chi=0.
    for c,p in zip(counts,probabilities):
        if p==0:
            if c>0: return {'nll':'infinity','chi2':'infinity'}
            continue
        nll -= c*math.log(p)
        chi += (c-9*p)**2/(9*p)
    return {'nll':nll,'chi2':chi}
print(json.dumps({'positive_count_zero_probability': costs([1.]*9,probabilities),
                  'zero_count_zero_probability': costs([1.,1.,1.,1.,0.,1.,1.,1.,1.],probabilities),
                  'normal': costs([1.]*9,[1/9]*9)},indent=2))

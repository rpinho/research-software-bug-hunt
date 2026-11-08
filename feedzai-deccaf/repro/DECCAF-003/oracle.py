"""Independent definitions: standard-library exhaustive enumeration, no repo imports."""
from itertools import product
from fractions import Fraction

def assignment_minimum(case_ids, human_capacity, loss_by_case):
    feasible=[]
    for choices in product(('human','model#0'), repeat=len(case_ids)):
        if choices.count('human') != human_capacity:
            continue
        loss=sum(Fraction(str(loss_by_case[c][w])) for c,w in zip(case_ids,choices))
        feasible.append((loss,dict(zip(case_ids,choices))))
    best=min(x[0] for x in feasible)
    return [a for loss,a in feasible if loss==best], float(best)

def constrained_threshold(labels,scores,rate=Fraction(1,20)):
    # Enumerate all deterministic >= threshold classifiers; compare integer counts.
    negatives=labels.count(0)
    positives=labels.count(1)
    candidates=[float('inf')]+sorted(set(scores),reverse=True)
    permitted=[]
    for t in candidates:
        decisions=[int(s>=t) for s in scores]
        fp=sum(y==0 and p==1 for y,p in zip(labels,decisions))
        tp=sum(y==1 and p==1 for y,p in zip(labels,decisions))
        if fp*rate.denominator <= negatives*rate.numerator:
            permitted.append((tp,fp,t,decisions))
    tp,fp,t,decisions=max(permitted,key=lambda x:(x[0],-x[2]))
    return {'false_positives':fp,'true_positives':tp,'negatives':negatives,'positives':positives,'decisions':decisions,'threshold':t}

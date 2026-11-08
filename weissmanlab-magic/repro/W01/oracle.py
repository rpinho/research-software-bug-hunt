"""Integer membership in consecutive 1-based windows; no NumPy or MAGIC."""
from collections import Counter

def windows(positions,coverage,L):
 return [[sum((i*L+1 <= p <= (i+1)*L) for p in positions),c] for i,c in enumerate(coverage)]

def reference():
 return {'windows':windows([1,81,161,241,320],[80]*4,80),
         'histogram':dict(sorted(Counter(w[0] for w in windows([1,81,161,241,320],[80]*4,80)).items()))}

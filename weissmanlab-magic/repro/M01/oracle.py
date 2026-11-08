"""Independent density quadrature, rather than the implementation's survival differences."""
import math
from scipy.integrate import quad
CASES=[([0.],[2.]),([0.,1.],[1.,2.]),([0.,2.],[3.,3.])]

def mean_by_density(breaks,rates):
 total=0.
 for i,(start,rate) in enumerate(zip(breaks,rates)):
  stop=breaks[i+1] if i+1<len(breaks) else math.inf
  prior_hazard=sum(rates[j]*(breaks[j+1]-breaks[j]) for j in range(i))
  total+=quad(lambda t:t*rate*math.exp(-prior_hazard-rate*(t-start)),start,stop,epsabs=1e-12)[0]
 return total

def reference():
 return {'means':[mean_by_density(b,r) for b,r in CASES],
         'one_piece_definition':1/2,
         'two_piece_definition':1-math.exp(-1)/2}

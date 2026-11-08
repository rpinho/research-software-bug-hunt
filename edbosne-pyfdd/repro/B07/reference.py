"""Independent analytic curvature for nine bins with ten counts in every bin.

Expected bin count=t/9. Pearson chi2(t)=9*(10-t/9)^2/(t/9)
=(90-t)^2/t. At t=90, chi2''=2/90, so variance=(chi2''/2)^-1=90.
Changing optimizer coordinates t=scale*z cannot change physical std=sqrt(90).
"""
import json
import math
std=round(math.sqrt(90),6)
print(json.dumps({'parameter_scales':{'1':{'fitted_total':90.,'std':std},
                                     '10':{'fitted_total':90.,'std':std}},
                  'normal':{'chi2_at_80_counts':(90-80)**2/80}},indent=2))

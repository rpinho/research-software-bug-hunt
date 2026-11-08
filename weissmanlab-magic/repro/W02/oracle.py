"""Aggregate consecutive count-table rows without importing the package."""
from collections import Counter

def hist_rows(counts,scales):
 result=[]
 for _ in range(scales):
  if len(counts)<2: break
  result.append(', '.join(f'{k} {v}' for k,v in sorted(Counter(counts).items()))+'\n')
  counts=[sum(counts[i:i+2]) for i in range(0,len(counts)-1,2)]
 return ''.join(result)

def reference():
 return {'counts_text':hist_rows([1,2,3,4],2),
         'default_down_text':hist_rows([64]*4,2),
         'up_text':hist_rows([80]*4,2)}

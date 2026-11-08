"""Exact rational classic GSEA walk; no R or package implementation imported."""
from fractions import Fraction
import csv,pathlib,math
here=pathlib.Path(__file__).resolve().parent
def read(name):return {r['metric']:float(r['value']) for r in csv.DictReader(open(here/name),delimiter='\t')}
a,b=read('before.tsv'),read('after.tsv')
running=[];balance=Fraction(0)
for label in 'ABCDEF':
 balance+=Fraction(1,2) if label in 'AD' else -Fraction(1,4)
 running.append(balance)
expected=max(running,key=abs)
assert expected==Fraction(1,2)
assert not math.isclose(a['edge_ES'],float(expected))
assert math.isclose(b['edge_ES'],float(expected))
for i,x in enumerate(running,1):assert math.isclose(b[f'edge_RS_{i}'],float(x),abs_tol=1e-14)
for key in a:
 if key.startswith('normal_'):assert a[key]==b[key],(key,a[key],b[key])
assert math.isclose(b['normal_ES'],2/3)
print('Independent exact walk:',[str(x) for x in running])
print(f"Classic ES: before={a['edge_ES']}, correct=after={b['edge_ES']}")
print('Default p=1 normal ES and complete running sum unchanged.')

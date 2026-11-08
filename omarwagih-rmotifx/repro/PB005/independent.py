"""Binomial upper tails computed as exact rational products, independent of R and rmotifx."""
from fractions import Fraction
import csv,math,pathlib
here=pathlib.Path(__file__).resolve().parent
def read(name):return {r['case']:r for r in csv.DictReader(open(here/name),delimiter='\t')}
a,b=read('before.tsv'),read('after.tsv')
# For n=20 successes out of n=20 trials, Pr[X>=20] is p**20.
# Both noncentral positions are fixed successively; each has background p=1/20.
tail=Fraction(1,20)**20
expected=-2*math.log10(float(tail))
assert math.isclose(expected,52.04119982655925)
assert float(a['edge']['score'])>600
assert math.isclose(float(b['edge']['score']),expected,rel_tol=1e-13)
for row in [a['edge'],b['edge']]:
 assert row['motif']=='ASA' and int(row['fg.matches'])==20 and int(row['bg.matches'])==1
 assert int(row['bg.size'])==400 and float(row['fold.increase'])==400
assert a['normal']==b['normal']
normal_expected=-2*math.log10(float(Fraction(1,2)**20))
assert math.isclose(float(b['normal']['score']),normal_expected,rel_tol=1e-13)
assert a['legacy']==b['legacy']
print('Exact one-position tail: (1/20)**20 =',float(tail))
print(f"Default score before={a['edge']['score']}; correct=after={b['edge']['score']}")
print('The entire normal output (representable tail) and requested Perl compatibility output are unchanged.')

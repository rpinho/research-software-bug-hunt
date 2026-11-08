"""Independent interface-contract check; no funscoR or training code imported."""
import csv,pathlib
here=pathlib.Path(__file__).resolve().parent
def read(name):return {r['metric']:float(r['value']) for r in csv.DictReader(open(here/name),delimiter='\t')}
a,b=read('before.tsv'),read('after.tsv')
assert a['custom_ok']==0
assert "object 'param' not found" in (here/'before.txt').read_text()
expected={'custom_ok':1,'custom_repeats':1,'custom_trees':2,'normal_repeats':5,'normal_folds':3,'normal_trees':500}
for key,value in expected.items():assert b[key]==value,(key,b[key],value)
for key in a:
 if key.startswith('normal_'):assert a[key]==b[key]
assert (here/'before.tsv.normal.rds').read_bytes()==(here/'after.tsv.normal.rds').read_bytes()
print('Documented contract: supplied parameters determine the fit; custom run must not look up an undefined variable.')
print('Before: object param not found. After: requested 1 repetition, 3 folds, 2 trees each.')
print('Default normal fit: all 15 fitted ensembles and folds byte-identical, excluding runtime metadata.')

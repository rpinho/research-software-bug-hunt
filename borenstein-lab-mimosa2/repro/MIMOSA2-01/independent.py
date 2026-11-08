"""Direct weighted sums of signed network entries; no R/package-code imports."""
import csv,pathlib,math,json
p=pathlib.Path(__file__).resolve().parent
kos={r['KO']:float(r['S1']) for r in csv.DictReader((p/'kos.csv').open())}
network=list(csv.DictReader((p/'network.csv').open()))
expected=[]
for row in csv.DictReader((p/'after.csv').open()):
    rel=row['relAbund']=='TRUE'; rem=row['remove_rev']=='TRUE';norm=row['normalize']=='TRUE'
    contributions=[]
    for r in network:
        if rem and int(r['Reversible']):continue
        abundance=kos[r['KO']]
        if rel:abundance=1000*abundance/sum(kos.values())
        for side,coeff,sign in [('Reac','stoichReac',-1),('Prod','stoichProd',1)]:
            if r[side]!=row['compound']:continue
            weight=float(r[coeff])
            if norm:
                weight/=sum(float(s[coeff]) for s in network if s[side]==row['compound'] and (not rem or not int(s['Reversible'])))
            contributions.append(sign*abundance*weight)
    value=sum(contributions)
    assert math.isclose(float(row['CMP']),value,rel_tol=1e-12,abs_tol=1e-12),(row,value)
    expected.append({k:row[k] for k in ['compound','normalize','relAbund','remove_rev']}|{'CMP':value})
(p/'correct-output.json').write_text(json.dumps(expected,indent=2)+'\n')
print('Independent signed-sum check: all 16 output values agree for the eight option combinations.')

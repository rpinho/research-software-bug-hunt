"""Build expected node records from sets and CSVs, without R or igraph."""
import csv,pathlib,json
p=pathlib.Path(__file__).resolve().parent
edges=list(csv.DictReader((p/'edges.csv').open()))
nodes={r['feature']:r for r in csv.DictReader((p/'nodes.csv').open())}
expected_all={}
for coverage in ['partial','metabolites_complete','ECs_complete','both_complete']:
    measured={'E1','M1'}
    if coverage in ['ECs_complete','both_complete']:measured.add('E2')
    if coverage in ['metabolites_complete','both_complete']:measured.add('M2')
    expected={}
    for side,kind in [('from','EC'),('to','Metabolite')]:
        for name in {e[side] for e in edges}:
            observed=name in measured
            expected[name]={'pval':float(nodes[name]['pval']) if observed else None,'anchor':int(nodes[name]['anchor']) if observed else 3,'type':kind,'imputed':not observed}
    expected_all[coverage]=expected
    actual=list(csv.DictReader((p/f'after-{coverage}-vertices.csv').open()))
    for row in actual:
        got={'pval':None if row['pval']=='NA' else float(row['pval']),'anchor':int(row['anchor']),'type':row['type'],'imputed':row['imputed']=='TRUE'}
        assert got==expected[row['name']],(row,expected)
    assert len(actual)==len(expected)
    got_edges=list(csv.DictReader((p/f'after-{coverage}-edges.csv').open()))
    assert {frozenset(r.values()) for r in got_edges}=={frozenset(r.values()) for r in edges}
(p/'correct-output.json').write_text(json.dumps(expected_all,indent=2,sort_keys=True)+'\n')
print('Independent set-based check: all four coverage cases agree; 4 vertices, 2 input edges.')

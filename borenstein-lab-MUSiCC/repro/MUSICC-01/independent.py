"""Scalar reference for the documented generic correction, with no MUSiCC imports."""
import csv, math, statistics, pathlib, json, sys

def calculate(repo, input_path):
    base = pathlib.Path(repo) / 'musicc/data'
    with (base/'Gene_level_features_for_all_KOs_DATA_HMP_STOOL_CLASS_HMP_SAMP_134_KO_76.tab').open() as f:
        rows = list(csv.reader(f, delimiter='\t'))
    feature = {r[0]: [float(x) for x in r[1:]] for r in rows[1:]}
    columns = list(zip(*feature.values()))
    means = [statistics.mean(c) for c in columns]
    stdev = [statistics.pstdev(c) for c in columns]
    with (base/'Final_Betas_ALL_SAMPLES_DATA_HMP_STOOL_CLASS_HMP_SAMP_134_KO_76.tab').open() as f:
        models = list(csv.reader(f, delimiter='\t'))[1:]
    intercept = statistics.mean(float(r[1]) for r in models)
    beta = [statistics.mean(float(r[j]) for r in models) for j in range(2,len(models[0]))]
    correction = {g: intercept + sum(b*((v-m)/s if s else 0) for b,v,m,s in zip(beta,x,means,stdev)) for g,x in feature.items()}
    with pathlib.Path(input_path).open() as f:
        abundance = {r['KO']:float(r['s1']) for r in csv.DictReader(f,delimiter='\t')}
    markers = set((base/'uscg_76_kegg_min_2313.lst').read_text().split()) & abundance.keys()
    lo,hi = min(correction[g] for g in markers),max(correction[g] for g in markers)
    result = {g: a/min(hi,max(lo,correction[g])) if g in correction else a for g,a in abundance.items()}
    return dict(sorted(result.items()))

if __name__ == '__main__':
    print(json.dumps(calculate(sys.argv[1],sys.argv[2]),indent=2))

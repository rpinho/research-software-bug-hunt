import sys,pathlib,io,contextlib,json,importlib.util
import numpy as np,pandas as pd
from independent import calculate
root=pathlib.Path(__file__).resolve().parents[2]
repo=pathlib.Path(sys.argv[1]).resolve(); mode=sys.argv[2]; here=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checked_core',repo/'musicc/core.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def run(input_path,outfile,normalize=False):
    with contextlib.redirect_stdout(io.StringIO()):
        m.correct_and_normalize(dict(input_file=str(input_path),output_file=str(outfile),input_format='tab',output_format='tab',musicc_inter=normalize,musicc_intra='use_generic',compute_scores=False,verbose=False))
    return pd.read_csv(outfile,sep='\t',index_col=0).sort_index()

actual=run(here/'input.tsv',here/f'{mode}-integer.tsv')
float_input=here/'float-input.tsv';pd.read_csv(here/'input.tsv',sep='\t',index_col=0).astype(float).to_csv(float_input,sep='\t')
float_result=run(float_input,here/f'{mode}-float.tsv')
reference=calculate(repo,here/'input.tsv')
assert np.allclose(float_result['s1'],list(reference.values()),rtol=1e-12,atol=1e-12)
equal=np.allclose(actual['s1'],list(reference.values()),rtol=1e-12,atol=1e-12)
assert equal == (mode=='after')
# Check the shipped normal floating-point example remains unchanged by this patch.
normal=run(repo/'musicc/examples/simulated_ko_relative_abundance.tab',here/f'.{mode}-normal.tsv',True)
if mode=='before':np.save(here/'.normal-before.npy',normal.values)
else:assert np.array_equal(normal.values,np.load(here/'.normal-before.npy'),equal_nan=True)
(here/f'.{mode}-normal.tsv').unlink()
print(json.dumps({'mode':mode,'actual':actual['s1'].to_dict(),'independent_expected':reference,'integer_matches_reference':bool(equal),'float_matches_reference':True,'normal_input': 'saved unpatched output' if mode=='before' else 'bit-for-bit unchanged'},indent=2))

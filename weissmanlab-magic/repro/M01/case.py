import sys,math,warnings
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import main,module
from oracle import reference,CASES
warnings.filterwarnings('ignore',category=DeprecationWarning)

def measure(repo,tmp):
 m=module(repo,'magic');ds=[m.PiecewiseExponential(b,r) for b,r in CASES]
 normal=ds[1]
 return {'means':[float(d.mean()) for d in ds],
         'normal_pdf':normal.pdf([.25,.5,1.,2.]).tolist(),
         'normal_cdf':normal.cdf([.25,.5,1.,2.]).tolist(),
         'normal_laplace':[float(normal.lt(s)) for s in [0.,.5,1.,2.]],
         'block_fraction_at_zero':float(normal.blcdf(0)[0])}

def verify(before,after,expected):
 assert before['means'][0]==0
 for a,b in zip(after['means'],expected['means']): assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
 assert math.isclose(after['means'][0],expected['one_piece_definition'],rel_tol=1e-12)
 assert math.isclose(after['means'][1],expected['two_piece_definition'],rel_tol=1e-12)
 assert math.isclose(after['block_fraction_at_zero'],1.,rel_tol=1e-12)
 assert before['block_fraction_at_zero']>1
 for k in ['normal_pdf','normal_cdf','normal_laplace']: assert before[k]==after[k]

if __name__=='__main__': main(Path(__file__).parent,measure,reference,verify)

import sys,numpy as np
from types import SimpleNamespace
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import main,module,run_cli
from oracle import reference,read_distribution,transform

def format_params(params):
 return '\n'.join(' '.join(str(x) for x in component) for component in params)

def measure(repo,tmp):
 tmp.mkdir();m=module(repo,'magic')
 try:
  params=m.clean_parameters(SimpleNamespace(x=np.array([.5,1.,1.,.5])),SimpleNamespace(family='gammamix',zero=True))
  formatted=format_params(params);failure=None
 except Exception as e: formatted=None;failure=type(e).__name__+': '+str(e)
 normal=format_params(m.clean_parameters(SimpleNamespace(x=np.array([.4,1.,1.,.6,2.,3.])),SimpleNamespace(family='gammamix',zero=False)))
 # Deterministic synthetic transform of 1/2 at zero plus 1/2 exponential.
 # --LT start is the existing, documented way to test the output layer alone.
 data=tmp/'LT.txt';data.write_text('\n'.join(f'{s} {p} 0.01' for s,p in reference()['laplace_points'])+'\n')
 out=tmp/'zero'
 cli=run_cli(repo,'magic.py',[data,'--LT','start','--family','gammamix','--zero','--components','2','--iterations','0','--maxfun','300','--out',out])
 final=Path(str(out)+'_final.txt')
 return {'format_error':failure,'formatted':formatted,'cli_exit':cli['exit'],
         'cli_error':cli['stderr'].strip().splitlines()[-1:] if cli['stderr'] else [],
         'cli_final':final.read_text() if final.exists() else None,
         'normal_nozero_output':normal}

def verify(before,after,expected):
 assert 'not iterable' in before['format_error'] and before['cli_exit']!=0
 assert after['format_error'] is None and after['cli_exit']==0
 rows=read_distribution(after['formatted'])
 assert rows==[expected['gamma_row'],expected['zero_row']]
 fitted=read_distribution(after['cli_final'])
 # This is a serialization check, not an optimizer-accuracy claim.
 assert 0 < fitted[-1][0] < 1
 for s,p in expected['laplace_points']: assert abs(transform(rows,s)-p)<1e-14
 assert before['normal_nozero_output']==after['normal_nozero_output']

if __name__=='__main__': main(Path(__file__).parent,measure,reference,verify)

import sys,numpy as np
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import main,module,run_cli
from oracle import reference

def measure(repo,tmp):
 tmp.mkdir();out={}
 for form in ['windows','reverse_windows']:
  for mode in ['no','down','up']:
   data=tmp/(form+'_'+mode+'.txt')
   values=[1,2,3,4] if mode=='no' else [80]*4
   data.write_text(''.join((f'{v} 80\n' if form=='windows' else f'80 {v}\n') for v in values))
   prefix=data.with_suffix('')
   cli=run_cli(repo,'windower.py',[prefix,'--input_form',form,'--scales','2','--sample_gaps',mode,'--seed','7'])
   counts=Path(str(prefix)+'_counts.txt')
   out[form+'_'+mode]={'exit':cli['exit'],'error':cli['stderr'].strip().splitlines()[-1:] if cli['stderr'] else [],'counts':counts.read_text() if counts.exists() else None}
 w=module(repo,'windower');args=w.parse_args(['toy'])
 out['normal_sampled_histogram']={str(k):int(v) for k,v in w.snpdist([[0,80],[1,80],[5,80],[10,80]],80,args,np.random.RandomState(7)).items()}
 out['normal_merge']=[row.tolist() for row in w.merge([np.array([k,80]) for k in [1,2,3,4]],2)]
 return out

def verify(before,after,expected):
 for form in ['windows','reverse_windows']:
  for mode in ['no','down','up']:
   key=form+'_'+mode
   assert before[key]['exit']!=0 and 'prng' in before[key]['error'][0]
   assert after[key]['exit']==0
   ref={'no':'counts_text','down':'default_down_text','up':'up_text'}[mode]
   assert after[key]['counts']==expected[ref]
 for key in ['normal_sampled_histogram','normal_merge']: assert before[key]==after[key]

if __name__=='__main__': main(Path(__file__).parent,measure,reference,verify)

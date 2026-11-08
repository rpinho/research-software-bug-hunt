"""Local-only patch runner. Every candidate is applied to a fresh copy of the pin."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
PIN='87fd0923480d28399c5078ff4efd60c3205c22a0'
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',MKL_NUM_THREADS='1')
def module(repo,name):
 spec=importlib.util.spec_from_file_location(name+'_'+repo.name,repo/(name+'.py'))
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def run_cli(repo,script,args):
 p=subprocess.run([sys.executable,str(repo/script),*map(str,args)],text=True,capture_output=True,env=os.environ,timeout=60)
 return {'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def save(path,value):
 path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

def main(folder,measure,oracle,verify):
 import os
 repo=Path(os.environ['REPRO_SOURCE']); folder=Path(folder)
 before=measure(repo,folder/'before-work')
 subprocess.run(['git','-C',str(repo),'apply',os.environ['REPRO_PATCH']],check=True)
 after=measure(repo,folder/'after-work')
 expected=oracle()
 try: verify(before,after,expected)
 except BaseException:
  subprocess.run(['git','-C',str(repo),'apply','-R',os.environ['REPRO_PATCH']],check=True)
  raise
 # Return values only; CLI stderr may contain temporary paths.
 for name,result in [('before',before),('after',after),('correct',expected)]:
  if isinstance(result,dict): result={k:v for k,v in result.items() if k not in ['stdout','stderr']}
  print(name+': '+json.dumps(result,allow_nan=True))
 print('Numerical reference agrees.')

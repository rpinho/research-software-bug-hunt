#!/usr/bin/env python3
"""Reproduce PB004 on its pinned source, then apply only its patch."""
import argparse, os, pathlib, shutil, subprocess, sys, tarfile, tempfile, io
HERE=pathlib.Path(__file__).resolve().parent
REPO='evocellnet/funscoR'
PIN='1ed6c74f112fd381626295245da327453d70cbe2'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=pathlib.Path, help='existing checkout at the exact pin; otherwise clone from GitHub')
p.add_argument('--rscript', default='Rscript')
a=p.parse_args()
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', NUMEXPR_NUM_THREADS='1', QT_QPA_PLATFORM='offscreen', PYTHONDONTWRITEBYTECODE='1', GIT_LFS_SKIP_SMUDGE='1')
try: os.nice(max(0, 10-os.nice(0)))
except (AttributeError, OSError): pass
def run(cmd, **kw):
 return subprocess.run(list(map(str,cmd)),check=True,**kw)
with tempfile.TemporaryDirectory(prefix='PB004-') as tmp:
 tmp=pathlib.Path(tmp); src=tmp/'source'; case=tmp/'case'
 shutil.copytree(HERE,case,ignore=shutil.ignore_patterns('__pycache__'))
 if a.source:
  original=a.source.resolve()
  assert subprocess.check_output(['git','-C',str(original),'rev-parse','HEAD'],text=True).strip()==PIN, 'wrong source commit'
  src.mkdir()
  data=subprocess.check_output(['git','-C',str(original),'archive',PIN])
  with tarfile.open(fileobj=io.BytesIO(data)) as archive:
   for member in archive.getmembers():
    assert not member.name.startswith('/') and '..' not in pathlib.PurePosixPath(member.name).parts
   archive.extractall(src)
  run(['git','init','-q',src])
 else:
  run(['git','clone','--depth','1','https://github.com/'+REPO+'.git',src])
  if subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()!=PIN:
   run(['git','-C',src,'fetch','--depth','1','origin',PIN]); run(['git','-C',src,'checkout','--detach',PIN])
 patch=HERE.parents[1]/'patches'/'PB004.patch'
 run(['git','-C',src,'apply','--check',patch])
 os.environ['MPLCONFIGDIR']=str(tmp/'matplotlib')
 try:
  for mode in ['before','after']:
   if mode=='after': run(['git','-C',src,'apply',patch])
   lib=tmp/('lib-'+mode); lib.mkdir()
   run([a.rscript,'--vanilla','-e',f'install.packages({str(src)!r},repos=NULL,type="source",lib={str(lib)!r})'],stdout=subprocess.DEVNULL)
   with (case/(mode+'.txt')).open('w') as out: run([a.rscript,'--vanilla',case/'check.R',lib,case/(mode+'.tsv')],stdout=out)
  run([sys.executable,case/'independent.py'])
 except BaseException:
  if subprocess.run(['git','-C',str(src),'apply','--reverse','--check',str(patch)],capture_output=True).returncode==0:
   run(['git','-C',src,'apply','--reverse',patch])
  raise


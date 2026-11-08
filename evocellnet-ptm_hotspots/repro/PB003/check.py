"""Run the documented CLI on a tiny custom alignment; seed only fixes its randomness."""
import contextlib,csv,io,json,pathlib,random,runpy,sys,tempfile,warnings
repo=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);here=pathlib.Path(__file__).resolve().parent
warnings.filterwarnings('ignore',category=Warning)
def cli(iterations,empty=False,dispersed=False):
 with tempfile.TemporaryDirectory(dir=here) as tmp:
  tmp=pathlib.Path(tmp);ali=tmp/'alignments';ali.mkdir()
  (ali/'TINY.fasta').write_text('>toy1 ;1;9\nSSSSSSSSS\n>toy2 ;1;9\nSSSSSSSSS\n')
  ptms=tmp/'ptms.csv'
  ptms.write_text('' if empty else ''.join(f'{i},{protein},{position},S\n' for i,(protein,position) in enumerate((p,x) for p in ['toy1','toy2'] for x in ([2,8] if dispersed else [3,4,5]))))
  csv_out=tmp/'sites.csv'
  sys.argv=[str(repo/'ptm_hotspots.py'),'--dir',str(ali),'--ptmfile',str(ptms),'-o',str(csv_out),'--printSites']
  if iterations is not None:sys.argv+=['--iter',str(iterations)]
  random.seed(0)
  with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(repo/'ptm_hotspots.py'),run_name='__main__')
  if empty or dispersed:
   pathlib.Path(str(out)+('-normal-empty.csv' if empty else '-normal-dispersed.csv')).write_bytes(csv_out.read_bytes())
  result=[]
  for row in csv.DictReader(csv_out.open()):
   if row['protein']=='toy1':result.append({k:(int(row[k]) if k=='position_aln' else float(row[k] or 'nan') if k in ['foreground','pvals','p_adjust'] else row[k]) for k in ['position_aln','foreground','pvals','p_adjust','hotspot']})
  return result
result={'iter2':cli(2),'default100':cli(None),'normal_empty_ptms':cli(None,True),'normal_dispersed_ptms':cli(None,dispersed=True)}
out.write_text(json.dumps(result,indent=2,allow_nan=True)+'\n')
print(json.dumps(result,indent=2,allow_nan=True))

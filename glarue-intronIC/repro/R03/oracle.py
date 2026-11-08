"""Independent base-by-base reference: imports Python standard library only.

GFF uses inclusive 1-based coordinates; motif offsets use half-open ranges
relative to the first intronic base (5′) or first base after it (3′).
No intronIC, BioGL, numpy, pandas, or pyfastx implementation is reused.
"""
import json,sys
from pathlib import Path
comp=dict(zip('ACGTN','TGCAN'))
def oracle(fasta,gff):
 genome={}
 name=None
 for line in Path(fasta).read_text().splitlines():
  if line.startswith('>'):
   name=line[1:].split()[0];genome[name]=''
  elif name: genome[name]+=line.strip().upper()
 exons={}
 for line in Path(gff).read_text().splitlines():
  if not line or line.startswith('#'): continue
  chrom,_,kind,a,b,_,strand,_,attrs=line.split('\t')
  if kind!='exon': continue
  parent=dict(s.split('=',1) for s in attrs.split(';'))['Parent']
  exons.setdefault((chrom,strand,parent),[]).append((int(a),int(b)))
 rows=[]
 for (chrom,strand,parent),ranges in sorted(exons.items()):
  ranges.sort()
  for lo,hi in zip(ranges,ranges[1:]):
   first,last=lo[1]+1,hi[0]-1
   if strand=='+':
    genomic_indices=list(range(first,last+1)); step=1
   else:
    genomic_indices=list(range(last,first-1,-1));step=-1
   def base(pos):
    if not 1<=pos<=len(genome[chrom]): return None
    b=genome[chrom][pos-1]
    return b if strand=='+' else comp[b]
   body=''.join(base(p) for p in genomic_indices)
   # Enumerate motif positions separately rather than slicing whole strings.
   five=''.join(b for d in range(-3,9) if (b:=base(genomic_indices[0]+step*d)) is not None)
   three=''.join(b for d in range(-6,4) if (b:=base(genomic_indices[-1]+step*(d+1))) is not None)
   bp=''.join(body[k] for k in range(len(body)) if -55<=k-len(body)<-5)
   longest=run=0
   for b in bp:
    run=run+1 if b in 'ACGT' else 0
    longest=max(longest,run)
   omitted='AMBIGUOUS' if any(b not in 'ACGT' for b in five+three) or longest<7 else 'NONE'
   rows.append({'chrom':chrom,'body':body,'five':five,'three':three,'bp':bp,'bp_longest_valid_run':longest,'omitted':omitted})
 return rows
if __name__=='__main__': print(json.dumps(oracle(*sys.argv[1:]),indent=2))

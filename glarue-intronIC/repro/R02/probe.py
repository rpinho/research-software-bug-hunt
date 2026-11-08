"""Observe extraction/filter outputs; the reference implementation is oracle.py."""
import json,sys
from pathlib import Path
from intronIC.extraction.annotator import AnnotationHierarchyBuilder
from intronIC.extraction.intronator import IntronGenerator
from intronIC.extraction.sequences import SequenceExtractor
from intronIC.extraction.filters import IntronFilter
from intronIC.file_io.indexed_genome import IndexedGenomeReader
fa,gff=sys.argv[1:]
rows=[]
for mode in ['cached','indexed']:
 builder=AnnotationHierarchyBuilder(['exon'])
 genes=builder.build_from_file(gff)
 introns=list(IntronGenerator().generate_from_genes(genes,builder.feature_index))
 if mode=='cached':
  extractor=SequenceExtractor(fa)
 else:
  reader=IndexedGenomeReader(fa)
  extractor=SequenceExtractor.from_indexed_reader(fa,reader)
 items=list(extractor.extract_sequences(introns,flank_size=100))
 for i in IntronFilter(min_length=30,allow_noncanonical=True).filter_introns(items):
  rows.append({'mode':mode,'chrom':i.coordinates.chromosome,'body':i.sequences.seq,'five':i.sequences.five_seq,'three':i.sequences.three_seq,'bp':i.sequences.bp_region_seq,'omitted':i.metadata.omitted.name})
 if mode=='indexed': reader.close()
print(json.dumps(rows,indent=2))

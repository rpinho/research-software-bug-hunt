"""Exercise the documented convenience API, including generator exhaustion."""
import json,sys
from intronIC.extraction.annotator import AnnotationHierarchyBuilder
from intronIC.extraction.intronator import IntronGenerator
from intronIC.extraction.sequences import extract_sequences_for_introns
builder=AnnotationHierarchyBuilder(['exon'])
genes=builder.build_from_file(sys.argv[2])
introns=list(IntronGenerator().generate_from_genes(genes,builder.feature_index))
# Print each yielded body so the failure is visibly at normal completion.
for intron in extract_sequences_for_introns(introns,sys.argv[1]):
 print(json.dumps({'chrom':intron.coordinates.chromosome,'body':intron.sequences.seq}),flush=True)
print('EXTRACTION_COMPLETE',flush=True)

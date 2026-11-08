# GO::TermFinder 0.86

Reported to the authors, Nov 2026.

Reproduction inputs and outputs are described below. The supplied bundle contains no reproduction scripts.

Source: CPAN GO-TermFinder-0.86.tar.gz (SHA-256 8daad833bffa65e726684ab98cb175f7c7f97d4e468362a2936fe0cd42bf0ea3). Each bug has a patch in [patches/](patches/) against pristine 0.86; [patches/all-six.patch](patches/all-six.patch) applies them together. With all six applied the original 8,116 tests still pass.

Four change results (GTF-001, 004, 005, 009); two are minor (GTF-007, 010). Issues already fixed in the Princeton version are not included.

## GTF-001: Compound NOT qualifiers become positive annotations

- **Location:** `lib/GO/AnnotationProvider/AnnotationParser.pm:583`.
- **Wrong behavior:** skips only a field equal to `NOT`, retaining valid pipe-separated fields such as `NOT|contributes_to` and `NOT|involved_in`.
- **Repro:** Two negated annotations to GO:0000011 produce a positive enrichment result, p = 1/190 = 0.00526315789473685. Correct output contains no result for that term. The two genes also have positive annotations to a different term, so their background membership is unchanged.
- **Fix:** match `NOT` as a complete pipe-delimited token. Positive annotations and bare NOT controls retain their behavior. This is a modern-GAF compatibility defect; the release's documentation predates those formats.
- **Reason / independent check:** [GAF 2.1, column 4](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/#qualifier-column-4), [GAF 2.2, relation/negation](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/#relation-column-4). Python splits the field into tokens before constructing annotation sets. Both qualifier orders and GAF 2.2 negation were checked.
- **Effect:** negative biological evidence can become apparently significant positive enrichment. **Confidence: high.**

## GTF-004: Tied p-values have different FDR estimates at the same cutoff

- **Location:** `lib/GO/TermFinder.pm:1977–2012`.
- **Wrong behavior:** divides expected null discoveries by array rank `i+1`; a cutoff at a tied p-value includes every tied hypothesis, not just the first members of the tie.
- **Repro:** Two identical annotation sets yield p = 1/6. With 50 explicitly enumerated draws, average null discoveries = 0.5. Original FDRs: 0.5 and 0.25. Correct: 0.25 and 0.25. With the unchanged standard sampler and seed 17: original 0.44/0.22, corrected 0.22/0.22.
- **Fix:** use the last rank of the tie for both the FDR denominator and the reported expected false positives; scan tie endpoints once. Non-tied FDR control is unchanged.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf), package documentation `TermFinder.pm:473–480, 573–578`: count real hypotheses as good or better than the cutoff. Python recomputes all null p-values from each recorded draw, then counts all real hypotheses at the cutoff.
- **Effect:** reported FDR depends on GO-ID tie ordering and can be inflated for early members of a tie. **Confidence: high.** This package implements a simulation estimator, not BH; replacing it with BH would change the method.

## GTF-005: Duplicate background names/aliases bias simulation sampling

- **Location:** `lib/GO/TermFinder.pm:1774`.
- **Wrong behavior:** background counts resolve and de-duplicate gene IDs, but the simulation pool uses the raw supplied names. A gene listed by ID and alias occupies two sampling slots; nominal two-gene draws can collapse to one gene.
- **Repro:** Four biological genes, but raw population `[g1, alias1, g2, g3, g4]`, where alias1 = g1. Under exhaustive index-subset cycles, corrected p changes from 300/1000 = 0.300 to 333/1000 = 0.333; FDR changes from 0.300 to 0.340 for the prescribed 50 draws. Exact uniform-subset null probability is 2/C(4,2) = 1/3. The finite 50/1000-draw values are not claimed to equal the limiting probability.
- **Fix:** build the sampling pool using the same ID resolution and de-duplication used for background counts.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf): simulations sample gene sets from the background. Python independently enumerates subsets of four distinct genes. With the unchanged random sampler and seed 17, corrected p is 0.308 before and 0.329 after; the patched output exactly matches the canonical unique-ID population. Unique-background normal control is unchanged.
- **Effect:** simulation-corrected p-values and FDR can depend on redundant spellings in the background. This differs from the index-sampling algorithm bias fixed in 0.83. **Confidence: high.**

## GTF-007 (minor): Obsolete status depends on tag order

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:310, 320`.
- **Wrong behavior:** `namespace` resets validity to true, resurrecting a term whose earlier tag was `is_obsolete: true`.
- **Repro:** Original `nodeFromId('GO:0000011')` returns an obsolete node. Correct: absent; the live root and other term remain present.
- **Fix:** retain a separate obsolete flag until the next term stanza. Conventionally ordered obsolete terms continue to be excluded.
- **Reason / independent check:** [OBO 1.2, is_obsolete and serializer conventions](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html). Parser acceptance must not depend on suggested serializer tag order. Python collects all stanza tags before filtering obsolete terms.
- **Effect:** obsolete terms can enter the graph and enrichment analysis with valid alternative tag layouts. **Confidence: high.**

## GTF-009: Typedef stanzas terminate the entire ontology parse

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:285`.
- **Wrong behavior:** stops at the first `[Typedef]`, ignoring all later terms.
- **Repro:** Put a valid `part_of` definition before the terms. Original: all three queried nodes absent. Correct: all three present, with the same GO graph as when the definition is last.
- **Fix:** finish the preceding term and skip non-term stanza contents, then resume at the next term; do not stop parsing the file.
- **Reason / independent check:** [OBO 1.2, stanza conventions](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) actually recommends typedefs before terms. Python discovers term stanzas independently of typedef placement.
- **Effect:** a correctly formatted ontology can load as an empty or incomplete graph. **Confidence: high.**

## GTF-010 (minor): Cyclic ontology input causes uncontrolled recursion

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:616–630`.
- **Wrong behavior:** recursively extends paths without detecting revisited nodes.
- **Repro:** GO:0000011 is_a GO:0000012 and vice versa. Original warns of deep recursion and returns no result before the 0.5-second watchdog kills it. Patched: promptly exits nonzero with `Cycle in ontology involving ...`.
- **Fix:** reject a path that revisits its originating node or an existing ancestor.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf) requires a DAG; [OBO parser requirements](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) require graceful failure. A separate Python DFS detects the cycle directly from the edge list. The valid diamond-DAG output is byte-identical.
- **Effect:** malformed user ontologies can hang or exhaust resources instead of producing a useful rejection. This is an invalid-input robustness defect, not a wrong p-value on a valid GO DAG. **Confidence: high.**

## References

- [Boyle et al. (2004). GO::TermFinder: open source software for accessing Gene Ontology information and finding significantly enriched Gene Ontology terms associated with a list of genes.](https://doi.org/10.1093/bioinformatics/bth456)
- [GO::TermFinder 0.86 on CPAN](https://metacpan.org/release/SHERLOCK/GO-TermFinder-0.86).
- [GAF 2.1](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/) and [GAF 2.2](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/).
- [OBO format 1.2](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html).

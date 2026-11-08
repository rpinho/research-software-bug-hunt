# research-software-bug-hunt

![Research software bug hunt](assets/banner.png)

AI agents look for correctness bugs in open-source research software. A separate referee rebuilds each claim from scratch. Only bugs the referee confirms are listed here. Each bug was reported to the authors before it appears here.

| Project | Language | Pinned version or commit | Bugs confirmed | Minor | Status |
|---|---|---|---:|---:|---|
| [omarwagih/rmotifx](https://github.com/omarwagih/rmotifx) ([report](omarwagih-rmotifx/README.md)) | R | `f13775f07679b86df173ccc2a9112263a1a9052f` | 1 | 0 | reported to the authors, Nov 2026 |
| [evocellnet/funscoR](https://github.com/evocellnet/funscoR) ([report](evocellnet-funscoR/README.md)) | R | `1ed6c74f112fd381626295245da327453d70cbe2` | 1 | 0 | reported to the authors, Nov 2026 |
| [evocellnet/ksea](https://github.com/evocellnet/ksea) ([report](evocellnet-ksea/README.md)) | R | `126a64541a11df9d8dc16a00cd9ea3ab9f16147f` | 2 | 0 | reported to the authors, Nov 2026 |
| [evocellnet/ptm_hotspots](https://github.com/evocellnet/ptm_hotspots) ([report](evocellnet-ptm_hotspots/README.md)) | Python | `15b4b256f7f2945eebe72f622d68115d4bdd5e70` | 1 | 1 | reported to the authors, Nov 2026 |
| [bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model) ([report](bentoayr-Efficient-Projection-onto-the-Perfect-Phylogeny-Model/README.md)) | C | `769ccd389a559085df8fa628047eba2f2d850c15` | 2 | 0 | reported to the authors, Nov 2026 |
| [edbosne/pyfdd](https://github.com/edbosne/pyfdd) ([report](edbosne-pyfdd/README.md)) | Python | `6aba44c5c4aaed278e08691f28abe79c724cf1da` | 7 | 3 | reported to the authors, Nov 2026 |
| [borenstein-lab/MUSiCC](https://github.com/borenstein-lab/MUSiCC) ([report](borenstein-lab-MUSiCC/README.md)) | Python | `478c9244cf406935e67abdf7622bdb05421ab1fb` | 1 | 0 | reported to the authors, Nov 2026 |
| [borenstein-lab/mimosa2](https://github.com/borenstein-lab/mimosa2) ([report](borenstein-lab-mimosa2/README.md)) | R | `581b307dee48577117ac42599a07b33a51b0822d` | 2 | 1 | reported to the authors, Nov 2026 |
| [borenstein-lab/MAAMOUL](https://github.com/borenstein-lab/MAAMOUL) ([report](borenstein-lab-MAAMOUL/README.md)) | R | `54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9` | 1 | 0 | reported to the authors, Nov 2026 |
| [glarue/intronIC](https://github.com/glarue/intronIC) ([report](glarue-intronIC/README.md)) | Python | `0db1d54274f1ffdbbc95dea6589a75a833eb831d` | 5 | 1 | reported to the authors, Nov 2026 |
| [feedzai/deccaf](https://github.com/feedzai/deccaf) ([report](feedzai-deccaf/README.md)) | Python | `b910b48d7e146d53b5f145224b819bdb0962d40a` | 3 | 2 | reported to the authors, Nov 2026 |
| [weissmanlab/magic](https://github.com/weissmanlab/magic) ([report](weissmanlab-magic/README.md)) | Python | `87fd0923480d28399c5078ff4efd60c3205c22a0` | 4 | 0 | reported to the authors, Nov 2026 |
| [GO::TermFinder](https://metacpan.org/release/SHERLOCK/GO-TermFinder-0.86) ([report](cpan-GO-TermFinder/README.md)) | Perl | `0.86` | 6 | 2 | reported to the authors, Nov 2026 |
| [glm-tools/pyglmnet](https://github.com/glm-tools/pyglmnet) ([report](glm-tools-pyglmnet/README.md)) | Python | `9339c5c71c908ec31cf4bebda5d9fe47dfed4f1c` | 3 | 0 | [#399](https://github.com/glm-tools/pyglmnet/pull/399), [#400](https://github.com/glm-tools/pyglmnet/pull/400), [#401](https://github.com/glm-tools/pyglmnet/pull/401) |

Minor defects are included in the confirmed counts. Reports preserve the limits of each finding; they do not establish changes to published scientific results.

## How a bug gets in

The full rules, and the numbers so far, are in [METHOD.md](METHOD.md).

1. Hunt for a correctness bug in a pinned upstream version.
2. An independent referee rebuilds the claim from scratch.
3. Prepare a patch and a small before/after example.
4. Check normal inputs and record the limits of the fix.

## References

- omarwagih/rmotifx: [Wagih et al. (2016). Uncovering phosphorylation-based specificities through functional interaction networks.](https://doi.org/10.1074/mcp.M115.052357)
- evocellnet/funscoR: [Ochoa et al. (2020). The functional landscape of the human phosphoproteome.](https://doi.org/10.1038/s41587-019-0344-3)
- evocellnet/ksea: [Ochoa et al. (2016). An atlas of human kinase regulation.](https://doi.org/10.15252/msb.20167295)
- evocellnet/ptm_hotspots: [Strumillo et al. (2018). Conserved phosphorylation hotspots in eukaryotic protein domain families (preprint).](https://doi.org/10.1101/391185)
- bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model: [Jia et al. (2018). Efficient Projection onto the Perfect Phylogeny Model.](https://doi.org/10.48550/arXiv.1811.01129)
- edbosne/pyfdd: [David-Bosne et al. (2024). Electron Emission Channeling for lattice location of radioactive isotopes in single crystals: Improvements from a Timepix3 quad detector and new PyFDD data analysis software.](https://doi.org/10.1016/j.nima.2023.169016)
- borenstein-lab/MUSiCC: [Manor and Borenstein (2015). MUSiCC: a marker genes based framework for metagenomic normalization and accurate profiling of gene abundances in the microbiome.](https://doi.org/10.1186/s13059-015-0610-8)
- borenstein-lab/mimosa2: [Noecker et al. (2022). MIMOSA2: a metabolic network-based tool for inferring mechanism-supported relationships in microbiome-metabolome data.](https://doi.org/10.1093/bioinformatics/btac003)
- borenstein-lab/MAAMOUL: [Muller, Baum and Borenstein (2026). MAAMOUL: metabolic network-based discovery of microbiome-metabolome shifts in disease.](https://doi.org/10.1093/bioinformatics/btag467)
- glarue/intronIC: [Moyer et al. (2020). Comprehensive database and evolutionary dynamics of U12-type introns.](https://doi.org/10.1093/nar/gkaa464)
- feedzai/deccaf: [Alves et al. (2024). Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints.](https://doi.org/10.48550/arXiv.2403.06906)
- weissmanlab/magic: [Weissman and Hallatschek (2017). Minimal-assumption inference from population-genomic data.](https://doi.org/10.7554/eLife.24836)
- GO::TermFinder: [Boyle et al. (2004). GO::TermFinder: open source software for accessing Gene Ontology information and finding significantly enriched Gene Ontology terms associated with a list of genes.](https://doi.org/10.1093/bioinformatics/bth456)
- pyglmnet: [Jas et al. (2020). Pyglmnet: Python implementation of elastic-net regularized generalized linear models.](https://doi.org/10.21105/joss.01959)

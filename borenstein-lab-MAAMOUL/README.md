# borenstein-lab/MAAMOUL

Pinned commit: [`54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9`](https://github.com/borenstein-lab/MAAMOUL/tree/54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9).

1 confirmed defect, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### MAAMOUL-01 : Complete coverage crashes initialization

[borenstein-lab/MAAMOUL · R/utils.R:102](https://github.com/borenstein-lab/MAAMOUL/blob/54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9/R/utils.R#L102). Two EC nodes and two metabolite nodes, two edges, complete coverage of either type: **row-count error → 4 vertices, 2 edges**; complete-both has zero imputed nodes. Scalar attributes cannot form a zero-row data.frame, blocking valid custom networks. Correct: impute only absent nodes under the [constructor contract](https://github.com/borenstein-lab/MAAMOUL/blob/54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9/R/utils.R#L83); partial coverage is unchanged. [Repro](repro/MAAMOUL-01/run.sh), [patch](patches/MAAMOUL-01.patch).

## References

- [Muller, Baum and Borenstein (2026). MAAMOUL: metabolic network-based discovery of microbiome-metabolome shifts in disease.](https://doi.org/10.1093/bioinformatics/btag467)
- [Upstream source at the reported commit](https://github.com/borenstein-lab/MAAMOUL/tree/54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9).

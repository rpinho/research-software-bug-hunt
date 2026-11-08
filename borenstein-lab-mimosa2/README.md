# borenstein-lab/mimosa2

Pinned commit: [`581b307dee48577117ac42599a07b33a51b0822d`](https://github.com/borenstein-lab/mimosa2/tree/581b307dee48577117ac42599a07b33a51b0822d).

2 confirmed defects, including 1 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### MIMOSA2-01 : KO dispatch drops options

[borenstein-lab/mimosa2 · R/core_mimosa2_funcs.R:1389](https://github.com/borenstein-lab/mimosa2/blob/581b307dee48577117ac42599a07b33a51b0822d/R/core_mimosa2_funcs.R#L1389). KO abundances 2 and 3, A→B reactions, `normalize=FALSE, relAbund=FALSE, remove_rev=FALSE`: CMP **(−400,400) → (−5,5)**. Dispatch ignores the last two flags, changing units and included reactions. Correct: forward them to the [documented callee](https://github.com/borenstein-lab/mimosa2/blob/581b307dee48577117ac42599a07b33a51b0822d/R/core_mimosa2_funcs.R#L1636); defaults are unchanged. [Repro](repro/MIMOSA2-01/run.sh), [patch](patches/MIMOSA2-01.patch).

```diff
-    spec_cmps = get_cmp_scores_kos(species_table, network, normalize = normalize, leave_rxns = leave_rxns)
+    spec_cmps = get_cmp_scores_kos(species_table, network, normalize = normalize, relAbund = relAbund, remove_rev = remove_rev, leave_rxns = leave_rxns)
```
### MIMOSA2-02 : Sparse-zero covariance shares : minor

[borenstein-lab/mimosa2 · R/core_mimosa2_funcs.R:485](https://github.com/borenstein-lab/mimosa2/blob/581b307dee48577117ac42599a07b33a51b0822d/R/core_mimosa2_funcs.R#L485). A=(1,2,3), B=(3,0,1), zero residuals, omit B’s zero row: shares **(A=0,B=0,R=0) → (0,1,0)**. Shortcut uses unequal sample sets, hiding a contributor. Correct: `Cov(B,total)/Var(total)=1` after zero-filling, matching the [default matrix path](https://github.com/borenstein-lab/mimosa2/blob/581b307dee48577117ac42599a07b33a51b0822d/R/core_mimosa2_funcs.R#L485). Only known-zero omissions qualify; sparse semantics are undocumented and normal tables are dense. [Repro](repro/MIMOSA2-02/run.sh), [patch](patches/MIMOSA2-02.patch).

## References

- [Noecker et al. (2022). MIMOSA2: a metabolic network-based tool for inferring mechanism-supported relationships in microbiome-metabolome data.](https://doi.org/10.1093/bioinformatics/btac003)
- [Upstream source at the reported commit](https://github.com/borenstein-lab/mimosa2/tree/581b307dee48577117ac42599a07b33a51b0822d).

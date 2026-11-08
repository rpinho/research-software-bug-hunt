# evocellnet/ptm_hotspots

Pinned commit: [`15b4b256f7f2945eebe72f622d68115d4bdd5e70`](https://github.com/evocellnet/ptm_hotspots/tree/15b4b256f7f2945eebe72f622d68115d4bdd5e70).

1 confirmed defect, including 1 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### PB003 : Last permutation omitted : minor

[evocellnet/ptm_hotspots · ptm_hotspots.py:203](https://github.com/evocellnet/ptm_hotspots/blob/15b4b256f7f2945eebe72f622d68115d4bdd5e70/ptm_hotspots.py#L203). Two nine-character strings, labels 3/4/5, seed 0: default raw p at the first reported position **0.005796981 → 0.005557604**. Three slices use 99/100 draws; two-draw runs give missing values. Correct: summarize all requested permutations ([CLI contract](https://github.com/evocellnet/ptm_hotspots/blob/15b4b256f7f2945eebe72f622d68115d4bdd5e70/README.md)); user p-values change, with no default classification change demonstrated. [Repro](repro/PB003/run.sh), [patch](patches/PB003.patch).

## References

- [Strumillo et al. (2018). Conserved phosphorylation hotspots in eukaryotic protein domain families (preprint).](https://doi.org/10.1101/391185)
- [Upstream source at the reported commit](https://github.com/evocellnet/ptm_hotspots/tree/15b4b256f7f2945eebe72f622d68115d4bdd5e70).

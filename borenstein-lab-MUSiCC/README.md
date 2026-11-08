# borenstein-lab/MUSiCC

Pinned commit: [`478c9244cf406935e67abdf7622bdb05421ab1fb`](https://github.com/borenstein-lab/MUSiCC/tree/478c9244cf406935e67abdf7622bdb05421ab1fb).

1 confirmed defect, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### MUSICC-01 : Integer correction truncates abundances

[borenstein-lab/MUSiCC · musicc/core.py:177](https://github.com/borenstein-lab/MUSiCC/blob/478c9244cf406935e67abdf7622bdb05421ab1fb/musicc/core.py#L177). Integer input K01866=1, K00001=1, K01867=2: corrected abundances **[0,1,2] → [0.9914541785,1.0066761508,2.0133523016]**. Assignment into integer storage truncates correction, potentially zeroing positive genes. Correct: retain real-valued division by the [generic bias factor](https://github.com/borenstein-lab/MUSiCC/blob/478c9244cf406935e67abdf7622bdb05421ab1fb/musicc/core.py#L372); decimal encoding of identical input already agrees. [Repro](repro/MUSICC-01/run.sh), [patch](patches/MUSICC-01.patch).

```diff
-    abun = ko_abun_data.values
+    abun = ko_abun_data.values.astype(np.float64)
```

## References

- [Manor and Borenstein (2015). MUSiCC: a marker genes based framework for metagenomic normalization and accurate profiling of gene abundances in the microbiome.](https://doi.org/10.1186/s13059-015-0610-8)
- [Upstream source at the reported commit](https://github.com/borenstein-lab/MUSiCC/tree/478c9244cf406935e67abdf7622bdb05421ab1fb).

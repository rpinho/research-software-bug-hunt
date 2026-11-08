# evocellnet/ksea

Pinned commit: [`126a64541a11df9d8dc16a00cd9ea3ab9f16147f`](https://github.com/evocellnet/ksea/tree/126a64541a11df9d8dc16a00cd9ea3ab9f16147f).

2 confirmed defects, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### PB002 : Null distribution ignores power

[evocellnet/ksea · R/ksea.R:120](https://github.com/evocellnet/ksea/blob/126a64541a11df9d8dc16a00cd9ea3ab9f16147f/R/ksea.R#L120). Ranks A–F, values 6–1, signature A/D, `p=2`, seed 3, 1,000 matched draws: empirical significance **0.154 → 0.277**, observed ES 0.8 unchanged. Null scores use default `p=1`, distorting non-default inference. Correct: apply the same weighted statistic to observed and permuted sets ([definition](https://github.com/evocellnet/ksea/blob/126a64541a11df9d8dc16a00cd9ea3ab9f16147f/man/ksea.Rd)). [Repro](repro/PB002/run.sh), [patch](patches/PB002.patch).
### PB001 : Classic enrichment counts nonmembers

[evocellnet/ksea · R/ksea.R:56](https://github.com/evocellnet/ksea/blob/126a64541a11df9d8dc16a00cd9ea3ab9f16147f/R/ksea.R#L56). Ranks A–F, values 6–1, signature A/D, `p=0`: ES **1/6 → 1/2**. `0^0` counts misses as hits, corrupting classic enrichment. Correct: the walk adds 1/2 only at members and subtracts 1/4 at misses ([running-sum definition](https://github.com/evocellnet/ksea/blob/126a64541a11df9d8dc16a00cd9ea3ab9f16147f/R/ksea.R#L53)). Classic significance also needs PB002. [Repro](repro/PB001/run.sh), [patch](patches/PB001.patch).

```diff
-  hitCases <- cumsum(abs(R) ^ p)
+  hitCases <- cumsum((abs(norm_express) ^ p) * HITS)
```

## References

- [Ochoa et al. (2016). An atlas of human kinase regulation.](https://doi.org/10.15252/msb.20167295)
- [Upstream source at the reported commit](https://github.com/evocellnet/ksea/tree/126a64541a11df9d8dc16a00cd9ea3ab9f16147f).

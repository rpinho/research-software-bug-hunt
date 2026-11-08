# evocellnet/funscoR

Pinned commit: [`1ed6c74f112fd381626295245da327453d70cbe2`](https://github.com/evocellnet/funscoR/tree/1ed6c74f112fd381626295245da327453d70cbe2).

1 confirmed defect, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### PB004 : Custom parameters crash

[evocellnet/funscoR · R/predict_score.R:58](https://github.com/evocellnet/funscoR/blob/1ed6c74f112fd381626295245da327453d70cbe2/R/predict_score.R#L58). 120 synthetic rows, one repetition, three folds and two trees: **undefined `param` → 3 fitted two-tree models**. Non-NULL `parameters` never initializes `param`, blocking customization. Correct: the supplied settings must be used ([documented interface](https://github.com/evocellnet/funscoR/blob/1ed6c74f112fd381626295245da327453d70cbe2/man/train_funscore.Rd)). [Repro](repro/PB004/run.sh), [patch](patches/PB004.patch).

```diff
+    param <- parameters
```

## References

- [Ochoa et al. (2020). The functional landscape of the human phosphoproteome.](https://doi.org/10.1038/s41587-019-0344-3)
- [Upstream source at the reported commit](https://github.com/evocellnet/funscoR/tree/1ed6c74f112fd381626295245da327453d70cbe2).

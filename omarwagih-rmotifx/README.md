# omarwagih/rmotifx

Pinned commit: [`f13775f07679b86df173ccc2a9112263a1a9052f`](https://github.com/omarwagih/rmotifx/tree/f13775f07679b86df173ccc2a9112263a1a9052f).

1 confirmed defect, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### PB005 : Upper-tail cancellation

[omarwagih/rmotifx · R/motifx-functions.R:96](https://github.com/omarwagih/rmotifx/blob/f13775f07679b86df173ccc2a9112263a1a9052f/R/motifx-functions.R#L96). Twenty `ASA` strings against the 400 strings `aSb` over 20 letters: default score **615.305311 → 52.041200**. Subtraction rounds representable binomial tails to zero, inflating reported motif scores. Correct: two tails `(1/20)^20`, summed as −log10 probabilities ([score definition](https://github.com/omarwagih/rmotifx/blob/f13775f07679b86df173ccc2a9112263a1a9052f/man/motifx.Rd)). Explicit Perl compatibility is preserved. [Repro](repro/PB005/run.sh), [patch](patches/PB005.patch).

## References

- [Wagih et al. (2016). Uncovering phosphorylation-based specificities through functional interaction networks.](https://doi.org/10.1074/mcp.M115.052357)
- [Upstream source at the reported commit](https://github.com/omarwagih/rmotifx/tree/f13775f07679b86df173ccc2a9112263a1a9052f).

# bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model

Pinned commit: [`769ccd389a559085df8fa628047eba2f2d850c15`](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/tree/769ccd389a559085df8fa628047eba2f2d850c15).

2 confirmed defects, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### BENTO-001 : Column-major input misread

[bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model · project_onto_PPM.c:970](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/blob/769ccd389a559085df8fa628047eba2f2d850c15/project_onto_PPM.c#L970). Two-node tree, frequency columns `(1,¼),(1,¾)`, unit weights: equality cost **0.562501 → 0**; fractions become `(¾,¼),(¼,¾)` within 3e−6. Documented column-major tokens are treated as row-major, changing fractions and tree costs. Correct: these feasible fractions give `UM=F` and zero squared residual ([objective](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/blob/769ccd389a559085df8fa628047eba2f2d850c15/test_against_CVX_matlab.m)). Patch also updates the writer and example. Existing row-major multi-sample files need reserialization; MATLAB execution was unavailable. [Repro](repro/BENTO-001/run.sh), [patch](patches/BENTO-001.patch).
### BENTO-002 : Absolute jitter breaks small weights

[bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model · project_onto_PPM.c:917](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/blob/769ccd389a559085df8fa628047eba2f2d850c15/project_onto_PPM.c#L917). Two-node tree, one column `(1,¼)`, both weights 0.0001: inequality fraction **−49.374222 → 0.250000** for the child; cost **0.000049 → 0**. Jitter added after `D²F` scaling can overwhelm data, yielding invalid fractions. Correct: `(¾,¼)` attains zero residual under the [weighted objective](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/blob/769ccd389a559085df8fa628047eba2f2d850c15/test_against_CVX_matlab.m). Scale jitter by `D²`; the existing approximate tie breaker remains, with no guarantee for extreme weight ratios. [Repro](repro/BENTO-002/run.sh), [patch](patches/BENTO-002.patch).

```diff
-        data[i] += x;
+        data[i] += x / gamma_init[i / T];
```

## References

- [Jia et al. (2018). Efficient Projection onto the Perfect Phylogeny Model.](https://doi.org/10.48550/arXiv.1811.01129)
- [Upstream source at the reported commit](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/tree/769ccd389a559085df8fa628047eba2f2d850c15).

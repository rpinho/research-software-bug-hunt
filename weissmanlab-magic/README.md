# weissmanlab/magic

Pinned commit: [`87fd0923480d28399c5078ff4efd60c3205c22a0`](https://github.com/weissmanlab/magic/tree/87fd0923480d28399c5078ff4efd60c3205c22a0).

4 confirmed defects, including 0 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### W01 : Initialization loses final window

[weissmanlab/magic · windower.py:61](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/windower.py#L61). Four 80-base windows, events at 1,81,161,241,320: counts **[1,1,2] → [1,1,1,2]**; retained events **4 → 5**. Too few histogram edges lose terminal data and misassign a boundary, changing inference inputs. Correct: integer window membership gives those four counts under the [producer’s coverage convention](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/combo_prep.py). [Repro](repro/W01/run.sh), [patch](patches/W01.patch).

```diff
-	windowcounts = numpy.histogram(SNPs, bins=list(range(1, len(basecoverage)*L0+1, L0)))[0]
+	windowcounts = numpy.histogram(SNPs, bins=list(range(1, (len(basecoverage)+1)*L0+1, L0)))[0]
```
### M02 : Zero-mass output serialization crashes

[weissmanlab/magic · magic.py:427](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/magic.py#L427). Gamma parameters `[0.5,1,1,0.5]`: **TypeError → rows `[0.5,1,1]` and `[0.5]`**. A scalar zero mass reaches a row iterator, preventing final output after fitting. Correct: the [documented format](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/README.md) requires a one-column final row; no-zero output is unchanged. [Repro](repro/M02/run.sh), [patch](patches/M02.patch).

```diff
-			niceparams += [wzero,]
+			niceparams += [[wzero],]
```
### W02 : Table inputs crash and merge too early

[weissmanlab/magic · windower.py:77](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/windower.py#L77). Count/coverage rows `(1,80)…(4,80)`, either advertised order: **NameError → scale-0 counts [1,2,3,4], scale-1 [3,7]**. RNG initialization is absent and scale 0 is prematurely merged, blocking these inputs. Correct: preserve input rows at their [declared base scale](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/windower.py#L112), merging only at later scales. [Repro](repro/W02/run.sh), [patch](patches/W02.patch).
### M01 : Mean omits infinite tail

[weissmanlab/magic · magic.py:503](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/magic.py#L503). One rate-2 exponential: mean **0 → 0.5**; breaks [0,1], rates [1,2]: **0.632120559 → 0.816060279**, normalized block fraction at zero **1.290988 → 1**. Dropped tail mass understates means and permits fractions above one. Correct: integrate the [implemented survival function](https://github.com/weissmanlab/magic/blob/87fd0923480d28399c5078ff4efd60c3205c22a0/magic.py#L496), including its unbounded last interval. CLI fitting does not call this mean. [Repro](repro/M01/run.sh), [patch](patches/M01.patch).

```diff
-		return -np.concatenate((np.diff(self.breakPs), [0])) @ (1/self.rates)
+		return -np.diff(np.concatenate((self.breakPs, [0]))) @ (1/self.rates)
```

## References

- [Weissman and Hallatschek (2017). Minimal-assumption inference from population-genomic data.](https://doi.org/10.7554/eLife.24836)
- [Upstream source at the reported commit](https://github.com/weissmanlab/magic/tree/87fd0923480d28399c5078ff4efd60c3205c22a0).

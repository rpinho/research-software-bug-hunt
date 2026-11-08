# edbosne/pyfdd

Pinned commit: [`6aba44c5c4aaed278e08691f28abe79c724cf1da`](https://github.com/edbosne/pyfdd/tree/6aba44c5c4aaed278e08691f28abe79c724cf1da).

7 confirmed defects, including 3 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### B01 : Angular grid distortion

[edbosne/pyfdd · pyfdd/core/patterncreator.py:388](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/patterncreator.py#L388). Library field `10+x+2y`, target coordinates −1,0,1: first row **[6.25,7.5,8.75] → [7,8,9]**; a flat 5×5 self-grid loses **16 → 0** pixels. Index scaling stretches coordinates, changing model shapes and support. Correct: index `(angle−first)/step` follows the [library grid definition](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/lib2dl/lib2dl.py#L109), retaining the existing interpolator. [Repro](repro/B01/run.sh), [patch](patches/B01.patch).
### B02 : JSON reload discards backing masks

[edbosne/pyfdd · pyfdd/core/datapattern/datapattern.py:389](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/datapattern/datapattern.py#L389). 3×3 data with one excluded 1,000-count pixel; save, reload, exclude another: included sum **1,035 → 35**. Constructor resets restored backing masks, allowing excluded pixels back into fits. Correct: preserve exclusions serialized by the [JSON writer](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/datapattern/datapattern.py#L704). [Repro](repro/B02/run.sh), [patch](patches/B02.patch).
### B03 : Orientation leaves masks behind

[edbosne/pyfdd · pyfdd/core/datapattern/datapattern.py:982](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/datapattern/datapattern.py#L982). Clockwise-rotate a masked 3×3 array, then edit its mask: included sum **1,029 → 36**; rectangular case **IndexError → 17**. Backing masks retain old coordinates, corrupting exclusions or crashing. Correct: transform exclusions with their pixels under the [documented orientation](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/datapattern/datapattern.py#L971). [Repro](repro/B03/run.sh), [patch](patches/B03.patch).
### B04 : Background retains earlier exclusions

[edbosne/pyfdd · pyfdd/core/patterncreator.py:425](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/patterncreator.py#L425). Uniform 90-count 3×3 input: render, displace, render original again: **6 masked pixels plus 3×30 → 9×10**. In-place background mutation makes results depend on earlier calls. Correct: identical [requested parameters](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/patterncreator.py#L159) define identical patterns. This concerns default PatternCreator masking; Fit’s masking-false path is outside this finding. [Repro](repro/B04/run.sh), [patch](patches/B04.patch).
### B06 : Zero-probability costs omitted : minor

[edbosne/pyfdd · pyfdd/core/fit.py:316](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/fit.py#L316). 7×7 library with a zero plateau, positive observed center: NLL **16.962108 → ∞**, Pearson cost **0.716049 → ∞**. Masked arithmetic drops impossible bins, favoring invalid models. Correct: `−n log(0)=∞` for `n>0` ([likelihood definition](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/fit.py#L381)). Exposure on ordinary positive library patterns is unestablished. [Repro](repro/B06/run.sh), [patch](patches/B06.patch).
### B07 : Zero-minimum uncertainty collapse : minor

[edbosne/pyfdd · pyfdd/core/fit.py:368](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/fit.py#L368). Fit total counts to nine ten-count bins: optimum 90 unchanged; standard deviation **3e−10 → 9.486833**. A ratio cap against previous cost zero corrupts curvature, giving extreme overconfidence. Correct: `χ²(t)=(90−t)²/t` has `χ²″(90)=2/90`, giving √90 under the [implemented Hessian convention](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/fit.py#L588). Exact-fit scope only. [Repro](repro/B07/run.sh), [patch](patches/B07.patch).

```diff
-        elif chi2 > self.previous_cost_value * 1e12:
+        elif self.previous_cost_value > 0 and chi2 > self.previous_cost_value * 1e12:
```
### B05 : Direct-input degrees of freedom : minor

[edbosne/pyfdd · pyfdd/core/fit.py:273](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/fit.py#L273). Nine bins, six active parameters: scalar-mask array **−5 → 3** degrees of freedom; ndarray **AttributeError → 3**. A scalar mask is counted as one bin and `np.Array` is misspelled, breaking direct Fit usage. Correct: count unmasked bins minus fitted parameters ([definition](https://github.com/edbosne/pyfdd/blob/6aba44c5c4aaed278e08691f28abe79c724cf1da/pyfdd/core/fit.py#L266)). Normal DataPattern masks avoid this. [Repro](repro/B05/run.sh), [patch](patches/B05.patch).

```diff
-            n_pixels = (~self.data_pattern.mask).sum()
-        elif isinstance(self.data_pattern, np.Array):
+            n_pixels = self.data_pattern.count()
+        elif isinstance(self.data_pattern, np.ndarray):
```

## References

- [David-Bosne et al. (2024). Electron Emission Channeling for lattice location of radioactive isotopes in single crystals: Improvements from a Timepix3 quad detector and new PyFDD data analysis software.](https://doi.org/10.1016/j.nima.2023.169016)
- [Upstream source at the reported commit](https://github.com/edbosne/pyfdd/tree/6aba44c5c4aaed278e08691f28abe79c724cf1da).

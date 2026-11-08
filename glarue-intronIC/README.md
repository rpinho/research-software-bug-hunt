# glarue/intronIC

Pinned commit: [`0db1d54274f1ffdbbc95dea6589a75a833eb831d`](https://github.com/glarue/intronIC/tree/0db1d54274f1ffdbbc95dea6589a75a833eb831d).

5 confirmed defects, including 1 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### R02 : Branch-point windows differ by strand

[glarue/intronIC · src/intronIC/extraction/sequences.py:368](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/extraction/sequences.py#L368). Two mirrored synthetic introns with an ambiguous boundary base: branch-point window/reference mismatches **3 → 0** across strands/access modes. Coordinate conversions select different bases, bypassing ambiguity exclusion. Correct: slice transcript-oriented intron offsets under the [scoring coordinates](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/extraction/sequences.py#L81). [Repro](repro/R02/run.sh), [patch](patches/R02.patch).
### R01 : Default installation omits pandas

[glarue/intronIC · pyproject.toml:25](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/pyproject.toml#L25). Fresh install with declared dependencies: pandas import **exit 1 → 0**; default classification **abort → completion**. Post-processing requires an undeclared package, blocking clean installs. Correct: declare the dependency used by [post-processing](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/cli/main.py#L327). [Repro](repro/R01/run.sh), [patch](patches/R01.patch).

```diff
+    "pandas>=1.3.0",
```
### R03 : Short flank empties quality window

[glarue/intronIC · src/intronIC/extraction/sequences.py:353](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/extraction/sequences.py#L353). Two synthetic introns with only three downstream bases and an intronic N: introns passing indexed ambiguity filtering **2 → 0**. A zero-relative stop becomes an empty 3′ quality slice, letting ambiguous inputs through. Correct: absolute half-open indices retain the [specified scoring interval](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/cli/main.py#L2921), including at contig ends. Both extraction and CLI copies are fixed. [Repro](repro/R03/run.sh), [patch](patches/R03.patch).
### R04 : Header-free classification aborts

[glarue/intronIC · src/intronIC/cli/main.py:5064](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/cli/main.py#L5064). Two toy introns, documented `--no-headers`: **exit 1 → 0**, with header-free score rows. Post-processing reads column names after headers were suppressed, preventing completion. Correct: retain internal headers until readers finish, then remove the single header row required by the [output option](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/cli/main.py). [Repro](repro/R04/run.sh), [patch](patches/R04.patch).
### R05 : Extraction helper crashes on exhaustion : minor

[glarue/intronIC · src/intronIC/file_io/genome.py:128](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/file_io/genome.py#L128). Exhaust the extraction generator on two toy introns: **2 records then AttributeError → 2 records and exit 0**. Cleanup calls a missing `close()`, breaking direct helper consumers. Correct: release cached state; FASTA streams already close after parsing ([reader implementation](https://github.com/glarue/intronIC/blob/0db1d54274f1ffdbbc95dea6589a75a833eb831d/src/intronIC/file_io/genome.py#L133)). No CLI impact demonstrated. [Repro](repro/R05/run.sh), [patch](patches/R05.patch).

## References

- [Moyer et al. (2020). Comprehensive database and evolutionary dynamics of U12-type introns.](https://doi.org/10.1093/nar/gkaa464)
- [Upstream source at the reported commit](https://github.com/glarue/intronIC/tree/0db1d54274f1ffdbbc95dea6589a75a833eb831d).

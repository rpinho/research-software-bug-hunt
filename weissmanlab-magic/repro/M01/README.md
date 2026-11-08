Run `sh repro/M01/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/M01.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11 with `numpy==1.26.4 scipy==1.13.1`. The scripts call the pinned implementation; M02 also exercises the actual CLI output writer on a synthetic transform. Its short optimization checks serialization rather than parameter recovery.

## References

- [Weissman and Hallatschek (2017). Minimal-assumption inference from population-genomic data.](https://doi.org/10.7554/eLife.24836)
- [Upstream source at the reported commit](https://github.com/weissmanlab/magic/tree/87fd0923480d28399c5078ff4efd60c3205c22a0).

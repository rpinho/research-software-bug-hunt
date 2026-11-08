Run `sh repro/R03/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/R03.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.10+. For R02–R05 install `numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 scikit-learn==1.5.2 biogl==3.0.1 matplotlib==3.9.4 networkx rich smart-open tqdm pyyaml joblib pyfastx`. R01 creates a separate temporary venv and installs the pinned package with its declared dependencies, before and after patching. Fixtures are hand-written toy inputs; no biological measurements are used.

## References

- [Moyer et al. (2020). Comprehensive database and evolutionary dynamics of U12-type introns.](https://doi.org/10.1093/nar/gkaa464)
- [Upstream source at the reported commit](https://github.com/glarue/intronIC/tree/0db1d54274f1ffdbbc95dea6589a75a833eb831d).

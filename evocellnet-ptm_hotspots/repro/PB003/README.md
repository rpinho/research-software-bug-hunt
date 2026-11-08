Run `sh repro/PB003/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/PB003.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. For PB003: `python -m pip install numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 statsmodels`. For the R cases: R 4.5.2, with `install.packages(c("caret","gbm","e1071","pROC","doParallel","foreach","dplyr","tibble","tidyr","stringr"))`; the reproduction installs the pinned target package into temporary libraries. Pass `--rscript PATH` if Rscript is outside PATH.

## References

- [Strumillo et al. (2018). Conserved phosphorylation hotspots in eukaryotic protein domain families (preprint).](https://doi.org/10.1101/391185)
- [Upstream source at the reported commit](https://github.com/evocellnet/ptm_hotspots/tree/15b4b256f7f2945eebe72f622d68115d4bdd5e70).

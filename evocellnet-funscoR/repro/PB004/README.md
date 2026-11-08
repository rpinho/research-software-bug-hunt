Run `sh repro/PB004/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/PB004.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. For PB003: `python -m pip install numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 statsmodels`. For the R cases: R 4.5.2, with `install.packages(c("caret","gbm","e1071","pROC","doParallel","foreach","dplyr","tibble","tidyr","stringr"))`; the reproduction installs the pinned target package into temporary libraries. Pass `--rscript PATH` if Rscript is outside PATH.

## References

- [Ochoa et al. (2020). The functional landscape of the human phosphoproteome.](https://doi.org/10.1038/s41587-019-0344-3)
- [Upstream source at the reported commit](https://github.com/evocellnet/funscoR/tree/1ed6c74f112fd381626295245da327453d70cbe2).

Run `sh repro/PB001/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/PB001.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. For PB003: `python -m pip install numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 statsmodels`. For the R cases: R 4.5.2, with `install.packages(c("caret","gbm","e1071","pROC","doParallel","foreach","dplyr","tibble","tidyr","stringr"))`; the reproduction installs the pinned target package into temporary libraries. Pass `--rscript PATH` if Rscript is outside PATH.

## References

- [Ochoa et al. (2016). An atlas of human kinase regulation.](https://doi.org/10.15252/msb.20167295)
- [Upstream source at the reported commit](https://github.com/evocellnet/ksea/tree/126a64541a11df9d8dc16a00cd9ea3ab9f16147f).

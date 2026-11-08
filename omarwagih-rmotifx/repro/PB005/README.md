Run `sh repro/PB005/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/PB005.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. For PB003: `python -m pip install numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 statsmodels`. For the R cases: R 4.5.2, with `install.packages(c("caret","gbm","e1071","pROC","doParallel","foreach","dplyr","tibble","tidyr","stringr"))`; the reproduction installs the pinned target package into temporary libraries. Pass `--rscript PATH` if Rscript is outside PATH.

## References

- [Wagih et al. (2016). Uncovering phosphorylation-based specificities through functional interaction networks.](https://doi.org/10.1074/mcp.M115.052357)
- [Upstream source at the reported commit](https://github.com/omarwagih/rmotifx/tree/f13775f07679b86df173ccc2a9112263a1a9052f).

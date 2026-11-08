Run `sh repro/MAAMOUL-01/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/MAAMOUL-01.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. MUSiCC requires `numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 scikit-learn==1.5.2`. The R cases require R 4.5.2 with `install.packages(c("data.table","RColorBrewer","igraph","dplyr","tibble","logger"))`. Pass `--rscript PATH` if necessary. The scripts call the actual relevant source functions; they do not run the complete analysis pipelines.

## References

- [Muller, Baum and Borenstein (2026). MAAMOUL: metabolic network-based discovery of microbiome-metabolome shifts in disease.](https://doi.org/10.1093/bioinformatics/btag467)
- [Upstream source at the reported commit](https://github.com/borenstein-lab/MAAMOUL/tree/54f174c5a3a8d07ebac5b3431c43eb4bbfdc83b9).

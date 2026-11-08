Run `sh repro/MUSICC-01/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/MUSICC-01.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. MUSiCC requires `numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 scikit-learn==1.5.2`. The R cases require R 4.5.2 with `install.packages(c("data.table","RColorBrewer","igraph","dplyr","tibble","logger"))`. Pass `--rscript PATH` if necessary. The scripts call the actual relevant source functions; they do not run the complete analysis pipelines.

## References

- [Manor and Borenstein (2015). MUSiCC: a marker genes based framework for metagenomic normalization and accurate profiling of gene abundances in the microbiome.](https://doi.org/10.1186/s13059-015-0610-8)
- [Upstream source at the reported commit](https://github.com/borenstein-lab/MUSiCC/tree/478c9244cf406935e67abdf7622bdb05421ab1fb).

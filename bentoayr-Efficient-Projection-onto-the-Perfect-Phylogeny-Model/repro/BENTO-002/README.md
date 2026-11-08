Run `sh repro/BENTO-002/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/BENTO-002.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.10+ and a C compiler named `cc`. No Python packages are required. Numeric fractions have a 3e-6 tolerance because the retained upstream tie breaker perturbs frequencies by up to 1e-6.

## References

- [Jia et al. (2018). Efficient Projection onto the Perfect Phylogeny Model.](https://doi.org/10.48550/arXiv.1811.01129)
- [Upstream source at the reported commit](https://github.com/bentoayr/Efficient-Projection-onto-the-Perfect-Phylogeny-Model/tree/769ccd389a559085df8fa628047eba2f2d850c15).

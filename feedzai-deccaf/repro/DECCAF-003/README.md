Run `sh repro/DECCAF-003/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/DECCAF-003.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11 with `numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 scikit-learn==1.5.2 ortools==9.7.2996 pyarrow==17.0.0`. Only function definitions are loaded from the source, avoiding experiment loops. Allocation uses the real solver with one worker. Threshold checks execute the original arithmetic, including the objective threshold block, without model training. These are arithmetic counterexamples, not performance benchmarks.

## References

- [Alves et al. (2024). Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints.](https://doi.org/10.48550/arXiv.2403.06906)
- [Upstream source at the reported commit](https://github.com/feedzai/deccaf/tree/b910b48d7e146d53b5f145224b819bdb0962d40a).

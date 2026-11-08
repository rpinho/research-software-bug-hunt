Run `sh repro/B07/run.sh` from the project folder, or set `PYTHON` to a Python environment with the dependencies below. Git, a network connection and the adjacent `patches/B07.patch` are required. `--source CHECKOUT` uses an existing pinned checkout without changing it. Temporary source copies are removed on exit.

Dependencies tested: Python 3.11. Install `numpy==1.26.4 scipy==1.13.1 pandas==1.5.3 matplotlib==3.9.4 numdifftools==0.9.42 PyQt5==5.15.11 seaborn==0.13.2`. Qt is imported by the package; the script sets offscreen mode and opens no GUI. No target-package installation is required; its pinned source is imported directly.

## References

- [David-Bosne et al. (2024). Electron Emission Channeling for lattice location of radioactive isotopes in single crystals: Improvements from a Timepix3 quad detector and new PyFDD data analysis software.](https://doi.org/10.1016/j.nima.2023.169016)
- [Upstream source at the reported commit](https://github.com/edbosne/pyfdd/tree/6aba44c5c4aaed278e08691f28abe79c724cf1da).

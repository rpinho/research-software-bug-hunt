# glm-tools/pyglmnet

Three confirmed defects, reported through the open pull requests below in Nov 2026. Patches and tests live in the pull requests.

Upstream base commit: [`9339c5c71c908ec31cf4bebda5d9fe47dfed4f1c`](https://github.com/glm-tools/pyglmnet/tree/9339c5c71c908ec31cf4bebda5d9fe47dfed4f1c).

- [#399: FIX: Bernoulli log likelihood is NaN at probabilities 0 and 1, and overflows for large logits](https://github.com/glm-tools/pyglmnet/pull/399). Uses stable Bernoulli likelihood expressions at probability endpoints and large logits.
- [#400: FIX: gamma deviance and pseudo-R2 omit the saturated log likelihood](https://github.com/glm-tools/pyglmnet/pull/400). Includes the gamma saturated log likelihood in deviance and pseudo-R2.
- [#401: FIX: simulate_glm(sample=True) for gamma returns exp(mu) instead of gamma samples](https://github.com/glm-tools/pyglmnet/pull/401). Draws gamma samples with the requested mean instead of returning exp(mu).

## References

- [Jas et al. (2020). Pyglmnet: Python implementation of elastic-net regularized generalized linear models.](https://doi.org/10.21105/joss.01959)
- [Upstream repository](https://github.com/glm-tools/pyglmnet).

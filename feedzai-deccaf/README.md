# feedzai/deccaf

Pinned commit: [`b910b48d7e146d53b5f145224b819bdb0962d40a`](https://github.com/feedzai/deccaf/tree/b910b48d7e146d53b5f145224b819bdb0962d40a).

3 confirmed defects, including 2 minor. Reported to the authors, Nov 2026.

Run `sh repro/<ID>/run.sh` from this project folder. Each patch applies individually from the upstream repository root at the pinned commit. Dependencies are listed with each reproduction. No change to published scientific results is established.

### DECCAF-003 : FPR threshold exceeds budget

[feedzai/deccaf · Code/alert_model/hpo_fpr.py:24](https://github.com/feedzai/deccaf/blob/b910b48d7e146d53b5f145224b819bdb0962d40a/Code/alert_model/hpo_fpr.py#L24). Nine negatives at 5%: false positives **9 → 0**; 100 negatives with 20 tied at the boundary: **20 → 0** (budget 5). Index −1 and ties inflate accepted negatives and the optimization objective. Correct: select the most permissive attainable ROC threshold within the [5% constraint](https://github.com/feedzai/deccaf/blob/b910b48d7e146d53b5f145224b819bdb0962d40a/Documents/Paper.pdf), across all four copies. Preprocessing uses strict `>`; the other callers use `>=`. No error is established in the archived 5% validation boundary. [Repro](repro/DECCAF-003/run.sh), [patch](patches/DECCAF-003.patch).
### DECCAF-002 : Batch labels drop cases : minor

[feedzai/deccaf · Code/deferral/run_alert.py:140](https://github.com/feedzai/deccaf/blob/b910b48d7e146d53b5f145224b819bdb0962d40a/Code/deferral/run_alert.py#L140). Two cases with matching capacity row, batch 0: saved rows **0 → 2** in all five methods; batch 2: capacity-aware methods **IndexError → 2 rows**. Loops invent absent labels, breaking relabeling/subsetting. Correct: membership and quotas are unchanged by labels ([batch definition, §3.2](https://github.com/feedzai/deccaf/blob/b910b48d7e146d53b5f145224b819bdb0962d40a/Documents/Paper.pdf)). Arbitrary labels are undocumented; supplied batches use 1. [Repro](repro/DECCAF-002/run.sh), [patch](patches/DECCAF-002.patch).
### DECCAF-001 : Capacity column order changes quotas : minor

[feedzai/deccaf · Code/deferral/run_alert.py:142](https://github.com/feedzai/deccaf/blob/b910b48d7e146d53b5f145224b819bdb0962d40a/Code/deferral/run_alert.py#L142). Two cases, one human slot; reorder named capacity columns: CP **no solution → 2 assignments**, minimum cost **0.2**; OvA **1 → 2 rows**, random allocation **crash → 2 rows**. Positional summation includes metadata, changing the problem. Correct: use named worker quotas ([constraints, §3.3](https://github.com/feedzai/deccaf/blob/b910b48d7e146d53b5f145224b819bdb0962d40a/Documents/Paper.pdf)). Column-order independence is undocumented; supplied files are unaffected. [Repro](repro/DECCAF-001/run.sh), [patch](patches/DECCAF-001.patch).

## References

- [Alves et al. (2024). Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints.](https://doi.org/10.48550/arXiv.2403.06906)
- [Upstream source at the reported commit](https://github.com/feedzai/deccaf/tree/b910b48d7e146d53b5f145224b819bdb0962d40a).

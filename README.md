# Variability and fairness of personal-baseline change detection

Simulation audit of four standard change detectors (fixed threshold, personal z-score, EWMA, CUSUM) across
day-to-day variability groups, with a small real-data check on LifeSnaps. Simulated users only for the main
results; not a clinical validation.

- `pilot/`: simulator, detectors, analysis plans, result files and their summaries.
- `paper/`: the preprint (LaTeX), tables and figures generated from the result files, number checks,
  arXiv source. See `paper/README.md`.

Plans were written and committed as dated text in this repository; see Appendix D of the paper for what was
committed before and after each result.

Licence: MIT (code). Citation: see `CITATION.cff`.

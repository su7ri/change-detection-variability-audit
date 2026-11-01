# Paper: Do personal-baseline change detectors treat low- and high-variability users equally?

Preprint source. Everything in the paper that is a number comes from the CSV result files of the repository
(`../pilot/results`, read directly; this folder has no copy of them), through generated files:

| step | command (run from this folder) | writes |
|---|---|---|
| tables and number macros | `python scripts/build_tables.py` | `tables/*.tex`, `numbers.tex` |
| figures | `python scripts/build_figures.py` | `figures/*.pdf`, `figures/*.png` |
| check the numbers against the repository summaries | `python scripts/check_numbers.py` | nothing (exit code 1 on any mismatch) |
| PDF | `latexmk -pdf main.tex` | `main.pdf` |

Do not edit `numbers.tex` or `tables/*.tex` by hand; change the script and rerun it.

Python needs `numpy`, `pandas`, `matplotlib`. LaTeX needs a standard TeX Live (`mathpazo`, `natbib`, `cleveref`,
`booktabs`, `longtable`, `microtype`, `enumitem`, `float`, `placeins`, `pdflscape`).

`arxiv_source.zip` is the upload for arXiv: `main.tex`, `numbers.tex`, `main.bbl`, `tables/`, `figures/*.pdf`.
It compiles with `pdflatex main.tex` (twice) without BibTeX. Rebuild it after any change to the text:
`latexmk -pdf main.tex`, then zip those files again.

Before submission see `SUBMISSION_CHECKLIST.md`.

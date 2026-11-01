# arXiv submission checklist

Paper: *Do personal-baseline change detectors treat low- and high-variability users equally?* (21 pages, A4).
Author line in the paper: Soroush Azarinejadianlangroudi, Independent researcher (see decision 1).
Target: arXiv/Zenodo preprint by **20 December 2026**. Exeter EPSRC DLA closes **8 December 2026, noon**
(repository plus 2-page summary by 5 December), so the repository, not the preprint, is the first deadline.

## A. Decisions only you can make

| # | Decision | What I did | What to check |
|---|---|---|---|
| 1 | Affiliation | "Independent researcher" | Use Exeter only if you may state that affiliation for this work (ask your supervisor/programme). The paper does not give an email address. |
| 2 | AI-assistance statement | none in the paper | arXiv has said it will ban authors for a year when unchecked AI output is clear-cut negligence, for example references to sources that do not exist. Whether and how you state AI use is your decision; what is not optional is that you have checked everything yourself (point 3 below). |
| 3 | References | all 19 entries were checked against the publisher, Crossref-type or preprint-server record while writing; fields I could not confirm are left out | Open every DOI in section D yourself before you submit. This takes about 20 minutes and removes the one risk that can cost a year. |
| 4 | Repository | `change-detection-variability-audit` (new, only `pilot/` and `paper/`) | The older report repository `evoki-drift-eval` is untouched and is not cited in the paper. The commit hashes in the paper are those of the new repository (history rewritten from the pilot commits; dates and messages unchanged). |
| 5 | Wording about pre-registration | "analysis plan written before the runs", "dated plans" | Three plans were committed before their results: the analysis plan (`9e57708`), the LifeSnaps plan (`ac26c93`) and the plan for the two checks added after a reader's comments (`5e57f66`, 29 October 2026). Every other amendment was committed together with its results. The paper says so briefly in Sections 3.6 and 8; the full list of deviations and the commit times are in Appendix E. The paper no longer calls the work "pre-specified": it says "an analysis plan written before the runs". The bootstrap departure (frozen plan 2000 resamples, reported runs 1000) was found on 29 October and is disclosed in `pilot/ANALYSIS_PLAN.md` (commit `fccc209`) and in Section 8; the 10000-resample re-run is in `pilot/results_mc/` and changes 3 of 3024 verdicts. Do not shorten it to "pre-registered": there is no external registry. |
| 6 | Licence | not chosen | arXiv asks you to pick one at upload. CC BY 4.0 is the usual choice for a preprint. The repository already has an MIT `LICENSE` for the code, so the two do not conflict. |
| 7 | Wording in old commit messages | unchanged | Commits `5a41316` and `69bb607` say "pre-registered" in their messages. The paper deliberately says "dated plans" and "analysis plan written before the runs" (decision 5). Do not rewrite history; if someone asks, point to Appendix E. |

## B. Before you upload

1. Repository is **public** and contains `paper/` and the `pilot/` results the paper cites (`git push`). The repository's `.gitignore` excludes any folder called `data/`, so nothing under `paper/data/` would be pushed; the paper therefore reads the CSVs from `pilot/results/` directly. The abstract says "Code, dated plans and all results are public"; if the repository is private, that sentence is false.
2. Zenodo DOI (about 10 minutes):
   1. Log in to zenodo.org with GitHub, switch on the repository under *GitHub*.
   2. On GitHub create a release (for example `v1.0-preprint`). Zenodo archives it and mints the DOI.
   3. Put the DOI in `main.tex` (`\zenodoDOI`, currently the text `[Zenodo DOI to be added]`) and in `CITATION.cff` (uncomment `doi:`).
   4. `grep -n "Zenodo DOI to be added" main.tex` must print nothing. Rebuild: `latexmk -pdf main.tex`.
   5. The archived snapshot will not contain the DOI itself; that is normal. Say in the arXiv comments field: "Code archived at doi:...".
3. `python scripts/check_numbers.py` ends with "0 failures" (run it inside the repository: it then also checks the commit list in Appendix E against `git log`).
4. Update the commit shown in the paper if you commit after the pilot: `\commit` in `main.tex` is `fccc209`, the last pilot commit (disclosure and 10000-resample re-run). The paper's own commit will have a different hash; that is expected.
5. Rebuild the PDF and `arxiv_source.zip`, then open the PDF once and read the abstract, Sections 3.6, 8 and Appendix E against what you remember doing. Run `pdffonts main.pdf`: no line may say `Type 3` (the typewriter font comes from `lmodern`; without it the T1 typewriter font is a bitmap).

## C. The arXiv form

* **Account and endorsement.** arXiv requires an endorsement before a first submission and for each new category. An institutional email address alone does not do it: it helps only if you have also claimed authorship of a paper on arXiv. Otherwise you need a personal endorser, an established arXiv author in the category. Start the submission first and choose the category; arXiv then gives you an endorsement-request link to send. On the abstract page of related arXiv papers, "Which authors of this paper are endorsers?" shows who qualifies. Write to one or two suitable people with a short message and the PDF. Do not mass-mail endorsers (arXiv says so explicitly).
* **Category.** Primary `stat.AP` (statistics, applications). Optional cross-lists: `stat.ME`, `cs.LG`. The primary category decides whose endorsement you need, so choose the one where you can find an endorser; the paper fits `stat.AP` best.
* **Upload** `arxiv_source.zip` (top-level `main.tex` with `\documentclass`, `numbers.tex`, `main.bbl`, `tables/`, `figures/`). Figures are PDF (pdfLaTeX). File names use only letters, digits and `_ + - . , =`. I compiled the zip in a clean folder with `pdflatex` twice: 21 pages, no undefined references. The arXiv preview must show the same.
* **Title** (plain text, no LaTeX): `Do personal-baseline change detectors treat low- and high-variability users equally?`
* **Abstract** (plain text, 1272 characters, five sentences; the limit is 1920; no word "Abstract"): see `abstract_plain.txt`. Paste it as one paragraph.
* **Comments:** `21 pages, 5 figures, 16 tables. Code and results: https://github.com/su7ri/change-detection-variability-audit` (add the Zenodo DOI once you have it).
* **Authors:** `Soroush Azarinejadianlangroudi` (same spelling as in the paper). An ORCID iD is optional and free (orcid.org); if you create one, link it in your arXiv account profile, not in the paper.
* **MSC/ACM class, journal ref, DOI:** leave empty.
* Submissions received before 14:00 Eastern are normally announced at 20:00 Eastern the same day. Before announcement you can unsubmit and fix; afterwards use *replace*, not a new submission.

## D. References to open yourself (DOI links)

| Key | Entry | Link |
|---|---|---|
| page1954 | Page, Biometrika 41, 1954 | https://doi.org/10.1093/biomet/41.1-2.100 |
| roberts1959 | Roberts, Technometrics 1, 1959 (no DOI printed) | search "Control chart tests based on geometric moving averages" |
| hawkins1987 | Hawkins, The Statistician 36, 1987 | https://doi.org/10.2307/2348827 |
| gama2014 | Gama et al., ACM Computing Surveys 46(4), 2014 | https://doi.org/10.1145/2523813 |
| aminikhanghahi2017 | Aminikhanghahi and Cook, KAIS 51, 2017 | https://doi.org/10.1007/s10115-016-0987-z |
| mishra2020 | Mishra et al., Nat. Biomed. Eng. 4, 2020 | https://doi.org/10.1038/s41551-020-00640-6 |
| alavi2022 | Alavi et al., Nat. Med. 28, 2022 | https://doi.org/10.1038/s41591-021-01593-2 |
| (footnote) | Alavi et al., medRxiv preprint | https://doi.org/10.1101/2021.06.13.21258795 |
| cacheda2026 | Cacheda et al., Digital Health 12, 2026 | https://doi.org/10.1177/20552076261477919 |
| morenomunoz2018 | Moreno-Muñoz et al., arXiv:1809.04197 | https://arxiv.org/abs/1809.04197 |
| yfantidou2022 | Yfantidou et al., Sci. Data 9, 2022 | https://doi.org/10.1038/s41597-022-01764-x |
| lifesnaps_zenodo | LifeSnaps, Zenodo v4 | https://doi.org/10.5281/zenodo.7229547 |
| smyth2004 | Smyth, SAGMB 3(1), 2004 | https://doi.org/10.2202/1544-6115.1027 |
| fraser1989 | Fraser and Harris, Crit. Rev. Clin. Lab. Sci. 27, 1989 (no DOI printed) | search the title |
| dwork2011 | Dwork et al., arXiv:1104.3913 | https://arxiv.org/abs/1104.3913 |
| morris2019 | Morris, White, Crowther, Stat. Med. 38, 2019 | https://doi.org/10.1002/sim.8086 |
| siepe2024 | Siepe et al., Psychological Methods, advance online publication | https://doi.org/10.1037/met0000695 (check whether volume, issue and pages exist now; if so, add them to `references.bib` and rebuild) |
| tolosa2026 | Tolosa et al., Electronics 15(4), 885, 2026 | https://doi.org/10.3390/electronics15040885 |
| lakens2017 | Lakens, SPPS 8, 2017 | https://doi.org/10.1177/1948550617697177 |
| royston2013 | Royston and Parmar, BMC Med. Res. Methodol. 13, 2013 | https://doi.org/10.1186/1471-2288-13-152 |

Three statements in the Related-work section rest on what the sources say, so read them once in the originals:
(a) the medRxiv version of Alavi et al. uses an alert rule with a fixed offset above each person's own baseline and says some individuals have a very unstable baseline;
(b) Moreno-Muñoz et al. detect changes in smartphone data with a hierarchical circadian model, motivated by relapse detection in psychiatric patients;
(c) Tolosa et al. mark a drift day when a composite of per-user rolling z-scores of Fitbit and phone data exceeds a participant-specific quantile threshold, judge it against proxy labels derived from the same rolling baselines with precision, recall and AUC, and (as far as I could see) do not study detection delay by variability group. Read the paper and correct our description if it is wrong.
The sentence "We did not find in our searches an evaluation of how the alarm rate and detection delay of such detectors depend on a person's own variability" is a statement about my searches, not a proof; if you or your supervisor know of such a paper, add it and soften the first contribution accordingly.

## E. How to describe the result in emails, the DLA summary and the arXiv comments

* Write every simulated result as a simulated result: "in simulation, a fixed threshold gives variable users about 3 more alarms per 100 user-days"; never "variable users get more alarms".
* The real-data part in one sentence: "a check on 51 users of the open LifeSnaps data (17 per group) is mostly inconclusive, and one CUSUM result there is unexplained".
* The contribution is the audit protocol and the explicit choice between two definitions of equal treatment, not the fixed-threshold result, which is predictable from the algebra. Say "audit", not "new method", and "analysis plan written before the runs", not "pre-registered".

## F. What the paper does not claim (keep it that way if you edit)

* It is an audit of existing detectors, not a new method; the mixed-scale family is a secondary, post hoc description.
* The main evidence is simulated. The LifeSnaps check has 51 users (17 per group) and most comparisons are uninformative.
* One result is unexplained: the real CUSUM alarm-rate gap (−3.33) is larger than in any simulation. Its interval ends at −1.62, close to the most negative simulated gap (−1.52).
* The pre-set trade-off criterion was not met; one prediction for the combined sensitivity settings was wrong. Both are stated in the paper.
* Two checks were added after all other results were known, on a reader's comments (plan committed first, `5e57f66`; results `5cd80a4`): the z-score with the baseline scale (the pattern does not depend on the choice of scale) and cross-fitted tuning on LifeSnaps (the conclusions do not depend on tuning in sample; 3 of 20 marginal verdicts are unstable). Say "checked" for these, not "validated": there are still 51 users.
* The bootstrap used 1000 resamples, not the 2000 of the frozen plan. This is disclosed, and a 10000-resample re-run gives identical point estimates and 3 changed verdicts out of 3024 (all marginal). Do not describe the work as having followed the plan "exactly".

"""Cross-check the numbers in the paper against the repository's own result summaries.

Run from the paper/ directory (the repository's pilot/results folder must be at ../pilot/results):

    python scripts/check_numbers.py

What it checks (each failure is printed; the exit code is 1 if anything fails):
  1. every "gap [lo, hi] verdict" string in the repository's *_summary.md files is reproduced, digit for digit,
     from the CSV copies in paper/data (so the paper's reading and rounding of the CSV files is the repository's);
  2. the verdict column of each CSV agrees with the pre-set rule recomputed from gap, interval and margin;
  3. every "gap [lo, hi]" string defined in numbers.tex occurs in a repository summary;
  4. values typed by hand in the paper (tuned constants, population scales, LifeSnaps descriptives, floor shares,
     robustness counts) agree with the strings in the summaries;
  5. the pre-set trade-off criterion was not met (recomputed from the CSV and from the summary text);
  6. every macro used in main.tex is defined, and the commits listed in Appendix D exist (when the git history is there).
"""
from __future__ import annotations

import re
import subprocess
import sys

import numpy as np
import pandas as pd

from lib import *  # noqa: F401,F403

RES = ROOT.parent / "pilot" / "results"
fails: list[str] = []
n_checks = 0


def check(cond: bool, msg: str) -> None:
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(msg)
        print("FAIL:", msg)


def norm(s: str) -> str:
    """Make '-0.00' and '+0.00' the same as '0.00' (the paper prints a zero without a sign)."""
    return re.sub(r"(?<![\d.])[+-]0\.00(?!\d)", "0.00", s.replace("\u2212", "-").replace("$-$", "-"))


NUM = r"[+-]\d+\.\d\d"
TOK = re.compile(rf"({NUM})(?: \|)? \[({NUM}), ({NUM})\](?:(?: \| | )(REAL|none|unclear)\b)?")

# ------------------------------------------------------------------ 1. md summaries vs CSV
CSV_NAMES = ["pilot_gaps", "tradeoff_gaps", "drift_gaps", "sensitivity_gaps", "sensitivity_tradeoff",
             "sensitivity_combos_gaps", "sensitivity_combos_tradeoff", "lifesnaps_gaps", "lifesnaps_log_gaps"]
csv_plain, csv_verdict = set(), set()
for name in CSV_NAMES:
    df = load(name)
    for r in df.itertuples():
        s = norm(f"{plain(r.gap_high_minus_low)} [{plain(r.gap_lo)}, {plain(r.gap_hi)}]")
        csv_plain.add(s)
        csv_verdict.add(f"{s} {r.verdict}")
    # 2. verdicts recomputed with the pre-set rule
    bad = 0
    for r in df.itertuples():
        if r.metric in MARGIN and verdict_of(r.gap_high_minus_low, r.gap_lo, r.gap_hi, r.metric) != r.verdict:
            bad += 1
    check(bad == 0, f"{name}.csv: {bad} verdicts differ from the pre-set rule")

md_files = sorted(RES.glob("*_summary.md"))
check(len(md_files) >= 7, f"found only {len(md_files)} summary files in {RES}")
md_tokens: set[str] = set()
n_md = 0
for f in md_files:
    for m in TOK.finditer(f.read_text()):
        s = norm(f"{m.group(1)} [{m.group(2)}, {m.group(3)}]")
        md_tokens.add(s)
        n_md += 1
        if m.group(4):
            check(f"{s} {m.group(4)}" in csv_verdict, f"{f.name}: '{m.group(0)}' is not in any CSV (with that verdict)")
        else:
            check(s in csv_plain, f"{f.name}: '{m.group(0)}' is not in any CSV")
print(f"1. {n_md} gap strings in {len(md_files)} summaries checked against the CSV files")

# ------------------------------------------------------------------ 3. numbers.tex vs md
macro_txt = (ROOT / "numbers.tex").read_text()
macros = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*)\}", macro_txt))
n_ci = 0
for k, v in macros.items():
    m = TOK.fullmatch(norm(v).replace("\\,", ""))
    if m:
        n_ci += 1
        s = norm(f"{m.group(1)} [{m.group(2)}, {m.group(3)}]")
        check(s in md_tokens, f"macro \\{k} = {v} does not occur in any repository summary")
print(f"3. {n_ci} interval macros in numbers.tex checked against the summaries ({len(macros)} macros in total)")

# ------------------------------------------------------------------ 4. typed values
txt = {f.name: f.read_text() for f in md_files}
main = (ROOT / "main.tex").read_text()


def block(md: str, heading: str) -> str:
    """Text of the '## <heading>' block of a summary."""
    parts = re.split(r"^## ", md, flags=re.M)
    for p in parts:
        if p.startswith(heading + "\n"):
            return p
    raise KeyError(heading)


# tuned constants and pooled alarm rates, realistic scenario
b = block(txt["pilot_summary.md"], "Scenario: realistic")
tc = dict(re.findall(r"(fixed|zscore|ewma|cusum)=(\d+(?:\.\d+)?(?:e\+\d+)?)", b.split("\n")[2]))
check(float(tc["fixed"]) == 1450 or round(float(tc["fixed"]), -1) == 1450, f"fixed constant {tc['fixed']}")
for key, macro in [("fixed", "T=1450"), ("zscore", f"c={tc['zscore']}"), ("ewma", f"L={tc['ewma']}"), ("cusum", f"h={tc['cusum']}")]:
    check(macro in main, f"main.tex lacks '{macro}' (tuned constant {key})")
pooled = re.findall(r"(fixed|zscore|ewma|cusum)=(\d+\.\d+)", b.split("\n")[3])
pooled_txt = ", ".join(v for _, v in pooled[:3]) + " and " + pooled[3][1]
check(pooled_txt.replace(", ", ", ") in main, f"main.tex lacks pooled alarm rates '{pooled_txt}'")
fl = re.search(r"standardised 2 SD: ([\d.]+), ([\d.]+), ([\d.]+)", b)
check(f"{float(fl.group(3)):.0%}".replace("%", "") in main.replace("40\\%", "40"), "floor share in the high tercile (40%)")
check(round(float(fl.group(3)), 3) == 0.402 and round(float(fl.group(1)), 3) == 0.049, f"floor shares {fl.groups()} are not 0.402 / 0.049")
check("40\\% of" in main and "5\\% in the low tercile" in main, "main.tex: floor-share sentence (40% vs 5%) not found")

# population scale of the mixed detector
ps = re.search(r"Population scale constants: sd=(\d+), mad=(\d+)", block(txt["tradeoff_summary.md"], "Scenario: realistic"))
check(f"{ps.group(1)} steps" in main and f"or {ps.group(2)}" in main, f"population scales {ps.groups()} not in main.tex")

# LifeSnaps descriptives (primary run)
ls_md = txt["lifesnaps_summary.md"]
prim = block(ls_md, "Primary: 0-step days treated as not observed")
m = re.search(r"Eligible users (\d+) of (\d+)", prim)
check((int(m.group(1)), int(m.group(2))) == (LS_ELIGIBLE, LS_TOTAL), f"eligible users {m.groups()}")
check(int(re.search(r"shrunk detector: (\d+) steps", prim).group(1)) == LS_POP_SCALE, "LifeSnaps population scale")
check(float(re.search(r"Spearman\(log-SD, median steps\) = (-?\d+\.\d+)", prim).group(1)) == LS_SPEARMAN, "Spearman")
rows = re.findall(r"^\| (low|mid|high) \| (\d+) \| (\d+) \| [\d.]+ \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|", prim, flags=re.M)
for (terc, users, med, nr, ev, sd), (_, t) in zip(rows, LS_TERCILES.iterrows()):
    check((terc, int(users), int(med), float(nr), float(ev), float(sd)) ==
          (t.tercile, t.users, t.median_steps, t.share_no_row, t.mean_eval_len, t.median_log_sd), f"LifeSnaps tercile row {terc}")
check(len(rows) == 3, "LifeSnaps tercile table not parsed")
cons = re.search(r"Consistent cells: (\d+) of (\d+); informative cells .*?: (\d+) of (\d+)", prim)
life = life_flags(load("lifesnaps_gaps").query("not zeros_observed"), load("pilot_gaps"), load("tradeoff_gaps"))
check((int(cons.group(1)), int(cons.group(2)), int(cons.group(3))) == (int(life.consistent.sum()), len(life), int(life.informative.sum())),
      f"LifeSnaps consistent/informative counts: summary {cons.groups()} vs recomputed {life.consistent.sum()}/{len(life)}/{life.informative.sum()}")
check(int(life.same_sign.sum()) == 34, "same-sign count (34 of 35)")
# zeros kept
zk = block(ls_md, "Sensitivity: 0-step days kept as observed")
check(int(re.search(r"Eligible users (\d+)", zk).group(1)) == 53, "zeros-kept eligible users (53)")
zc = re.search(r"Consistent cells: (\d+) of (\d+); informative cells .*?: (\d+) of", zk)
check((zc.group(1), zc.group(3)) == (macros["LsZeroConsistent"], macros["LsZeroInformative"]), "zeros-kept counts")
# log run
lg = txt["lifesnaps_log_summary.md"]
lgm = re.search(r"Consistent cells: (\d+) of (\d+); informative cells .*?: (\d+) of", lg)
check(lgm is not None and (lgm.group(1), lgm.group(2), lgm.group(3)) == (macros["LsLogConsistent"], macros["LsLogCells"], macros["LsLogInformative"]),
      "log-run counts (summary vs macros)")

# robustness counts
s1, s2 = txt["sensitivity_summary.md"], txt["sensitivity_combos_summary.md"]
for tag, md, n in [("single", s1, 16), ("combos", s2, 3)]:
    got = {k: int(re.search(rf"\*\*R{k}[^\n]*?holds in (\d+) of {n}", md).group(1)) for k in (1, 2, 3)}
    mac = {"single": {1: "SensRoneOk", 2: "SensRtwoOk", 3: "SensRthreeOk"}, "combos": {1: "CombRoneOk", 2: "CombRtwoOk", 3: "CombRthreeOk"}}[tag]
    for k in (1, 2, 3):
        check(str(got[k]) == macros[mac[k]], f"robustness R{k} ({tag}): summary {got[k]} vs macro {macros[mac[k]]}")

# ------------------------------------------------------------------ 5. the pre-set trade-off criterion was not met
t = load("tradeoff_gaps")


def g(conv, lam):
    return cell(t, scenario="realistic", kind="sd", convention=conv, metric="rmd", **{"lambda": lam}).gap_high_minus_low


abs_grow = abs(g("absolute", 1.0)) - abs(g("absolute", 0.0))
std_shrink = abs(g("standardised", 0.0)) - abs(g("standardised", 1.0))
check(not (abs_grow > 1.5 and std_shrink > 1.5), "the trade-off criterion would have been met")
check(abs_grow < 1.5 and std_shrink > 1.5, f"expected: abs change {abs_grow:+.2f} (< 1.5) and std shrink {std_shrink:+.2f} (> 1.5)")
trade_md = block(txt["tradeoff_summary.md"], "Scenario: realistic")
check("-2.86" in trade_md and "+2.27" in trade_md and "-3.37" in trade_md and "+0.34" in trade_md, "criterion cells not found in tradeoff_summary.md")
print(f"5. criterion: absolute gap changes in size by {abs_grow:+.2f} d (needed > +1.5), standardised by {-std_shrink:+.2f} d")

# ------------------------------------------------------------------ 6. macros and commits
used = set(re.findall(r"\\([A-Za-z]+)\b", main))
body_macros = {u for u in used if u in macros}
undefined = [u for u in re.findall(r"\\([A-Z][A-Za-z]+)\{\}", main) if u not in macros and u not in {"zenodoDOI", "repo", "commit"}]
check(not undefined, f"macros used but not defined: {sorted(set(undefined))}")
print(f"6. {len(body_macros)} of {len(macros)} number macros are used in main.tex")

hashes = re.findall(r"\\texttt\{([0-9a-f]{7})\}", main)
repo = ROOT.parent
try:
    log = subprocess.run(["git", "-C", str(repo), "log", "--format=%h %ci"], capture_output=True, text=True, check=True).stdout
    known = {ln.split()[0] for ln in log.splitlines()}
    for h in hashes:
        check(h in known, f"commit {h} from Appendix D is not in the repository history")
    print(f"   {len(hashes)} commits of Appendix D found in git history")
except Exception:
    print("   (no git history here: the commit list in Appendix D was not checked; run this script inside the repository)")

print(f"\n{n_checks} checks, {len(fails)} failures")
sys.exit(1 if fails else 0)

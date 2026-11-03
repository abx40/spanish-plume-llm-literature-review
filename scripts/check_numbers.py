"""Recompute the manuscript's numbers from the tables in this repository.

Each line prints a value as the manuscript reports it, recomputed from the data, and
the script stops with an error if any value differs. The usage-flag, configuration
and prefrontal-trough rows of Table 4 need the benchmark's full database, which is
not in this repository; for those, Data/reading/extraction.csv gives the scores.

Usage: python3 scripts/check_numbers.py
"""
from __future__ import annotations

import csv
import statistics
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "Data"


def read_csv(path: str) -> list[dict[str, str]]:
    with (DATA / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check(label: str, got, expected) -> None:
    ok = got == expected if not isinstance(expected, float) else abs(got - expected) < 0.005
    print(f"{'ok ' if ok else 'BAD'} {label}: {got}")
    if not ok:
        raise SystemExit(f"{label}: recomputed {got}, manuscript reports {expected}")


def pct(part: int, whole: int) -> int:
    return int(100 * part / whole + 0.5)


bench = {r["source_id"]: r for r in read_csv("discovery/benchmark/benchmark_reference.csv")}
year = {sid: int(r["year"]) for sid, r in bench.items()}
klass = {sid: r["benchmark_class"] for sid, r in bench.items()}
key = {sid for sid, c in klass.items() if c != "passing"}
check("corpus size", len(bench), 102)
check("benchmark classes", dict(Counter(klass.values())), {"passing": 84, "informative": 14, "essential": 4})

print("\nSection 3: finding the articles (Table 2, Fig. 2)")
disc = {r["source_id"]: r for r in read_csv("discovery/per_paper_discovery.csv")}
for col, label, n, n_key in [("codex_listed", "Codex", 42, 10), ("chatgpt_listed", "ChatGPT Deep Research", 40, 12),
                             ("gemini_listed", "Gemini Deep Research", 16, 7), ("claude_code_listed", "Claude Code", 15, 4),
                             ("claude_web_listed", "Claude web interface", 7, 5)]:
    check(f"{label} found", sum(int(disc[s][col]) for s in bench), n)
    check(f"{label} found of the 18 substantial", sum(int(disc[s][col]) for s in key), n_key)
pooled = {s for s in bench if disc[s]["pooled_documented"] == "1"}
check("found by at least one tool", len(pooled), 57)
recent = [s for s in bench if year[s] >= 2020]
middle = [s for s in bench if 1995 <= year[s] <= 2019]
check("articles from 2020 onward found (of 27)", (sum(s in pooled for s in recent), len(recent)), (21, 27))
check("articles from 1995-2019 found (of 71)", (sum(s in pooled for s in middle), len(middle)), (34, 71))
check("essential articles found", sum(s in pooled for s in bench if klass[s] == "essential"), 3)
check("median year: found, corpus", (statistics.median(year[s] for s in pooled), statistics.median(year.values())), (2018, 2015))

print("\nSection 3: journals (Table 3)")
journals = {r["journal"]: r for r in read_csv("access_barriers/journal_recall.csv")}
for name, total, found in [("Weather", 35, 13), ("Quarterly Journal of the Royal Meteorological Society", 13, 9),
                           ("Atmospheric Research", 7, 4), ("International Journal of Climatology", 6, 6),
                           ("Weather and Forecasting", 5, 5), ("Monthly Weather Review", 4, 3),
                           ("Journal of Geophysical Research: Atmospheres", 3, 0), ("Meteorological Applications", 3, 2),
                           ("Natural Hazards and Earth System Sciences", 3, 3)]:
    check(name, (int(journals[name]["articles_in_corpus"]), int(journals[name]["documented"])), (total, found))

print("\nSection 3: login test (Figs. 3 and 4)")
auth = read_csv("authentication/per_paper_matches.csv")
for col, n in [("codex_before", 42), ("codex_after", 82), ("claude_before", 15), ("claude_after", 79)]:
    check(f"{col} found", sum(int(r[col]) for r in auth), n)
pre2000 = [r for r in auth if int(r["year"]) < 2000]
since2020 = [r for r in auth if int(r["year"]) >= 2020]
for col, a, b in [("codex_before", 28, 59), ("claude_before", 6, 33), ("codex_after", 72, 74), ("claude_after", 39, 93)]:
    check(f"{col}: % before 2000, % from 2020", (pct(sum(int(r[col]) for r in pre2000), len(pre2000)),
                                                  pct(sum(int(r[col]) for r in since2020), len(since2020))), (a, b))
pre1995 = [r for r in auth if int(r["year"]) < 1995]
check("Codex, articles before 1995 found before/after login (of 4)",
      (sum(int(r["codex_before"]) for r in pre1995), sum(int(r["codex_after"]) for r in pre1995)), (0, 3))
wiley = [r for r in auth if r["publisher_group"] == "Wiley"]
check("Wiley articles", len(wiley), 62)
check("Wiley: Codex before/after, Claude Code before/after",
      tuple(sum(int(r[c]) for r in wiley) for c in ("codex_before", "codex_after", "claude_before", "claude_after")), (21, 53, 12, 53))
ams = [r for r in auth if r["publisher_group"] == "AMS"]
check("AMS articles found before login: Codex, Claude Code (of 11)",
      (sum(int(r["codex_before"]) for r in ams), sum(int(r["claude_before"]) for r in ams), len(ams)), (8, 0, 11))
check("AMS articles found by at least one search tool", sum(r["source_id"] in pooled for r in ams), 10)
groups = {r["publisher_group"] for r in auth}
check("publisher groups where Claude Code found none before login",
      (sum(all(r["claude_before"] == "0" for r in auth if r["publisher_group"] == g) for g in groups), len(groups)), (5, 7))

print("\nSection 4: interpreting the articles (Table 4, Fig. 5)")
coding = read_csv("reading/per_paper_coding_and_quote_check.csv")
PASSING_ROLES = {"PASSING_MENTION", "NO_BODY_EVIDENCE"}
for tool, fp_expected, kappa_expected, precision, f1 in [("codex", 66, 0.09, 0.21, 0.35),
                                                          ("notebooklm", 65, 0.09, 0.22, 0.36),
                                                          ("claude", 34, 0.34, 0.35, 0.51)]:
    bench_sub = [r["benchmark_class"] != "passing" for r in coding]
    tool_sub = [r[f"{tool}_term_role"] not in PASSING_ROLES for r in coding]
    tp = sum(b and t for b, t in zip(bench_sub, tool_sub))
    fp = sum(t and not b for b, t in zip(bench_sub, tool_sub))
    tn = sum(not b and not t for b, t in zip(bench_sub, tool_sub))
    n = len(coding)
    agree = (tp + tn) / n
    chance = (sum(bench_sub) * sum(tool_sub) + (n - sum(bench_sub)) * (n - sum(tool_sub))) / n / n
    kappa = (agree - chance) / (1 - chance)
    prec, rec = tp / (tp + fp), tp / sum(bench_sub)
    check(f"{tool}: substantial correct (of 18), passing misclassified (of 84)", (tp, fp), (18, fp_expected))
    check(f"{tool}: kappa", round(kappa, 2), kappa_expected)
    check(f"{tool}: precision, recall, F1", (round(prec, 2), round(rec, 2), round(2 * prec * rec / (prec + rec), 2)),
          (precision, 1.0, f1))
for tool, offered, verbatim, altered in [("codex", 100, 100, 0), ("notebooklm", 101, 94, 7), ("claude", 101, 101, 0)]:
    verdicts = Counter(r[f"{tool}_quote_verdict"] for r in coding)
    check(f"{tool}: quotations offered, word for word, altered",
          (102 - verdicts["n"], sum(verdicts[v] for v in "PJX"), verdicts["A"]), (offered, verbatim, altered))
check("Codex quotations on the stated PDF page", Counter(r["codex_quote_verdict"] for r in coding)["P"], 100)
check("Claude quotations on the stated PDF page", Counter(r["claude_quote_verdict"] for r in coding)["P"], 98)

print("\nSection 5: the syntheses (Tables 5 and 6)")
coverage = {r["system"]: r for r in read_csv("synthesis/citation_coverage.csv")}
cited = read_csv("synthesis/per_paper_citations.csv")
for system, col, expected in [("NotebookLM", "notebooklm_cited", (4, 12, 25, 41)), ("Codex", "codex_cited", (4, 9, 14, 27)),
                              ("Claude", "claude_cited", (4, 14, 61, 79))]:
    counts = tuple(sum(int(r[col]) for r in cited if r["benchmark_class"] == c) for c in ("essential", "informative", "passing"))
    check(f"{system}: essential, informative, passing, total cited", counts + (sum(counts),), expected)
    row = coverage["Claude Opus 5" if system == "Claude" else system]
    assert (int(row["essential_of_4"]), int(row["informative_of_14"]), int(row["passing_of_84"]), int(row["total_cited"])) == expected
    check(f"{system}: median year cited", statistics.median(int(r["year"]) for r in cited if r[col] == "1"),
          {"NotebookLM": 2016, "Codex": 2012, "Claude": 2017}[system])

themes = read_csv("synthesis/per_theme_reviewer_scores.csv")
CRITERIA = ("quality", "depth", "veracity", "insight", "utility")
for r in read_csv("synthesis/reviewer_scores.csv"):
    rows = [t for t in themes if t["reviewer"] == r["reviewer"] and t["system"] == r["system"]]
    check(f"Reviewer {r['reviewer']}, {r['system']}: criterion means",
          tuple(round(statistics.mean(int(t[c]) for t in rows), 1) for c in CRITERIA),
          tuple(float(r[c]) for c in CRITERIA))
pairs = {}
for t in themes:
    for c in CRITERIA:
        pairs.setdefault((t["system"], t["theme"], c), {})[t["reviewer"]] = int(t[c])
diffs = [p["A"] - p["B"] for p in pairs.values()]
check("ratings per reviewer", len(diffs), 150)
check("exact agreement, within one point (%)", (pct(sum(d == 0 for d in diffs), 150), pct(sum(abs(d) <= 1 for d in diffs), 150)), (24, 67))
check("Reviewer A minus Reviewer B, mean", round(statistics.mean(diffs), 2), 0.94)
print("\nAll recomputed values match the manuscript.")

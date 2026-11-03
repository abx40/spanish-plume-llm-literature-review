#!/usr/bin/env python3
"""Export per-paper and figure data for the public experiment archive."""

from __future__ import annotations

import csv
import glob
import json
import statistics
from pathlib import Path

from build_appendix_tables import load_tables, quote_status, synthesis_citations
from publisher_groups import ORDER as PUBLISHER_ORDER, publisher_group


ROOT = Path(".")  # run from the project folder
OUT = ROOT / "public_archive"
BINS = [
    (1965, 1999, "pre-2000"),
    (2000, 2009, "2000-09"),
    (2010, 2014, "2010-14"),
    (2015, 2019, "2015-19"),
    (2020, 2024, "2020-24"),
]
MODELS = {"1": "NotebookLM", "2": "Codex", "3": "Claude"}
CLASS = {"SP": "essential", "NP": "informative", "P": "passing"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    canon = {
        row["source_id"]: row
        for row in read_csv(ROOT / "spanish_plume_corpus/database/canonical_102.csv")
    }
    ids = sorted(canon)
    assert len(ids) == 102
    year = {sid: int(canon[sid]["year"]) for sid in ids}
    klass = {
        sid: CLASS[canon[sid]["how_cited"].split(",")[0].strip().upper()]
        for sid in ids
    }

    # Discovery outputs (per_paper_discovery.csv, discovery_year_histogram.csv) are
    # written by reconcile_discovery.py from the itemized model lists, not here.
    benchmark_fields = ["source_id", "canonical_database_number", "title", "authors",
                        "year", "journal", "volume", "issue", "pages",
                        "source_search_codes", "how_cited", "benchmark_class"]
    benchmark = [
        {**{key: canon[sid][key] for key in benchmark_fields[:-1]},
         "benchmark_class": klass[sid]}
        for sid in ids
    ]
    write_csv(OUT / "Data/discovery/benchmark/benchmark_reference.csv",
              benchmark_fields, benchmark)
    years = list(range(min(year.values()), max(year.values()) + 1))

    matches = json.loads((ROOT / "analysis/auth_runs_corpus_matches.json").read_text())
    matched = {key: set(value) for key, value in matches.items()}
    assert {key: len(value) for key, value in matched.items()} == {
        "codex_before": 42, "codex_after": 82,
        "claude_before": 15, "claude_after": 79,
    }
    authentication = [
        dict(source_id=sid, year=year[sid], benchmark_class=klass[sid],
             **{key: int(sid in matched[key]) for key in matched})
        for sid in ids
    ]
    def mean_recall(keys: tuple[str, str], pool: list[str]) -> float:
        return statistics.mean(
            100 * len(matched[key].intersection(pool)) / len(pool)
            for key in keys
        )

    period_rows = []
    for lo, hi, label in BINS:
        pool = [sid for sid in ids if lo <= year[sid] <= hi]
        period_rows.append(dict(
            period=label, first_year=lo, last_year=hi, n=len(pool),
            before_mean_percent=round(mean_recall(("codex_before", "claude_before"), pool), 6),
            after_mean_percent=round(mean_recall(("codex_after", "claude_after"), pool), 6),
        ))
    write_csv(
        OUT / "Figures/plot_data/access_age.csv", list(period_rows[0]), period_rows,
    )

    # Publisher group comes from the benchmark's journal name. It is not an access label.
    for row in authentication:
        row["publisher_group"] = publisher_group(canon[row["source_id"]]["journal"])
    write_csv(
        OUT / "Data/authentication/per_paper_matches.csv",
        list(authentication[0]), authentication,
    )
    publisher_rows = []
    for group in PUBLISHER_ORDER:
        pool = [row for row in authentication if row["publisher_group"] == group]
        publisher_rows.append(dict(
            publisher_group=group, articles_in_corpus=len(pool),
            **{key: sum(row[key] for row in pool) for key in matched},
        ))
    assert sum(row["articles_in_corpus"] for row in publisher_rows) == 102
    assert {key: sum(row[key] for row in publisher_rows) for key in matched} == {
        key: len(matched[key]) for key in matched}
    write_csv(
        OUT / "Figures/plot_data/publisher_login.csv",
        list(publisher_rows[0]), publisher_rows,
    )

    tables = load_tables()
    verdict = quote_status(tables)
    reading = [
        dict(source_id=sid, benchmark_class=klass[sid],
             **{f"{name.lower()}_term_role": tables[name][sid]["term_role"].split(":")[0].strip()
                for name in ("Codex", "NotebookLM", "Claude")},
             **{f"{name.lower()}_quote_verdict": verdict[(name, sid)]
                for name in ("Codex", "NotebookLM", "Claude")})
        for sid in ids
    ]
    write_csv(
        OUT / "Data/reading/per_paper_coding_and_quote_check.csv",
        list(reading[0]), reading,
    )

    cited = synthesis_citations()
    assert {key: len(value) for key, value in cited.items()} == {"1": 41, "2": 27, "3": 79}
    synthesis = [
        dict(source_id=sid, year=year[sid], benchmark_class=klass[sid],
             notebooklm_cited=int(sid in cited["1"]),
             codex_cited=int(sid in cited["2"]),
             claude_cited=int(sid in cited["3"]))
        for sid in ids
    ]
    write_csv(
        OUT / "Data/synthesis/per_paper_citations.csv",
        list(synthesis[0]), synthesis,
    )
    write_csv(
        OUT / "Figures/plot_data/key_paper_positions.csv",
        list(synthesis[0]), [row for row in synthesis if row["benchmark_class"] != "passing"],
    )
    citation_years = []
    for model, column in (("NotebookLM", "notebooklm_cited"),
                          ("Codex", "codex_cited"), ("Claude Opus 5", "claude_cited")):
        for yr in years:
            pool = [row for row in synthesis if row["year"] == yr]
            found = sum(row[column] for row in pool)
            citation_years.append(dict(model=model, year=yr, cited=found,
                                       not_cited=len(pool) - found))
    write_csv(
        OUT / "Figures/plot_data/citation_year_histograms.csv",
        list(citation_years[0]), citation_years,
    )

    ratings = json.loads((ROOT / "analysis/assessor_ratings.json").read_text())
    score_rows = read_csv(OUT / "Data/synthesis/reviewer_scores.csv")
    criteria = ("quality", "depth", "veracity", "insight", "utility")
    theme_rows = []
    for row in score_rows:
        reviewer = row["reviewer"]
        model = next(n for n, label in MODELS.items() if label == row["system"])
        all_scores = []
        for theme in range(1, 11):
            values = {
                criterion: ratings[reviewer][f"{model}|{theme}|{criterion}"]
                if reviewer == "A" else ratings[reviewer][f"{model}|{theme}"][criterion]
                for criterion in criteria
            }
            theme_rows.append(dict(reviewer=reviewer, system=row["system"],
                                   theme=theme, **values,
                                   mean=round(statistics.mean(values.values()), 2)))
        for criterion in criteria:
            values = [
                ratings[reviewer][f"{model}|{theme}|{criterion}"]
                if reviewer == "A" else ratings[reviewer][f"{model}|{theme}"][criterion]
                for theme in range(1, 11)
            ]
            assert abs(statistics.mean(values) - float(row[criterion])) < 0.051
            all_scores.extend(values)
        assert abs(statistics.mean(all_scores) - float(row["mean"])) < 0.006
    write_csv(
        OUT / "Data/synthesis/per_theme_reviewer_scores.csv",
        list(theme_rows[0]), theme_rows,
    )

    for path in sorted((OUT / "Figures/plot_data").glob("*.csv")):
        print(path.relative_to(OUT))
    print("Exported 102-row experiment tables and verified report totals.")


if __name__ == "__main__":
    main()

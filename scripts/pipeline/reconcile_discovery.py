"""Rebuild the public discovery tables from itemized model outputs.

The match lists below were checked against the saved eligible-paper tables by
title, author, year, and DOI. A zero means "not listed", not "not found";
Gemini's 19 unitemized claimed records cannot be assigned to corpus rows.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(".")  # run from the project folder
PUBLIC = ROOT / "public_archive"
DISCOVERY = PUBLIC / "Data/discovery"

MATCHES = {
    "codex_listed": set(json.loads((ROOT / "analysis/auth_runs_corpus_matches.json").read_text())["codex_before"]),
    "chatgpt_listed": set("""SP003 SP012 SP013 SP014 SP020 SP023 SP031 SP035 SP034 SP038
        SP040 SP046 SP050 SP051 SP056 SP063 SP065 SP062 SP070 SP069 SP073 SP074
        SP079 SP076 SP077 SP080 SP081 SP087 SP088 SP085 SP083 SP092 SP094 SP090
        SP095 SP091 SP098 SP100 SP102 SP097""".split()),
    "gemini_listed": set("""SP001 SP003 SP014 SP019 SP023 SP026 SP031 SP034
        SP042 SP046 SP050 SP056 SP063 SP081 SP088 SP095""".split()),
    "claude_code_listed": set("""SP013 SP034 SP046 SP053 SP070 SP073 SP078 SP080
        SP084 SP085 SP087 SP090 SP092 SP100 SP102""".split()),
    "claude_web_listed": set("SP034 SP013 SP014 SP031 SP061 SP046 SP102".split()),
}


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalized_journal(name: str) -> str:
    return name.split(":", 1)[0].strip().lower()


def main() -> None:
    benchmark = list(csv.DictReader((DISCOVERY / "benchmark/benchmark_reference.csv").open(encoding="utf-8-sig")))
    ids = {row["source_id"] for row in benchmark}
    assert len(ids) == len(benchmark) == 102
    expected = {"codex_listed": 42, "chatgpt_listed": 40, "gemini_listed": 16,
                "claude_code_listed": 15, "claude_web_listed": 7}
    assert {key: len(value) for key, value in MATCHES.items()} == expected
    for key, values in MATCHES.items():
        assert values <= ids, (key, values - ids)
    pooled = set().union(*MATCHES.values())
    assert len(pooled) == 57

    matrix = []
    for source_id in sorted(ids):
        row = {"source_id": source_id}
        row.update({name: int(source_id in values) for name, values in MATCHES.items()})
        row["pooled_documented"] = int(source_id in pooled)
        matrix.append(row)
    write_csv(DISCOVERY / "per_paper_discovery.csv", list(matrix[0]), matrix)

    summary = [
        dict(system="Codex (GPT-5.6 Sol)", type="coding agent", raw_records_reported=88,
             unique_candidates_reported=88, additional_eligible_records=13,
             eligible_claimed=42, eligible_itemized=42, benchmark_matches_documented=42),
        dict(system="ChatGPT Deep Research (GPT-5.6 Sol)", type="online assistant", raw_records_reported="",
             unique_candidates_reported=61, additional_eligible_records="",
             eligible_claimed=40, eligible_itemized=40, benchmark_matches_documented=40),
        dict(system="Gemini Deep Research (Gemini 3.1 Pro)", type="online assistant", raw_records_reported=277,
             unique_candidates_reported=185, additional_eligible_records="",
             eligible_claimed=35, eligible_itemized=16, benchmark_matches_documented=16),
        dict(system="Claude Code (Claude Opus 5)", type="coding agent", raw_records_reported=159,
             unique_candidates_reported=130, additional_eligible_records="",
             eligible_claimed=15, eligible_itemized=15, benchmark_matches_documented=15),
        dict(system="Claude web (Claude Opus 5)", type="online assistant", raw_records_reported="",
             unique_candidates_reported=13, additional_eligible_records="",
             eligible_claimed=7, eligible_itemized=7, benchmark_matches_documented=7),
        dict(system="At least one itemized list", type="pooled", raw_records_reported="",
             unique_candidates_reported="", additional_eligible_records="",
             eligible_claimed="", eligible_itemized="", benchmark_matches_documented=57),
    ]
    write_csv(DISCOVERY / "summary.csv", list(summary[0]), summary)

    manifest = {row["source_id"]: row for row in csv.DictReader(
        (ROOT / "search_and_access_results/corpus_access_audit/download_manifest.csv").open(encoding="utf-8-sig"))}
    assert set(manifest) == ids
    access_rows = []
    for source_id in sorted(ids):
        status = manifest[source_id]["download_status"]
        assert status in {"downloaded_automatically", "imported_manual"}
        access_rows.append({"source_id": source_id, "retrieval_route":
                            "automatic" if status == "downloaded_automatically" else "manual_import"})
    write_csv(PUBLIC / "Data/access_barriers/access_status.csv", list(access_rows[0]), access_rows)

    publishers = {
        "weather and forecasting": "AMS", "monthly weather review": "AMS",
        "international journal of climatology": "Wiley (RMetS)",
        "quarterly journal of the royal meteorological society": "Wiley (RMetS)",
        "weather": "Wiley (RMetS)", "meteorological applications": "Wiley (RMetS)",
        "atmospheric research": "Elsevier",
        "journal of geophysical research": "Wiley (AGU)",
        "natural hazards and earth system sciences": "Copernicus",
    }
    display = {
        "weather": "Weather",
        "quarterly journal of the royal meteorological society": "Quarterly Journal of the Royal Meteorological Society",
        "atmospheric research": "Atmospheric Research",
        "international journal of climatology": "International Journal of Climatology",
        "weather and forecasting": "Weather and Forecasting",
        "monthly weather review": "Monthly Weather Review",
        "journal of geophysical research": "Journal of Geophysical Research: Atmospheres",
        "meteorological applications": "Meteorological Applications",
        "natural hazards and earth system sciences": "Natural Hazards and Earth System Sciences",
    }
    groups = defaultdict(list)
    for row in benchmark:
        groups[normalized_journal(row["journal"])].append(row["source_id"])
    journal_rows = []
    for name, members in sorted(groups.items(), key=lambda pair: (-len(pair[1]), pair[0])):
        if len(members) < 3:
            continue
        documented = len(pooled.intersection(members))
        journal_rows.append(dict(journal=display.get(name, name), publisher=publishers.get(name, ""),
                                 articles_in_corpus=len(members), documented=documented,
                                 documented_percent=round(100 * documented / len(members))))
    write_csv(PUBLIC / "Data/access_barriers/journal_recall.csv", list(journal_rows[0]), journal_rows)

    by_year = defaultdict(lambda: [0, 0])
    for row in benchmark:
        source_id, year = row["source_id"], int(row["year"])
        by_year[year][0 if source_id in pooled else 1] += 1
    years = [dict(year=year, documented=by_year[year][0], not_documented=by_year[year][1])
             for year in range(min(by_year), max(by_year) + 1)]
    write_csv(PUBLIC / "Figures/plot_data/discovery_year_histogram.csv", list(years[0]), years)
    print("documented matches:", {name: len(values) for name, values in MATCHES.items()})
    print("pooled:", len(pooled), "not documented:", len(ids - pooled))


if __name__ == "__main__":
    main()

# Scripts

Python 3 with matplotlib and numpy. Run every command from the repository root.

## Redraw the figures

`figures/` holds one script per manuscript figure. Each reads only files in this
repository and writes its PNG to `Figures/images/`, or to a folder given as the
first argument. They reproduce the published images exactly.

| Script | Manuscript figure | Reads |
| --- | --- | --- |
| `fig1_workflow.py` | Fig. 1, workflow of the study | nothing (a diagram) |
| `fig2_discovery_year_histogram.py` | Fig. 2, articles found by year | `Figures/plot_data/discovery_year_histogram.csv`, discovery tables |
| `fig3_access_age.py` | Fig. 3, login test by publication period | `Data/authentication/per_paper_matches.csv` |
| `fig4_publisher_login.py` | Fig. 4, login test by publisher | `Figures/plot_data/publisher_login.csv`, `Data/authentication/per_paper_matches.csv` |
| `fig5_confusion_matrices.py` | Fig. 5, substantial/passing classification | `Figures/plot_data/confusion_matrices.csv` |
| `fig6_key_paper_positions.py` | Fig. 6, articles cited in each synthesis (also writes the PDF used in the manuscript) | benchmark reference, `Data/synthesis/per_paper_citations.csv` |
| `fig7_citation_year_histograms.py` | Fig. 7, articles cited by year | `Figures/plot_data/citation_year_histograms.csv` |

```
python3 scripts/figures/fig2_discovery_year_histogram.py /tmp/figures
```

## Check the numbers

```
python3 scripts/check_numbers.py
```

recomputes the counts, percentages and scores reported in the manuscript from the
tables in `Data/` and stops if any differs. Three rows of Table 4 (the two usage
senses, configuration and prefrontal trough) are scored against fields of the
benchmark's full database, which is not in this repository; it is available from
its own DOI (see `Data/discovery/benchmark/README.md`).

## Pipeline that built the tables

`pipeline/` holds the scripts that produced the tables in `Data/` from the tools'
original outputs. They are included as a record of the method and do not run on
this repository alone: they also need the article PDFs, the benchmark's full
database and the project's working folders, which are not public. They expect to be
run from the project folder that held those files.

| Script | What it did |
| --- | --- |
| `reconcile_discovery.py` | Matched each search tool's itemized list to the 102 articles; wrote the discovery tables and the journal table. |
| `match_auth_runs_to_corpus.py` | Matched the before- and after-login search reports to the 102 articles by DOI and title. |
| `publisher_groups.py` | Maps each journal to a publisher group. |
| `score_extraction_tables.py` | Scored the three tools' databases against the benchmark database (Table 4). |
| `verify_extraction_quotes.py` | Checked every database quotation against the supplied PDFs. Quotations it could not find were then reviewed by hand (`Data/reading/raw_data/manual_quote_review.json`). |
| `build_appendix_tables.py` | Loads the tools' tables, the quotation verdicts and the synthesis citations; used by the export script. |
| `export_public_experiment_data.py` | Wrote the per-paper tables and plot data in this repository. |

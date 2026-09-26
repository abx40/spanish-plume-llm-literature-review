# Spanish Plume LLM literature-review experiments

This repository holds the data used in *Can Large Language Models Review the
Scientific Literature? A Test Against a 102-Article Benchmark on the Spanish
Plume* (draft manuscript, September 2026).

## Layout

Each experiment has clean tables directly in its folder. Original model outputs
and ratings are in that experiment's `raw_data/` subfolder.

| Section | Source material | Published tables |
| --- | --- | --- |
| `Data/discovery/` | Five open-search model reports. | Model match counts and per-paper pooled matches. The separately credited benchmark reference is in `benchmark/`. |
| `Data/access_barriers/` | The discovery reports above are the source outputs. | The separate post-search omission/access audit and journal-level comparison. |
| `Data/authentication/` | Codex and Claude Code search reports before and after university login. | Per-paper matches and before/after benchmark recall. |
| `Data/reading/` | Three complete 102-row model-built evidence tables, the first automated quotation check, and manual review corrections. | Database scores and corrected per-paper coding/quotation verdicts. |
| `Data/synthesis/` | Three raw ten-theme syntheses and anonymized per-theme reviewer ratings. | Reviewer means, citation coverage, and per-paper citation flags. |

The locked prompt for each experiment is at `Data/<experiment>/prompt.md`.
`Figures/images/` contains only the five figures in the manuscript;
`Figures/plot_data/` contains the values plotted in each one.

The discovery benchmark is adapted from [Schultz, Lowe, and Herrerias Azcue's
2024 dataset](https://doi.org/10.48420/28022981.v1), published under CC BY 4.0,
and accompanies the [2025 review by Schultz, Young, and
Kirshbaum](https://doi.org/10.1175/MWR-D-24-0139.1). Its original fields and
this project's derived labels are identified in the
[benchmark source note](Data/discovery/benchmark/README.md).

## Interpretation

- The five initial discovery runs had no institutional login, but browser state
  was not otherwise uniform. They are separate from the paired authentication
  experiment. Model-reported eligible totals in the raw search reports are not
  the same measure as matches to the 102-paper benchmark.
- The access-barrier omission audit excludes legacy row `SP101` from the
  manuscript's 41-paper missed set. It is a post-search analysis, not a model
  output. Join discovery results to
  `Data/discovery/benchmark/benchmark_reference.csv` by `source_id`; benchmark
  labels and bibliographic fields are not model findings.
- The authentication figure uses OpenAlex open-access status, available for 96
  of the 102 articles. The other six are marked `uncovered` in the clean table.
- The raw automated quotation check flagged 14 missing-text results. Manual
  review found seven verbatim matches and seven altered quotations.
  `Data/reading/raw_data/manual_quote_review.json` records this review, and
  the corrected verdicts are in `Data/reading/per_paper_coding_and_quote_check.csv`.
  A verbatim-text verdict does not establish that the model's page locator is
  correct; the code meanings are described below.
- Reviewer A and B are anonymized. The raw ratings use Synthesis 1 =
  NotebookLM, 2 = Codex, and 3 = Claude Code; the clean means use model names.
  The raw syntheses are original model outputs and may contain incorrect claims
  or page citations.
- One institutional IP address was redacted from the public copy of
  `Data/authentication/raw_data/claude_after.md`; no result was changed.

Quotation-verdict codes in the clean reading table: `P` = verbatim on the
stated PDF page; `J` = verbatim when the locator is interpreted as a printed
journal page; `X` = verbatim elsewhere in the article; `V` = verbatim on manual
review with locator unresolved; `A` = wording altered; `n` = no quote offered.
These codes are not a complete manual page-location audit.

The `SPxxx` identifiers are local corpus IDs, not the published benchmark's row
numbers. The credited benchmark reference includes the original database
numbers and the crosswalk; see its [source note](Data/discovery/benchmark/README.md).

Publisher-hosted article PDFs, the full benchmark database, private browser
authentication material, and named reviewer correspondence are not included.
The model-built tables contain model-extracted quotations; consult the original
articles and their rights holders before reusing that text.

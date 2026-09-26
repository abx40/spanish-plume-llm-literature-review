# Spanish Plume LLM literature-review experiments

This repository holds the data used in *Can Large Language Models Review the
Scientific Literature? A Test Against a 102-Article Benchmark on the Spanish
Plume* (draft manuscript, September 2026).

## Layout

Each experiment has its own `raw_data` (model outputs or original ratings) and
`clean_data` (matched, checked, or aggregated results used in the report).

| Experiment | Raw data | Clean data |
| --- | --- | --- |
| `Data/discovery/` | Five open-search model reports. | Benchmark matches, journal recall, omission audit, and the `SPxxx` bibliographic crosswalk. |
| `Data/authentication/` | Codex and Claude Code search reports before and after university login. | Per-paper matches and before/after benchmark recall. |
| `Data/reading/` | Three complete 102-row model-built evidence tables, the first automated quotation check, and manual review corrections. | Database scores and corrected per-paper coding/quotation verdicts. |
| `Data/synthesis/` | Three raw ten-theme syntheses and anonymized per-theme reviewer ratings. | Reviewer means, citation coverage, and per-paper citation flags. |

The locked prompt for each experiment is at `Data/<experiment>/prompt.md`.
`Figures/images/` contains only the five figures in the manuscript;
`Figures/plot_data/` contains the values plotted in each one.

## Interpretation

- The five initial discovery runs had no institutional login, but browser state
  was not otherwise uniform. They are separate from the paired authentication
  experiment. Model-reported eligible totals in the raw search reports are not
  the same measure as matches to the 102-paper benchmark.
- In the discovery omission audit, `SP101` is a legacy audit row excluded from
  the manuscript's 41-paper missed set. The clean per-paper table follows the
  manuscript. `missed_manual_required` is defined only among missed papers; it
  is not a corpus-wide open-access classification.
- The authentication figure uses OpenAlex open-access status, available for 96
  of the 102 articles. The other six are marked `uncovered` in the clean table.
- The raw automated quotation check flagged 14 missing-text results. Manual
  review found seven verbatim matches and seven altered quotations.
  `Data/reading/raw_data/manual_quote_review.json` records this review, and
  the corrected verdicts are in `clean_data/per_paper_coding_and_quote_check.csv`.
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
numbers. `Data/discovery/clean_data/corpus_metadata.csv` includes the crosswalk.

Publisher-hosted article PDFs, the full benchmark database, private browser
authentication material, and named reviewer correspondence are not included.
The model-built tables contain model-extracted quotations; consult the original
articles and their rights holders before reusing that text.

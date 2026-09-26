# Spanish Plume LLM study: results reported in the manuscript

This repository contains only summary results and figures explicitly presented
in *Can Large Language Models Review the Scientific Literature? A Test Against a
102-Article Benchmark on the Spanish Plume* (draft manuscript, September 2026).

## Reported tables

- `data/discovery.csv`: Table 2, initial discovery of benchmark articles.
- `data/journal_recall.csv`: Table 3, pooled discovery by journal.
- `data/login_recall.csv`: before/after-login benchmark counts reported in the text.
- `data/extraction.csv`: Table 4, coded database comparison and quotation audit.
- `data/reviewer_scores.csv`: Table 5, mean blinded ratings by reviewer.
- `data/citation_coverage.csv`: Table 6, article coverage by benchmark class.

`figures/` holds only the five figure images included in the manuscript. The
CSV files reproduce reported aggregate values; they are not independent raw
datasets and do not support a full reanalysis.

The source-article PDFs, model prompts and raw outputs, full 102-row model
databases, per-paper results, blind keys, and individual reviewer scores are
**not** included. They remain with the corresponding author, subject to source
and reviewer permissions. Model outputs should be checked against the source
articles before scientific reuse.

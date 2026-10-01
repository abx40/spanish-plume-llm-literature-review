# Paired authentication search

`login_recall.csv` counts matches to the 102-paper benchmark, not every article
the systems included. `per_paper_matches.csv` and `benchmark_matches.json`
provide the underlying `SPxxx` assignments; the original reports are in
`raw_data/`.

Claude Code's authenticated report lists 80 included articles. Title and
author matching against the benchmark identifies 79 distinct benchmark
articles. Its Collier and Lilley (1994) article, *Forecasting thunderstorm
initiation in north-west Europe using thermodynamic indices, satellite and
radar data*, is outside the benchmark. The 79 include SP004 (McCallum and
Waters, 1993, report row 2) and SP077 (Steeneveld and Peerlings, 2020, report
row 58), which were omitted from an earlier match list. Eleven further
candidates that Claude marked unverified are not counted. The resulting
paired counts are Codex 42 to 82 and Claude Code 15 to 79.

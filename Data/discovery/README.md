# Discovery results

`summary.csv` separates candidate records, a model's own eligibility claim,
and papers actually itemized and matched to the 102-paper benchmark.
`per_paper_discovery.csv` records those itemized matches by local `SPxxx` ID.
Each `*_listed` zero means the paper was **not named in the saved eligible
list**; it does not prove that the model never encountered the paper.

The five saved outputs are in `raw_data/`. Codex's 42-paper column uses the
8 August cookie-cleared run, not its separate 86-paper search report. The
four other outputs were produced in late July or early August under the same
search prompt, but browser conditions were not uniform. Matches were checked
against the credited reference in `benchmark/` using title, author, year, and
DOI. Some model titles are inaccurate; a match was retained only where the
other metadata identified a benchmark paper.

Gemini reports 277 raw hits, 92 duplicates, and 242 total exclusions, yielding
35 *claimed* eligible papers. Its saved eligible table names only 16. The
other 19 cannot be assigned to benchmark rows. The five itemized lists
together name 57 distinct benchmark papers; 45 are **not documented as found**
in these lists. These are lower-bound documentation counts, not an exhaustive
recall estimate. The previously reported 61/41 split came from an earlier,
different group of runs and is not used here.

The Codex report gives 88 distinct records from the two accessible requested
databases plus 13 additional eligible papers from independent publisher and
repository searching. ChatGPT gives 61 deduplicated candidates; Claude Code
gives 130; Claude web carries 13 scholarly candidates forward and notes four
more post-cutoff records. Candidate counts therefore do not have a perfectly
uniform capture boundary and should not be ranked as search recall.

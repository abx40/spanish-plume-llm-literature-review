# Post-search access analysis

These are descriptive comparisons against the itemized model outputs, not
results returned by any one model. `access_status.csv` records whether each
benchmark PDF was obtained automatically or required manual import for the
closed-corpus project. This is an observed retrieval route, not a publisher
licensing classification. `journal_recall.csv` groups the 57 documented
benchmark matches by journal; its denominators come from the credited
benchmark in `../discovery/benchmark/`.

The older 41-paper omission audit was based on a different set of discovery
runs and was removed. Gemini names only 16 of its 35 claimed eligible papers,
so the 45 not named by any saved list must not be described as verified misses
or assigned model-specific causes.

The source reports and model-match results remain in `../discovery/`. The
authentication experiment, which directly compares runs before and after
institutional login, is in `../authentication/`.

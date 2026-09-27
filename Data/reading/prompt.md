# Final Structured Evidence-Table Prompt

Using only the supplied corpus index and PDFs SP001-SP102, create one structured
evidence-table row for every paper in exact SP-number order.

Do not use Schultz, Young, and Kirshbaum (2025), its database, web search,
outside knowledge, previous conversations, or previous model outputs. Inspect
the full paper, not only the title and abstract. A reference-list occurrence is
not evidence that the paper discusses the Spanish Plume.

This is extraction only. Do not write a synthesis, infer consensus, identify
research gaps, or suggest future work.

Use these columns in this exact order:

`source_id | term_role | concept_usage | airstream_properties |
diagnostic_variables | origin_and_transport_claim | origin_evidence |
configuration | capping_or_instability_mechanism |
capping_or_instability_evidence | initiation_mechanism |
initiation_evidence | hazards_locations_and_event_types |
prefrontal_trough | key_supporting_quote | quote_pdf_page |
limitations_or_uncertainty`

Coding rules:

- `term_role`: `ANALYTICAL_FOCUS`, `CASE_APPLICATION`,
  `CONCEPTUAL_BACKGROUND`, `PASSING_MENTION`, `NO_BODY_EVIDENCE`, or
  `UNAVAILABLE`.
- `concept_usage`: `AIRSTREAM`, `SYNOPTIC_PATTERN`, `EVENT_LABEL`,
  `FORECASTING_CONCEPT`, `OTHER`, `UNCLEAR`, or `NR`. Join multiple codes with
  `+`.
- Evidence fields must begin with `DIRECT`, `INDIRECT`, `CITED_ONLY`,
  `ASSERTED_ONLY`, `CONFLICTING`, `UNCLEAR`, or `NR`, followed by a brief reason.
- `configuration`: `CLASSIC`, `MODIFIED`, `EUROPEAN_EASTERLY`, `OTHER`,
  `UNCLASSIFIED`, `UNCLEAR`, or `NR`.
- `prefrontal_trough`: `PRESENT`, `ABSENT`, `UNCLEAR`, or `NR`. Do not treat no
  mention as evidence of absence.
- Use `NR` when a field is not reported, `UNCLEAR` when it cannot be classified,
  and `UNAVAILABLE` when the required text cannot be inspected.

Distinguish each paper's own findings from background claims attributed to other
sources. The `source_id` identifies the source for all coded fields; page numbers
are required only for the supporting quotation.

For `key_supporting_quote`, copy one verbatim passage of no more than 25 words.
Do not alter or combine text. Record its supplied-file page as `PDF p. N`. Use
`NOT_FOUND` and `NR` if no quotation can be verified, or `PAGE_UNRESOLVED` if the
page cannot be established. Never guess.

Return a UTF-8 TSV file named `spanish_plume_structured_evidence_table.tsv`, or a
fenced `tsv` block if file creation is unavailable. Include SP001-SP102 exactly
once, use one physical line per paper, leave no cells blank, and keep entries
concise.

Finish with counts for rows, unique IDs, missing or duplicate IDs, unavailable
PDFs, verified quotations, `NOT_FOUND`, and `PAGE_UNRESOLVED`. Do not claim the
table is complete unless all 102 rows are present.

# FINAL: Closed-Corpus Ten-Theme Critical Synthesis Prompt

**Status:** Final canonical prompt

**Used for:** The ten-part Spanish Plume synthesis comparison across Codex,
Claude Opus, and NotebookLM.

The scientific task and ten themes below were shared across all three systems.
Platform-specific operational instructions varied slightly: Claude was also told
where to save its output, while NotebookLM was asked to include its native source
citations and ignore previous notebook conversations.

## Prompt

Using only the supplied closed corpus, produce a critical synthesis of the
scientific literature concerning the Spanish Plume.

Do not use Schultz, Young, and Kirshbaum (2025), its database, any prior model
output or conversation, or outside knowledge as evidence.

This must be a cross-paper synthesis, not a paper-by-paper summary.

Organize the synthesis around:

1. Evolution of the term and concept
2. Airstream versus synoptic-pattern usage
3. Thermodynamic and moisture properties
4. Claimed geographical origin and transport pathways
5. Evidence used to support origin claims
6. Capping, instability, and convection-initiation mechanisms
7. Hazards, locations, and event types
8. Areas of agreement
9. Disagreements, unsupported assumptions, and uncertainty
10. Remaining research gaps

For every substantive claim:

- Cite the supporting source and one-based PDF page as `[SPxxx, PDF p. N]`.
- Distinguish:
  - Direct finding
  - Author interpretation
  - Cross-paper synthesis inference
- Weight analytical studies more heavily than passing mentions.
- Distinguish an article's own findings from background claims it attributes to
  other literature.
- Do not treat a reference-list occurrence as evidence that the paper discusses
  the Spanish Plume.
- Do not convert repeated unsupported claims into established facts.
- Identify contradictory or qualifying evidence explicitly.
- Do not describe something as consensus unless the supplied sources demonstrate
  it.
- Never guess a PDF page number. If it cannot be established, state that clearly.
- If evidence is insufficient, state: `Not established by the provided sources.`

After the narrative, provide a claim ledger with these columns:

`theme | synthesis claim | supporting sources | contradicting or qualifying sources | evidence strength | uncertainty`

Finally, state:

- How many of the 102 PDFs were inspected.
- How many received page-level citations.
- Which sources could not be used and why.
- Whether any requested claim could not be supported.


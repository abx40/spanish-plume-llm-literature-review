#!/usr/bin/env python3
"""Generate the report's data appendix as LaTeX.

Emits report/claude_draft/appendix_tables.tex, holding the per-paper results of
all three experiments and the complete rating sheets of both assessors. Every
number is recomputed here from the primary files; nothing is transcribed.
"""
from __future__ import annotations

import csv
import json
import os
import re
import statistics as st
import sys

ROOT = '.'  # run from the project folder
OUT = os.path.join(ROOT, 'report/claude_draft/appendix_tables.tex')

NAME = {'1': 'NotebookLM', '2': 'Codex', '3': 'Claude'}
CRIT = ['quality', 'depth', 'veracity', 'insight', 'utility']
THEMES = ['Evolution of the term', 'Airstream vs pattern', 'Thermodynamics and moisture',
          'Claimed origin', 'Evidence for origin', 'Capping and initiation',
          'Hazards and locations', 'Areas of agreement', 'Disagreements', 'Research gaps']
JAB = {
    'weather': 'Weather',
    'quarterly journal of the royal meteorological society': 'QJRMS',
    'international journal of climatology': 'Int. J. Climatol.',
    'weather and forecasting': 'Wea. Forecasting',
    'atmospheric research': 'Atmos. Res.',
    'journal of geophysical research: atmospheres': 'JGR Atmos.',
    'monthly weather review': 'Mon. Wea. Rev.',
    'natural hazards and earth system sciences': 'NHESS',
    'meteorologische zeitschrift': 'Meteor. Z.',
    'atmosphere': 'Atmosphere',
    'meteorological applications': 'Meteor. Appl.',
    'tellus': 'Tellus',
    'meteorol. mag': 'Meteor. Mag.',
    'meteorological magazine': 'Meteor. Mag.',
    'ann. bull. soc. jersiaise': 'Bull. Soc. Jers.',
    'meteorology and atmospheric physics': 'Meteor. Atmos. Phys.',
    'tellus a: dynamic meteorology and oceanography': 'Tellus A',
    'global and planetary change': 'Global Planet. Change',
    'int j meteorology uk': 'Int. J. Meteor.',
    'int. j. meteorol': 'Int. J. Meteor.',
    'journal of flood risk management': 'J. Flood Risk Manage.',
    'id\u0151j\u00e1r\u00e1s/quarterly journal of the hungarian meteorological service': 'Id\u0151j\u00e1r\u00e1s',
    'water': 'Water',
    'journal of climate': 'J. Climate',
    'natural hazards': 'Nat. Hazards',
    'weather and climate dynamics': 'Wea. Climate Dyn.',
    'journal of physical oceanography': 'J. Phys. Oceanogr.',
    'geophysical research letters': 'Geophys. Res. Lett.',
}


def journal(name):
    """Map a raw journal string to a short AMS-style abbreviation."""
    n = re.sub(r'\s+', ' ', (name or '').strip()).lower()
    n = re.sub(r'\s*\[discussions\]$', '', n)
    n = re.sub(r'-berlin-$', '', n).strip()
    if ':' in n and n.split(':')[0].strip() in JAB:
        n = n.split(':')[0].strip()
    return JAB.get(n, (name or '').strip())



def esc(s):
    s = str(s)
    for a, b in (('&', r'\&'), ('%', r'\%'), ('_', r'\_'), ('#', r'\#')):
        s = s.replace(a, b)
    return s


def load_tables():
    def ld(p, d):
        with open(os.path.join(ROOT, p), encoding='utf-8-sig', newline='') as f:
            return {r['source_id'].strip(): r for r in csv.DictReader(f, delimiter=d)}
    return {
        'NotebookLM': ld('table_first_experiment/notebooklm/stage_1_extraction/notebooklm_structured_evidence_table.csv', ','),
        'Codex': ld('table_first_experiment/codex/stage_1_extraction/output/codex_structured_evidence_table.tsv', '\t'),
        'Claude': ld('table_first_experiment/claude/stage_1_extraction/outputs/claude_structured_evidence_table.tsv', '\t'),
    }


def synthesis_citations():
    import pypdf
    t = "\n".join((p.extract_text() or "") for p in pypdf.PdfReader(
        os.path.join(ROOT, 'synthesis_results/reviewer_packets/Spanish_Plume_Blinded_Syntheses_By_Part.pdf')).pages)
    marks = [(m.start(), m.group(0)) for m in re.finditer(
        r"SYNTHESIS [123]|BENCHMARK SUMMARY FROM SCHULTZ|PART \d+ / 10", t)]
    blk = {"1": [], "2": [], "3": []}
    for i, (pos, lab) in enumerate(marks):
        if lab.startswith("SYNTHESIS"):
            blk[lab[-1]].append(t[pos: marks[i + 1][0] if i + 1 < len(marks) else len(t)])
    return {n: {"SP" + x for x in re.findall(r"SP(\d{3})", " ".join(blk[n]))} for n in "123"}


def quote_status(tables):
    """Combine the automated locator audit with documented manual text checks."""
    with open(os.path.join(ROOT, 'analysis/extraction_quote_verification.json')) as f:
        audit = json.load(f)
    with open(os.path.join(ROOT, 'analysis/quote_review_overrides.json')) as f:
        reviewed = json.load(f)
    out = {}
    groups = {'declined': 'n', 'journal_page': 'J',
              'wrong_page': 'X', 'absent': '--'}
    for sysname, result in audit.items():
        for sid in tables[sysname]:
            out[(sysname, sid)] = 'P'
        for group, code in groups.items():
            for sid in result['detail'][group]:
                if out[(sysname, sid)] != 'P':
                    raise ValueError(f'Duplicate quote classification: {sysname} {sid}')
                out[(sysname, sid)] = code
    for sid in reviewed['NotebookLM']['verbatim_extraction_false_negatives']:
        if out[('NotebookLM', sid)] != '--':
            raise ValueError(f'Unexpected NotebookLM automated verdict: {sid}')
        out[('NotebookLM', sid)] = 'V'
    for sid in reviewed['NotebookLM']['altered_wording']:
        if out[('NotebookLM', sid)] != '--':
            raise ValueError(f'Unexpected NotebookLM automated verdict: {sid}')
        out[('NotebookLM', sid)] = 'A'
    for sid in reviewed['Claude']['verbatim_on_stated_page']:
        if out[('Claude', sid)] != '--':
            raise ValueError(f'Unexpected Claude automated verdict: {sid}')
        out[('Claude', sid)] = 'P'
    expected = {'Codex': (100, 0, 2), 'NotebookLM': (94, 7, 1), 'Claude': (101, 0, 1)}
    for sysname, (verbatim, altered, none) in expected.items():
        codes = [v for (name, _), v in out.items() if name == sysname]
        actual = (sum(v in ('P', 'J', 'X', 'V') for v in codes),
                  codes.count('A'), codes.count('n'))
        if len(codes) != 102 or actual != (verbatim, altered, none):
            raise ValueError(f'Quote counts do not match manuscript for {sysname}: {actual}')
    return out


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'spanish_plume_corpus/database/canonical_102.csv'),
                                    encoding='utf-8-sig')))
    canon = {r['source_id']: r for r in rows}
    ids = sorted(canon)
    klass = {s: (canon[s]['how_cited'] or '').split(',')[0].strip().upper() for s in ids}

    discovery = {r['source_id']: r for r in csv.DictReader(open(os.path.join(
        ROOT, 'public_archive/Data/discovery/per_paper_discovery.csv')))}
    manifest = {r['source_id']: r for r in csv.DictReader(open(os.path.join(
        ROOT, 'search_and_access_results/corpus_access_audit/download_manifest.csv'),
        encoding='utf-8-sig'))}
    assert set(discovery) == set(manifest) == set(ids)
    manual = {s for s in ids if manifest[s]['download_status'] == 'imported_manual'}

    M = json.load(open(os.path.join(ROOT, 'analysis/auth_runs_corpus_matches.json')))
    cb, ca = set(M['codex_before']), set(M['codex_after'])
    lb, la = set(M['claude_before']), set(M['claude_after'])

    cited = synthesis_citations()
    tables = load_tables()
    qs = quote_status(tables)
    ratings = json.load(open(os.path.join(ROOT, 'analysis/assessor_ratings.json')))
    A, B = ratings['A'], ratings['B']

    L = []
    add = L.append
    add('%% Generated by scripts/build_appendix_tables.py -- do not edit by hand.')
    add(r'\clearpage')
    add(r'\begin{appendix}[B]')
    add(r'\appendixtitle{Per-Paper Discovery and Synthesis Outcomes}')
    add('')
    add(r'Table~\ref{t:b1x} gives the corpus and every per-paper outcome of the discovery '
        r'experiment. Class is the benchmark classification: E for the four essential papers, '
        r'I for the fourteen informative papers, P for the 84 passing mentions. Manual retrieval '
        r'marks records manually imported for this project; it is not a '
        r'publisher licensing classification. Documented search marks papers named in at least '
        r'one of the five saved eligible lists. Gemini named only 16 of its 35 claimed eligible '
        r'papers, so a dash means not documented rather than confirmed absent. Browser state was '
        r'not otherwise controlled uniformly. '
        r'The login columns are the two paired runs, before and '
        r'after institutional authentication.')
    add('')
    add(r'\begin{center}')
    add(r'\footnotesize')
    add(r'\begin{longtable}{llllcccccc}')
    add(r'\caption{The 102 benchmark papers and their discovery outcomes.}\label{t:b1x}\\')
    add(r'\hline\hline')
    add(r'Paper & Year & Journal & Class & Manual & Documented & \multicolumn{2}{c}{Codex} & \multicolumn{2}{c}{Claude} \\')
    add(r' & & & & retrieval & search & pre & post & pre & post \\')
    add(r'\hline')
    add(r'\endfirsthead')
    add(r'\multicolumn{10}{l}{\footnotesize Table~\ref{t:b1x}, continued}\\')
    add(r'\hline\hline')
    add(r'Paper & Year & Journal & Class & Manual & Documented & \multicolumn{2}{c}{Codex} & \multicolumn{2}{c}{Claude} \\')
    add(r' & & & & retrieval & search & pre & post & pre & post \\')
    add(r'\hline')
    add(r'\endhead')
    add(r'\hline')
    add(r'\endfoot')
    tick = lambda b: r'$\bullet$' if b else '--'
    for s in ids:
        r = canon[s]
        j = journal(r['journal'])
        cl = {'SP': 'E', 'NP': 'I', 'P': 'P'}.get(klass[s], klass[s])
        add(f"{s} & {r['year']} & {esc(j)} & {cl} & {tick(s in manual)} & {tick(discovery[s]['pooled_documented'] == '1')} & "
            f"{tick(s in cb)} & {tick(s in ca)} & {tick(s in lb)} & {tick(s in la)} \\\\")
    add(r'\end{longtable}')
    add(r'\end{center}')
    add('')
    add(r'Table~\ref{t:b2x} gives the per-paper outcomes of the synthesis and database experiments. '
        r'Cited records whether each closed-corpus synthesis cited the paper. Role is the term role '
        r'each system assigned in its database: AF analytical focus, CA case application, CB '
        r'conceptual background, PM passing mention, NB no body evidence. Quote records the '
        r"verification verdict for that system's quotation: P verbatim on the stated PDF page, J "
        r'verbatim on the page interpreted as a printed journal page, X verbatim in the article '
        r'but not at the stated location in the automated check, V verbatim in the article on '
        r'manual review but locator unverified, A wording altered, n no quotation offered. '
        r'The automated check used three PDF text-extraction modes and normalized whitespace, '
        r'hyphenation and line numbers. Manual review corrected seven false missing-text results: '
        r'six NotebookLM quotations and the Claude SP048 quotation. Seven other NotebookLM quotations '
        r'were drawn from the cited articles but changed wording without marking it (SP009, '
        r'SP010, SP017, SP019, SP020, SP028 and SP087). Page-location codes are not a '
        r'fully manual locator audit and should not be read as comparable page-accuracy rates.')
    add('')
    add(r'\begin{center}')
    add(r'\footnotesize')
    add(r'\begin{longtable}{lcccccccccc}')
    add(r'\caption{Per-paper synthesis citation, database coding and quotation verdict. '
        r'N is NotebookLM, C is Codex, L is Claude.}\label{t:b2x}\\')
    add(r'\hline\hline')
    add(r' & \multicolumn{3}{c}{Cited by} & \multicolumn{3}{c}{Role assigned} & '
        r'\multicolumn{3}{c}{Quote} \\')
    add(r'Paper & N & C & L & N & C & L & N & C & L \\')
    add(r'\hline')
    add(r'\endfirsthead')
    add(r'\multicolumn{10}{l}{\footnotesize Table~\ref{t:b2x}, continued}\\')
    add(r'\hline\hline')
    add(r' & \multicolumn{3}{c}{Cited by} & \multicolumn{3}{c}{Role assigned} & '
        r'\multicolumn{3}{c}{Quote} \\')
    add(r'Paper & N & C & L & N & C & L & N & C & L \\')
    add(r'\hline')
    add(r'\endhead')
    add(r'\hline')
    add(r'\endfoot')
    SHORT = {'ANALYTICAL_FOCUS': 'AF', 'CASE_APPLICATION': 'CA', 'CONCEPTUAL_BACKGROUND': 'CB',
             'PASSING_MENTION': 'PM', 'NO_BODY_EVIDENCE': 'NB', 'UNAVAILABLE': 'UN'}
    for s in ids:
        role = [SHORT.get(tables[m][s]['term_role'].split(':')[0].strip().upper(), '?')
                for m in ('NotebookLM', 'Codex', 'Claude')]
        qv = [qs[(m, s)] for m in ('NotebookLM', 'Codex', 'Claude')]
        add(f"{s} & {tick(s in cited['1'])} & {tick(s in cited['2'])} & {tick(s in cited['3'])} & "
            f"{role[0]} & {role[1]} & {role[2]} & {qv[0]} & {qv[1]} & {qv[2]} \\\\")
    add(r'\end{longtable}')
    add(r'\end{center}')
    add(r'\end{appendix}')
    add('')
    add(r'\clearpage')
    add(r'\begin{appendix}[C]')
    add(r'\appendixtitle{Reviewer Rating Sheets}')
    add('')
    add(r'The two reviewers rated each of the ten themes of each synthesis on five criteria, from '
        r'1 (strongly disagree) to 5 (strongly agree), giving 150 ratings each and 300 in total. '
        r'Both rated blind, without knowing which system produced which synthesis. The tables below '
        r'are the complete sheets, and the per-criterion means reported in the main text are '
        r'computed from them.')
    add('')
    for s in '123':
        add(r'\begin{table}[htbp]')
        add(r'\begin{center}')
        add(r'\footnotesize')
        add(r'\begin{tabular}{lcccccccccc}')
        add(r'\hline\hline')
        add(r' & \multicolumn{5}{c}{Reviewer A} & \multicolumn{5}{c}{Reviewer B} \\')
        add(r'Theme & Qual & Depth & Ver & Ins & Util & Qual & Depth & Ver & Ins & Util \\')
        add(r'\hline')
        for t in range(1, 11):
            a = [A[f'{s}|{t}|{c}'] for c in CRIT]
            b = [B[f'{s}|{t}'][c] for c in CRIT]
            add(f"{t}. {esc(THEMES[t-1])} & " + ' & '.join(map(str, a)) + ' & ' +
                ' & '.join(map(str, b)) + r' \\')
        add(r'\hline')
        am = [st.mean([A[f'{s}|{t}|{c}'] for t in range(1, 11)]) for c in CRIT]
        bm = [st.mean([B[f'{s}|{t}'][c] for t in range(1, 11)]) for c in CRIT]
        add('Mean & ' + ' & '.join(f'{v:.1f}' for v in am) + ' & ' +
            ' & '.join(f'{v:.1f}' for v in bm) + r' \\')
        add(r'\hline')
        add(r'\end{tabular}')
        add(r'\end{center}')
        add(rf'\caption{{Complete rating sheet for the {NAME[s]} synthesis. Criteria are writing '
            r'quality, depth and breadth, veracity, insight and utility.}'
            rf'\label{{t:c{s}}}')
        add(r'\end{table}')
        add('')
    add(r'\end{appendix}')

    with open(OUT, 'w') as f:
        f.write('\n'.join(L) + '\n')
    print('wrote', OUT)
    print(f'  A1 rows {len(ids)}; A2 rows {len(ids)}; B tables 3 x 10 themes')


if __name__ == '__main__':
    main()

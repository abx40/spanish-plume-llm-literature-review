#!/usr/bin/env python3
"""Score the structured evidence tables against the benchmark database.

Compares each system's 102-row extraction table with the four fields of the
Schultz et al. (2025) database that record the same information:
how_cited (passing vs substantive), how_used (airstream / conceptual-model
sense), classic_modified (configuration) and prefrontal_trough.

Usage: python3 scripts/score_extraction_tables.py [--json out.json]
"""
import argparse
import csv
import json
import os
import sys

ROOT = '.'  # run from the project folder
DB = os.path.join(ROOT, 'spanish_plume_corpus/database/canonical_102.csv')
TFE = os.path.join(ROOT, 'table_first_experiment')
TABLES = {
    'Codex': (os.path.join(TFE, 'codex/stage_1_extraction/output/codex_structured_evidence_table.tsv'), '\t'),
    'NotebookLM': (os.path.join(TFE, 'notebooklm/stage_1_extraction/notebooklm_structured_evidence_table.csv'), ','),
    'Claude': (os.path.join(TFE, 'claude/stage_1_extraction/outputs/claude_structured_evidence_table.tsv'), '\t'),
}


def code(v):
    """Leading controlled-vocabulary token, dropping any appended explanation."""
    return v.split(':')[0].split(';')[0].strip().split()[0].strip().upper() if v.strip() else ''


def load(path, delim):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return {r['source_id'].strip(): r for r in csv.DictReader(f, delimiter=delim)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', help='write results to this JSON file')
    args = ap.parse_args()

    rows = list(csv.DictReader(open(DB, encoding='utf-8-sig')))
    canon = {r['source_id']: r for r in rows}
    ids = sorted(canon)
    n = len(ids)

    systems = {}
    for name, (path, delim) in TABLES.items():
        if os.path.exists(path):
            systems[name] = load(path, delim)
        else:
            print(f'[skip] {name}: no table at {path}', file=sys.stderr)

    out = {}

    # 1. passing vs substantive
    dave_pass = {s: (canon[s]['how_cited'] or '').split(',')[0].strip().upper() == 'P' for s in ids}
    n_pass = sum(dave_pass.values())
    n_sub = n - n_pass
    print(f'1. PASSING vs SUBSTANTIVE (benchmark: {n_pass} passing, {n_sub} substantive)')
    for m, T in systems.items():
        missing = [s for s in ids if s not in T]
        if missing:
            print(f'   {m}: MISSING rows {missing}')
        mod_pass = {s: code(T[s]['term_role']) in ('PASSING_MENTION', 'NO_BODY_EVIDENCE') for s in ids if s in T}
        agree = sum(dave_pass[s] == mod_pass[s] for s in mod_pass)
        kept = sum((not dave_pass[s]) and (not mod_pass[s]) for s in mod_pass)
        demoted = [s for s in mod_pass if (not dave_pass[s]) and mod_pass[s]]
        promoted = sum(dave_pass[s] and (not mod_pass[s]) for s in mod_pass)
        a = sum(dave_pass[s] for s in mod_pass); b = sum(mod_pass.values()); k = len(mod_pass)
        pe = (a * b + (k - a) * (k - b)) / k / k
        kappa = ((agree / k) - pe) / (1 - pe) if pe < 1 else float('nan')
        print(f'   {m:11s} agree {agree}/{k} ({agree/k:.0%}) kappa {kappa:.2f} | substantive kept {kept}/{n_sub}, demoted {len(demoted)} {demoted}; passing promoted {promoted}/{n_pass}; called passing {b}')
        out.setdefault(m, {})['passing_vs_substantive'] = dict(agree=agree, n=k, kappa=round(kappa, 3), substantive_kept=kept, substantive_total=n_sub, demoted=demoted, passing_promoted=promoted, passing_total=n_pass, model_called_passing=b)

    # 2. term usage flags
    def dflags(s):
        u = (canon[s]['how_used'] or '').lower()
        return ('airstream' in u, 'conceptual model' in u or 'constellation' in u)
    dav = {s: dflags(s) for s in ids}
    print(f'\n2. TERM USAGE (benchmark: airstream {sum(a for a,_ in dav.values())}, pattern {sum(p for _,p in dav.values())})')
    for m, T in systems.items():
        mf = {s: ('AIRSTREAM' in T[s]['concept_usage'].upper(), 'SYNOPTIC_PATTERN' in T[s]['concept_usage'].upper()) for s in ids if s in T}
        ag_a = sum(dav[s][0] == mf[s][0] for s in mf); ag_p = sum(dav[s][1] == mf[s][1] for s in mf); k = len(mf)
        print(f'   {m:11s} airstream agree {ag_a}/{k} ({ag_a/k:.0%}); pattern agree {ag_p}/{k} ({ag_p/k:.0%}) | says airstream {sum(a for a,_ in mf.values())}, pattern {sum(p for _,p in mf.values())}')
        out[m]['usage_flags'] = dict(airstream_agree=ag_a, pattern_agree=ag_p, n=k, model_airstream=sum(a for a, _ in mf.values()), model_pattern=sum(p for _, p in mf.values()))

    # 3. configuration
    lab = {s: (canon[s]['classic_modified'] or '').strip().lower() for s in ids}
    coded = [s for s in ids if lab[s] in ('classic', 'modified', 'classic/modified')]
    print(f'\n3. CONFIGURATION (benchmark codes {len(coded)}): ' + ', '.join(f'{s}={lab[s]}' for s in coded))
    for m, T in systems.items():
        got = {s: code(T[s]['configuration']) for s in coded if s in T}
        match = sum(1 for s in coded if s in got and (
            (lab[s] == 'classic' and got[s] == 'CLASSIC') or
            (lab[s] == 'modified' and got[s] == 'MODIFIED') or
            (lab[s] == 'classic/modified' and got[s] in ('CLASSIC', 'MODIFIED'))))
        print(f'   {m:11s} matched {match}/{len(coded)} | ' + ', '.join(f'{s}={got.get(s)}' for s in coded))
        out[m]['configuration'] = dict(matched=match, coded=len(coded), values=got)

    # 4. prefrontal trough
    Y = [s for s in ids if (canon[s]['prefrontal_trough'] or '').strip().upper().startswith('Y')]
    print(f'\n4. PREFRONTAL TROUGH (benchmark Y for {len(Y)}): {Y}')
    for m, T in systems.items():
        pres = [s for s in ids if s in T and code(T[s]['prefrontal_trough']) == 'PRESENT']
        hit = [s for s in Y if s in pres]
        print(f'   {m:11s} PRESENT on {len(pres)}/{n}; of benchmark {len(Y)}: {len(hit)} caught {hit}')
        out[m]['prefrontal_trough'] = dict(present=len(pres), n=n, caught=len(hit), benchmark=len(Y), caught_ids=hit)

    if args.json:
        with open(args.json, 'w') as f:
            json.dump(out, f, indent=2)
        print(f'\nwrote {args.json}')


if __name__ == '__main__':
    main()

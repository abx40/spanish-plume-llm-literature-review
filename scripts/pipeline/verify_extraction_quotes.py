#!/usr/bin/env python3
"""Independently verify the quotations in each structured evidence table.

For every row, the recorded quotation is checked against the supplied PDF: first
on the page the system named, then anywhere in the document. This distinguishes
a verbatim quotation on the stated page from one that is real but mislocated,
and from one that does not appear in the paper at all.

Two conventions differ between systems and are accommodated so that the
comparison measures fidelity rather than house style. A quotation elided with an
ellipsis counts as located when every fragment appears verbatim. A page locator
is tested both as a position in the supplied file, which is what the schema
asked for, and as the printed journal page, using each article's first page from
the corpus index.

Usage: python3 scripts/verify_extraction_quotes.py [--json out.json]
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import unicodedata

ROOT = '.'  # run from the project folder
SOURCES = os.path.join(ROOT, 'table_first_experiment/claude/stage_1_extraction/sources')
INDEX = os.path.join(ROOT, 'table_first_experiment/claude/stage_1_extraction/corpus_index.csv')
TFE = os.path.join(ROOT, 'table_first_experiment')
TABLES = {
    'Codex': (os.path.join(TFE, 'codex/stage_1_extraction/output/codex_structured_evidence_table.tsv'), '\t'),
    'NotebookLM': (os.path.join(TFE, 'notebooklm/stage_1_extraction/notebooklm_structured_evidence_table.csv'), ','),
    'Claude': (os.path.join(TFE, 'claude/stage_1_extraction/outputs/claude_structured_evidence_table.tsv'), '\t'),
}
SENTINELS = {'NOT_FOUND', 'NR', 'PAGE_UNRESOLVED', 'UNAVAILABLE', ''}


def norm(s):
    """Squeeze to lowercase alphanumerics only.

    Dropping spaces as well as punctuation makes the comparison immune to
    hyphenation across line breaks, column and page breaks, and the spacing
    artefacts of PDF text extraction, none of which are errors by the system
    that recorded the quotation.
    """
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    # Drop standalone numeric tokens: manuscript line numbers and running page
    # numbers are interleaved with the text by PDF extraction and would
    # otherwise split an otherwise verbatim quotation. Applied to the quotation
    # as well as the page text, so the comparison stays symmetric.
    s = re.sub(r'(?<!\S)\d+(?!\S)', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s.lower())


MODES = ([], ['-layout'], ['-raw'])


def pdftext(pdf, first=None, last=None):
    """Normalised text of a page (or the document) under every extraction mode."""
    out = []
    for mode in MODES:
        cmd = ['pdftotext', '-q'] + mode
        if first:
            cmd += ['-f', str(first), '-l', str(last or first)]
        cmd += [pdf, '-']
        try:
            out.append(subprocess.run(cmd, capture_output=True, text=True, timeout=180).stdout)
        except Exception:
            pass
    return norm(' '.join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json')
    args = ap.parse_args()

    pdfs, firstpage = {}, {}
    with open(INDEX, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            pdfs[r['source_id']] = os.path.join(SOURCES, r['filename'])
            m = re.match(r'\s*(\d+)', r['pages'] or '')
            firstpage[r['source_id']] = int(m.group(1)) if m else None

    doc_cache = {}
    out = {}
    for name, (path, delim) in TABLES.items():
        if not os.path.exists(path):
            print(f'[skip] {name}: no table', file=sys.stderr)
            continue
        with open(path, encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f, delimiter=delim))

        on_page = wrong_page = absent = declined = no_page = short = 0
        journal_page = spliced = 0
        detail = {'wrong_page': [], 'absent': [], 'declined': [], 'short': [],
                  'journal_page': [], 'spliced': []}
        for r in rows:
            sid = r['source_id'].strip()
            q = r['key_supporting_quote'].strip()
            p = r['quote_pdf_page'].strip()
            if q.upper() in SENTINELS:
                declined += 1
                detail['declined'].append(sid)
                continue
            frags = [norm(f) for f in re.split(r'\.\.\.|\u2026', q) if len(norm(f)) >= 12]
            elided = len(frags) > 1
            if elided:
                short += 0
            nq = norm(q) if not elided else frags[0]
            if len(norm(q)) < 1:
                declined += 1
                detail['declined'].append(sid)
                continue
            if len(q.split()) < 5:
                short += 1
                detail['short'].append(sid)
            pdf = pdfs.get(sid)
            if not pdf or not os.path.exists(pdf):
                absent += 1
                detail['absent'].append(sid)
                continue
            if sid not in doc_cache:
                doc_cache[sid] = pdftext(pdf)
            located = all(f in doc_cache[sid] for f in frags) if elided else (nq in doc_cache[sid])
            if elided and located:
                spliced += 1
                detail['spliced'].append(sid)
            if not located:
                absent += 1
                detail['absent'].append(sid)
                continue
            m = re.search(r'(\d+)', p)
            if not m:
                no_page += 1
                wrong_page += 1
                detail['wrong_page'].append(sid)
                continue
            pg = int(m.group(1))
            if nq in pdftext(pdf, pg):
                on_page += 1
                continue
            fp = firstpage.get(sid)
            if fp is not None and pg - fp + 1 >= 1 and nq in pdftext(pdf, pg - fp + 1):
                journal_page += 1
                detail['journal_page'].append(sid)
                continue
            wrong_page += 1
            detail['wrong_page'].append(sid)

        n = len(rows)
        print(f'{name}')
        print(f'   rows {n} | quoted {n - declined} | declined to quote {declined}')
        print(f'   verbatim on the stated page   {on_page}')
        print(f'   page reads as the journal page {journal_page}  {detail["journal_page"][:10]}')
        print(f'   verbatim but page unusable    {wrong_page}  {detail["wrong_page"][:10]}')
        print(f'   not found in the paper        {absent}  {detail["absent"][:12]}')
        print(f'   elided with an ellipsis       {spliced}  (counted as located when every fragment matches)')
        if no_page:
            print(f'   no parsable page number       {no_page}')
        print(f'   quotation under 5 words       {short}  {detail["short"][:12]}')
        out[name] = dict(rows=n, quoted=n - declined, declined=declined, on_page=on_page,
                         journal_page=journal_page, wrong_page=wrong_page, absent=absent,
                         spliced=spliced, short=short, detail=detail)

    if args.json:
        with open(args.json, 'w') as f:
            json.dump(out, f, indent=2)
        print(f'wrote {args.json}')


if __name__ == '__main__':
    main()

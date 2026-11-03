"""Match each authentication-comparison run's included papers to the 102-paper corpus."""
from __future__ import annotations
import csv, json, re, unicodedata
from pathlib import Path
import pypdf

ROOT = Path(".")  # run from the project folder
AC = ROOT/"search_and_access_results/authentication_comparison"

def norm_doi(d):
    d = d.lower().strip().rstrip(').,;"\'')
    d = re.sub(r'^https?://(dx\.)?doi\.org/', '', d)
    return d

def norm_title(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

rows = list(csv.DictReader((ROOT/"spanish_plume_corpus/database/canonical_102.csv").open(encoding="utf-8-sig")))
by_doi, by_title = {}, {}
for r in rows:
    sid = r["source_id"]
    if r.get("doi"): by_doi[norm_doi(r["doi"])] = sid
    by_title[norm_title(r["title"])] = sid
corpus_titles = list(by_title.items())

# canonical_102.csv has almost no DOIs, so take them from the cached OpenAlex records too.
# Without this, a run that abbreviates a long title (SP004, SP077) is silently dropped.
for _p in (ROOT/"spanish_plume_corpus/database/cache/openalex").glob("SP*.json"):
    _d = (json.loads(_p.read_text()) or {}).get("doi")
    if _d: by_doi.setdefault(norm_doi(_d), _p.stem)

def text_of(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        return "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(str(p)).pages)
    return p.read_text(encoding="utf-8", errors="replace")

def tokens(t): return set(norm_title(t).split())

def match_pdf(path: Path):
    """PDF tables lose their pipes and wrap titles across lines, so match titles as
    whitespace-stripped substrings of the flattened page text."""
    flat = re.sub(r'[^a-z0-9]', '', unicodedata.normalize("NFKD", text_of(path)).lower())
    hits = set()
    for title, sid in corpus_titles:
        key = re.sub(r'[^a-z0-9]', '', title)
        if len(key) >= 25 and key in flat:
            hits.add(sid)
    # Titles the run shortened (SP078) are still identified by their DOI, which the PDF
    # wraps across lines, so compare DOIs with everything but letters and digits removed.
    for d, sid in by_doi.items():
        if re.sub(r'[^a-z0-9]', '', d) in flat:
            hits.add(sid)
    return hits, 0


def match_run(path: Path):
    if path.suffix.lower() == ".pdf":
        return match_pdf(path)
    t = text_of(path)
    hits, unmatched = set(), 0
    seen = set()
    for line in t.splitlines():
        if not line.strip().startswith("|"): continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4: continue
        if not re.match(r'^\d+$', cells[0]): continue         # numbered result rows only
        row = " ".join(cells)
        sid = None
        for d in re.findall(r'10\.\d{4,9}/[^\s\)\]|,;"]+', row):
            if norm_doi(d) in by_doi: sid = by_doi[norm_doi(d)]; break
        if sid is None:
            title = cells[1] if len(cells) > 1 else ""
            title = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', title)
            nt = norm_title(title)
            if nt in by_title: sid = by_title[nt]
            else:
                tk = tokens(title)
                if len(tk) >= 4:
                    best, bs = None, 0.0
                    for ct, cs in corpus_titles:
                        ck = set(ct.split())
                        j = len(tk & ck)/max(1, len(tk | ck))
                        if j > bs: best, bs = cs, j
                    if bs >= 0.6: sid = best
                    else:
                        # a run may give only the main title of a "Title: subtitle" article
                        pref = [cs for ct, cs in corpus_titles if len(nt) >= 30 and ct.startswith(nt)]
                        if len(pref) == 1: sid = pref[0]
        key = row[:80]
        if key in seen: continue
        seen.add(key)
        if sid: hits.add(sid)
        else: unmatched += 1
    return hits, unmatched

runs = {
  "codex_before":  AC/"codex/before_authentication/spanish_plume_search_report.md",
  "codex_after":   AC/"codex/after_authentication/spanish_plume_systematic_search.md",
  "claude_before": AC/"claude/before_authentication/Claude_Opus_5_Code.pdf",
  "claude_after":  AC/"claude/after_authentication/claude_authenticated_discovery_test/run_2026-08-13/spanish_plume_discovery_results.md",
}
out = {}
for k, p in runs.items():
    h, u = match_run(p)
    out[k] = sorted(h)
    print(f"{k:15s} matched to corpus: {len(h):3d}/102   unmatched rows: {u}")
json.dump(out, (ROOT/"analysis/auth_runs_corpus_matches.json").open("w"), indent=1)
print("\nwrote analysis/auth_runs_corpus_matches.json")
b = set(out["codex_before"]) | set(out["claude_before"])
a = set(out["codex_after"])  | set(out["claude_after"])
print(f"pooled BEFORE {len(b)}/102   pooled AFTER {len(a)}/102")

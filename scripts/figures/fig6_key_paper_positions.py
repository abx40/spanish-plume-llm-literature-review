"""Fig. 6: corpus articles cited in each synthesis, one column per article, by benchmark class.

Writes key_paper_positions.pdf (used in the manuscript) and key_paper_positions.png.
"""
from __future__ import annotations

from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle

from _common import DATA, out_path, read_csv


MODEL_COLUMNS = [
    ("NotebookLM", "notebooklm_cited"),
    ("Codex", "codex_cited"),
    ("Claude", "claude_cited"),
]
COLORS = {"essential": "#192847", "informative": "#6B7686", "passing": "#C9CFD6"}
INK, MUTED, BORDER, GROUP = "#202B35", "#66717C", "#DCE2E6", "#ACB6BF"


def validate():
    benchmark = read_csv(DATA / "discovery/benchmark/benchmark_reference.csv")
    citations = read_csv(DATA / "synthesis/per_paper_citations.csv")
    bmap = {r["source_id"]: r for r in benchmark}
    cmap = {r["source_id"]: r for r in citations}
    assert len(benchmark) == len(bmap) == len(citations) == len(cmap) == 102
    assert set(bmap) == set(cmap) == {f"SP{i:03d}" for i in range(1, 103)}
    counts = Counter(r["benchmark_class"] for r in benchmark)
    assert counts == {"essential": 4, "informative": 14, "passing": 84}
    for sid, row in cmap.items():
        assert row["year"] == bmap[sid]["year"]
        assert row["benchmark_class"] == bmap[sid]["benchmark_class"]
        assert all(row[field] in {"0", "1"} for _, field in MODEL_COLUMNS)
    expected = {"NotebookLM": (4, 12, 25, 41), "Codex": (4, 9, 14, 27),
                "Claude": (4, 14, 61, 79)}
    summary = {}
    for name, field in MODEL_COLUMNS:
        totals = [sum(int(r[field]) for r in citations if r["benchmark_class"] == cat)
                  for cat in ("essential", "informative", "passing")]
        totals.append(sum(totals))
        assert tuple(totals) == expected[name]
        summary[name] = dict(zip(("essential", "informative", "passing", "total"), totals))
    ordered = sorted(benchmark, key=lambda r: (int(r["year"]), r["source_id"]))
    assert len([r for r in ordered if r["benchmark_class"] != "passing"]) == 18
    return ordered, cmap, dict(counts), summary


def spaced_labels(targets, gap, lower, upper):
    """Pack rotated labels while retaining their order and exact leader targets."""
    # Isotonic regression of x_i - i*gap gives the nearest nonoverlapping positions.
    blocks = []
    for index, value in enumerate(np.asarray(targets)-np.arange(len(targets))*gap):
        blocks.append([float(value), 1])
        while len(blocks) > 1 and blocks[-2][0]/blocks[-2][1] > blocks[-1][0]/blocks[-1][1]:
            total, count = blocks.pop()
            blocks[-1][0] += total
            blocks[-1][1] += count
    fitted = np.array([total/count for total, count in blocks for _ in range(count)])
    fitted = np.clip(fitted, lower, upper-gap*(len(targets)-1))
    result = fitted+np.arange(len(targets))*gap
    assert np.all(np.diff(result) >= gap-1e-9)
    return result


def build():
    ordered, cited, counts, summary = validate()
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8, "text.color": INK,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "pdf.fonttype": 42,
        "ps.fonttype": 42, "svg.fonttype": "none",
    })
    fig = plt.figure(figsize=(6.5, 3.2))
    ax = fig.add_axes([.17, .18, .78, .76])
    ax.set(xlim=(-.7, 109), ylim=(-.9, 5.0))
    ax.axis("off")
    rows = [("Corpus", None, 3)]+[(name, field, 2-i) for i, (name, field) in enumerate(MODEL_COLUMNS)]
    for name, field, y in rows:
        ax.text(-1.5, y, name, ha="right", va="center", fontsize=8.2, weight="bold")
        total = 0
        for i, row in enumerate(ordered):
            present = field is None or cited[row["source_id"]][field] == "1"
            total += present
            ax.add_patch(Rectangle((i-.43, y-.31), .86, .62,
                                   facecolor=COLORS[row["benchmark_class"]] if present else "white",
                                   edgecolor=BORDER, linewidth=.22))
        ax.text(105.0, y, str(total), ha="center", va="center", fontsize=8.2, weight="bold")
    ax.text(105.0, 3.74, "Total", ha="center", va="bottom", fontsize=7.2, color=MUTED)

    groups = [(year, [i for i, r in enumerate(ordered) if int(r["year"]) == year])
              for year in sorted({int(r["year"]) for r in ordered})]
    group_centres = [float(np.mean(indices)) for _, indices in groups]
    points_per_unit = fig.get_figwidth()*72*.78/(109+.7)
    year_positions = spaced_labels(group_centres, 8.4/points_per_unit, -.2, 101.2)
    year_texts, key_texts = [], []
    for (year, indices), original, label_x in zip(groups, group_centres, year_positions):
        ax.plot([indices[0]-.55]*2, [-.43, 3.42], color=GROUP, lw=.25)
        ax.plot([original, original, label_x], [3.38, 3.53, 3.66], color=GROUP, lw=.32)
        year_texts.append(ax.text(label_x, 3.72, str(year), rotation=90, fontsize=7.2,
                                  ha="center", va="bottom", color=MUTED))
    ax.plot([101.55]*2, [-.43, 3.42], color=GROUP, lw=.25)
    key_indices = [i for i, r in enumerate(ordered) if r["benchmark_class"] != "passing"]
    key_positions = spaced_labels(key_indices, 8.2/points_per_unit, -.2, 101.2)
    for i, label_x in zip(key_indices, key_positions):
        ax.plot([i, i, label_x], [-.35, -.49, -.64], color=GROUP, lw=.32)
        key_texts.append(ax.text(label_x, -.70, ordered[i]["source_id"], rotation=90,
                                fontsize=7.0, color=COLORS["essential"],
                                ha="center", va="top", clip_on=False))
    ax.text(-1.5, -.70, "Key IDs", ha="right", va="top", fontsize=7.2, color=MUTED)
    legend = fig.legend(handles=[Patch(facecolor=COLORS[k], label=label)
                                 for k, label in (("passing", "Passing mention (84)"),
                                                  ("informative", "Informative (14)"),
                                                  ("essential", "Essential (4)"))],
                        loc="upper left", bbox_to_anchor=(.17, .995), ncol=3,
                        frameon=False, fontsize=7.7, handlelength=1.2,
                        handletextpad=.5, columnspacing=1.3, borderaxespad=0)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for group in (year_texts, key_texts):
        boxes = [text.get_window_extent(renderer) for text in group]
        assert all(a.x1 < b.x0 for a, b in zip(boxes, boxes[1:])), "Rotated labels overlap"
    for text in year_texts+key_texts+[t for t in ax.texts if t not in year_texts+key_texts]:
        box = text.get_window_extent(renderer)
        assert box.x0 >= 0 and box.x1 <= fig.bbox.width, f"Text outside figure: {text.get_text()}"
        assert box.y0 >= 0 and box.y1 <= fig.bbox.height, f"Text outside figure: {text.get_text()}"
    assert legend.get_window_extent(renderer).x1 <= fig.bbox.width
    fig.savefig(out_path("key_paper_positions.pdf"), metadata={"Title": "Corpus classification and synthesis citations",
                                                              "Subject": "102 Spanish plume articles"})
    fig.savefig(out_path("key_paper_positions.png"), dpi=600)
    plt.close(fig)
    print(summary)

if __name__ == "__main__":
    build()

"""Fig. 7: corpus articles cited and not cited by each synthesis, by year of publication."""
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerBase
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from _common import PLOT_DATA, out_path, read_csv

BLACK, GRAY, MED, LABEL = "#192847", "#AEB6C0", "#7F8A96", "#4B5563"


class TriangleOverLine(HandlerBase):
    """Legend symbol drawn as on the chart: a short line, with its triangle above it."""
    def __init__(self, ls, filled):
        super().__init__(); self.ls, self.filled = ls, filled

    def create_artists(self, legend, orig, xd, yd, w, h, fontsize, trans):
        cx = xd + w/2
        line = Line2D([cx, cx], [yd - 1.05*h, yd + 0.6*h], color=MED, ls=self.ls, lw=1.4, transform=trans)
        tri = Line2D([cx], [yd + 1.0*h], ls="none", marker="v", ms=5, color=MED,
                     mfc=(MED if self.filled else "white"), mec=MED, mew=1.0, transform=trans)
        return [line, tri]


rows = read_csv(PLOT_DATA / "citation_year_histograms.csv")
TOOLS = [("NotebookLM", "NotebookLM"), ("Codex", "Codex"), ("Claude", "Claude Opus 5")]
fig, axes = plt.subplots(3, 1, figsize=(7.4, 7.4), sharex=True, sharey=True)
for ax, (label, key) in zip(axes, TOOLS):
    r = sorted((x for x in rows if x["model"] == key), key=lambda x: int(x["year"]))
    yrs = [int(x["year"]) for x in r]; got = [int(x["cited"]) for x in r]; miss = [int(x["not_cited"]) for x in r]
    assert sum(got) + sum(miss) == 102
    med = statistics.median([y for y, g in zip(yrs, got) for _ in range(g)])
    ax.bar(yrs, got, color=BLACK, width=0.82)
    ax.bar(yrs, miss, bottom=got, color=GRAY, alpha=0.55, width=0.82)
    ax.axvline(med, color=MED, ls="--", lw=1.5, zorder=4)
    ax.plot([med], [8.3], marker="v", color=MED, ms=5.5, clip_on=False, zorder=5)
    ax.text(med, 8.7, f"{med:.0f}", ha="center", va="bottom", fontsize=6.8, color=LABEL)
    ax.set_title(f"{label}: Cited {sum(got)} out of 102; median year {med:.0f}", fontsize=10, loc="left", pad=8)
    ax.set_ylabel("Number of articles", fontsize=9)
    ax.set_ylim(0, 8); ax.set_yticks(range(0, 9, 2)); ax.tick_params(labelsize=8)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axes[-1].set_xlim(1966, 2025); axes[-1].set_xticks(range(1965, 2024, 5))
axes[-1].set_xlabel("Year of publication", fontsize=9)
hM = Line2D([0], [0])
fig.legend(handles=[Patch(facecolor=BLACK), Patch(facecolor=GRAY, alpha=0.55), hM],
           labels=["Cited", "Not cited", "Median year of the articles cited"],
           handler_map={hM: TriangleOverLine("--", True)}, loc="upper center", ncol=3, frameon=False,
           fontsize=7.5, numpoints=1, handlelength=1.4, columnspacing=1.6, bbox_to_anchor=(0.5, 0.995))
fig.tight_layout(rect=(0, 0, 1, 0.955))
fig.savefig(out_path("citation_year_histograms.png"), dpi=220)

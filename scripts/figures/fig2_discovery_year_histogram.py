"""Fig. 2: articles found and not found by at least one of the five search tools, by year."""
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerBase
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from _common import DATA, PLOT_DATA, out_path, read_csv

BLACK, GRAY, MED = "#192847", "#AEB6C0", "#7F8A96"


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


data = read_csv(PLOT_DATA / "discovery_year_histogram.csv")
years = [int(r["year"]) for r in data]; found = [int(r["documented"]) for r in data]; notf = [int(r["not_documented"]) for r in data]
assert sum(found) == 57 and sum(notf) == 45
b = read_csv(DATA / "discovery/benchmark/benchmark_reference.csv")
m = {r["source_id"]: r for r in read_csv(DATA / "discovery/per_paper_discovery.csv")}
med_found = statistics.median(int(r["year"]) for r in b if m[r["source_id"]]["pooled_documented"] == "1")
med_all = statistics.median(int(r["year"]) for r in b)
fig, ax = plt.subplots(figsize=(7.4, 3.1))
ax.bar(years, found, color=BLACK, width=0.82)
ax.bar(years, notf, bottom=found, color=GRAY, alpha=0.55, width=0.82)
ax.axvline(med_found, color=MED, ls="--", lw=1.5, zorder=4)
ax.plot([med_found], [8.3], marker="v", color=MED, ms=5.5, clip_on=False, zorder=5)
ax.axvline(med_all, color=MED, ls=":", lw=1.6, zorder=4)
ax.plot([med_all], [8.3], marker="v", mfc="white", mec=MED, mew=1.1, ms=5.5, clip_on=False, zorder=5)
ax.set_xlim(min(years) - 2, max(years) + 2); ax.set_ylim(0, 8); ax.set_yticks(range(0, 9, 2))
ax.set_xticks(range(1965, max(years) + 1, 5)); ax.set_xlabel("Year of publication", fontsize=9)
ax.set_ylabel("Number of articles", fontsize=9); ax.tick_params(labelsize=8)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.text(med_found, 8.7, f"{med_found:.0f}", ha="center", va="bottom", fontsize=6.8, color="#4B5563")
ax.text(med_all, 8.7, f"{med_all:.0f}", ha="center", va="bottom", fontsize=6.8, color="#4B5563")
hF = Patch(facecolor=BLACK); hN = Patch(facecolor=GRAY, alpha=0.55)
hMF = Line2D([0], [0])
hMC = Line2D([0], [0])
fig.legend(handles=[hF, hN, hMF, hMC],
           labels=["Found by at least one tool", "Not found", "Median year of articles found", "Median year of the corpus"],
           handler_map={hMF: TriangleOverLine("--", True), hMC: TriangleOverLine(":", False)}, loc="upper center", ncol=4, frameon=False,
           fontsize=7.5, numpoints=1, handlelength=1.4, columnspacing=1.6, labelspacing=1.6, bbox_to_anchor=(0.5, 0.985))
fig.tight_layout(rect=(0, 0, 1, 0.86)); fig.savefig(out_path("discovery_year_histogram.png"), dpi=220)
print(f"median year found {med_found:.0f}, corpus {med_all:.0f}")

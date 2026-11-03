"""Fig. 5: confusion matrices for the substantial/passing classification, one panel per tool."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from _common import PLOT_DATA, out_path, read_csv

cells = {(r["tool"], r["benchmark_class"]): r for r in read_csv(PLOT_DATA / "confusion_matrices.csv")}
TOOLS = [(t, int(cells[t, "substantial"]["classified_substantial"]), int(cells[t, "substantial"]["classified_passing"]),
          int(cells[t, "passing"]["classified_substantial"]), int(cells[t, "passing"]["classified_passing"]))
         for t in ("Codex", "NotebookLM", "Claude")]  # TP, FN, FP, TN
assert all(tp + fn == 18 and fp + tn == 84 for _, tp, fn, fp, tn in TOOLS)
cmap = LinearSegmentedColormap.from_list("g", ["#FFFFFF", "#192847"])
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9))
for ax, (name, tp, fn, fp, tn) in zip(axes, TOOLS):
    m = [[tp / 18, fn / 18], [fp / 84, tn / 84]]          # shade by share of each benchmark row
    counts = [[tp, fn], [fp, tn]]
    ax.imshow(m, cmap=cmap, vmin=0, vmax=1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{counts[i][j]}\n({100*m[i][j]:.0f}%)", ha="center", va="center", fontsize=9,
                    color="white" if m[i][j] > 0.5 else "#192847")
    ax.set_xticks([0, 1], ["Substantial", "Passing"], fontsize=8); ax.set_yticks([0, 1], ["Substantial\n(18)", "Passing\n(84)"], fontsize=8)
    ax.set_title(name, fontsize=10, loc="left")
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
axes[0].set_ylabel("Benchmark database", fontsize=9)
fig.supxlabel("Classified by the tool", fontsize=9)
fig.tight_layout(); fig.savefig(out_path("confusion_matrices.png"), dpi=220)

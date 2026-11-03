"""Fig. 4: share of each publisher group's articles found by Codex and Claude Code, before and after login."""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from _common import DATA, PLOT_DATA, out_path, read_csv


BEFORE, AFTER = "#8792A2", "#192847"
INK, GRID = "#222B35", "#E7EBEF"


def main():
    rows = read_csv(PLOT_DATA / "publisher_login.csv")
    papers = read_csv(DATA / "authentication/per_paper_matches.csv")
    assert len(papers) == len({row["source_id"] for row in papers}) == 102
    assert sum(int(row["articles_in_corpus"]) for row in rows) == 102
    for row in rows:
        group = [paper for paper in papers
                 if paper["publisher_group"] == row["publisher_group"]]
        assert len(group) == int(row["articles_in_corpus"])
        for run in ("codex_before", "codex_after", "claude_before", "claude_after"):
            assert int(row[run]) == sum(int(paper[run]) for paper in group)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": "#66717C", "ytick.color": INK,
                         "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 6.0), sharey=True)
    fig.subplots_adjust(left=.205, right=.975, bottom=.15, top=.825, wspace=.22)
    fig.legend(handles=[Patch(facecolor=BEFORE, label="Before login"),
                        Patch(facecolor=AFTER, label="After login")],
               loc="upper center", bbox_to_anchor=(.59, .965), frameon=False,
               ncol=2, fontsize=10, handlelength=1.25, columnspacing=2.0)
    labels = [f"{row['publisher_group']} (n={row['articles_in_corpus']})" for row in rows]
    for panel, (ax, agent, title) in enumerate(zip(
            axes, ("codex", "claude"), ("(a) Codex", "(b) Claude Code"))):
        ax.set_title(title, loc="left", fontsize=12, pad=15)
        for y, row in enumerate(rows):
            n = int(row["articles_in_corpus"])
            for state, offset, color, text_color in (
                    ("before", -.17, BEFORE, "white"),
                    ("after", .17, AFTER, "white")):
                count = int(row[f"{agent}_{state}"])
                percentage = 100 * count / n
                position = y + offset
                ax.barh(position, percentage, height=.285, color=color, zorder=3)
                label = f"{math.floor(percentage + .5)}%"
                ax.text(percentage - 2 if count else 1.6, position, label,
                        ha="right" if count else "left", va="center", fontsize=9.6,
                        color=text_color if count else INK, zorder=4)
        ax.set_xlim(0, 100)
        ax.set_ylim(len(rows) - .5, -.65)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks(range(len(rows)), labels)
        for x in (0, 25, 50, 75, 100):
            ax.axvline(x, color=GRID, lw=.65, zorder=0)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#B8C0C8")
        ax.tick_params(axis="x", length=3, color="#B8C0C8", labelsize=9)
        ax.tick_params(axis="y", length=0, pad=11, labelsize=10.5)
    fig.text(.59, .078, "Share of articles found (%)", ha="center", fontsize=11)
    fig.text(.205, .027, "n: articles in the corpus.",
             fontsize=9, color="#66717C")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for item in fig.findobj(match=matplotlib.text.Text):
        if item.get_visible() and item.get_text():
            box = item.get_window_extent(renderer)
            assert box.x0 >= 0 and box.x1 <= fig.bbox.width
            assert box.y0 >= 0 and box.y1 <= fig.bbox.height
    fig.savefig(out_path("publisher_login.png"), dpi=250, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()

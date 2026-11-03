"""Fig. 3: share of each publication period's benchmark articles found by Codex and Claude Code, before and after login."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from _common import DATA, PLOT_DATA, out_path, read_csv

PERIODS = [("pre-2000", 1965, 1999), ("2000-09", 2000, 2009),
           ("2010-14", 2010, 2014), ("2015-19", 2015, 2019),
           ("2020-24", 2020, 2024)]
LOGIN_BEFORE, LOGIN_AFTER = "#8792A2", "#192847"
AGENT_RUNS = {  # column: (line style, colour, legend label), in legend order
    "codex_after": ("-", LOGIN_AFTER, "Codex after login"),
    "codex_before": ("-", LOGIN_BEFORE, "Codex before login"),
    "claude_after": ("--", LOGIN_AFTER, "Claude Code after login"),
    "claude_before": ("--", LOGIN_BEFORE, "Claude Code before login"),
}

rows = read_csv(DATA / "authentication/per_paper_matches.csv")
age_rows = []
for label, low, high in PERIODS:
    group = [r for r in rows if low <= int(r["year"]) <= high]
    n = len(group)
    row = dict(period=label, first_year=low, last_year=high, n=n)
    for key in AGENT_RUNS:
        row[f"{key}_percent"] = round(100 * sum(int(r[key]) for r in group) / n, 6)
    age_rows.append(row)

# The published plot data must match what the per-paper table gives.
published = {r["period"]: r for r in read_csv(PLOT_DATA / "access_age.csv")}
for row in age_rows:
    assert int(published[row["period"]]["n"]) == row["n"]
    for key in AGENT_RUNS:
        assert abs(float(published[row["period"]][f"{key}_percent"]) - row[f"{key}_percent"]) < 1e-6

# One curve per agent and login state: solid for Codex, dashed for Claude Code,
# near-black after login, gray before.
x = list(range(len(PERIODS)))
labels = [f"{r['period']}\n(n={r['n']})" for r in age_rows]
fig, ax = plt.subplots(figsize=(7.4, 3.6))
for key in AGENT_RUNS:
    linestyle, color, label = AGENT_RUNS[key]
    ax.plot(x, [r[f"{key}_percent"] for r in age_rows], linestyle, marker="o",
            color=color, linewidth=2.0, markersize=4.5,
            clip_on=False, zorder=3)  # draw a 0% point over the axis, not under it
handles = [Line2D([0], [0], linestyle=s, color=c, linewidth=2.0, label=lab)
           for s, c, lab in AGENT_RUNS.values()]
ax.set_xticks(x, labels)
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 10))
ax.grid(axis="y", color="#E7E9ED", linewidth=0.7)
ax.set_axisbelow(True)
ax.set_xlabel("Publication period")
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2,
          frameon=False, fontsize=8, handlelength=3.2, columnspacing=3.0)
ax.set_ylabel("Share of articles found (%)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=8)
fig.tight_layout()
fig.savefig(out_path("access_age.png"), dpi=220, bbox_inches="tight")
plt.close(fig)

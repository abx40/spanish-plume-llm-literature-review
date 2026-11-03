"""Fig. 1: workflow of the study (inputs, tools, tasks and evaluation). A diagram; it uses no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from _common import out_path


plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'})
INK, EDGE = '#192847', '#8792a2'
INPUT, TASK, RESULT = '#f2f4f6', '#e7ebef', '#d3dae2'
fig, ax = plt.subplots(figsize=(14.5, 8.2))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set(xlim=(0, 15.8), ylim=(0, 9.6))
ax.axis('off')
contained_text = []


def box(x, y, w, h, heading, body='', fill=INPUT, hs=13, bs=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, fc=fill, ec=EDGE, lw=1,
                              boxstyle='round,pad=0,rounding_size=.06'))
    if not body:
        obj = ax.text(x+w/2, y+h/2, heading, ha='center', va='center',
                      fontsize=hs, weight='bold', color=INK, linespacing=1.6)
        contained_text.append((obj, x, y, w, h))
    else:
        obj = ax.text(x+w/2, y+h-.24, heading, ha='center', va='top',
                      fontsize=hs, weight='bold', color=INK)
        contained_text.append((obj, x, y, w, h))
        obj = ax.text(x+w/2, y+h-.68, body, ha='center', va='top',
                      fontsize=bs, color=INK, linespacing=1.5)
        contained_text.append((obj, x, y, w, h))


def arrow(x1, x2, y):
    ax.annotate('', xy=(x2-.035, y), xytext=(x1+.035, y), arrowprops={
        'arrowstyle': '-|>', 'lw': 1.1, 'color': EDGE, 'mutation_scale': 12})


def bullet_box(x, y, w, h, items, heading='', fill='white'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, fc=fill, ec=EDGE, lw=1,
                              boxstyle='round,pad=0,rounding_size=.06'))
    if heading:
        obj = ax.text(x+w/2, y+h-.16, heading, ha='center', va='top',
                      fontsize=14, weight='bold', color=INK)
        contained_text.append((obj, x, y, w, h))
    top = y+h-(.56 if heading else .24)
    for item in items:
        ax.text(x+.18, top, '\u2022', ha='left', va='top', fontsize=10.5, color=INK)
        obj = ax.text(x+.38, top, item, ha='left', va='top',
                      fontsize=10.5, color=INK, linespacing=1.4)
        contained_text.append((obj, x, y, w, h))
        top -= .30 * (item.count('\n')+1)


box(.4, 8.4, 15, .95, 'Benchmark: Schultz et al. (2025)',
    '102 articles: 4 essential, 14 informative, 84 passing mentions; benchmark review and classifications withheld from the tools',
    hs=14, bs=10.5)

cols = [(.4, 2.35, 'INPUT'), (3.25, 3.0, 'AI TOOLS'),
        (6.75, 4.15, 'TASK'), (11.4, 4, 'EVALUATION')]
for x, w, label in cols:
    ax.text(x+w/2, 8.12, label, ha='center', va='top', fontsize=11,
            weight='bold', color=INK)

box(.4, 6.14, 2.35, 1.6, 'Search instructions',
    'Find eligible journal\narticles mentioning', hs=12, bs=10.5)
ax.text(1.575, 6.52, '\u201cSpanish plume\u201d', ha='center', va='top',
        fontsize=11, weight='normal', color=INK)
box(3.25, 6.14, 3, 1.6,
    'ChatGPT Deep Research\nGemini Deep Research\nClaude web\nCodex\nClaude Code', hs=11)
box(.4, 1.25, 2.35, 4.78, 'Closed corpus\n102 PDFs', hs=13)
box(3.25, 1.25, 3, 4.78, 'Codex\nClaude Code\nNotebookLM', hs=13)

rows = [
    (6.2, '1. Find', ['Search for Spanish plume articles',
                      'Repeat search with library login\n(coding agents only)'],
     ['Measure discovery recall', 'Assess effect of login on discovery']),
    (4.55, '2. Interpret', ["Classify each article's use of the term",
                           'Record supporting quotations'],
     ['Check quotations and page numbers', 'Score classifications against benchmark']),
    (2.9, '3. Synthesize', ['Write a synthesis across ten themes',
                            'Support claims with sources'],
     ['Check cited sources and quotations', 'Obtain blind expert ratings of syntheses']),
    (1.25, '4. Propose', ['Identify remaining research gaps', 'Suggest future research'],
     ['Compare proposals with the benchmark\nand expert assessments']),
]
for y, heading, task_body, evaluation in rows:
    bullet_box(6.75, y, 4.15, 1.48, task_body, heading=heading, fill=TASK)
    bullet_box(11.4, y, 4, 1.48, evaluation)
    for x1, x2 in [(2.75, 3.25), (6.25, 6.75), (10.9, 11.4)]:
        arrow(x1, x2, y+.74)

box(6.15, .25, 5.35, .65, 'Eight recommendations', fill=RESULT, hs=14)

# Ensure all node labels remain inside their boundaries at export resolution.
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for obj, x, y, w, h in contained_text:
    bounds = obj.get_window_extent(renderer).transformed(ax.transData.inverted())
    if bounds.x0 < x or bounds.x1 > x+w or bounds.y0 < y or bounds.y1 > y+h:
        raise ValueError(f'Text exceeds node: {obj.get_text()}')
fig.savefig(out_path('workflow_inputs_tasks_evaluation.png'), dpi=200, facecolor='white')

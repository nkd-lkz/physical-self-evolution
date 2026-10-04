"""Rebuild the October 4 figure from the two public result files."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[2]
train = json.loads((root / 'data/zeva-matched-results-2026-10-04.json').read_text())
evaluation = json.loads((root / 'data/zeva-frozen-eval-2026-10-04.json').read_text())
plt.rcParams.update({'font.size': 10, 'svg.fonttype': 'none', 'svg.hashsalt': 'zeva-2026-10-04'})
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout='constrained')
for key, label, color, style in [('zero', 'Zero context', '#225b96', '-o'), ('response', 'Response memory', '#b76627', '--s')]:
    rows = train['common_evaluations']
    axes[0].plot([r['iteration'] for r in rows], [r[key]['success_rate'] * 100 for r in rows], style, color=color, label=label, markersize=4)
axes[0].set(xlabel='Completed outer iterations (unequal learner updates)', ylabel='Success (%)', ylim=(0, 100), title='Training-time evaluation: 8 lanes per checkpoint')
axes[0].legend(frameon=False)
keys = ['zero_native', 'response_native', 'response_zero_context', 'zero_reference']
labels = ['Zero\ncontext', 'Response\nmemory', 'Response\ncontext off', 'VLA\nreference']
counts = [evaluation['arms'][k]['successes'] for k in keys]
axes[1].bar(labels, [100 * n / 64 for n in counts], color=['#225b96', '#b76627', '#a87947', '#357158'], width=.65)
for i, n in enumerate(counts): axes[1].text(i, n / 64 * 100 + 2, f'{n}/64', ha='center')
axes[1].set(ylabel='Success (%)', ylim=(0, 100), title='Frozen checkpoint 275: 64 episodes per arm')
for ax in axes:
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=.2)
    ax.set_axisbelow(True)
fig.suptitle('Zeva / RLT development results — 2026-10-04', fontsize=14)
fig.supxlabel('One training seed. Evaluation seeds are paired. No expert. These data do not establish a memory benefit.', fontsize=9)
fig.savefig(root / 'research/figures/zeva-results-2026-10-04.svg', metadata={'Date': '2026-10-04'})

output = root / 'research/figures/zeva-results-2026-10-04.svg'
output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines()) + '\n')

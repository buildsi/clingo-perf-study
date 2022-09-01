import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

labelsize=20

matplotlib.rc('xtick', labelsize=labelsize)
matplotlib.rc('ytick', labelsize=labelsize)

def fix_tex_ticks():
    """Fix an issue with usetex and fonts in matplotlib (remove strict math mode)"""
    formatter = matplotlib.ticker.EngFormatter
    method = "format_eng"

    old_format = getattr(formatter, method)
    def new_format(self, num):
        result = old_format(self, num)
        result = re.sub(r"\$([^\$]*)\$", r"\1", result)
        return result

    setattr(formatter, method, new_format)

fix_tex_ticks()

def fix_hist_step_vertical_line_at_end(ax):
    axpolygons = [
        poly for poly in ax.get_children() if isinstance(poly, matplotlib.patches.Polygon)
    ]
    for poly in axpolygons:
        poly.set_xy(poly.get_xy()[:-1])

DESCRIPTION = """Produce a CDF plot of Package number vs. Total execution time"""

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('csvfile', help='CSV file with timing data')
parser.add_argument('outfile', help='output file name')
args = parser.parse_args()

df = pd.read_csv(
    args.csvfile,
    header=None,
    names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'],
    converters={'cfg': str.strip}
)

df = df[df.cfg != "many"]
df = df[df.iter == 0]

print(df.head())

cfg_ls = list(sorted(set(df['cfg'])))
pkg_ls = list(sorted(set(df['pkg'])))

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

for cfg, color in [('tweety', "tab:red"), ('trendy', "tab:blue"), ('handy', "tab:purple")]:
    df_by_config = df[df['cfg'] == cfg]
    times = df_by_config['total']
    times.hist(cumulative=True, density=False, bins=1000, ax=ax, label=cfg, histtype='step', color=color)

ax.set_xlabel('Time [s]', fontsize=labelsize)
ax.set_ylabel('Package count', fontsize=labelsize)
ax.legend(loc='lower right', prop={'size': labelsize})
plt.grid(axis='both', color='0.9')

fix_hist_step_vertical_line_at_end(ax)

fmt = matplotlib.ticker.EngFormatter(usetex=True)
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)

fig.tight_layout()
fig.savefig(args.outfile)

import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

labelsize=20

import matplotlib
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
parser.add_argument('variable', help='variable (column) to plot')
parser.add_argument('outfile', help='output file name')
args = parser.parse_args()

DATA = [
    ("cache_runs/out_log_cache_1.csv", "tab:blue", "6804 cached pkgs"),
    ("cache_runs/out_log_cache_2.csv", "tab:red", "15255 cached pkgs"),
    ("cache_runs/out_log_cache_3.csv", "tab:purple", "27160 cached pkgs"),
    ("cache_runs/out_log_cache_full.csv", "tab:brown", "63099 cached pkgs")
]

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

with open("../container/e4s-transitive.list") as e4s_file:
    e4s = set(pkg.strip() for pkg in e4s_file)

for csvfile, color, label in DATA:
    df = pd.read_csv(
        csvfile,
        header=None,
        names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'],
        converters={'cfg': str.strip}
    )
    df = df[df.cfg == "tweety"]
    df = df[df.iter == 1]

    df = df[df.pkg.isin(e4s)]

    print(df.head())

    # take median time for ach unique package
    times = df.groupby("pkg")[args.variable].median()

    times.hist(
        cumulative=True,
        density=False,
        bins=1000,
        ax=ax,
        label=label,
        histtype='step',
        color=color,
    )


ax.set_xlabel('Time [s]', fontsize=labelsize)
ax.set_ylabel('Package count', fontsize=labelsize)
ax.legend(loc='lower right', prop={'size': labelsize})
plt.grid(axis='both', color='0.9', which='both')

fix_hist_step_vertical_line_at_end(ax)

fmt = matplotlib.ticker.EngFormatter(usetex=True)
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)

max_time = max(df[args.variable])
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(10))

fig.tight_layout()
fig.savefig(args.outfile)

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

DESCRIPTION = """Produce a CDF plot of "Package Number vs. Total Execution Time" comparing the old and ASP concretizer"""

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument(
    '-m', '--mode',
    choices=('relative', 'absolute', 'normalized'),
    default='normalized',
    help=('Use absolute number of packages (absolute), percentage'
          ' of concretized packages (relative), or discard pkgs that'
          ' could not concretize with the old concretizer (normalized)')
)
parser.add_argument('old_csvfile', help='CSV file with timing data for the old concretizer')
parser.add_argument('asp_csvfile', help='CSV file with timing data for the ASP concretizer')
parser.add_argument('outfile', help='output file name')
args = parser.parse_args()

# Load the data for the old and the new concretizer
df_old = pd.read_csv(args.old_csvfile, header=None, names=['pkg', 'iter', 'concrete', 'total'])
df_asp = pd.read_csv(
    args.asp_csvfile,
    header=None,
    names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'],
    converters={'cfg': str.strip}
)

df_old = df_old[df_old.iter == 0]
df_asp = df_asp[df_asp.iter == 0]
df_asp = df_asp[df_asp.cfg == 'tweety']

print(df_old.head())
print(df_asp.head())

if args.mode == 'absolute':
    density = 0
    ylabel = "Package count"
    df_old = df_old[df_old['concrete'] == True]
elif args.mode == 'relative':
    density = 1
    ylabel = "Percentage of packages"
    df_old = df_old[df_old['concrete'] == True]
elif args.mode == 'normalized':
    df_failed_old = df_old[df_old['concrete'] == False]
    print("The old concretizer failed on {0} packages. Skipping them from the plot.".format(len(df_failed_old)))
    df_old = df_old[~df_old.pkg.isin(df_failed_old['pkg'])]
    df_asp = df_asp[~df_asp.pkg.isin(df_failed_old['pkg'])]
    density = 0
    ylabel = "Package count"

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

for df, label, color in ((df_old, "Old concretizer", "tab:blue"), (df_asp, "Clingo", "tab:red")):
    times = df['total']
    times.hist(cumulative=True, density=density, bins=500, ax=ax, label=label, histtype='step', color=color)

ax.set_xlabel('Time [s]', fontsize=labelsize)
ax.set_ylabel(ylabel, fontsize=labelsize)
ax.legend(loc='lower right', prop={'size': labelsize})
plt.grid(axis='both', color='0.9')

fix_hist_step_vertical_line_at_end(ax)

fmt = matplotlib.ticker.EngFormatter(usetex=True)
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)

fig.tight_layout()
fig.savefig(args.outfile)

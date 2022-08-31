import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

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
    
fig, axs = plt.subplots(figsize=(6, 6), dpi=150)  

for df, label, color in ((df_old, "Old concretizer", "tab:blue"), (df_asp, "Clingo", "tab:red")):
    times = df['total']
    times.hist(cumulative=True, density=density, bins=500, ax=axs, label=label, histtype='step', color=color)

axs.set_xlabel('Time [s]', fontsize=20)
axs.set_ylabel(ylabel, fontsize=20)
axs.legend(loc='lower right')

fig.tight_layout()
fig.savefig(args.outfile)



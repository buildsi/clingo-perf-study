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

DESCRIPTION = """Produce a CDF plot of Package number vs. Total execution time"""

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('variable', help='variable (column) to plot')
parser.add_argument('outfile', help='output file name')
args = parser.parse_args()

DATA = [
    ("../lassen/cache_runs/out_log_cache_1.csv", "tab:blue", "6804 cached pkgs"),
    ("../lassen/cache_runs/out_log_cache_2.csv", "tab:red", "15255 cached pkgs"),
    ("../lassen/cache_runs/out_log_cache_3.csv", "tab:purple", "27160 cached pkgs"),
    ("../lassen/cache_runs/out_log_cache_full.csv", "tab:brown", "63099 cached pkgs")
]

fig, axs = plt.subplots(figsize=(6, 6), dpi=150)  

for csvfile, color, label in DATA:
    df = pd.read_csv(
        csvfile,
        header=None,
        names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'],
        converters={'cfg': str.strip}
    )
    df = df[df.cfg == "tweety"]
    df = df[df.iter == 1]

    print(df.head())

    times = df[args.variable]
    times.hist(cumulative=True, density=True, bins=500, ax=axs, label=label, histtype='step', color=color)


axs.set_xlabel('Time [s]', fontsize=20)
axs.set_ylabel('Percentage of packages', fontsize=20)
axs.legend(loc='lower right')

fig.tight_layout()
fig.savefig(args.outfile)

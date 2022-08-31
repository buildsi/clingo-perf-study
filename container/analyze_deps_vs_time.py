import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

labelsize=20

import matplotlib
matplotlib.rc('xtick', labelsize=labelsize)
matplotlib.rc('ytick', labelsize=labelsize)

DESCRIPTION = """Produce a scatter plot of the "Total execution time" vs. "Number of possible dependencies" """

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('csvfile', help='CSV file with timing data')
parser.add_argument('variable', help='variable (column) to plot')
parser.add_argument('outfile', help='output file name')
args = parser.parse_args()

df = pd.read_csv(
    args.csvfile,
    header=None,
    names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'],
    converters={'cfg': str.strip}
)

df = df[df.cfg == "tweety"]


df_full = df
print(df_full.head())

cfg_ls = list(sorted(set(df['cfg'])))
pkg_ls = list(sorted(set(df['pkg'])))

timings = {}
deps = []

df_deps = df_full

fig, axs = plt.subplots(figsize=(6, 6), dpi=150)

df.plot.scatter(x="dep_len", y=args.variable, ax=axs)
axs.set_xlabel('Number of dependencies', fontsize=labelsize)
axs.set_ylabel('Time [s]', fontsize=labelsize)

fig.savefig(args.outfile)

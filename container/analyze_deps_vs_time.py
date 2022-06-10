import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

DESCRIPTION = """Produce a scatter plot of the "Total execution time" vs. "Number of possible dependencies" """

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('csvfile', help='CSV file with timing data')
args = parser.parse_args()

df = pd.read_csv(args.csvfile, header=None, names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'])

df_full = df
print(df_full.head())

cfg_ls = list(sorted(set(df['cfg'])))
pkg_ls = list(sorted(set(df['pkg'])))

timings = {}
deps = []

df_deps = df_full

fig, axs = plt.subplots(figsize=(6, 6), dpi=150)  

df.plot.scatter(x="dep_len", y="total", ax=axs)
axs.set_xlabel('Number of possible dependencies', fontsize=20)
axs.set_ylabel('Total time [s]', fontsize=20)
fig.savefig("total_time_vs_deps.png")



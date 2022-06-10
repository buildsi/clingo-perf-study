import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

DESCRIPTION = """Produce a CDF plot of Package number vs. Total execution time"""

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('csvfile', help='CSV file with timing data')
args = parser.parse_args()

df = pd.read_csv(args.csvfile, header=None, names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'dep_len'])

print(df.head())

cfg_ls = list(sorted(set(df['cfg'])))
pkg_ls = list(sorted(set(df['pkg'])))

fig, axs = plt.subplots(figsize=(6, 6), dpi=150)  

for cfg in cfg_ls:
    df_by_config = df[df['cfg'] == cfg]
    times = df_by_config['total']
    times.hist(cumulative=True, density=1, bins=100, ax=axs, label=cfg, histtype='step')

axs.set_xlabel('Total Time [sec.]', fontsize=20)
axs.set_ylabel('Percentage of package', fontsize=20)
axs.legend(loc='upper left')
fig.savefig("total_time_cdf.png")



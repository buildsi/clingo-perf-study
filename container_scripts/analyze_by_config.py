import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

DESCRIPTION = """Analyze CSV files"""

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('csvfile', help='CSV file with timing data')
args = parser.parse_args()

# Data analysis
df = pd.read_csv(args.csvfile, header=None, names=['pkg', 'cfg', 'iter', 'setup', 'load', 'ground', 'solve', 'total', 'ndeps'])
print(df.head())

cfg_ls = list(sorted(set(df['cfg'])))
pkg_ls = list(sorted(set(df['pkg'])))
timings = {}
for cf in cfg_ls:
    timings[cf] = {}
    for ph in SOLUTION_PHASES:
        timings[cf][ph] = []
    for pk in pkg_ls:
        tmp_df = df[df['pkg'] == pk]
        tdf = tmp_df[tmp_df['cfg'] == cf]
        for ph in SOLUTION_PHASES:
            timings[cf][ph].append(tdf[ph].median())

for cf in cfg_ls:
    fig, axs = plt.subplots(2, 3, sharey=True, tight_layout=True, figsize=(18,14), dpi=100)
    axes = list(axs.flatten())
    n_bins = 100

    fig.suptitle(cf, fontsize=24)
    
    axes[5].remove()
    for i, ph in enumerate(SOLUTION_PHASES):
        solve_times = sorted(zip(pkg_ls, timings[cf][ph]), key=lambda x: x[1], reverse=True)
        tab_data = [[p, "{:.3f}".format(t)] for p, t in solve_times[0:5]]

        axes[i].hist(sorted(timings[cf][ph], reverse=True), n_bins, label=ph)
        axes[i].set_title(ph, fontsize=18)
        tab = axes[i].table(cellText=tab_data, bbox=[0.1, -0.5, 0.75, 0.4])
        tab.auto_set_font_size(False)
        tab.auto_set_column_width(col=[0, 1])
        tab.set_fontsize(12)
    plt.savefig('times_{0}.png'.format(cf.strip()), dpi=150)

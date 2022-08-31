import argparse

import pandas as pd
import numpy as np
import glob
import re
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

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

fig, axs = plt.subplots(figsize=(6, 6), dpi=150)  

for cfg, color in [('tweety', "tab:red"), ('trendy', "tab:blue"), ('handy', "tab:purple")]:
    df_by_config = df[df['cfg'] == cfg]
    times = df_by_config['total']
    times.hist(cumulative=True, density=False, bins=500, ax=axs, label=cfg, histtype='step', color=color)

axs.set_xlabel('Time [s]', fontsize=20)
axs.set_ylabel('Package count', fontsize=20)
axs.legend(loc='lower right')

fig.tight_layout()
fig.savefig(args.outfile)

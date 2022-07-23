import argparse
import csv
import functools
import math
import multiprocessing
import os
import sys
import warnings

import tqdm

import spack.cmd
import spack.cmd.pkg
import spack.solver.asp as asp

sys.path.append('/opt/sc22/experiments')
import mpscript


DESCRIPTION = """
Run concretization tests on specs from an input file. Output the results in csv format.
"""

VALID_CONFIGURATIONS = 'tweety', 'handy', 'trendy', 'many'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-r', '--repetitions', type=int, help='number of repetitions for each spec', default=1)
parser.add_argument('--no-cores', dest='cores', action='store_false', help='disable cores in clingo')
parser.add_argument('-o', '--output', help='CSV output file', required=True)
parser.add_argument('--reuse', help='maximum reuse of buildcaches and installations', action='store_true')
parser.add_argument('--configs', help='comma separated clingo configurations', default='tweety')
parser.add_argument('-n', '--nprocess', help='number of processes to use to produce the results', default=os.cpu_count(), type=int)
parser.add_argument('specfile', help='text file with one spec per line')
args = parser.parse_args()
configs = args.configs.split(',')
if any(x not in VALID_CONFIGURATIONS for x in configs):
    print("Invalid configuration. Valid options are {0}".format(', '.join(VALID_CONFIGURATIONS)))

# Warmup spack to ensure caches have been written, and clingo is ready
# (we don't want to measure bootstrapping time)
specs = spack.cmd.parse_specs('hdf5')
asp.solve(specs, timers=False, reuse=args.reuse, rtimer=False, coref=args.cores)

# Read the list of specs to be analyzed
with open(args.specfile, "r") as f:
    lines = f.readlines()
    pkg_ls = [l.strip() for l in lines if l.strip()]


# Collect all the inputs in a single list to be passed to a multiprocessing Pool
input_list = []
for idx, pkg in enumerate(pkg_ls):
    specs = spack.cmd.parse_specs(pkg)
    for cf in configs:
        for i in range(args.repetitions):
            item = (args, specs, idx, cf, i)
            input_list.append(item)

# Perform the concretization tests
with multiprocessing.Pool(processes=args.nprocess) as pool:    
    pkg_stats = list(tqdm.tqdm(pool.imap(mpscript.process_single_item, input_list), total=len(input_list)))

pkg_stats = [x for x in pkg_stats if x is not None]
    
# Write results to CSV file
with open(args.output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(pkg_stats)

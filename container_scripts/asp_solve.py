import argparse
import csv
import math
import sys
import warnings

import spack.cmd
import spack.cmd.pkg
import spack.solver.asp as asp

DESCRIPTION = """
Run concretization tests on specs from an input file. Output the results in csv format.
"""

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'

# Basic command line options
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-r', '--repetitions', type=int, help='number of repetitions for each spec', default=1)
parser.add_argument('--no-cores', dest='cores', action='store_false', help='disable cores in clingo')
parser.add_argument('-o', '--output', help='CSV output file', required=True)
parser.add_argument('--reuse', help='maximum reuse of buildcaches and installations', action='store_true')
parser.add_argument('specfile', help='text file with one spec per line')
args = parser.parse_args()


# configs = ['tweety', 'handy', 'trendy', 'many']
configs = ['tweety']

# Warmup spack to ensure caches have been written, and clingo is ready
# (we don't want to measure bootstrapping time)
specs = spack.cmd.parse_specs('hdf5')
asp.solve(specs, timers=False, reuse=args.reuse, rtimer=False, coref=args.cores)

# Read the list of specs to be analyzed
with open(args.specfile, "r") as f:
    lines = f.readlines()
    pkg_ls = [l.strip() for l in lines if l.strip()]

# Perform the concretization tests
pkg_stats = []
for idx, pkg in enumerate(pkg_ls):

    print('Processing "{0}" [{1}/{2}]'.format(pkg, idx + 1, len(pkg_ls)))
    specs = spack.cmd.parse_specs(pkg)
    for cf in configs:
        for i in range(args.repetitions):
            try:
                sol_res, timer, len_pkgs, solve_stat = asp.solve(specs, timers=False, reuse=args.reuse, rtimer=True, coref=args.cores, conf=cf)
                timer.stop()
                time_by_phase = tuple(timer.phases[ph] for ph in SOLUTION_PHASES)
                pkg_stats.append(
                    (pkg, cf, i) +  time_by_phase + (timer.total, len_pkgs)
                )
            except Exception as e:
                warnings.warn(str(e))
                pass

# Write results to CSV file
with open(args.output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(pkg_stats)

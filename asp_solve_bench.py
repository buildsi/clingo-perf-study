#!/bin/sh
# -*- python -*-
#
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# This file is bilingual. The following shell code finds our preferred python.
# Following line is a shell no-op, and starts a multi-line Python comment.
# See https://stackoverflow.com/a/47886254
""":"
# prefer SPACK_PYTHON environment variable, python3, python, then python2
SPACK_PREFERRED_PYTHONS="python3 python python2 /usr/libexec/platform-python"
for cmd in "${SPACK_PYTHON:-}" ${SPACK_PREFERRED_PYTHONS}; do
    if command -v > /dev/null "$cmd"; then
        export SPACK_PYTHON="$(command -v "$cmd")"
        exec "${SPACK_PYTHON}" "$0" "$@"
    fi
done

echo "==> Error: spack could not find a python interpreter!" >&2
exit 1
":"""
# Line above is a shell no-op, and ends a python multi-line comment.
# The code above runs this file with our preferred python interpreter.

from __future__ import print_function

import os
import sys

min_python3 = (3, 5)

if sys.version_info[:2] < (2, 6) or (
    sys.version_info[:2] >= (3, 0) and sys.version_info[:2] < min_python3
):
    v_info = sys.version_info[:3]
    msg = "Spack requires Python 2.6, 2.7 or %d.%d or higher " % min_python3
    msg += "You are running spack with Python %d.%d.%d." % v_info
    sys.exit(msg)

# Find spack's location and its prefix.
# spack_file = os.path.realpath(os.path.expanduser(__file__))
# spack_prefix = os.path.dirname(os.path.dirname(spack_file))

spack_prefix = '/g/g92/shudler1/projects/asp/spack'

# Allow spack libs to be imported in our scripts
spack_lib_path = os.path.join(spack_prefix, "lib", "spack")
sys.path.insert(0, spack_lib_path)

# Add external libs
spack_external_libs = os.path.join(spack_lib_path, "external")

if sys.version_info[:2] <= (2, 7):
    sys.path.insert(0, os.path.join(spack_external_libs, "py2"))
if sys.version_info[:2] == (2, 6):
    sys.path.insert(0, os.path.join(spack_external_libs, "py26"))

sys.path.insert(0, spack_external_libs)

# Here we delete ruamel.yaml in case it has been already imported from site
# (see #9206 for a broader description of the issue).
#
# Briefly: ruamel.yaml produces a .pth file when installed with pip that
# makes the site installed package the preferred one, even though sys.path
# is modified to point to another version of ruamel.yaml.
if "ruamel.yaml" in sys.modules:
    del sys.modules["ruamel.yaml"]

if "ruamel" in sys.modules:
    del sys.modules["ruamel"]

# import spack.main  # noqa

import spack.cmd
import spack.cmd.pkg
import spack.solver.asp as asp

import math
from mpi4py import MPI


# Once we've set up the system path, run the spack main method
# if __name__ == "__main__":
#     pkg_ls = pkg.list_packages('')
#     for p in pkg_ls:
#         print(p)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    nsz = comm.Get_size()
    mrank = comm.Get_rank()

    solphases = ['setup', 'load', 'ground', 'solve']
    confs = ['tweety', 'handy', 'trendy', 'many']
    # confs = ['handy', 'trendy', 'many']
    # confs = ['many']
    opts = 'usc,one'
    single_pkg = None
    # reps = 5
    reps = 3

    if len(sys.argv) > 1:
        confs = [sys.argv[1]]
    if len(sys.argv) > 2:
        opts = sys.argv[2]
    if len(sys.argv) > 3:
        single_pkg = sys.argv[3]

    # print('rank = {0}: size = {1}'.format(mrank, nsz))

    # outfile = 'timings/out_log_{0}.csv'.format(rank)
    # of = open(outfile, "w")

    # # stdout = sys.stdout
    # # sys.stdout = open(outfile, 'w')

    # warmup
    specs = spack.cmd.parse_specs('hdf5')
    asp.solve(specs, timers=False, conf='many', opts=opts)

    if mrank == 0:
        # print(confs)
        # print(opts)
        with open("pkg_list.txt", "r") as f:
            lines = f.readlines()
        pkg_ls = [l.strip() for l in lines]
        # pkg_ls = spack.cmd.pkg.list_packages('HEAD')
        # pkg_ls = pkg_ls[:512]
    else:
        pkg_ls = None
    
    if single_pkg and mrank == 0:
        # print('>> {0}'.format(single_pkg))
        specs = spack.cmd.parse_specs(single_pkg)
        sol_res = asp.solve(specs, timers=True, conf=nsz, opts=opts)
    elif not single_pkg:
        # pkg_ls = comm.bcast(pkg_ls, root = 0)
        
        # loc_pkg_sz = max(int(len(pkg_ls) / float(nsz) + 0.5), 2)
        # loc_pkg_sz = int(math.ceil(len(pkg_ls) / float(nsz)))
        # print('rank = {0}: loc_pkg_sz = {1}'.format(mrank, loc_pkg_sz))
        # sys.stdout.flush()

        term_str = '=='
        req_str = '^^'

        if mrank == 0:
            pkg_idx = 0
            terminated = 0
            for i in range(1, nsz):
                pkg = term_str      # termination string
                if pkg_idx < len(pkg_ls):
                    pkg = pkg_ls[pkg_idx]
                else:
                    terminated += 1
                comm.send(pkg, dest=i)
                # print('send pkg {0} to rank {1}'.format(pkg, i))
                # sys.stdout.flush()
                pkg_idx += 1
                print('package {0} out of {1}'.format(pkg_idx, len(pkg_ls)), file=sys.stderr)
            while pkg_idx < len(pkg_ls):
                pkg = pkg_ls[pkg_idx]
                status = MPI.Status()
                comm.recv(source=MPI.ANY_SOURCE, status=status, tag=11)    # pkg request
                comm.send(pkg, dest=status.Get_source())
                # print('send pkg {0} to rank {1}, idx = {2}'.format(pkg, status.Get_source(), pkg_idx))
                # sys.stdout.flush()
                pkg_idx += 1
                print('package {0} out of {1}'.format(pkg_idx, len(pkg_ls)), file=sys.stderr)
            while terminated < nsz - 1:
                comm.recv(source=MPI.ANY_SOURCE, status=status, tag=11)    # pkg request
                comm.send(term_str, dest=status.Get_source())
                # print('send termination to rank {1}'.format(pkg, status.Get_source()))
                # sys.stdout.flush()
                terminated += 1
        else:   # mrank > 0
            pkg = comm.recv(source=0)
            # print('rank {0} recv {1}'.format(mrank, pkg))
            # sys.stdout.flush()
            while pkg != '==':
                rp = reps
                if pkg == 'arbor' or pkg == 'py-unicycler':
                    rp = 1
                specs = spack.cmd.parse_specs(pkg)
                for cfg in confs:
                    for i in range(rp):
                        try:
                            # print('{0} {1} {2}'.format(pkg, cfg, i))
                            sol_res, timer = asp.solve(specs, timers=False, conf=cfg, opts=opts)
                            timer.stop()

                            all_times = ', '.join([str(timer.phases[ph]) for ph in solphases])
                            print('{0}, {1}, {2}, {3}, {4}'.format(pkg, cfg, i, all_times, timer.total))
                            sys.stdout.flush()
                        except:
                            pass
                comm.send(req_str, dest=0, tag=11)    # request another package
                # print('send req from rank {0}'.format(mrank))
                # sys.stdout.flush()
                pkg = comm.recv(source=0)
                # print('rank {0} recv {1}'.format(mrank, pkg))
                # sys.stdout.flush()
                                        
    # print('entering barrier - rank {0}'.format(mrank))
    # sys.stdout.flush()
    comm.Barrier() 

        # timings = {}

        # for i in range(loc_pkg_sz*mrank, loc_pkg_sz*(mrank+1)):
        #     # print('rank = {0}: i = {1}'.format(mrank, i))
        #     if i >= len(pkg_ls):
        #         break
        #     pkg = pkg_ls[i]
        #     timings[pkg] = {}
        #     # print('>> {0}'.format(pkg))
        #     # sys.stdout.flush()
        #     specs = spack.cmd.parse_specs(pkg)
        #     for cfg in confs:
        #         timings[pkg][cfg] = []
        #         for i in range(reps):
        #             # sys.stdout = open('{0}_{1}'.format(outfile, cfg), 'a')

        #             try:
        #                 sol_res, timer = asp.solve(specs, timers=False, conf=cfg, opts=opts)
        #                 timer.stop()
        #                 # print('Timer: {0}'.format(timer.total))

        #                 all_times = ', '.join([str(timer.phases[ph]) for ph in solphases])
        #                 print('{0}, {1}, {2}, {3}, {4}'.format(pkg, cfg, i, all_times, timer.total))
        #                 sys.stdout.flush()

        #                 timings[pkg][cfg].append(timer)
        #             except:
        #                 pass
                                        
        #             # of.write('{0}, {1}, {2}, '.format(pkg, cfg, i))
        #             # for ph in solphases:
        #             #     of.write('{0}, '.format(timers.phases[ph]))
        #             # of.write('{0}\n'.format(timers.total))

        # all_timings = comm.gather(timings, root = 0)
        # if mrank == 0:
        #     of = open('timings_data.csv', "w")
        #     for rank_timings in all_timings:
        #         for pkg in rank_timings.keys():
        #             for cfg in rank_timings[pkg].keys():
        #                 for j, tim in enumerate(rank_timings[pkg][cfg]):
        #                     of.write('{0}, {1}, {2}, '.format(pkg, cfg, j))
        #                     for ph in solphases:
        #                         of.write('{0}, '.format(tim.phases[ph]))
        #                     of.write('{0}\n'.format(tim.total))
        #     of.close()

    # of.close()
    # sys.stdout = stdout

    # comm.Barrier()

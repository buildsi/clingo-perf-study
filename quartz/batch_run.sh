#!/usr/bin/bash

#SBATCH -N 16
#SBATCH -t 8:00:00
#SBATCH -p pbatch

echo "Start: `date`"

source /g/g92/shudler1/projects/py-venv/bin/activate

TESTDIR=/g/g92/shudler1/projects/asp/timings
# mkdir $TESTDIR
# cd $TESTDIR
srun -N16 -n512 python3 ./asp_solve_1.py > out_log_full_complete.csv

echo "Done: `date`"

#!/usr/bin/bash

# ACCOUNT=${ACCOUNT:-`groups | awk '{print $NF}'`}

TMPFILE=batchjob.lsf

cat > $TMPFILE << ENDINPUT
#!/usr/bin/bash
#BSUB -W 06:00
#BSUB -nnodes 16
#BSUB -alloc_flags smt1
#BSUB -J BenchRun
#BSUB -o BenchRun-o.%J
#BSUB -e BenchRun-e.%J


echo "Start: `date`"

# source $HOME/projects/asp/lassen/spack/share/spack/setup-env.sh
# cd $HOME/projects/asp/lassen/runs

# mkdir stats

# lrun -n 128 python3 ../../asp_solve_bench.py 0 > out_log_full_crs_0.csv

# source ../pyenv/bin/activate

# Full cache  [63099 packages]
# lrun -n 128 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_full.csv

lrun -n 128 python3 ../../concrete_solve_bench.py 1 > log_old_concretizer.csv

# Reduced cache (only target ppc64)  [27160 packages]
# cp ~/.spack/cache/indices/reduced_ppc64le.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json
# lrun -n 128 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_3.csv

# Reduced cache (only os rhel7)  [15255 packages]
# cp ~/.spack/cache/indices/reduced_rhel7.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json
# lrun -n 128 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_2.csv

# Reduced cache (only target ppc64 and os rhel7)  [6804 packages]
# cp ~/.spack/cache/indices/reduced_ppc64le_rhel7.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json
# lrun -n 128 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_1.csv

# Restore full cache
# cp ~/.spack/cache/indices/bak-714ed82990_a42a15256d.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json

echo "Done: `date`"

ENDINPUT

cat $TMPFILE

bsub $TMPFILE

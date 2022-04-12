#!/usr/bin/bash

# ACCOUNT=${ACCOUNT:-`groups | awk '{print $NF}'`}

TMPFILE=batchjob.slurm

cat > $TMPFILE << ENDINPUT
#!/usr/bin/bash
#SBATCH -N 4
#SBATCH -t 4:00:00
#SBATCH -p pbatch

echo "Start: `date`"

source /g/g92/shudler1/projects/py-venv/bin/activate

# TESTDIR=/g/g92/shudler1/projects/asp/timings
# mkdir $TESTDIR
# cd $TESTDIR
# srun -N8 -n256 python3 ../../asp_solve_bench.py 1 > out_log_full_sshot.csv

# Full cache  [63099 packages]
cp ~/.spack/cache/indices/bak-714ed82990_a42a152 ~/.spack/cache/indices/714ed82990_a42a15256d.json
# srun -N4 -n128 python3 ../../asp_solve_bench.py 1 > log_mpi_dep.csv
srun -N4 -n128 python3 ../../concrete_solve_bench.py 1 > log_old_concretizer.csv

# # Reduced cache (only target ppc64)  [27160 packages]
# cp ~/.spack/cache/indices/reduced_ppc64le.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json
# srun -N8 -n256 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_3.csv

# # Reduced cache (only os rhel7)  [15255 packages]
# cp ~/.spack/cache/indices/reduced_rhel7.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json
# srun -N8 -n256 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_2.csv

# # Reduced cache (only target ppc64 and os rhel7)  [6804 packages]
# cp ~/.spack/cache/indices/reduced_ppc64le_rhel7.json.bak ~/.spack/cache/indices/714ed82990_a42a15256d.json
# srun -N8 -n256 python3 ../../asp_solve_bench.py 1 > cache_runs/out_log_cache_1.csv

# # Restore full cache
# cp ~/.spack/cache/indices/bak-714ed82990_a42a152 ~/.spack/cache/indices/714ed82990_a42a15256d.json

echo "Done: `date`"


ENDINPUT

cat $TMPFILE

sbatch $TMPFILE

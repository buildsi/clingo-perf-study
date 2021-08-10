# Scripts and data for Clingo performance study

`asp_solve_bench.py` - Modified `asp_solve.py` that uses MPI4Py to benchmark Clingo solving times for all the current packages in Spack.
`batch_run.sh` - A script to run the benchmarking (so far only on Quartz).
`pkg_list.txt` - A list of current packages (should be updated from time to time). Easier to read the packages of from the list (rather than scan Spack's package directory / git) when running benchmarks.
`*.csv` - Results from the last benchmarking run (on Quartz). The columns are: package name, Clingo conf name, benchmark repetition number, setup time, load time, ground time, solve time, and total time. All the times are in seconds.
`Analyze_results.ipynb` - Jupyter notebook for analyzing the results and producing plots.
`*.png` - Plots produced from the current results.

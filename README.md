# Reproducing smaller scale analysis with a container

The `ghcr.io/buildsi/clingo-performance-study` image
permits to reproduce results of the same kind of the ones
appearing in the paper. To get the image and
run it interactively just:
```console
$ docker pull ghcr.io/buildsi/clingo-performance-study:latest
$ docker run -it ghcr.io/buildsi/clingo-performance-study:latest
root@451285db7312:/opt/sc22/experiments#
```

## Description of the image content

In the image we'll find one script to produce CSV data from concretization:
```console
# spack python asp_solve.py -h
usage: asp_solve.py [-h] [-r REPETITIONS] [--no-cores] -o OUTPUT [--reuse]
                    [--configs CONFIGS]
                    specfile

Run concretization tests on specs from an input file. Output the results in
csv format.

positional arguments:
  specfile              text file with one spec per line

optional arguments:
  -h, --help            show this help message and exit
  -r REPETITIONS, --repetitions REPETITIONS
                        number of repetitions for each spec
  --no-cores            disable cores in clingo
  -o OUTPUT, --output OUTPUT
                        CSV output file
  --reuse               maximum reuse of buildcaches and installations
  --configs CONFIGS     comma separated clingo configurations
```
This script must be run using `spack python` to load automatically a few
Spack core Python packages that will be benchmarked. Its only mandatory inputs are:
1. The name of the output file, passed with the `--output` argument
2. The name of the input file to process

The input file is a simple text file with one abstract spec per line. There are 4
inputs already prepared for convenience:
- `build-tools.list` is the smallest and contains only 10 specs
- `radiuss.list` is slightly larger, with 26 specs
- `e4s.list` is a medium sized example, with 94 specs
- `full.list` is the full analysis containing 5969 packages

The full analysis done in the paper targets thousands of packages in the built-in repository,
and might take a few hours when reproduced in the docker container. For convenience,
we also added a parallel version of the script in the container:
```console
root@ecd657dc1733:/opt/sc22/experiments# spack python asp_solve_parallel.py -h
usage: asp_solve_parallel.py [-h] [-r REPETITIONS] [--no-cores] -o OUTPUT
                             [--reuse] [--configs CONFIGS] [-n NPROCESS]
                             specfile

Run concretization tests on specs from an input file. Output the results in
csv format.

positional arguments:
  specfile              text file with one spec per line

optional arguments:
  -h, --help            show this help message and exit
  -r REPETITIONS, --repetitions REPETITIONS
                        number of repetitions for each spec
  --no-cores            disable cores in clingo
  -o OUTPUT, --output OUTPUT
                        CSV output file
  --reuse               maximum reuse of buildcaches and installations
  --configs CONFIGS     comma separated clingo configurations
  -n NPROCESS, --nprocess NPROCESS
                        number of processes to use to produce the results
```
The only difference with the serial script above is the possibility to run the analysis using
multiple processes.

There are then a few scripts that produce different PNG images out of the CSV files.
These scripts can be run directly with the Python interpreter:
```console
# python analyze_deps_vs_time.py -h
usage: analyze_deps_vs_time.py [-h] csvfile

Analyze CSV files

positional arguments:
  csvfile     CSV file with timing data

optional arguments:
  -h, --help  show this help message and exit
```

### Example: create a CSV file for Radiuss timing 4 different clingo configurations

Running the following command:
```console
# spack python asp_solve.py --configs=tweety,handy,many,trendy -o radiuss.csv radiuss.list 
Processing "ascent" [1/26]
Processing "axom" [2/26]
Processing "blt" [3/26]
Processing "caliper" [4/26]
Processing "care" [5/26]
Processing "chai" [6/26]
Processing "conduit" [7/26]
Processing "flux-core" [8/26]
Processing "flux-sched" [9/26]
Processing "glvis" [10/26]
Processing "hypre" [11/26]
Processing "lbann" [12/26]
Processing "lvarray" [13/26]
Processing "mfem" [14/26]
Processing "py-hatchet" [15/26]
Processing "py-maestrowf" [16/26]
Processing "py-merlin" [17/26]
Processing "py-shroud" [18/26]
Processing "raja" [19/26]
Processing "samrai" [20/26]
Processing "scr" [21/26]
Processing "sundials" [22/26]
Processing "umpire" [23/26]
Processing "visit" [24/26]
Processing "xbraid" [25/26]
Processing "zfp" [26/26]
```
we are able to produce timings for 4 different clingo configurations in a file called `e4s.csv`:
```console
# ls *.csv
radiuss.csv
```

### Example: create a CSV file for E4S using multiple processes

Running the following command:
```console
# spack python asp_solve_parallel.py -n 4 --configs=tweety,handy,many,trendy -o e4s.csv e4s.list
  5%|███████▊                                                                                                                                                                     | 17/376 [00:46<15:36,  2.61s/it]
```
we are able to produce the same timings as above, using 4 processes.

### Example: create a scatter plot from the previous analysis

To create a scatter plot of the "Total execution time" vs. "Number of possible dependencies" we can:
```console
# python analyze_deps_vs_time.py radiuss.csv 
      pkg     cfg  iter     setup      load    ground      solve      total  dep_len
0  ascent  tweety     0  9.002133  0.020047  2.254575   6.058987  17.683321      569
1  ascent   handy     0  7.693530  0.019825  2.236072   9.878695  20.397330      569
2  ascent    many     0  7.778153  0.019949  2.220320   6.538377  17.011132      569
3  ascent  trendy     0  7.746319  0.019906  2.221928  10.713907  21.302030      569
4    axom  tweety     0  7.307354  0.019735  2.203507   5.262867  15.186229      568
```
This will produce a PNG file in the current folder:
```console
# ls *.png
total_time_vs_deps.png
```
This image can be copied out of the container to be viewed.

### Example: compare the old concretizer with the ASP-based concretizer

To compare the old concretizer with the ASP-based concretizer, we need to create CSV data
files with timings for both:
```console
# spack python asp_solve_parallel.py -o full.csv full.list
# spack python old_solve_parallel.py -o full_old.csv  full.list
```
After the data is available we can produce CDF plots:
```console
# spack python analyze_old_vs_asp.py full_old.csv full.csv 
                      pkg  concrete  iter      total
0                    3dtk      True     0  19.763435
1                  3proxy      True     0   1.060040
2                  abduco      True     0   0.055681
3  abi-compliance-checker      True     0   1.613308
4              abi-dumper      True     0   1.819048
                      pkg     cfg  iter     setup      load    ground     solve      total  dep_len
0                    3dtk  tweety     0  5.733069  0.021333  1.887932  4.313959  12.334170      526
1                  3proxy  tweety     0  0.286021  0.022896  0.047723  0.017978   0.397128       22
2                  abduco  tweety     0  0.237749  0.022638  0.023535  0.001426   0.288637        1
3  abi-compliance-checker  tweety     0  4.151938  0.027763  1.273631  2.331371   7.996720      446
4              abi-dumper  tweety     0  4.018198  0.021273  1.260120  2.323686   7.830463      445
The old concretizer failed on 428 packages. Skipping them from the plot.

# ls *.png 
total_time_old_vs_asp_cdf.png
```

# Real analysis performed in the paper

For the full scale analysis we used modified versions of the script in the container. The
modification consists in the use of MPI4PY to distribute the work among different nodes in
a cluster, in order to speed-up the analysis.

Relevant files have been stored in this repository and are:

- `asp_solve_bench.py` - Modified `asp_solve.py` that uses MPI4Py to benchmark Clingo solving times for all the current packages in Spack.
- `pkg_list.txt` - A list of current packages (should be updated from time to time). Easier to read the packages of from the list (rather than scan Spack's package directory / git) when running benchmarks.
- `Analyze_results.ipynb` - Jupyter notebook for analyzing the results and producing plots.
- `quartz` subdirectory:
    - `batch_run.sh` - A script to run the benchmarking (so far only on Quartz).
    - `*.csv` - Results from the last benchmarking run (on Quartz). The columns are: package name, Clingo conf name, benchmark repetition number, setup time, load time, ground time, solve time, and total time. All the times are in seconds.
    - `*.png` - Plots produced from the current results.
    - `sizes_db.csv` - Number of lines in the fact and grounded files per each package.
- `lassen` subdirectory:
    - `*.csv` - Results from the last benchmarking run (on Lassen). The columns are: package name, Clingo conf name, benchmark repetition number, setup time, load time, ground time, solve time, and total time. All the times are in seconds.
    - `*.png` - Plots produced from the current results.
    - `sizes_db.csv` - Number of lines in the fact and grounded files per each package.
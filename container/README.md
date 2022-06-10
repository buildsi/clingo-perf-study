This image permits to reproduce smaller scale results similar to the full analysis
conducted on the full Spack built-in repository.

There's one script to produce CSV data from concretization:
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
this script must be run using `spack python` to setup the Python configuration for
using Spack core Python packages. It's only mandatory inputs are:
1. The name of the output file, passed with the `--output` argument
2. The name of the input file to process

The input file is a simple text file with one abstract spec per line. There are 3
inputs already prepared for convenience:
- `build-tools.list` is the smallest and contains only 10 specs
- `radiuss.list` is slightly larger, with 26 specs
- `e4s.list` is the largest, with 94 specs

The full analysis targets thousands of packages in the built-in repository.

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

## Example: create a CSV file for Radiuss timing 4 different clingo configurations

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

## Example: create a scatter plot from the previous analysis

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
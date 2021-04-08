# GateBenchmarks

This repository contains Gate benchmarks used to compare current an previous Gate versions. 

To use it: 
* Clone the repository: `git clone --recursive https://github.com/OpenGATE/GateBenchmarks.git`
* Check that the Gate version you want to test is in your PATH: `which Gate` and `Gate --version` (for recent Gate version)
* Install the https://github.com/OpenGATE/GateTools : `pip install gatetools` (required)
* Run a benchmark: `./runBenchmark.py  -t t1` (for test t1)
* This will create a result in the t1 folder, you can then look at the file `output.pdf`

Note the you can run all tests at once with `./runBenchmark.py` (without argument)

**STILL WORK IN PROGRESS**

# How to deal with LFS:
* To avoid to exceed Github LFS quota, the binary data are pointers (symbolic links) to a Gitlab subdirectory (https://gitlab.in2p3.fr/opengate/gatebenchmarks_data)
* If you clone the repository for the first time, use `--recursive` option to download the subdirectory
* To pull new commits of the subdirectory, you can do: `git submodule update --recursive --remote`
* If you already have the repository without the subdirectory, you can do: `git submodule update --init --recursive`

# How to propose a new test ?

* Create a Gate macro in a folder, with the subfolders `data`, `mac`and `output` (see folder `t1` for example)
* Create a `runTest.py` Python script that will run your simulation
* Create a `runAnalysis.py`Python script to analyse the output. This script must take as input a list of output folders where the output of different Gate version for this test will be compared and analyzed. 
* To avoid to reach the Github quota for LFS, we share the LFS binary data in https://gitlab.in2p3.fr/opengate/gatebenchmarks_data


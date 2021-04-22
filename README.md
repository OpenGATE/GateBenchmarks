# GateBenchmarks

This repository contains Gate benchmarks used to compare current an previous Gate versions. 

To use it: 
* Clone the repository: `git clone --recursive https://github.com/OpenGATE/GateBenchmarks.git`
* Check that the Gate version you want to test is in your PATH: `which Gate` and `Gate --version` (for recent Gate version)
* Install the https://github.com/OpenGATE/GateTools : `pip install gatetools` (required)
* Run a benchmark: `./runBenchmark.py -t t1_edep_profiles` (for test t1_edep_profiles)
* This will create a result in the t1_edep_profiles folder, you can then look at the file `output.pdf`

Note the you can run all tests at once with `./runBenchmark.py` (without argument).  
You can also run the tests in a docker image with:  
`docker run --rm -e "COMMIT=v9.1" -e "TEST=t1_edep_profiles" -v $PWD:/home tbaudier/gatebenchmarks:9.1 /home/.github/workflows/runTest.sh`  
You can adapt the variables `COMMIT` with the commit/tag of Gate you want to compile and `TEST`with the test folder name you want to execute. The docker image is available here https://hub.docker.com/r/tbaudier/gatebenchmarks with the corresponding tags of different Gate versions.

**WARNING** (04/2021) This is a first version of the benchmarks, still incomplete. Some tests (in particular t4 and t7) sometimes still fail due to the stochastic nature of the simulation. It would require a simulation with too long computation time regarding the CPU limits (or a too high tolerance). It will be improved in the future.

# How to deal with LFS:

* To avoid to exceed Github LFS quota, the binary data are pointers (symbolic links) to a Gitlab subdirectory (https://gitlab.in2p3.fr/opengate/gatebenchmarks_data)
* If you clone the repository for the first time, use `--recursive` option to download the subdirectory
* To pull new commits of the subdirectory, you can do: `git submodule update --recursive --remote`
* If you already have the repository without the subdirectory, you can do: `git submodule update --init --recursive`

# How to propose a new test ?

* Create a Gate macro in a folder, with the subfolders `data`, `mac`and `output` (see folder `t1_edep_profiles` for example)
* Create a `runTest.py` Python script that will run your simulation
* Create a `runAnalysis.py`Python script to analyse the output. This script must take as input a list of output folders where the output of different Gate versions for this test will be compared and analyzed. You have to implement two functions: `analyse_command_line` and `analyse_all_folders` and you have to return `True` or `False`.
* To avoid to reach the Github quota for LFS, we share the LFS binary data in https://gitlab.in2p3.fr/opengate/gatebenchmarks_data
* Contact us in issues or pull request to have help or submit your test




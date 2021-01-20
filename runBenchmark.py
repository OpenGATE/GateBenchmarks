#!/usr/bin/env python3

import os
import click
import shutil
import colorama
import subprocess
import sys

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--test', default="all", help="Name of the test, if all run all benchmarks")
def runTests_click(test, **kwargs):
    '''
    Run the benchmarks available in the current folder
    '''
    returnedTest = runTests(test)
    print(returnedTest)

def runTests(test, release=None):

    #Look for the tests
    testFolders = [ ]
    currentDirectory = os.getcwd()
    for dir in os.listdir(currentDirectory):
        if os.path.isdir(dir) and test == "all" or test == dir:
            if not dir.startswith('.git') and not dir == "gatebenchmarks_data":
                testFolders += [dir]
    print(testFolders)

    command = 'which Gate'
    subprocess.run(command, shell=True, check=True)

    if release is not None:
        print(colorama.Fore.RED + 'Are you sure to use Gate release: ' + str(release) + ' ? (y/n) ' + colorama.Style.RESET_ALL)
        while(True):
            choice = input().lower()
            if choice == "y":
               break
            elif choice == "n":
               return
            else:
               print("Please respond with 'y' or 'n'")

    #Go inside folders and run the tests:
    for testFolder in testFolders:
        print("Run test: " + testFolder)
        os.chdir(testFolder)
        if os.path.isdir("output"):
            shutil.rmtree("output")
        os.makedirs("output")
        command = 'bash ./runTest.sh'
        subprocess.run(command, shell=True, check=True)
        if release is not None:
            shutil.move("output", "output-" + str(release))
        os.chdir(currentDirectory)

    #Go inside folders and run the analysis:
    analyseOutput = 0
    for testFolder in testFolders:
        print("Run analysis: " + testFolder)
        os.chdir(testFolder)
        outputFolders = []
        for dir in os.listdir(path='.'):
          if os.path.isdir(dir) and dir.startswith("output"):
              outputFolders.append(dir)
        sys.path.insert(1, '.')
        import runAnalysis
        analyseOutput = runAnalysis.analyse_all_folders(outputFolders)
        os.chdir(currentDirectory)
    if len(testFolders) == 1:
        return analyseOutput
    else:
        return 1

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    runTests_click()


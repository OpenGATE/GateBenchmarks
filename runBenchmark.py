#!/usr/bin/env python3

import os
import click
import shutil

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--test', default="all", help="Name of the test, if all run all benchmarks")
@click.option('-r', '--release', default="9.0", help="Run the test for this release")
def runTests_click(test, release, **kwargs):
    '''
    Run the benchmarks available in the current folder
    '''
    runTests(test, release)

def runTests(test, release):

    #Look for the tests
    testFolders = [ ]
    currentDirectory = os.getcwd()
    for dir in os.listdir(currentDirectory):
        if os.path.isdir(dir) and test == "all" or test == dir:
            testFolders += [dir]
    print(testFolders)

    command = 'which Gate'
    os.system(command)

    #Go inside folders and run the tests:
    for testFolder in testFolders:
        os.chdir(testFolder)
        if os.path.isdir("output"):
            shutil.rmtree("output")
        os.makedirs("output")
        command = 'bash ./runTest.sh'
        os.system(command)
        os.chdir(currentDirectory)

    #Go inside folders and run the analysis:
    currentDirectory = os.getcwd()
    for testFolder in testFolders:
        os.chdir(testFolder)
        command = 'python ./runAnalysis.py output*'
        os.system(command)
        os.chdir(currentDirectory)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    runTests_click()


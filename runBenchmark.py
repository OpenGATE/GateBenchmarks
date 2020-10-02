#!/usr/bin/env python3

import os
import click
import shutil
import colorama

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--test', default="all", help="Name of the test, if all run all benchmarks")
def runTests_click(test, **kwargs):
    '''
    Run the benchmarks available in the current folder
    '''
    runTests(test)

def runTests(test, release=None):

    #Look for the tests
    testFolders = [ ]
    currentDirectory = os.getcwd()
    for dir in os.listdir(currentDirectory):
        if os.path.isdir(dir) and test == "all" or test == dir:
            if not dir.startswith('.git'):
                testFolders += [dir]
    print(testFolders)

    command = 'which Gate'
    os.system(command)

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
        os.system(command)
        if release is not None:
            shutil.move("output", "output-" + str(release))
        os.chdir(currentDirectory)

    #Go inside folders and run the analysis:
    for testFolder in testFolders:
        print("Run analysis: " + testFolder)
        os.chdir(testFolder)
        command = 'python ./runAnalysis.py output*'
        os.system(command)
        os.chdir(currentDirectory)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    runTests_click()


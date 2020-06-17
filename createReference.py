#!/usr/bin/env python3

import click
from runBenchmark import *

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--test', default="all", help="Name of the test, if all run all benchmarks")
@click.option('-r', '--reference', default=None, help="Create the reference for the tests for the version of Gate")
def runTestsReference_click(test, reference, **kwargs):
    '''
    Run the benchmarks available in the current folder and create the reference for the release of Gate available in the PATH
    For developpers only
    '''
    runTests(test, reference)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    runTestsReference_click()


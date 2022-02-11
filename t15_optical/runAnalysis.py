#!/usr/bin/env python3

import gatetools as gt
import gatetools.phsp as phsp
import itk
import click
import sys
import os
import numpy as np
import logging
import numpy.lib.recfunctions as rfn

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import glob
logger=logging.getLogger(__name__)

# Tolerance
TOL = 98

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_click(output_folders, **kwargs):
    '''
    TODO
    '''
    r = analyse_all_folders(output_folders)
    print(f'Last test return is: {r}')


def analyse_all_folders(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)

    print("analyse_all_folders = ", output_folders)

    rets = map(analyse_one_folder, output_folders)


    return all(rets)

def analyse_one_folder(output_folder):
    print("analyse_one_folder = ", output_folder)
    hits_path = os.path.join(output_folder, "p.hits.npy")
    Hits = np.load(hits_path)

    rets = []
    #rets.append(np.all(RootHits['PDGEncoding'] >= 0))

    photons = Hits[Hits['PDGEncoding'] < 0]
    _, count = np.unique(photons['eventID'], return_counts=True)
    n = count[count > 300]
    y, x = np.histogram(n, bins=32)
    x = (x[0:-1] + x[1:]) / 2
    mean = 450
    sigma = np.std(n)

    # Gaussian function
    def gauss_function(x, a, x0, sigma):
        return a / (sigma * np.sqrt(2 * 3.14)) * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

    # do the fit!
    popt, pcov = curve_fit(gauss_function, x, y, p0=[1, mean, sigma])
    # plot the fit results
    plt.plot(x, gauss_function(x, *popt))
    # confront with the given data
    plt.hist(n, bins=32)

    a, x0, sigma = popt


    print("mean = ", x0)

    rets.append(372 < x0 < 490)
    res = 100*(2.355 * sigma) / x0

    rets.append(9 < res < 13)

    print( "res = ",  res )







    return all(rets)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

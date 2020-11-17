#!/usr/bin/env python3

import gatetools as gt
import gatetools.phsp as phsp
import itk
import click
import sys
import os
import numpy as np
import logging
import matplotlib.pyplot as plt
logger=logging.getLogger(__name__)

# -----------------------------------------------------------------------------
def plot(output_folder, a, filename, axis1, axis2):

    if not os.path.isdir(output_folder):
        return
    
    if os.path.isfile(os.path.join(output_folder, filename + "_" + str(axis1) + "_"+ str(axis2) + ".npy")):
        x, y = np.loadtxt(os.path.join(output_folder, filename + "_" + str(axis1) + "_"+ str(axis2) + ".npy"), unpack=True)
    elif os.path.isfile(os.path.join(output_folder, filename)):
        f = os.path.join(output_folder, filename)
        logger.info('Load ' + f)
        img = itk.imread(f)

        # img spacing
        spacing = img.GetSpacing()

        # get data in np
        data = itk.GetArrayViewFromImage(img)

        y = np.sum(data, axis=axis1)
        y = np.sum(y, axis=axis2)
        x = np.arange(len(y)) * spacing[2]

        # saving:
        np.savetxt(os.path.join(output_folder, filename + "_" + str(axis1) + "_"+ str(axis2) + ".npy"), np.array([x, y]).T)
    else:
        return

    a.plot(x,y, label=output_folder)
    a.legend()

# -----------------------------------------------------------------------------
def plot_all(output_folders, filename, ax, i, axis1, axis2):
    a = phsp.fig_get_sub_fig(ax,i)
    a.set_title(filename)
    for o in output_folders:
        plot(o, a, filename, axis1, axis2)
    return i+1
    
# -----------------------------------------------------------------------------
def plot_axes(output_folders, filename, ax, i):
    i = plot_all(output_folders, filename, ax, i, 0, 0)
    i = plot_all(output_folders, filename, ax, i, 1, 1)
    i = plot_all(output_folders, filename, ax, i, 0, 1)
    return i
    
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
    analyse(output_folders)

def analyse(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)

    # plot
    ncols=3
    nrows=4
    fig, ax = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15, 10))

    i = 0
    i = plot_axes(output_folders, 'dose-photon-NPV1-Edep.mhd', ax, i)
    i = plot_axes(output_folders, 'dose-photon-NPV2-Edep.mhd', ax, i)
    i = plot_axes(output_folders, 'dose-photon-RV1-Edep.mhd', ax, i)
    i = plot_axes(output_folders, 'dose-photon-RV2-Edep.mhd', ax, i)
    
    plt.savefig('output.pdf')
    plt.show()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

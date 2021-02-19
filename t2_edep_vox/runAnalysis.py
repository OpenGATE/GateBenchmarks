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

# Tolerance
TOL = 14

# -----------------------------------------------------------------------------
def plot(output_folder, a, filename, axis1, axis2):

    if not os.path.isdir(output_folder):
        return
    
    if os.path.isfile(os.path.join(output_folder, filename)):
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
    r = analyse_all_folders(output_folders)
    print(f'Last test return is: {r}')

def analyse_all_folders(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)
    
    #Analyze folder
    previous_folder = None
    r = None
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(folder, previous_folder)
        previous_folder = folder

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
    return r


def gamma_index(filename, ref_filename):
    img = itk.imread(filename)
    img_ref = itk.imread(ref_filename)
    gi = gt.gamma_index_3d_equal_geometry(img_ref, img, dta=3, dd=3, ddpercent=True)
    data = itk.GetArrayViewFromImage(gi)
    # total
    max = np.amax(data)
    print(f'Max gamma index {ref_filename} {filename}: {max}')
    if max > TOL:
        return False
    return True


def analyse_one_file(folder, previous_folder, filename):
    f = os.path.join(folder, filename)
    if previous_folder:
        previous_filename = os.path.join(previous_folder, filename)
        r = gamma_index(f, previous_filename)
        return r
    return True


def analyse_one_folder(folder, previous_folder):
    # gi
    rnpv1 = analyse_one_file(folder, previous_folder, 'dose-photon-NPV1-Edep.mhd')
    rnpv2 = analyse_one_file(folder, previous_folder, 'dose-photon-NPV2-Edep.mhd')
    rrv1 = analyse_one_file(folder, previous_folder, 'dose-photon-RV1-Edep.mhd')
    rrv2 = analyse_one_file(folder, previous_folder, 'dose-photon-RV2-Edep.mhd')
    # return error if one is failed
    if not rnpv1 or not rnpv2 or not rrv1 or not rrv2:
        return False
    return True

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

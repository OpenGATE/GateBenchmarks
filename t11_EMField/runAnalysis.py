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
    
    #Analyze folder
    previous_folder = None
    r = None
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(folder, previous_folder)
        previous_folder = folder

    return r


def gamma_index(filename, ref_filename):
    img = itk.imread(filename)
    img_ref = itk.imread(ref_filename)
    gi = gt.gamma_index_3d_equal_geometry(img_ref, img, dta=1, dd=1, ddpercent=True)
    data = itk.GetArrayViewFromImage(gi)
    # total
    indexThreshold = np.where(data > 0)
    index = np.where(data[indexThreshold] <= 1.0)
    percentageVoxelOk = index[0].size/indexThreshold[0].size*100
    print(f'%voxel passes gamma index {ref_filename} {filename}: {percentageVoxelOk}')
    if percentageVoxelOk < TOL:
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
    print("Analyse: " + folder)
    r_xz = analyse_one_file(folder, previous_folder, 'doseInXZ-Dose.mhd')
    r_yz = analyse_one_file(folder, previous_folder, 'doseInYZ-Dose.mhd')
    # return error if one is failed
    if not r_xz or not r_yz:
        return False
    return True

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

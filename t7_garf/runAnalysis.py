#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#   Copyright (C): OpenGATE Collaboration
#   This software is distributed under the terms
#   of the GNU Lesser General  Public Licence (LGPL)
#   See LICENSE.md for further details
# -----------------------------------------------------------------------------

import gatetools as gt
import gatetools.phsp as phsp
import itk
import click
import os
import numpy as np
import logging
import matplotlib.pyplot as plt
import matplotlib.cm as cm

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_command_line(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)
    # Run the analysis with the command line (click)
    # the return code is 0 (fail) or 1 (success)
    r = analyse_all_folders(output_folders)
    print(f'Last test return is: {r}')


def analyse_all_folders(output_folders):
    # sort folders: the current simple 'output' must be at the end
    output_folders = list(output_folders)
    if 'output' in output_folders:
        output_folders.pop(output_folders.index('output'))
    output_folders.append('output')

    fig, ax = plt.subplots(ncols=6, nrows=1, figsize=(35, 5))
    plt.rc('font', size=12)
    iFolder = 0
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(folder, ax, iFolder)
        iFolder += 1
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.savefig('output.pdf')
    return r

def analyse_one_folder(folder, ax, iFolder):
    # Load image
    img_ref = itk.imread("reference_data/analog/results._p93vfh_/projection.mhd")
    img = itk.imread(os.path.join(folder, "projection-s.mhd"))
    islice = 64
    wslice = 10

    # Get the pixels values as np array
    data_ref = itk.GetArrayFromImage(img_ref).astype(float)
    data = itk.GetArrayFromImage(img).astype(float)

    # Sometimes not same nb of slices -> crop the data_ref
    if len(data_ref) > len(data):
        data_ref = data_ref[0:len(data),:,:]

    # Criterion1: global counts in every windows
    s_ref = np.sum(data_ref, axis=(1, 2))
    s = np.sum(data, axis=(1, 2))
    rel_diff = (s-s_ref)/s_ref*100.0

    print("Ref:     Singles/Scatter1/Peak113/Scatter2/Scatter3/Peak208/Scatter4: {}".format(s_ref))
    print("Img:     WARNING/Scatter1/Peak113/Scatter2/Scatter3/Peak208/Scatter4: {}".format(s))
    print("% diff : WARNING/Scatter1/Peak113/Scatter2/Scatter3/Peak208/Scatter4: {}".format(rel_diff))
    print("Peak113: " + str(abs(rel_diff[2])) + " vs 20% / Peak208: " + str(abs(rel_diff[5])) + " vs 20% ")

    # Profiles
    # data image: !eee!Z,Y,X
    p_ref = np.mean(data_ref[:, islice-wslice:islice+wslice-1, :], axis=1)
    p = np.mean(data[:, islice-wslice:islice+wslice-1, :], axis=1)
    x = np.arange(0, 128, 1)

    nb_ene = 7
    win = ['WARNING', 'Scatter1', 'Peak113', 'Scatter2', 'Scatter3', 'Peak208', 'Scatter4']
 
    i = 1
    colors = cm.rainbow(np.linspace(0, 1, 20))
    while i < 7:
        a = ax[i-1]
        a.plot(x, p_ref[i], 'g', label='Analog', alpha=0.5, linewidth=2.0)
        #a.plot(x, p[i], colors[iFolder]+'--', label='ARF '+str(folder), alpha=0.9, linewidth=1.0)
        a.plot(x, p[i], c=colors[iFolder], ls='--' , label='ARF '+str(folder), alpha=0.9, linewidth=1.0)
        a.set_title(win[i], fontsize=17)
        a.legend(loc='best')
        # a.labelsize = 40
        a.tick_params(labelsize=12)
        #a.set_ylim([0, vmax])
        i += 1

    if abs(rel_diff[2]) < 22 and abs(rel_diff[5]) < 22:
        return True
    return False


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

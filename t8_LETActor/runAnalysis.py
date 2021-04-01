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

logger = logging.getLogger(__name__)

# Tolerance
TOL = 5

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
    r_proton = analyse_all_folders(output_folders, 'proton')
    r_carbon = analyse_all_folders(output_folders, 'carbon')
    print(f'Last test return is: proton {r_proton} and carbon {r_carbon}')
    return r_proton & r_carbon


def plot_edep(filename, a, subType):
    # read the image
    logger.info('Load ' + filename)
    img = itk.imread(filename)
    spacing = img.GetSpacing()
    data = itk.GetArrayViewFromImage(img)
    y = data[:, 0, 0]
    x = np.arange(len(y)) * spacing[2]
    a.plot(x, y, label=filename)
    a.set_xlabel('Depth [mm]')
    a.set_ylabel( subType )
    a.legend()


def analyse_all_folders(output_folders, particle_name):
    # init the plot: 3 rows for gamma/proton/carbon
    fig, ax = plt.subplots(ncols=1, nrows=3, figsize=(25, 10))
    # compare with the previous folder
    previous_folder = None
    r = None
    # sort folders: the current simple 'output' must be at the end
    output_folders = list(output_folders)
    if 'output' in output_folders:
        output_folders.pop(output_folders.index('output'))
    output_folders.append('output')
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(ax, folder, previous_folder, particle_name)
        previous_folder = folder
    plt.xlabel('Depth [mm]')
    plt.savefig('output-' + particle_name +'.pdf')
    plt.show()
    return r


def gamma_index(a, filename, ref_filename):
    img = itk.imread(filename)
    img_ref = itk.imread(ref_filename)
    gi = gt.gamma_index_3d_equal_geometry(img_ref, img, dta=3, dd=3, ddpercent=True)
    # itk.imwrite(gi, 'gi.mhd')
    spacing = img.GetSpacing()
    data = itk.GetArrayViewFromImage(gi)
    y = data[:, 0, 0]
    x = np.arange(len(y)) * spacing[2]
    
    L1 =x<= 160;
#    L1 =np.where( x<= 155);
    ytemp = np.array(y)
    y2 = ytemp[L1]
    x2 = x[L1]
    
    
    # total
    max = y2.max()
    print(f'Max gamma index {ref_filename} {filename}: {max}')
    # get shared axis if already exist
    ax = a.get_shared_x_axes().get_siblings(a)[0]
    if ax == a:
        ax = a.twinx()
    ax.plot(x2, y2, '--', alpha=0.5, label=f'G.I. {ref_filename} vs {filename} max={max:.2f}')
    ax.set_ylabel( 'Gamma' )
    ax.legend()
    if max > TOL:
        return False
    return True


def analyse_one_curve(ax, i, folder, previous_folder, filename, subType):
    a = phsp.fig_get_sub_fig(ax, i)
    filename = filename + '-' + subType + '.mhd'
    f = os.path.join(folder, filename)
    if (subType != 'Edep'):
        plot_edep(f, a, subType + ' [MeV]')
    else:
        plot_edep(f, a, 'LET ' + subType + ' [keV/um]')
    if previous_folder and (subType != 'Edep'):
        print('Found previous folder:', previous_folder)
        previous_filename = os.path.join(previous_folder, filename)
        r = gamma_index(a, f, previous_filename)
        return r
    return True


def analyse_one_folder(ax, folder, previous_folder, particle_name):
    # plot and gi
    rg = analyse_one_curve(ax, 0, folder, previous_folder, 'IDD-' + particle_name , 'Edep')
    rp = analyse_one_curve(ax, 1, folder, previous_folder, 'LET_primaries-' + particle_name , 'doseAveraged')
    rc = analyse_one_curve(ax, 2, folder, previous_folder, 'LET_primaries-' + particle_name ,'trackAveraged')
    # return error if one is failed
#    if not rg or not rp or not rc :
#        return False
    return rp & rc


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

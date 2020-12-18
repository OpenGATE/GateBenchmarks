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
def plot(output_folder, a, filename):

    if not os.path.isdir(output_folder):
        return
  
    if os.path.isfile(os.path.join(output_folder, filename + ".npy")):
        x, y = np.loadtxt(os.path.join(output_folder, filename + ".npy"), unpack=True)
    elif os.path.isfile(os.path.join(output_folder, filename)):
        f = os.path.join(output_folder, filename)
        logger.info('Load ' + f)
        img = itk.imread(f)

        # img spacing
        spacing = img.GetSpacing()

        # get data in np
        data = itk.GetArrayViewFromImage(img)

        y = data[:,0,0]
        x = np.arange(len(y)) * spacing[2]
      
        # saving:
        np.savetxt(os.path.join(output_folder, filename) + ".npy", np.array([x, y]).T)
    else:
        return

    a.plot(x,y, label=output_folder)
    a.legend()

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
    ncols=1
    nrows=3
    fig, ax = plt.subplots(ncols=ncols, nrows=nrows, figsize=(25, 10))

    a = phsp.fig_get_sub_fig(ax,0)
    for o in output_folders:
        plot(o, a, 'output-gamma-Edep.mhd')

    a = phsp.fig_get_sub_fig(ax,1)
    for o in output_folders:
        plot(o, a, 'output-proton-Edep.mhd')
    
    a = phsp.fig_get_sub_fig(ax,2)
    for o in output_folders:
        plot(o, a, 'output-carbon-Edep.mhd')
    
    plt.savefig('output.pdf')
    plt.show()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

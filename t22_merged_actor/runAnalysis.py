#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#   Copyright (C): OpenGATE Collaboration
#   This software is distributed under the terms
#   of the GNU Lesser General  Public Licence (LGPL)
#   See LICENSE.md for further details
# -----------------------------------------------------------------------------

import gatetools as gt
import click
import os
import numpy as np
import logging
import sys

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
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(folder)
    return r


def analyse_one_folder(folder):
    # Open Edep map
    try:
        Edep = np.fromfile(os.path.join(folder, "dose-Edep.raw"), "float32")
        Edep = Edep.reshape((50, 50, 50))
        Edep = Edep[25, ...] # Get slice 25
    except:
        return False

    # Get background mean value (upper left image corner)
    avgBackground = Edep[:10, :10].mean()

    # Get mean value inside the meshed sphere
    avgMesh = Edep[22:28, 12:18].mean()

    print(folder + " dose-Edep.raw: avgMesh = " + str(avgMesh) + " and avgBackground = " + str(avgBackground)) 
    # Mean background energy value should be always bigger
    if (avgMesh > avgBackground):
        return False

    return True


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

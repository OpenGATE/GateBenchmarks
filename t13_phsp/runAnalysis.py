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
import uproot

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


def compare_branch(t1, t2, key, tol):
    b1 = t1[key]
    b2 = t2[key]
    m1 = np.mean(b1)
    m2 = np.mean(b2)
    diff_m = (m1 - m2) / m1 * 100
    diff_s = (np.std(b1) - np.std(b2)) / np.std(b1) * 100
    r = True
    if diff_m > tol:
        r = False
    print(f'Branch {key} \t\t mean {m1:.2f} {m2:.2f} \t {diff_m:.2f}%  \t'
          f' std {diff_s:.2f}% \t Check ? {r} (tol = {tol:.0f}%) ')
    return r


def analyse_one_folder(folder):
    # read first phsp
    tree1 = uproot.open(f'{folder}/phsp-write-waterbox.root')['PhaseSpace']
    tree1 = tree1.arrays(library="numpy")
    n1 = len(tree1['X'])
    print(f'First (write) phsp {n1} {tree1.keys()}')

    # read second phsp
    tree2 = uproot.open(f'{folder}/phsp-read-waterbox.root')['PhaseSpace']
    tree2 = tree2.arrays(library="numpy")
    n2 = len(tree2['X'])
    print(f'Second (read) phsp {n2} {tree2.keys()}')

    # compare some branches
    keys = ['Ekine', 'X', 'Y', 'Z', 'dX', 'dY', 'dZ', 'Weight', 'Time']
    tols = [2, 15, 5, 5, 30, 30, 30, 2, 2]
    r = True
    for k, t in zip(keys, tols):
        r = compare_branch(tree1, tree2, k, t) & r
    return r


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

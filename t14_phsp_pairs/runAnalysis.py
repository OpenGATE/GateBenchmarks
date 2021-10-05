#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#   Copyright (C): OpenGATE Collaboration
#   This software is distributed under the terms
#   of the GNU Lesser General  Public Licence (LGPL)
#   See LICENSE.md for further details
# -----------------------------------------------------------------------------

import gatetools as gt
import gatetools.phsp as phsp
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
    print(f'Final test return is: {r}')


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


def compare_branch(b1, b2, key, tol):
    m1 = np.mean(b1)
    m2 = np.mean(b2)
    max1 = np.max(b1)
    min1 = np.min(b1)
    # relative difference according to the range
    diff_m = (m1 - m2) / (max1 - min1) * 100
    r = True
    if np.fabs(diff_m) > tol:
        r = False
    print(f'Branch {key} \t\t mean {m1:.2f} {m2:.2f} \t diff {diff_m:.2f}%  \t'
          f' Check ? {r} (tol = {tol:.0f}%) \t range {min1:.1f}:{max1:.1f} ')
    return r


def compare_two_trees(tname1, tname2, tree1, tree2, n1, n2, keys1, keys2):
    print(f'First tree {tname1}  : {n1} {keys1}')
    print(f'Second tree {tname2} : {n2} {keys2}')
    diffn = (n1 - n2) / n1 * 100
    tol = 10
    r = np.fabs(diffn) < tol
    print(f'Differences: {diffn:.1f}% (tol = {tol}%): {r}')
    return r


def analyse_one_folder(folder):
    print('Compare detected counts from real source or phsp source')
    # read first phsp
    f1 = f'{folder}/output_write_detector.root'
    print(f1)
    tree1 = uproot.open(f1)['PhaseSpace']
    tree1 = tree1.arrays(library="numpy")
    f2 = f'{folder}/output_read_detector.root'
    print(f2)
    tree2 = uproot.open(f2)['PhaseSpace']
    tree2 = tree2.arrays(library="numpy")
    r = compare_two_trees('write', 'read', tree1, tree2,
                          len(tree1['X']), len(tree2['X']), tree1.keys(), tree2.keys())

    # compare some branches
    keys = ['Ekine', 'X', 'Y', 'Z', 'dX', 'dY', 'dZ', 'Time']
    tols = [0.2] * len(keys)
    for k, t in zip(keys, tols):
        r = compare_branch(tree1[k], tree2[k], k, t) and r

    # compare gaga conversion
    print()
    print('Compare conversion pairs->tlor->pairs')
    f = f'{folder}/phsp_write_pairs.npy'
    tree1, read_keys1, m = phsp.load(f)
    f = f'{folder}/phsp_write_pairs2.npy'
    tree2, read_keys2, m = phsp.load(f)
    r = compare_two_trees('pairs', 'pairs2', tree1, tree2, len(tree1), len(tree2), read_keys1, read_keys2) and r

    tols = [1] * len(read_keys1)
    tols = [0.01] * len(keys)
    for k, t in zip(read_keys1, tols):
        k1 = read_keys1.index(k)
        if k in read_keys2:
            k2 = read_keys2.index(k)
            r = compare_branch(tree1[:, k1], tree2[:, k2], k, t) & r

    # compare from GAN
    print()
    print('Compare analog vs GAN')
    print(f1)
    tree1 = uproot.open(f1)['PhaseSpace']
    tree1 = tree1.arrays(library="numpy")
    f2 = f'{folder}/output_gaga_read_gan_detector.root'
    print(f2)
    tree2 = uproot.open(f2)['PhaseSpace']
    tree2 = tree2.arrays(library="numpy")
    r = compare_two_trees('analog', 'gan', tree1, tree2, len(tree1['X']), len(tree2['X']), read_keys1, read_keys2) and r

    # compare some branches
    keys = ['Ekine', 'X', 'Y', 'Z', 'dX', 'dY', 'dZ', 'Time']  # weight ?
    tols = [1] * len(keys)
    for k, t in zip(keys, tols):
        r = compare_branch(tree1[k], tree2[k], k, t) and r

    return r


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

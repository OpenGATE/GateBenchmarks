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
import itk
import gatetools as gt


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
    r = True
    i = 1
    while i < len(output_folders):
        if not os.path.isdir(output_folders[i]):
            i = i +1
            continue
        r1 = analyse_one_folder(output_folders[i], output_folders[i-1])
        r2 = analyse_one_folder_2D(output_folders[i], output_folders[i-1])
        r3 = analyse_one_folder_mhd(output_folders[i], output_folders[i-1])
        if not r1 or not r2 or not r3:
            r = False
        i = i+1
    return r


def compare_branch(t1, t2, key, tol):
    b1 = t1[key]
    b2 = t2[key]
    m1 = np.mean(b1)
    m2 = np.mean(b2)
    diff_m = (m1 - m2) / m1 * 100.
    diff_s = (np.std(b1) - np.std(b2)) / np.std(b1) * 100.
    r = True
    if diff_m > tol:
        r = False
    print(f'Branch {key} \t\t mean {m1:.2f} {m2:.2f} \t {diff_m:.2f}%  \t'
          f' std {diff_s:.2f}% \t Check ? {r} (tol = {tol:.0f}%) ')
    return r


def compare_branch_2D(t1, t2, key, tol):
    h1 = t1[key].to_hist()
    w1, x1, y1 = h1.to_numpy()
    b1 = w1.sum(axis=1)    
    h2 = t2[key].to_hist()
    w2, x2, y2 = h2.to_numpy()
    b2 = w2.sum(axis=1)    
    m1 = np.sum(b1)
    m2 = np.sum(b2)
    diff_m = (m1 - m2) / m1 * 100.
    diff_s = (np.std(b1) - np.std(b2)) / np.std(b1) * 100.
    r = True
    if diff_m > tol:
        r = False
    print(f'Branch {key} \t\t mean {m1:.2f} {m2:.2f} \t {diff_m:.2f}%  \t'
          f' std {diff_s:.2f}% \t Check ? {r} (tol = {tol:.0f}%) ')
    return r


def compare_branch_mhd(f1, f2, tol):
    img = itk.imread(f1)
    img_ref = itk.imread(f2)

    imga = itk.GetArrayFromImage(img)
    imga_ref = itk.GetArrayFromImage(img_ref)

    m1 = np.sum(imga)
    m2 = np.sum(imga_ref)
    
    diff_m = (m1 - m2) / m1 * 100.
    diff_s = (np.std(imga) - np.std(imga_ref)) / np.std(imga) * 100.
    r = True
    if diff_m > tol:
        r = False
    print(f'Image {f1} \t\t mean {m1:.2f} {m2:.2f} \t {diff_m:.2f}%  \t'
          f' std {diff_s:.2f}% \t Check ? {r} (tol = {tol:.0f}%) ')
    return r


def analyse_one_folder(folder, previous_folder):
    # read first phsp
    tree1 = uproot.open(f'{folder}/detector_vpg_Carbon.root')['PhaseSpace']
    #tree1 = tree1.arrays(library="numpy")
    tree1 = tree1.arrays(["AtomicNumber", "X", "Ekine", "Time", "IonTime"], library="np")
    n1 = len(tree1['X'])
    print(f'First (write) phsp {n1} {tree1.keys()}')

    # read second phsp
    tree2 = uproot.open(f'{previous_folder}/detector_vpg_Carbon.root')['PhaseSpace']
    tree2 = tree2.arrays(library="numpy")
    n2 = len(tree2['X'])
    print(f'Second (read) phsp {n2} {tree2.keys()}')

    # compare some branches
    keys = ['Ekine', 'Time', 'IonTime']
    tols = [10, 10, 10]
    r = True
    for k, t in zip(keys, tols):
        r = compare_branch(tree1, tree2, k, t) & r
    return r

def analyse_one_folder_2D(folder, previous_folder):
    # read first phsp
    tree1 = uproot.open(f'{folder}/db-Carbon.root')['Carbon']
    print(f'First (write) phsp {tree1.keys()}')

    # read second phsp 
    tree2 = uproot.open(f'{previous_folder}/db-Carbon.root')['Carbon']
    print(f'Second (read) phsp {tree2.keys()}')

    # compare some branches
    keys = ['GammaZ']
    tols = [20]
    r = True
    for k, t in zip(keys, tols):
        r = compare_branch_2D(tree1, tree2, k, t) & r
    return r


def analyse_one_folder_mhd(folder, previous_folder):
    # gi
    tol = 10
    f1 = os.path.join(folder, "source_vpg_Carbon.mhd")
    f2 = os.path.join(previous_folder, "source_vpg_Carbon.mhd")
    r1 = compare_branch_mhd(f1,f2,tol)
    f1 = os.path.join(folder, "source_vpg_Carbon-tof.mhd")
    f2 = os.path.join(previous_folder, "source_vpg_Carbon-tof.mhd")
    r2 = compare_branch_mhd(f1,f2,tol)

    # return error if one is failed
    if not r1 or not r2:
        return False
    return True


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

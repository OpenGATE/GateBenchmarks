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
import math

import itertools
import collections

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
        r = analyse_one_folder(folder, previous_folder)
        previous_folder = folder
    return r


def analyze(folder, previous_folder, filename):
    f= os.path.join(folder, filename)

    if previous_folder:
        previous_filename = os.path.join(previous_folder, filename)
        r = compare_with_previous_version(f, previous_filename)
        return r
    return True   


def compare_with_previous_version(file_new, file_old):
    branches_old = ["edep","posX", "posY", "posZ", "time"]
    hitTree_old = uproot.open(file_old)['Hits'].arrays(branches_old,library="numpy")
    edep_old=hitTree_old["edep"]
    posX_old=hitTree_old["posX"]
    posY_old=hitTree_old["posY"]
    posZ_old=hitTree_old["posZ"]
    time_old=hitTree_old["time"]
    
    branches_new = ["edep","posX", "posY", "posZ", "time"]
    hitTree_new = uproot.open(file_new)['Hits'].arrays(branches_new,library="numpy")
    edep_new=hitTree_new["edep"]
    posX_new=hitTree_new["posX"]
    posY_new=hitTree_new["posY"]
    posZ_new=hitTree_new["posZ"]
    time_new=hitTree_new["time"]



    CRED = '\033[91m'
    CGRE = '\033[92m'

    CEND = '\033[0m'

    returnBool = True
    #N entries test
    if (len(edep_new) == len(edep_old)) :
        print("Entries test is OK: ", len(edep_new), " vs. ", len(edep_old))
    else:
        print(CRED+"Entries test failed"+CEND, len(edep_new), " vs. ", len(edep_old))
        exit()
        returnBool = False

    edep_old.sort() 
    posX_old.sort()
    posY_old.sort()
    posZ_old.sort()
    time_old.sort()
    
    edep_new.sort() 
    posX_new.sort()
    posY_new.sort()
    posZ_new.sort()
    time_new.sort()
        

    acceptance = 0.00001   
    for i in range(len(edep_old)) : 
        if (math.fabs(edep_old[i]-edep_new[i])>acceptance):
            print(CRED+"Energy test failed"+CEND, edep_old[i], " vs. ",  edep_new[i])
            exit()
            returnBool = False
        if (math.fabs(time_old[i]-time_new[i])>acceptance):
            print(CRED+"Min time test failed"+CEND, time_old[i], " vs. ", time_new[i])
            exit()
            returnBool = False
        if (math.fabs(posX_old[i]-posX_new[i])>acceptance):
            print(CRED+"PosX test failed"+CEND, posX_old[i], " vs. ", posX_new[i])
            exit()
            returnBool = False
        if (math.fabs(posY_old[i]-posY_new[i])>acceptance):
            print(CRED+"PosY test failed"+CEND, posY_old[i], " vs. ", posY_new[i])
            exit()
            returnBool = False
        if (math.fabs(posZ_old[i]-posZ_new[i])>acceptance):
            print(CRED+"PosZ time test failed"+CEND, posZ_old[i], " vs. ", posZ_new[i])
            exit()
            returnBool = False

    print(CGRE+"Test is OK!"+CEND)

 
    return(returnBool)


def analyse_one_folder(folder, previous_folder):
    # analyze cylPET
    r_1 = analyze(folder, previous_folder, "cylPET.root") 

    # analyze ecat
    r_2 = analyze(folder, previous_folder, "ecat.root")

    # analyze SPECT
    r_3 = analyze(folder, previous_folder, "SPECT.root")

    return (r_1 and r_2 and r_3)



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

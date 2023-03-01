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
from statistics import mean, median
from scipy.stats import wasserstein_distance

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


def analyze(folder, previous_folder, name):
    filename = name + ".root"
    #print(folder +" "+filename)
    f= os.path.join(folder, filename)

    if previous_folder:
        previous_filename = os.path.join(previous_folder, filename)
        r = compare_with_previous_version(f, previous_filename)
        return r
    return True   


def compare_with_previous_version(filename_new, filename_old):
    branches = ["energy","globalPosX", "globalPosY", "globalPosZ", "time"]

    energy_old=[]
    posX_old=[]
    globalPosY_old=[]
    globalPosZ_old=[]
    time_old=[]
    
    energy_new=[]
    globalPosX_new=[]
    globalPosY_new=[]
    globalPosZ_new=[]
    time_new=[]


    with uproot.open(filename_old) as file_old:
        for keyname in file_old:
            if keyname == "Singles;1":
                singlesTree_old = file_old["Singles"].arrays(branches,library="numpy")

                energy_old=singlesTree_old["energy"]
                globalPosX_old=singlesTree_old["globalPosX"]
                globalPosY_old=singlesTree_old["globalPosY"]
                globalPosZ_old=singlesTree_old["globalPosZ"]
                time_old=singlesTree_old["time"]
                                             
            else:
                if keyname == "Singles_crystal;1" :
                    singlesTree_tmp = file_old['Singles_crystal'].arrays(branches,library="numpy")

                    energy_tmp=singlesTree_tmp["energy"]
                    globalPosX_tmp=singlesTree_tmp["globalPosX"]
                    globalPosY_tmp=singlesTree_tmp["globalPosY"]
                    globalPosZ_tmp=singlesTree_tmp["globalPosZ"]
                    time_tmp=singlesTree_tmp["time"]

                    singlesTree2_tmp = uproot.open(file_tmp)['Singles_crystal2'].arrays(branches,library="numpy")
                    energy2_tmp=singlesTree2_tmp["energy"]
                    globalPosX2_tmp=singlesTree2_tmp["globalPosX"]
                    globalPosY2_tmp=singlesTree2_tmp["globalPosY"]
                    globalPosZ2_tmp=singlesTree2_tmp["globalPosZ"]
                    time2_tmp=singlesTree2_tmp["time"]

                
                    energy_old=np.concatenate([energy_tmp,energy2_tmp])
                    globalPosX_old=np.concatenate([globalPosX_tmp,globalPosX2_tmp])
                    globalPosY_old=np.concatenate([globalPosY_tmp,globalPosY2_tmp])
                    globalPosZ_old=np.concatenate([globalPosZ_tmp,globalPosZ2_tmp])
                    time_old=np.concatenate([time_tmp,time2_tmp])


                    
    with uproot.open(filename_new) as file_new:
        for keyname in file_new:
            if keyname == "Singles;1":
                print("found singles")
                singlesTree_new = file_new["Singles"].arrays(branches,library="numpy")

                energy_new=singlesTree_new["energy"]
                globalPosX_new=singlesTree_new["globalPosX"]
                globalPosY_new=singlesTree_new["globalPosY"]
                globalPosZ_new=singlesTree_new["globalPosZ"]
                time_new=singlesTree_new["time"]
                                             
            else:
                if keyname == "Singles_crystal;1" :
                    singlesTree_tmp = file_new['Singles_crystal'].arrays(branches,library="numpy")

                    energy_tmp=singlesTree_tmp["energy"]
                    globalPosX_tmp=singlesTree_tmp["globalPosX"]
                    globalPosY_tmp=singlesTree_tmp["globalPosY"]
                    globalPosZ_tmp=singlesTree_tmp["globalPosZ"]
                    time_tmp=singlesTree_tmp["time"]

                    singlesTree2_tmp = uproot.open(file_tmp)['Singles_crystal2'].arrays(branches,library="numpy")
                    energy2_tmp=singlesTree2_tmp["energy"]
                    globalPosX2_tmp=singlesTree2_tmp["globalPosX"]
                    globalPosY2_tmp=singlesTree2_tmp["globalPosY"]
                    globalPosZ2_tmp=singlesTree2_tmp["globalPosZ"]
                    time2_tmp=singlesTree2_tmp["time"]

                
                    energy_new=np.concatenate([energy_tmp,energy2_tmp])
                    globalPosX_new=np.concatenate([globalPosX_tmp,globalPosX2_tmp])
                    globalPosY_new=np.concatenate([globalPosY_tmp,globalPosY2_tmp])
                    globalPosZ_new=np.concatenate([globalPosZ_tmp,globalPosZ2_tmp])
                    time_new=np.concatenate([time_tmp,time2_tmp])                


    CRED = '\033[91m'
    CGRE = '\033[92m'

    CEND = '\033[0m'

    returnBool = True
    #N entries test
    if (math.fabs(len(energy_new)- len(energy_old)) < 10*math.sqrt(len(energy_old)) ) :
        print("Entries test is OK: ", len(energy_new), " vs. ", len(energy_old))
    else:
        print(CRED+"Entries test failed"+CEND, len(energy_new), " vs. ", len(energy_old))
        exit()
        returnBool = False

    # energy test
    if (math.fabs(mean(energy_old)-mean(energy_new) ) < 3*np.std(energy_old)) :
        print("Mean energy test is OK: ", mean(energy_new), " vs. ", mean(energy_old))
    else:
        print(CRED+"Mean energy test failed"+CEND, mean(energy_new), " vs. ", mean(energy_old))
        exit()
        returnBool = False

    if (math.fabs(median(energy_old)-median(energy_new) ) < 3*np.std(energy_old)) :
        print("Median energy test is OK: ", median(energy_new), " vs. ", median(energy_old))
    else:
        print(CRED+"Median energy test failed"+CEND, median(energy_new), " vs. ", median(energy_old))
        exit()
        returnBool = False
        
    # globalPosX test
    if (math.fabs(mean(globalPosX_old)-mean(globalPosX_new) ) < 3*np.std(globalPosX_old)) :
        print("Mean globalPosX test is OK: ", mean(globalPosX_new), " vs. ", mean(globalPosX_old))
    else:
        print(CRED+"Mean globalPosX test failed"+CEND, mean(globalPosX_new), " vs. ", mean(globalPosX_old))
        exit()
        returnBool = False

    if (math.fabs(median(globalPosX_old)-median(globalPosX_new) ) < 3*np.std(globalPosX_old)) :
        print("Median globalPosX test is OK: ", median(globalPosX_new), " vs. ", median(globalPosX_old))
    else:
        print(CRED+"Median globalPosX test failed"+CEND, median(globalPosX_new), " vs. ", median(globalPosX_old))
        exit()
        returnBool = False
        
    # globalPosY test
    if (math.fabs(mean(globalPosY_old)-mean(globalPosY_new) ) < 3*np.std(globalPosY_old)) :
        print("Mean globalPosY test is OK: ", mean(globalPosY_new), " vs. ", mean(globalPosY_old))
    else:
        print(CRED+"Mean globalPosY test failed"+CEND, mean(globalPosY_new), " vs. ", mean(globalPosY_old))
        exit()
        returnBool = False

    if (math.fabs(median(globalPosY_old)-median(globalPosY_new) ) < 3*np.std(globalPosY_old)) :
        print("Median globalPosY test is OK: ", median(globalPosY_new), " vs. ", median(globalPosY_old))
    else:
        print(CRED+"Median globalPosY test failed"+CEND, median(globalPosY_new), " vs. ", median(globalPosY_old))
        exit()
        returnBool = False

    # globalPosZ test
    if (math.fabs(mean(globalPosZ_old)-mean(globalPosZ_new) ) < 3*np.std(globalPosZ_old)) :
        print("Mean globalPosZ test is OK: ", mean(globalPosZ_new), " vs. ", mean(globalPosZ_old))
    else:
        print(CRED+"Mean globalPosZ test failed"+CEND, mean(globalPosZ_new), " vs. ", mean(globalPosZ_old))
        exit()
        returnBool = False

    if (math.fabs(median(globalPosZ_old)-median(globalPosZ_new) ) < 3*np.std(globalPosZ_old)) :
        print("Median globalPosZ test is OK: ", median(globalPosZ_new), " vs. ", median(globalPosZ_old))
    else:
        print(CRED+"Median globalPosZ test failed"+CEND, median(globalPosZ_new), " vs. ", median(globalPosZ_old))
        exit()
        returnBool = False

    # time test
    if (math.fabs(mean(time_old)-mean(time_new) ) < 3*np.std(time_old)) :
        print("Mean time test is OK: ", mean(time_new), " vs. ", mean(time_old))
    else:
        print(CRED+"Mean time test failed"+CEND, mean(time_new), " vs. ", mean(time_old))
        exit()
        returnBool = False

    if (math.fabs(median(time_old)-median(time_new) ) < 3*np.std(time_old)) :
        print("Median time test is OK: ", median(time_new), " vs. ", median(time_old))
    else:
        print(CRED+"Median time test failed"+CEND, median(time_new), " vs. ", median(time_old))
        exit()
        returnBool = False
        
    wd_energy=wasserstein_distance(energy_new,energy_old)
    wd_globalPosX=wasserstein_distance(globalPosX_new,globalPosX_old)
    wd_globalPosY=wasserstein_distance(globalPosY_new,globalPosY_old)
    wd_globalPosZ=wasserstein_distance(globalPosZ_new,globalPosZ_old)
    wd_time=wasserstein_distance(time_new,time_old)


    if "cylPET" in filename_new:
        if (wd_energy>0.01):
            print(CRED+"Wasserstein distance test for energy failed"+CEND)
            exit()
            returnBool = False
        if (wd_globalPosX>8):
            print(CRED+"Wasserstein distance test for globalPosX failed"+CEND)
            exit()
            returnBool = False
        if (wd_globalPosY>10):
            print(CRED+"Wasserstein distance test for globalPosY failed"+CEND)
            exit()
            returnBool = False    
        if (wd_globalPosZ>1.6):
            print(CRED+"Wasserstein distance test for globalPosZ failed"+CEND)
            exit()
            returnBool = False    
        if (wd_time>0.6):
            print(wd_time)
            print(CRED+"Wasserstein distance test for time failed"+CEND)
            exit()
            returnBool = False
            
    else:
        if (wd_energy>0.01):
            print(CRED+"Wasserstein distance test for energy failed"+CEND)
            exit()
            returnBool = False
        if (wd_globalPosX>4.5):
            print(CRED+"Wasserstein distance test for globalPosX failed"+CEND)
            exit()
            returnBool = False
        if (wd_globalPosY>0.5):
            print(CRED+"Wasserstein distance test for globalPosY failed"+CEND)
            exit()
            returnBool = False    
        if (wd_globalPosZ>2.):
            print(CRED+"Wasserstein distance test for globalPosZ failed"+CEND)
            exit()
            returnBool = False    
        if (wd_time>1.3):
            print(CRED+"Wasserstein distance test for time failed"+CEND)
            exit()
            returnBool = False         

            
    print(CGRE+"Test "+filename_new+" is OK!"+CEND)
    return(returnBool)


def analyse_one_folder(folder, previous_folder):
    # analyze cylPET
    r_1 = analyze(folder, previous_folder, "cylPET") 

    # analyze SPECT
    r_2 = analyze(folder, previous_folder, "SPECT")

    return (r_1 and r_2)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

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


def analyze(folder, previous_folder, filename):
    f= os.path.join(folder, filename)

    if previous_folder:
        previous_filename = os.path.join(previous_folder, filename)
        r = compare_with_previous_version(f, previous_filename)
        return r
    return True   


def compare_with_previous_version(filename_new, filename_old):
    branches = ["edep","posX", "posY", "posZ", "time"]
    edep_old=[]
    posX_old=[]
    posY_old=[]
    posZ_old=[]
    time_old=[]
    
    edep_new=[]
    posX_new=[]
    posY_new=[]
    posZ_new=[]
    time_new=[]

                      

    with uproot.open(filename_old) as file_old:
        for keyname in file_old:
            if keyname == "Hits;1":
                hitTree_old = file_old["Hits"].arrays(branches,library="numpy")

                edep_old=hitTree_old["edep"]
                posX_old=hitTree_old["posX"]
                posY_old=hitTree_old["posY"]
                posZ_old=hitTree_old["posZ"]
                time_old=hitTree_old["time"]
                              
            else:
                if keyname == "Hits_crystal;1" :
                    hitTree_tmp = file_old['Hits_crystal'].arrays(branches,library="numpy")
                    edep_tmp=hitTree_tmp["edep"]
                    posX_tmp=hitTree_tmp["posX"]
                    posY_tmp=hitTree_tmp["posY"]
                    posZ_tmp=hitTree_tmp["posZ"]
                    time_tmp=hitTree_tmp["time"]

                    hitTree2_tmp = file_old['Hits_crystal2'].arrays(branches,library="numpy")
                    edep2_tmp=hitTree2_tmp["edep"]
                    posX2_tmp=hitTree2_tmp["posX"]
                    posY2_tmp=hitTree2_tmp["posY"]
                    posZ2_tmp=hitTree2_tmp["posZ"]
                    time2_tmp=hitTree2_tmp["time"]
                
                    edep_old=np.concatenate([edep_tmp,edep2_tmp])
                    posX_old=np.concatenate([posX_tmp,posX2_tmp])
                    posY_old=np.concatenate([posY_tmp,posY2_tmp])
                    posZ_old=np.concatenate([posZ_tmp,posZ2_tmp])
                    time_old=np.concatenate([time_tmp,time2_tmp])
                
                
    with uproot.open(filename_new) as file_new:
        for keyname in file_new:
            if keyname == "Hits;1":
                hitTree_new = file_new['Hits'].arrays(branches,library="numpy")

                edep_new=hitTree_new["edep"]
                posX_new=hitTree_new["posX"]
                posY_new=hitTree_new["posY"]
                posZ_new=hitTree_new["posZ"]
                time_new=hitTree_new["time"]
             
            else:
                if keyname == "Hits_crystal;1" :
                    hitTree_tmp = file_new['Hits_crystal'].arrays(branches,library="numpy")
                    edep_tmp=hitTree_tmp["edep"]
                    posX_tmp=hitTree_tmp["posX"]
                    posY_tmp=hitTree_tmp["posY"]
                    posZ_tmp=hitTree_tmp["posZ"]
                    time_tmp=hitTree_tmp["time"]

                    hitTree2_tmp = file_new['Hits_crystal2'].arrays(branches,library="numpy")
                    edep2_tmp=hitTree2_tmp["edep"]
                    posX2_tmp=hitTree2_tmp["posX"]
                    posY2_tmp=hitTree2_tmp["posY"]
                    posZ2_tmp=hitTree2_tmp["posZ"]
                    time2_tmp=hitTree2_tmp["time"]
                     
                    edep_new=np.concatenate([edep_tmp,edep2_tmp])
                    posX_new=np.concatenate([posX_tmp,posX2_tmp])
                    posY_new=np.concatenate([posY_tmp,posY2_tmp])
                    posZ_new=np.concatenate([posZ_tmp,posZ2_tmp])
                    time_new=np.concatenate([time_tmp,time2_tmp])
               
    
    CRED = '\033[91m'
    CGRE = '\033[92m'

    CEND = '\033[0m'
    
    returnBool = True
    #N entries test
    if (math.fabs(len(edep_new)- len(edep_old)) < 10*math.sqrt(len(edep_old)) ) :
        print("Entries test is OK: ", len(edep_new), " vs. ", len(edep_old))
    else:
        print(CRED+"Entries test failed"+CEND, len(edep_new), " vs. ", len(edep_old))
        exit()
        returnBool = False

    # edep test
    if (math.fabs(mean(edep_old)-mean(edep_new) ) < 3*np.std(edep_old)) :
        print("Mean edep test is OK: ", mean(edep_new), " vs. ", mean(edep_old))
    else:
        print(CRED+"Mean edep test failed"+CEND, mean(edep_new), " vs. ", mean(edep_old))
        exit()
        returnBool = False

    if (math.fabs(median(edep_old)-median(edep_new) ) < 3*np.std(edep_old)) :
        print("Median edep test is OK: ", median(edep_new), " vs. ", median(edep_old))
    else:
        print(CRED+"Median edep test failed"+CEND, median(edep_new), " vs. ", median(edep_old))
        exit()
        returnBool = False
        
    # posX test
    if (math.fabs(mean(posX_old)-mean(posX_new) ) < 3*np.std(posX_old)) :
        print("Mean posX test is OK: ", mean(posX_new), " vs. ", mean(posX_old))
    else:
        print(CRED+"Mean posX test failed"+CEND, mean(posX_new), " vs. ", mean(posX_old))
        exit()
        returnBool = False

    if (math.fabs(median(posX_old)-median(posX_new) ) < 3*np.std(posX_old)) :
        print("Median posX test is OK: ", median(posX_new), " vs. ", median(posX_old))
    else:
        print(CRED+"Median posX test failed"+CEND, median(posX_new), " vs. ", median(posX_old))
        exit()
        returnBool = False
        
    # posY test
    if (math.fabs(mean(posY_old)-mean(posY_new) ) < 3*np.std(posY_old)) :
        print("Mean posY test is OK: ", mean(posY_new), " vs. ", mean(posY_old))
    else:
        print(CRED+"Mean posY test failed"+CEND, mean(posY_new), " vs. ", mean(posY_old))
        exit()
        returnBool = False

    if (math.fabs(median(posY_old)-median(posY_new) ) < 3*np.std(posY_old)) :
        print("Median posY test is OK: ", median(posY_new), " vs. ", median(posY_old))
    else:
        print(CRED+"Median posY test failed"+CEND, median(posY_new), " vs. ", median(posY_old))
        exit()
        returnBool = False

    # posZ test
    if (math.fabs(mean(posZ_old)-mean(posZ_new) ) < 3*np.std(posZ_old)) :
        print("Mean posZ test is OK: ", mean(posZ_new), " vs. ", mean(posZ_old))
    else:
        print(CRED+"Mean posZ test failed"+CEND, mean(posZ_new), " vs. ", mean(posZ_old))
        exit()
        returnBool = False

    if (math.fabs(median(posZ_old)-median(posZ_new) ) < 3*np.std(posZ_old)) :
        print("Median posZ test is OK: ", median(posZ_new), " vs. ", median(posZ_old))
    else:
        print(CRED+"Median posZ test failed"+CEND, median(posZ_new), " vs. ", median(posZ_old))
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
        
    wd_edep=wasserstein_distance(edep_new,edep_old)
    wd_posX=wasserstein_distance(posX_new,posX_old)
    wd_posY=wasserstein_distance(posY_new,posY_old)
    wd_posZ=wasserstein_distance(posZ_new,posZ_old)
    wd_time=wasserstein_distance(time_new,time_old)

    if "cylPET" in filename_new:
        if (wd_edep>0.01):
            print(CRED+"Wasserstein distance test for edep failed"+CEND)
            exit()
            returnBool = False
        if (wd_posX>15):
            print(CRED+"Wasserstein distance test for posX failed"+CEND)
            exit()
            returnBool = False
        if (wd_posY>10):
            print(CRED+"Wasserstein distance test for posY failed"+CEND)
            exit()
            returnBool = False    
        if (wd_posZ>1.5):
            print(CRED+"Wasserstein distance test for posZ failed"+CEND)
            exit()
            returnBool = False    
        if (wd_time>0.002):
            print(wd_time)
            print(CRED+"Wasserstein distance test for time failed"+CEND)
            exit()
            returnBool = False
            
    else:
        if (wd_edep>0.01):
            print(CRED+"Wasserstein distance test for edep failed"+CEND)
            exit()
            returnBool = False
        if (wd_posX>4.5):
            print(CRED+"Wasserstein distance test for posX failed"+CEND)
            exit()
            returnBool = False
        if (wd_posY>0.5):
            print(CRED+"Wasserstein distance test for posY failed"+CEND)
            exit()
            returnBool = False    
        if (wd_posZ>2.):
            print(CRED+"Wasserstein distance test for posZ failed"+CEND)
            exit()
            returnBool = False    
        if (wd_time>0.002):
            print(CRED+"Wasserstein distance test for time failed"+CEND)
            exit()
            returnBool = False         
    

    
        

        
    print(CGRE+filename_new+" test is OK!"+CEND)

 
    return(returnBool)


def analyse_one_folder(folder, previous_folder):
    # analyze cylPET
    r_1 = analyze(folder, previous_folder, "cylPET.root") 

    # analyze SPECT
    r_2 = analyze(folder, previous_folder, "SPECT.root")

    return (r_1 and r_2)



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()



   
    

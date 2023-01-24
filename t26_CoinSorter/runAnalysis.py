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


def analyze(folder, type):
    if type == "test1":
        file= os.path.join(folder, "test1.root")
    elif type == "test2":
        file= os.path.join(folder, "test2.root")
    elif type == "test3":
        file= os.path.join(folder, "test3.root")
    elif type == "test4":
        file= os.path.join(folder, "test4.root")
        
    branches = ["eventID","time"]
    singleTree = uproot.open(file)['Singles'].arrays(branches,library="numpy")
    eventID_single=singleTree["eventID"]
    time_single=singleTree["time"]
    
    
    branches = ["eventID1"]
    coinTree = uproot.open(file)['Coincidences'].arrays(branches,library="numpy")
    eventID1_coin=coinTree["eventID1"]
    
    timeWindow = 10e-9
    buffer_size=32
    coin=[]
    coin_noMulti1=[]
    coin_noMulti2=[]
    coin_noMulti3=[]
    coin_noMulti4=[]
    
    j=0
    i = 0
    
    tmp_time2 = []
    tmp_eventID2 = []
    
    nentries_signle=len(eventID_single)

    breaker = False #to break loops at the last entry
    while i<nentries_signle :
        start_time=time_single[i]
        eventID1 = eventID_single[i]
        
        time1 = time_single[i]
        start_time = time1
        j=0
        
        time=time_single[i]
        
        #print("--------------Iteration i = ", i) #, start_time,time-start_time )
        #print("event = ",eventID1, blockID1) #, start_time) #,eventID1,time1, current_time, time1-start_time, blockID1 )
    
        while (time-start_time) < timeWindow:
            #print("Subiteration j = ", j, start_time, time-start_time)
            
            if(i+j == (nentries_signle -1)): # for the last iteration
                breaker=True
                break
            if(time-start_time) < timeWindow :
                time2 = time_single[i+j]
                eventID2 = eventID_single[i+j]
                
                time=time2
                tmp_time2.append(time2)
                tmp_eventID2.append(eventID2)
                j +=1
                
        #remove the last element from extra step in while loop
        del tmp_eventID2[len(tmp_eventID2)-1]
        del tmp_time2[len(tmp_time2)-1]

    
        #print(tmp_blockID2)
        for subset in itertools.combinations(tmp_eventID2,2):
            combi = list (subset)
            coin.append(combi[0])
        
        i = i + j -1
        del tmp_time2[:]
        del tmp_eventID2[:]
    
        if breaker:
            break

    if type == "test1":
        coin_noMulti1=coin
    elif type == "test2":
        coin_noMulti2=list(set(coin))
    elif type == "test3":
        coin_noMulti3=[v for v, c in collections.Counter(coin).items() if c == 1]
    elif type == "test4":
        coin_noMulti4=[v for v, c in collections.Counter(coin).items() if c == 1]

    CRED = '\033[91m'
    CEND = '\033[0m'

    #N entries test
    returnBool = True
    if len(coin_noMulti1)-len(eventID1_coin) > buffer_size:
        print(CRED+"Test1 (takeAllGoods policy) failed: difference in the result "+CEND, len(coin_noMulti1)-len(eventID1_coin), " >  buffer size: ",buffer_size )
        returnBool = False
    else:
        print("Test1 (takeAllGoods policy) is OK: difference in the result ", len(coin_noMulti1)-len(eventID1_coin), " < buffer size: ", buffer_size)

    if len(coin_noMulti2)-len(eventID1_coin) > buffer_size:
        print(CRED+"Test2 (takeWinnerOfGoods policy) failed: difference in the result "+CEND, len(coin_noMulti2), " - ", len(eventID1_coin), " = ",len(coin_noMulti2)-len(eventID1_coin), " >  buffer size: ",buffer_size )
        returnBool = False
    else:
        print("Test2 (takeWinnerOfGoods policy) is OK: difference in the result ", len(coin_noMulti2)-len(eventID1_coin), " < buffer size: ", buffer_size)

    if len(coin_noMulti3)-len(eventID1_coin) > buffer_size:
        print(CRED+"Test3 (killAll policy) failed: difference in the result "+CEND, len(coin_noMulti3), " - ", len(eventID1_coin), " = ",len(coin_noMulti3)-len(eventID1_coin), " >  buffer size: ",buffer_size )
        returnBool = False
    else:
        print("Test3 (killAll policy) is OK: difference in the result ", len(coin_noMulti3)-len(eventID1_coin), " < buffer size: ", buffer_size)

    if len(coin_noMulti4)-len(eventID1_coin) > buffer_size:
        print(CRED+"Test4 (keepIfOnlyOneGood policy) failed: difference in the result "+CEND, len(coin_noMulti4), " - ", len(eventID1_coin), " = ",len(coin_noMulti4)-len(eventID1_coin), " >  buffer size: ",buffer_size )
        returnBool = False
    else:
        print("Test4 (keepIfOnlyOneGood policy) is OK: difference in the result ", len(coin_noMulti4)-len(eventID1_coin), " < buffer size: ", buffer_size)

    return(returnBool)


def analyse_one_folder(folder):
    # analyze test1
    r_1 = analyze(folder, "test1") 

    # analyze test2
    r_2 = analyze(folder, "test2")

    # analyze test2
    r_3 = analyze(folder, "test3")

    # analyze test2
    r_4 = analyze(folder, "test4") 

    return (r_1 and r_2 and r_3 and r_4)



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

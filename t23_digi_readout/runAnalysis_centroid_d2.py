#!/usr/bin/env python3

import gatetools as gt
import gatetools.phsp as phsp
import itk
import click
import sys
import os
import numpy as np
import logging
import numpy.lib.recfunctions as rfn
import uproot
import math 

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import glob
logger=logging.getLogger(__name__)



file="output/test_centroid_d2.root"
#file_path = os.path.join(folder, filename)
#file = uproot.open("output/test.root")
#print(file_path.classnames())

branches = ["edep","eventID","blockID", "crystalID", "posX", "posY", "posZ", "time"]
hitTree = uproot.open(file)['Hits'].arrays(branches,library="numpy")
edep_hit=hitTree["edep"]
eventID_hit=hitTree["eventID"]
crystalID_hit=hitTree["crystalID"]
blockID_hit=hitTree["blockID"]
posX_hit=hitTree["posX"]
posY_hit=hitTree["posY"]
posZ_hit=hitTree["posZ"]
time_hit=hitTree["time"]

branches = ["energy","eventID","blockID","globalPosX", "globalPosY", "globalPosZ", "time"]
singleTree = uproot.open(file)['Singles'].arrays(branches,library="numpy")
energy_single=singleTree["energy"]
eventID_single=singleTree["eventID"]
blockID_single=singleTree["blockID"]
globalPosX_single=singleTree["globalPosX"]
globalPosY_single=singleTree["globalPosY"]
globalPosZ_single=singleTree["globalPosZ"]
time_single=singleTree["time"]

#############################  ADDER #####################################

nextIterEventID=0

#tmp vectors to make operations "within a block"
tmp_crystalID_hit=[]
tmp_blockID_hit=[]
tmp_volumeID_hit=[]
tmp_edep_hit=[]
tmp_time_hit=[]
tmp_posX_hit=[]
tmp_posY_hit=[]
tmp_posZ_hit=[]
tmp_eventID_hit=[]

#arrays to fill for offline singles
crystalID_adder=[]
blockID_adder=[]
edep_adder=[]
minTime_adder=[]
posX_adder=[]
posY_adder=[]
posZ_adder=[]
eventID_adder=[]

for index in range(len(edep_hit)) :
    #print (eventID_hit[index], blockID_hit[index], edep_hit[index], posX_hit[index],posY_hit[index], posZ_hit[index])  
    # last iteration
    if index == (len(edep_hit)-1) :
        nextIterEventID=-1
    else : #//all other iterations
        nextIterEventID = eventID_hit[index+1]

    # fill the tmp vectors if edep is not 0
    if edep_hit[index] != 0:
        tmp_crystalID_hit.append(crystalID_hit[index])
        tmp_blockID_hit.append(blockID_hit[index])
        tmp_edep_hit.append(edep_hit[index])
        tmp_time_hit.append(time_hit[index])
        tmp_posX_hit.append(posX_hit[index])
        tmp_posY_hit.append(posY_hit[index])
        tmp_posZ_hit.append(posZ_hit[index])
        tmp_volumeID_hit.append(crystalID_hit[index]+3*blockID_hit[index])
        tmp_eventID_hit.append(eventID_hit[index])
        
    # if this hit is the last in this event -> process all the stored hits     
    if eventID_hit[index] != nextIterEventID :
        # how many unique blocks are touched ?
        set_unique_volumeID = set(tmp_volumeID_hit)
        n_unique_volumeID = len(set_unique_volumeID)
        unique_volumeID = (list(set_unique_volumeID))
        
        
        #prepare arraies to store singles
        maxEdep = np.empty(n_unique_volumeID, dtype=float)
        totEdep = np.empty(n_unique_volumeID, dtype=float)
        minTime = np.empty(n_unique_volumeID, dtype=float)
        winnerX = np.empty(n_unique_volumeID, dtype=float)
        winnerY = np.empty(n_unique_volumeID, dtype=float)
        winnerZ = np.empty(n_unique_volumeID, dtype=float)
        crystalID = np.empty(n_unique_volumeID, dtype=int)
        blockID = np.empty(n_unique_volumeID, dtype=int)
        volumeID = np.empty(n_unique_volumeID, dtype=int)
        eventID = np.empty(n_unique_volumeID, dtype=int)
   
        for k in range(n_unique_volumeID):
            maxEdep[k]=-1
            totEdep[k]=0.
            minTime[k]=999
            winnerX[k]=0
            winnerY[k]=0
            winnerZ[k]=0
            crystalID[k]=-1
            blockID[k]=-1
            volumeID[k]=-1
            eventID[k]=-1
            
            
        for j in range(len(tmp_volumeID_hit)) :
            for k in range(n_unique_volumeID) :
                if ( tmp_volumeID_hit[j] ==  unique_volumeID[k]) :
                    winnerX[k] += tmp_posX_hit[j]*tmp_edep_hit[j]
                    winnerY[k] += tmp_posY_hit[j]*tmp_edep_hit[j]
                    winnerZ[k] += tmp_posZ_hit[j]*tmp_edep_hit[j]
                    crystalID[k] = tmp_crystalID_hit[j]
                    blockID[k] = tmp_blockID_hit[j]
                    volumeID[k] = tmp_volumeID_hit[j]
                    eventID[k] = tmp_eventID_hit[j]
        
                    if (tmp_time_hit[j]<minTime[k]) : #min time
                        minTime[k]=tmp_time_hit[j]

                    totEdep[k] += tmp_edep_hit[j] # energy sum
                    
        for k in range(n_unique_volumeID) :
            crystalID_adder.append(crystalID[k])
            blockID_adder.append(blockID[k])
            edep_adder.append(totEdep[k])
            minTime_adder.append(minTime[k])
            posX_adder.append(winnerX[k]/totEdep[k])
            posY_adder.append(winnerY[k]/totEdep[k])
            posZ_adder.append(winnerZ[k]/totEdep[k])
            eventID_adder.append(eventID[k])
            #print ("winner! ", unique_blockID[k], totEdep[k], winnerX[k], winnerY[k], winnerZ[k])

        del tmp_crystalID_hit[:] 
        del tmp_blockID_hit[:]
        del tmp_volumeID_hit[:]
        del tmp_edep_hit[:]
        del tmp_time_hit[:]
        del tmp_posX_hit[:]
        del tmp_posY_hit[:]
        del tmp_posZ_hit[:]
        del tmp_eventID_hit[:]


        
#############################  READOUT #####################################
print(len(edep_adder))
nextROIterEventID=0

#tmp vectors to make operations "within a block"
tmp_crystalID_RO=[]
tmp_blockID_RO=[]
tmp_volumeID_RO=[]
tmp_edep_RO=[]
tmp_time_RO=[]
tmp_posX_RO=[]
tmp_posY_RO=[]
tmp_posZ_RO=[]
tmp_eventID_RO=[]

#arrays to fill for offline singles
crystalID_from_RO=[]
blockID_from_RO=[]
edep_from_RO=[]
minTime_from_RO=[]
posX_from_RO=[]
posY_from_RO=[]
posZ_from_RO=[]
eventID_from_RO=[]

pi=3.141592653589793238462643383279502884

for index in range(len(edep_adder)) :
    dA=360./2.;
    alpha=dA*blockID_adder[index]
    centerX=(140.+crystalID_adder[index]*20.)*math.cos(alpha*pi/180.)
    centerY=(140.+crystalID_adder[index]*20.)*math.sin(alpha*pi/180.) 
    centerZ = 0
    
    crystalID_from_RO.append(crystalID_adder[index])
    blockID_from_RO.append(blockID_adder[index])
    edep_from_RO.append(edep_adder[index])
    minTime_from_RO.append(minTime_adder[index])
    posX_from_RO.append(centerX)
    posY_from_RO.append(centerY)
    posZ_from_RO.append(centerZ)
    eventID_from_RO.append(eventID_adder[index])


        

CRED = '\033[91m'
CEND = '\033[0m'

#N entries test
if (len(edep_from_RO) == len(energy_single)) :
    print("Entries test is OK: ", len(edep_from_RO), " vs. ", len(energy_single))
else:
    print(CRED+"Entries test failed"+CEND, len(edep_from_RO), " vs. ", len(energy_single))

#Energy test
blockID_single.sort()
energy_single.sort()
globalPosX_single.sort()
globalPosY_single.sort()
globalPosZ_single.sort()
time_single.sort()

blockID_from_RO.sort()
edep_from_RO.sort()
minTime_from_RO.sort()
posX_from_RO.sort()
posY_from_RO.sort()
posZ_from_RO.sort()

for i in range(len(energy_single)) :
    if (blockID_from_RO[i] != blockID_single[i]):
        print(CRED+"BlockID test failed"+CEND, blockID_from_RO[i], " vs. ", blockID_single[i])
    if (math.fabs(edep_from_RO[i]-energy_single[i])>0.0001):
        print(CRED+"Energy test failed"+CEND, edep_from_RO[i], " vs. ", energy_single[i])
    if (math.fabs(minTime_from_RO[i] - time_single[i]) >0.0001 ):
        print(CRED+"Min time test failed"+CEND, minTime_from_RO[i], " vs. ", time_single[i])
    if (math.fabs(posX_from_RO[i] - globalPosX_single[i]) >0.0001):
        print(CRED+"PosX test failed"+CEND, posX_from_RO[i], " vs. ", globalPosX_single[i])
    if (math.fabs(posY_from_RO[i] - globalPosY_single[i]) >0.0001):
        print(CRED+"PosY test failed"+CEND, posY_from_RO[i], " vs. ", globalPosY_single[i])
    if (math.fabs(posZ_from_RO[i] - globalPosZ_single[i]) >0.0001):
        print(CRED+"PosZ test failed"+CEND, posZ_from_RO[i], " vs. ", globalPosZ_single[i])    


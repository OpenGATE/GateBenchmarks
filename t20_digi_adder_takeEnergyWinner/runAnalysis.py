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



file="output/test.root"
#file_path = os.path.join(folder, filename)
#file = uproot.open("output/test.root")
#print(file_path.classnames())

branches = ["edep","eventID","blockID","posX", "posY", "posZ", "time"]
hitTree = uproot.open(file)['Hits'].arrays(branches,library="numpy")
edep_hit=hitTree["edep"]
eventID_hit=hitTree["eventID"]
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


nextIterEventID=0

#tmp vectors to make operations "within a block"
tmp_blockID=[]
tmp_edep_hit=[]
tmp_time_hit=[]
tmp_posX_hit=[]
tmp_posY_hit=[]
tmp_posZ_hit=[]

#arrays to fill for offline singles
blockID_from_hit=[]
edep_from_hit=[]
minTime_from_hit=[]
posX_from_hit=[]
posY_from_hit=[]
posZ_from_hit=[]


for index in range(len(edep_hit)) :
    #print (eventID_hit[index], blockID_hit[index], edep_hit[index], posX_hit[index],posY_hit[index], posZ_hit[index])  
    # last iteration
    if index == (len(edep_hit)-1) :
        nextIterEventID=-1
    else : #//all other iterations
        nextIterEventID = eventID_hit[index+1]

    # fill the tmp vectors if edep is not 0
    if edep_hit[index] != 0:
        tmp_blockID.append(blockID_hit[index])
        tmp_edep_hit.append(edep_hit[index])
        tmp_time_hit.append(time_hit[index])
        tmp_posX_hit.append(posX_hit[index])
        tmp_posY_hit.append(posY_hit[index])
        tmp_posZ_hit.append(posZ_hit[index])

    # if this hit is the last in this event -> process all the stored hits     
    if eventID_hit[index] != nextIterEventID :
        # how many unique blocks are touched ?
        set_unique_blockID = set(tmp_blockID)
        n_unique_blockID = len(set_unique_blockID)
        unique_blockID = (list(set_unique_blockID))
        
        
        #prepare arraies to store singles
        maxEdep = np.empty(n_unique_blockID, dtype=float)
        totEdep = np.empty(n_unique_blockID, dtype=float)
        minTime = np.empty(n_unique_blockID, dtype=float)
        winnerX = np.empty(n_unique_blockID, dtype=float)
        winnerY = np.empty(n_unique_blockID, dtype=float)
        winnerZ = np.empty(n_unique_blockID, dtype=float)

        for k in range(n_unique_blockID):
            maxEdep[k]=-1
            totEdep[k]=0.
            minTime[k]=999
            
            
        for j in range(len(tmp_blockID)) :
            for k in range(n_unique_blockID) :
                if ( tmp_blockID[j] ==  unique_blockID[k]) :
                    if (tmp_edep_hit[j] >= maxEdep[k]) : #find max energy and position of energy winner
                        maxEdep[k]=tmp_edep_hit[j]
                        winnerX[k]=tmp_posX_hit[j]
                        winnerY[k]=tmp_posY_hit[j]
                        winnerZ[k]=tmp_posZ_hit[j]

                    if (tmp_time_hit[j]<minTime[k]) : #min time
                        minTime[k]=tmp_time_hit[j]

                    totEdep[k] += tmp_edep_hit[j] # energy sum
                    
        for k in range(n_unique_blockID) :
            blockID_from_hit.append(unique_blockID[k])
            edep_from_hit.append(totEdep[k])
            minTime_from_hit.append(minTime[k])
            posX_from_hit.append(winnerX[k])
            posY_from_hit.append(winnerY[k])
            posZ_from_hit.append(winnerZ[k])
            #print ("winner! ", unique_blockID[k], totEdep[k], winnerX[k], winnerY[k], winnerZ[k])
	    
        del tmp_blockID[:]
        del tmp_edep_hit[:]
        del tmp_time_hit[:]
        del tmp_posX_hit[:]
        del tmp_posY_hit[:]
        del tmp_posZ_hit[:]

CRED = '\033[91m'
CEND = '\033[0m'

#N entries test
if (len(edep_from_hit) == len(energy_single)) :
    print("Entries test is OK: ", len(edep_from_hit), " vs. ", len(energy_single))
else:
    print(CRED+"Entries test failed"+CEND, len(edep_from_hit), " vs. ", len(energy_single))

#Energy test
blockID_single.sort()
energy_single.sort()
globalPosX_single.sort()
globalPosY_single.sort()
globalPosZ_single.sort()
time_single.sort()

blockID_from_hit.sort()
edep_from_hit.sort()
minTime_from_hit.sort()
posX_from_hit.sort()
posY_from_hit.sort()
posZ_from_hit.sort()

for i in range(len(energy_single)) :
    if (blockID_from_hit[i] != blockID_single[i]):
        print(CRED+"BlockID test failed"+CEND, blockID_from_hit[i], " vs. ", blockID_single[i])
    if (math.fabs(edep_from_hit[i]-energy_single[i])>0.00001):
        print(CRED+"Energy test failed"+CEND, edep_from_hit[i], " vs. ", energy_single[i])
    if (minTime_from_hit[i] != time_single[i]):
        print(CRED+"Min time test failed"+CEND, minTime_from_hit[i], " vs. ", time_single[i])
    if (posX_from_hit[i] != globalPosX_single[i]):
        print(CRED+"PosX test failed"+CEND, posX_from_hit[i], " vs. ", globalPosX_single[i])
    if (posY_from_hit[i] != globalPosY_single[i]):
        print(CRED+"PosY test failed"+CEND, posY_from_hit[i], " vs. ", globalPosY_single[i])
    if (posZ_from_hit[i] != globalPosZ_single[i]):
        print(CRED+"PosZ time test failed"+CEND, posZ_from_hit[i], " vs. ", globalPosZ_single[i])
    

"""
fig, ((ax0,ax1),(ax2,ax3),(ax4,ax5)) = plt.subplots(ncols=2,nrows=3, figsize=(10,10))

#a = phsp.fig_get_sub_fig(ax, 1)

ax0.hist(energy_single, bins=100, alpha=0.5, label="Singles")
ax00.hist(edep_from_hit, bins=100, alpha=0.5, label="Offline hits analysis")
ax0.legend(loc='upper right')
ax0.set_xlabel("edep")

ax1.hist(time_single, bins=100, alpha=0.5, label="time")
#ax1.legend(loc='upper right')
ax1.set_xlabel("time")

ax2.hist(globalPosX_single, bins=100, alpha=0.5, label="globalPosX")
#ax2.legend(loc='upper right')
ax2.set_xlabel("globalPosX")

ax3.hist(globalPosY_single, bins=100, alpha=0.5, label="globalPosY")
ax3.set_xlabel("globalPosY")

ax4.hist(globalPosZ_single, bins=100, alpha=0.5, label="globalPosZ")
ax4.set_xlabel("globalPosZ")

plt.show()


plt.hist(posX_from_hit, bins=100, alpha=0.5, label="edep")
plt.hist(globalPosX_single, bins=100, alpha=0.5, label="edep")
plt.legend(loc='upper right')
plt.xlabel("edep, MeV")
plt.show()

print (edep_hit[2])
"""
#input()


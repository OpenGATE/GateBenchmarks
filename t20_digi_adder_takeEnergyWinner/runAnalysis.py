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



for batch in hitTree.iterate(step_size=1):
    print(repr(batch))








fig, ((ax0,ax1),(ax2,ax3),(ax4,ax5)) = plt.subplots(ncols=2,nrows=3, figsize=(10,10))

#a = phsp.fig_get_sub_fig(ax, 1)

ax0.hist(energy_single, bins=100, alpha=0.5, label="edep")
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

"""
plt.hist(edep_single, bins=100, alpha=0.5, label="edep")
plt.hist(edep_single, bins=100, alpha=0.5, label="edep")
plt.legend(loc='upper right')
plt.xlabel("edep, MeV")
plt.show()

print (edep_hit[2])
"""
input()

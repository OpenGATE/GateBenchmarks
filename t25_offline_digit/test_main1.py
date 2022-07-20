#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gam_gate as gam

# ------------------------------------------------------
gam.warning('Compare root singles')
root_ref = 'output/output1.root'
root_offline = 'output/output1-singles.root'

checked_keys = ['time', 'energy',
                'globalPosX', 'globalPosY', 'globalPosZ']
scalings = [1] * len(checked_keys)
tols = [0.01] * len(checked_keys)
tols[0] = 0.02  # time
tols[1] = 0.001  # energy
tols[2] = 0.8  # globalPosX
tols[3] = 0.4  # globalPosY
tols[4] = 0.2  # globalPosZ
is_ok = gam.compare_root3(root_ref, root_offline,
                          "Singles", "Singles",
                          checked_keys, checked_keys,
                          tols, scalings,
                          'output/main1_root_singles.png')
print(is_ok)


# ------------------------------------------------------
# not yet possible to compare

print()
gam.warning('Compare root coinc')
root_ref = 'output/output1.root'
root_offline = 'output/output1-coinc.root'

checked_keys = ['time1','time2', 'energy1','energy2',
                'globalPosX1','globalPosX2', 'globalPosY1','globalPosY2', 'globalPosZ1','globalPosZ2']
scalings = [1] * len(checked_keys)
tols = [0.01] * len(checked_keys)
tols[0] = 0.02  # time1
tols[1] = 0.02
tols[2] = 0.001  # energy1
tols[3] = 0.001  # energy2
tols[4] = 0.8  # globalPosX1
tols[5] = 0.8  # globalPosX2
tols[6] = 0.8  # globalPosY1
tols[7] = 0.8  # globalPosY2
tols[8] = 0.2  # globalPosZ1
tols[9] = 0.2  # globalPosZ2

print(scalings, tols)
is_ok = gam.compare_root3(root_ref, root_offline,
                          "Coincidences", "Coincidences",
                          checked_keys, checked_keys,
                          tols, scalings,
                          'output/main1_root_coincidences.png')
print(is_ok)

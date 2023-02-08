Gate mac/cylPET_1SD/main.mac
Gate mac/ecat_1SD/main.mac
Gate mac/SPECT_1SD/main.mac

#if [  $Gate_Version -gt 9.2 ]
#then
#    Gate mac/main_energyWinner.mac
#else
#    Gate mac/main_centroid.mac
#fi

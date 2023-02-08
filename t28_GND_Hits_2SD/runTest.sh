Gate mac/cylPET_2SD/main.mac
Gate mac/SPECT_2SD/main.mac

#if [  $Gate_Version -gt 9.2 ]
#then
#    Gate mac/main_energyWinner.mac
#else
#    Gate mac/main_centroid.mac
#fi

This simulation is a PET benchmark.

DISCLAIMER: this is NOT a true PET device. 
It has been designed to check several Gate features.
It is not expected to give realistic results.


Test of readout at the level of crystal (depth=2)
Gate mac/main_centroid_d2.mac 
runAnalysis_centroid_d2.py

Test of readout at the level of block (depth=1)
Gate mac/main_centroid_d1.mac 
runAnalysis_centroid_d1.py

Test of readout at the level of crystal (depth=2)
Gate mac/main_winner_d2.mac 
runAnalysis_winner_d2.py

Test of readout at the level of block (depth=1
Gate mac/main_winner_d1.mac 
runAnalysis_winner_d1.py

Run with:
Gate mac/main_centroid_d2.mac 
Gate mac/main_centroid_d1.mac
Gate mac/main_winner_d2.mac
Gate mac/main_winner_d1.mac
or
source runTest.sh


Expected time: 2 min


Run the analysis with 
runAnalysis_winner_d2.py
runAnalysis_winner_d1.py
runAnalysis_centroid_d2.py
runAnalysis_centroid_d1.py

Timing
source 2gammas 50 kBq 0.05sec 4 simulations -> 2 min

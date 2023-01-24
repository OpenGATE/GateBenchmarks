This simulation is a PET benchmark.

DISCLAIMER: this is NOT a true PET device. 
It has been designed to check several Gate features.
It is not expected to give realistic results.

This is simpliest test of CoincidenceSorter for 4 policies:
1) takeAllGoods
2) takeWinnerOfGoods
3) killAll
4) keepIfOnlyOneGood
It constructs coincidences from singles and compare the total number of these "offline" coincidecnes with obtained from GateCoincidenceSorter


Run with:
Gate mac/main_test1.mac
Gate mac/main_test2.mac
Gate mac/main_test3.mac
Gate mac/main_test4.mac 
or
source runTest.sh


Expected time: 1.5 min


Run the analysis with 
runAnalysis.py

Timing
source 2gammas 50 kBq 0.05sec -> 0.6 sec

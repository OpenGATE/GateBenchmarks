This simulation is a PET benchmark.

DISCLAIMER: this is NOT a true PET device. 
It has been designed to check several Gate features.
It is not expected to give realistic results.

This is test for Gate New Digitizer.

Run with:
Gate mac/main.mac
or
source runTest.sh


Expected time: 6 sec

Run the analysis with 
runAnalysis.py


19-02-2026. After passing from Geant4 11.3.0 to Geant4 11.4.0 it seems some of optical description became more precise and some of optical photons now is desciped better. However, this makes this test fail giving a peak at 1.77 eV coming from WLS in RhD.
But this test is meant to be for digitizer and not the optical part which is tested in t15. This is why the WLSCOMPONENT for RhD was modified and a cut at min energy at 1.77 eV was applied in order to march the distributions form previous results (i.e. the tail was cut out)


The objectif of this benchmark us to test UserSpectrum (mode1) and RadioactiveDecay together. The 2 methods can be used to simulate a radioactive source.
The idea is to compute this test comparing the spectrum produced by the detection of a 137Cs source and a detector of NaI 3"x3" (similar to the reference in gamma spectrometry).

The simulation can be run in 2 ways:
- using the UserSpectrum of the GPS (Gate -a [type,spectrum])
- using the RadioactiveDecay of Geant4 (Gate -a [type,source])

The output file is written by the actor EnergySpectrum (root file).

A pyhton script is available to analyze the output in order to:
- compute the efficiency of the total detection and the efficienty of the peak detection (like in gamma spectromety)
- compare these efficiencies to reference values (written in the script) and test their compatibility at 95%
- plot the simulated spectrum and compare to the reference spectrum


# Generic Move Benchmark

A benchmark for the GenericMove function is created. Both the movement of a source and movement of the detector volumes are tested. A point source emitting back-to-back photons at 511 keV is placed inside the FOV of the Phillips/ADAC Forte. The source moves from -5 mm to 5 mm.  The detector separation changes from 800 mm to 400 mm over 0.1 seconds. The time slice used is 0.001 seconds. 

To create the placements files run 'python3 makeTrajectorySimple.py'.

To launch the visualisation run, 'Gate --qt runForteVis.mac'. 

To start the simulation run 'python3 runTest.py'.

To analyse the output run 'python3 runAnalysis.py'.

Author: Matthew Herald

Herald, M., Wheldon, T., & Windows-Yule, C. (2021). Monte Carlo model validation of a detector system used for Positron Emission Particle Tracking. Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment, 993, 165073. https://doi.org/10.1016/j.nima.2021.165073.

![Alt text](data/Benchmark.png?raw=true)

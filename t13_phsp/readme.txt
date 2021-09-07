
Check PhaseSpaceSource (and PhaseSpaceActor)

First simulation : Gate mac/main-write-phsp.mac
It is a fake Linac, that simulate a e- source to a Tungsten target to generate high E gamma (Brem). A variance reduction technique is used (Bremsstrahlung splitting). There are two output: 1) a plane phase space at the exit of the Linac and 2) another phase space associated with a waterbox below the Linac.

Second simulation : Gate mac/main-read-phsp.mac
This is the same simulation where the beam has been replaced by the phase space source, reading data from the previous first output. The same second output is considered.

Analysis: compare both waterbox phase space
gt_phsp_plot output/phsp-*-waterbox.root
./runAnalysis.py output

WARNING about Time in the PhaseSpaceActor, 'enableTime' stores GlobalTime, and 'enableLocalTime' stores LocalTime. If both are enabled, only LocalTime is stored. This behavior should probably be changed in the future. 





Check PhaseSpaceSource (and PhaseSpaceActor)

First simulation : Gate mac/main-write-phsp.mac

Second simulation : Gate mac/main-read-phsp.mac

Analysis: compare both waterbox phase space
gt_phsp_plot output/phsp-*-waterbox.root
./runAnalysis.py output




# Part1

Check PhaseSpaceSource (and PhaseSpaceActor)

First simulation : Gate mac/main-write-phsp.mac
- write a PET phsp
- convert into "pairs" with gaga_pet_to_pairs
- warning, the used branch is "TimeFromBeginOfEvent" that store the relative time between the time at which the primary has been emitted and the time when it has been detected.
- the input source: 10kBq during 2 seconds, with *FAKE* decay of 1 second
- a total of about 7k e+ is emitted, leading to 13762 gamma pairs in the phsp, 1162 detected
- in the phsp, Time is in Geant4 units

Second simulation : Gate mac/main-read-phsp.mac
- read from "pairs" file
- timing ?

Analysis: compare both waterbox phase space

gt_phsp_plot output/phsp-*-waterbox.root
./runAnalysis.py output

# Part2

check convert pairs -> tlor -> pairs

gaga_pet_to_pairs output/phsp_write.root -o output/phsp_write_pairs.npy
gaga_pairs_to_tlor output/phsp_write_pairs.npy -o output/phsp_write_tlor.npy --det_radius 400 --cyl_height 2500
gaga_tlor_to_pairs output/phsp_write_tlor.npy -o output/phsp_write_pairs2.npy --cyl_radius 300 --cyl_height 2500
gt_phsp_plot output/phsp_write_pairs*.npy

# Part3

Idem but replace phsp reading with a GAN
1) train the gan
    gaga_pairs_to_tlor
    gaga_train
    gaga_generate
    gaga_tlor_to_pairs --> data/gan_generated_pairs.npy

Compare gan pre-generated pairs with gan generated in Gate

Gate mac/main-read-gan-phsp.mac
Gate mac/main-read-gan.mac



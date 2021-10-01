
# Part 1 (write then read phsp with pairs)
Gate mac/main_write_phsp.mac
gaga_pet_to_pairs output/phsp_write.root -o output/phsp_write_pairs.npy -t TimeFromBeginOfEvent
Gate mac/main_read_phsp.mac

# test conversion from pairs to tlor, from tlor to pairs
gaga_pairs_to_tlor output/phsp_write_pairs.npy -o output/phsp_write_tlor.npy --det_radius 400 --cyl_height 2500
gaga_tlor_to_pairs output/phsp_write_tlor.npy -o output/phsp_write_pairs2.npy --cyl_radius 300 --cyl_height 2500
gt_phsp_plot output/phsp_write_pairs*.npy -o output/compare_pairs_pairs2.pdf

# Part 2: idem from phsp generated from GAN
# Part 3: idem from from GAN
#

nice gaga_train output/phsp_write_tlor.npy test175.json -o a.pth -pi epoch 1000

gaga_plot output/phsp_write_tlor.npy  test175_GP_SquareHinge_1_80000.pth

nice gaga_train output/phsp_write_tlor.npy test002.json -o a_002_10K.pth -pi epoch 10000 ; nice gaga_train output/phsp_write_tlor.npy test001.json -o a_001_10K.pth -pi epoch 10000; nice gaga_train output/phsp_write_tlor.npy test002.json -o a_002_40K.pth -pi epoch 40000;  nice gaga_train output/phsp_write_tlor.npy test001.json -o a_001_40K.pth -pi epoch 40000;



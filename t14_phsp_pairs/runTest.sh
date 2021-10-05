
# --------------------------------------------------------------------------------------------
# Part 1 (write then read phsp with pairs)
Gate mac/main_write_phsp.mac
gaga_pet_to_pairs output/phsp_write.root -o output/phsp_write_pairs.npy -t TimeFromBeginOfEvent
Gate mac/main_read_phsp.mac

# test conversion from pairs to tlor, from tlor to pairs
gaga_pairs_to_tlor output/phsp_write_pairs.npy -o output/phsp_write_tlor.npy --det_radius 400 --cyl_height 2500
gaga_tlor_to_pairs output/phsp_write_tlor.npy -o output/phsp_write_pairs2.npy --cyl_radius 300 --cyl_height 2500
gt_phsp_plot output/phsp_write_pairs*.npy -o output/compare_pairs_pairs2.pdf

# --------------------------------------------------------------------------------------------
# Part 2: idem from phsp generated from GAN

# train the gan (not done during the test)
# gaga_train output/phsp_write_tlor.npy test002.json -o pth/a_002_40K.pth -pi epoch 40000
gaga_plot output/phsp_write_tlor.npy pth/a_002_40K.pth -o a_002_40K_marginals.png

# generate phsp from the GAN (only plot here no quantitative analysis)
gaga_generate pth/a_002_40K.pth -o data/a_002_40K_tlor.npy -n 1e5
gaga_tlor_to_pairs data/a_002_40K_tlor.npy -o data/a_002_40K_pairs.npy --cyl_radius 300 --cyl_height 2500
gt_phsp_plot output/phsp_write_tlor.npy data/a_002_40K_tlor.npy -n 1e4 -o a_002_40K_tlor.png
gt_phsp_plot output/phsp_write_pairs.npy data/a_002_40K_pairs.npy -n 1e4 -o a_002_40K_pairs.png

# run simulation using the gan generated phsp
Gate mac/main_read_gan_phsp.mac
gt_phsp_plot output/output_read_detector.root output/output_read_gan_phsp_detector.root -o a_002_40K_gan_phsp.png

# --------------------------------------------------------------------------------------------
# Part 3: idem from from GAN

gaga_convert_pth_to_pt pth/a_002_40K.pth -o data/a_002_40K --cyl_radius 300  --cyl_height 2500 -v
Gate mac/main_read_gan.mac
gt_phsp_plot output/output_read_detector.root output/output_gaga_read_gan_detector.root -o a_002_40K_gan.png

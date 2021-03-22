
pip3 install garf matplotlib click
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

Gate mac/main_arf.mac

garf_scale --ref reference_data/analog/results._p93vfh_/stats.txt -n output/projection.mhd
#garf_compare_image_profile reference_data/analog/results._p93vfh_/projection.mhd output/projection-s.mhd -w 10




echo $1

source ../../g${1}.sh
which Gate

garf_scale output-${1}/projection.mhd --ref garf/reference_data/analog/results.e75f9s13/stats.txt --noise -j 5
garf_compare_image_profile garf/reference_data/analog/results.e75f9s13/projection.mhd output-${1}/projection-s.mhd -w 2



echo $1

source ../../g${1}.sh
which Gate

gaga-phsp/plot_err.py /home/dsarrut/public_html/gaga/results.ref.part1/ /home/dsarrut/public_html/gaga/results.ref.part2/ output-${1}/ -s 1 -s 1 -s 1


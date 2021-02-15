
echo $1

source ../../g${1}.sh
which Gate

gate_power_merge.sh gaga-phsp/output-t4-${1}

\rm -rf output-${1}
cp -r results.0 output-${1}



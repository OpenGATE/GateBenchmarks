
gate_split_and_run.py mac/main_arf_v2.mac -a RADIONUCLIDE Lu177 -a SPECT_RADIUS 25 -a N 2e5 -j 1 -o output

#Wait Gate pids
processId=($(ps -ef | grep 'Gate' | grep -v 'grep' | awk '{ print $2 }'))
for pid in ${processId[*]}; do
  while [[ ${?} == 0 ]]; do
    sleep 1s
    ps -p $pid >/dev/null
  done
done

ls
ls output
cat output/gate.o_0

gate_power_merge.sh output
rm -rf output
mv results output



gate_split_and_run.py mac/main.mac -a N 2e5 -a TYPE gaga -j 5 -o output

#Wait Gate pids
processId=($(ps -ef | grep 'Gate' | grep -v 'grep' | awk '{ print $2 }'))
for pid in ${processId[*]}; do
  while [[ ${?} == 0 ]]; do
    sleep 1s
    ps -p $pid >/dev/null
  done
done

gate_power_merge.sh output
rm -rf output
mv results output


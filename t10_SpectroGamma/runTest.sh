#emstandard_opt4
gate_split_and_run.py mac/main.mac -a type spectrum -a physic_list emstandard_opt4 -j 1 -o output

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
mv results output_spectrum_emstandard_opt4
mkdir output

gate_split_and_run.py mac/main.mac -a type source -a physic_list emstandard_opt4 -j 1 -o output

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
mv results output_source_emstandard_opt4
mkdir output


#QGSP_BERT_EMZ
gate_split_and_run.py mac/main.mac -a type spectrum -a physic_list QGSP_BERT_EMZ -j 1 -o output

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
mv results output_spectrum_qgsp_bert_emz
mkdir output

gate_split_and_run.py mac/main.mac -a type source -a physic_list QGSP_BERT_EMZ -j 1 -o output

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
mv results output_source_qgsp_bert_emz
mkdir output

mv output_*/* output
rm -rf output_*
ls output


# for reference :
# gaga_train ELEKTA_PRECISE_6mv_part1.root params/config_003_v3.json -o pth/003_v3_20k.pth -pi epoch 40000

# trial pth3/001.pth :       PHSP1 vs GAN mu et sigma =  0.20612659 1.2270443 no
# trial pth/001_v3_50k.pth : PHSP1 vs GAN mu et sigma =  0.15138769 1.2516584 no
# trial pth/002_v3_30k.pth : PHSP1 vs GAN mu et sigma =  0.12511426 1.1965427 OK
# trial pth/003_v3_20k.pth : PHSP1 vs GAN mu et sigma =  0.09131236 1.1889951 OK
# trial pth/003_v3_40k.pth : PHSP1 vs GAN mu et sigma =  0.07085757 1.1661557 OK <-- best
# trial pth/004_v3_20k.pth : PHSP1 vs GAN mu et sigma =  0.12475119 1.2066121 no

gaga_convert_pth_to_pt pth/003_v3_40k.pth --no-gpu -k Z 271.1 -v --no-denorm -o pth/current
gaga_convert_pth_to_pt pth/003_v3_40k.pth --no-gpu -k Z 271.1 -v --denorm -o pth/current_norm

gate_split_and_run.py mac/main1.mac -a N 1e7 -a TYPE gaga -j 1 -o output1
gate_split_and_run.py mac/main2.mac -a N 1e7 -a TYPE gaga -j 1 -o output2

# Wait Gate pids
processId=($(ps -ef | grep 'Gate' | grep -v 'grep' | awk '{ print $2 }'))
echo "Waiting for Gate to terminate ..."
for pid in ${processId[*]}; do
  while [[ ${?} == 0 ]]; do
    sleep 1s
    ps -p $pid >/dev/null
  done
done

mv output1/output.local_0/* output1

mv output2/output.local_0/* output2

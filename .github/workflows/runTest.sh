#!/bin/bash

set -e -x

source /opt/rh/devtoolset-7/enable
#source /etc/mybashrc
export PATH=/software/cmake-3.18.4-Linux-x86_64/bin/:/opt/rh/devtoolset-7/root/usr/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
source /software/geant4/install/bin/geant4.sh
source /software/root-cern/install/bin/thisroot.sh

#Install gatetools and clustertools
mkdir /software/gatetools
cd /software
git clone https://github.com/OpenGATE/GateTools.git gatetools
cd gatetools
pip3 install -e .
echo "export PATH=/software/gatetools/clustertools/:$PATH" >> /etc/mybashrc

cd /software/gate
git clone https://github.com/OpenGATE/Gate.git src
cd bin
cmake ../src
make -j4
source /etc/mybashrc
echo "export PATH=/software/gate/bin:$PATH" >> /etc/mybashrc
source /etc/mybashrc

cd /home/
rm /usr/bin/python
ln -s /usr/bin/python3 /usr/bin/python
which python3
python3 --version
export LC_ALL=en_US.utf8
export LANG=en_US.utf8
pip3 install click colorama
python3 runBenchmark.py -t ${TEST}


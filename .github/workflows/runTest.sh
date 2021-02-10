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
pip3 install uproot uproot3 xxhash lz4
echo "export PATH=/software/gatetools/clustertools/:$PATH" >> /etc/mybashrc

#Install dependencies according the test
compile_torch=false
compile_rtk=false
if [ "$TEST" = "t3" ]; then
   compile_torch=true
fi
export GATE_USE_TORCH=OFF
if [ "$compile_torch" = true ] ; then
    cd /software
    mkdir torch
    cd torch
    wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-1.4.0%2Bcpu.zip
    unzip libtorch-cxx11-abi-shared-with-deps-1.4.0+cpu.zip
    export GATE_USE_TORCH=OFF
    export TORCH_DIR=/software/torch/libtorch/share/cmake/Torch
fi

# Compile master versio of Gate
cd /software/gate
git clone https://github.com/OpenGATE/Gate.git src
cd bin
cmake -DGATE_USE_TORCH=$GATE_USE_TORCH \
      -DTorch_DIR=$TORCH_DIR \
      ../src
make -j4
source /etc/mybashrc
echo "export PATH=/software/gate/bin:$PATH" >> /etc/mybashrc
source /etc/mybashrc

# Go to execute the test
cd /home/
rm /usr/bin/python
ln -s /usr/bin/python3 /usr/bin/python
which python3
python3 --version
export LC_ALL=en_US.utf8
export LANG=en_US.utf8
pip3 install click colorama
OutputTest=$(python3 runBenchmark.py -t ${TEST} | tail -1)
if [ $OutputTest = 0 ]; then
    exit -1
else
    exit 0
fi


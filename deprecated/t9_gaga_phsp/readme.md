
Example associated with:
Phys Med Biol. 2019. Generative adversarial networks (GAN) for compact beam source modelling in Monte Carlo simulations [published online ahead of print, 2019 Aug 30]. 
Sarrut D, Krah N, Letang JM. 
Phys Med Biol. 2019;10.1088/1361-6560. doi:10.1088/1361-6560/ab3fc1 https://www.ncbi.nlm.nih.gov/pubmed/31470418

The source code is : https://github.com/dsarrut/gaga

The example is : https://github.com/OpenGATE/GateContrib/tree/master/dosimetry/gaga-phsp

- Here, we start from already computed GAN (pth file).
- The pth file is converted into .pt and .json file that can be processed by GATE
_ Simulations are run with GAN as sources, computing the dose distribution in a waterbox.
- Resulting doses are compared to reference doses
- Two simulations are performed:
    - the first (output1) with denormalisation perform by GATE (old)
    - the second (output2) with denormalisation included in the .pt (new)
    Both must lead to the exact same result

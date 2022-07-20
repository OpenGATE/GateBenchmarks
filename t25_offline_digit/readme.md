


## Example 1

Simple Cylindrical PET with 20 x 20 block, 5x5 crystal, LSO and BGO layer, 4 rings. 
- No phantom.
- Physics list: emstandard_opt4
- Digitizer: adder, NO readout, threshold, coinc 10 ns
- Source: back to back 511 keV, half-life of 1223 sec (C11)

```shell
Gate mac/main1.mac
```
This will generate ```output/output1.root``` with hits, singles and coincidences

Offline digitizer
```shell 
GateDigit_hits_digitizer output/output1.root output/output1-singles.root mac/main1_offline_digitizer.mac
```
This will generate ```output/output1-singles.root``` with the singles. There is an error message since there are branches not found since it is designed for CCMod data and those branches are missing here 

Offline sorter
```shell 
GateDigit_singles_sorter output/output1-singles.root output/output1-coincCCMod.root mac/main1_offline_sorter.mac abs
GateDigit_singles_sorter output/output1.root    output/output1-coincCCMod.root  mac/main1_offline_sorter.mac abs
```
We can generate the coincidences either from the  singles of simulation stored in   ```output/output1.root``` or from the offline generated singles  ```output/output1-singles.root```
This will generate ```output/output1-coincCCMod.root``` with the coincidences

Convert CCMod coincidences into PET/SPECT coincidences format  ( On branch anetxe offlineDigitizer, not yet in OpenGate)
```shell 
 Convert_CCMod2PETCoinc output/output1-coincCCMod.root output/output1-coinc.root  mac/main1_offline_geom.mac
 ```

 test with gam_gate. test_main.py
 
 ## Example 1.b

Simple Cylindrical PET with 20 x 20 block, 5x5 crystal, LSO and BGO layer, 4 rings. 
- No phantom.
- Physics list: emstandard_opt4
- Digitizer: adder, readout (depth 1 or head), threshold, coinc 10 ns
- Source: back to back 511 keV, half-life of 1223 sec (C11)

```shell
Gate mac/main1b.mac
```
This will generate ```output/output1b.root``` with hits, singles and coincidences




## Example 2


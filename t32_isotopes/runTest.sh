#!/usr/bin/bash

#physicLists="QGSP_BIC_HP QGSP_BERT_HP QGSP_INCLXX_HP Shielding ShieldingM FTFP_BERT_HP"
physicLists="QGSP_BIC_HP QGSP_BERT_HP Shielding"

for pl in $physicLists; do
    Gate -a [suffix,500K][npart,500000][mainMaterial,C][physicList,$pl] mac/main.mac
    Gate -a [suffix,500K][npart,500000][mainMaterial,C14][physicList,$pl] mac/main.mac
done

#!/usr/bin/bash

parallel -j 2 Gate92 -a [suffix,5M][npart,5000000][mainMaterial,C][physicList,{}] mac/main.mac ::: QGSP_BIC_HP QGSP_BERT_HP QGSP_INCLXX_HP Shielding ShieldingM FTFP_BERT_HP &
parallel -j 2 Gate92 -a [suffix,5M][npart,5000000][mainMaterial,C14][physicList,{}] mac/main.mac ::: QGSP_BIC_HP QGSP_BERT_HP QGSP_INCLXX_HP Shielding ShieldingM FTFP_BERT_HP &

#!/bin/bash

#LANG="$1"
H5="/mnt/nas_home/mrgj4/marvl_experiments/marvl-ta_boxes36.h5"
LMDB="/mnt/nas_home/mrgj4/marvl_experiments/marvl-ta_boxes36.lmdb"

#source activate /science/image/nlp-datasets/emanuele/envs/volta

python h5_to_lmdb.py --h5 $H5 --lmdb $LMDB

#conda deactivate

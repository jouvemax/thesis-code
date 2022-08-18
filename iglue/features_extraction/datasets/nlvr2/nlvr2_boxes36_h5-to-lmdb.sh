#!/bin/bash

DATA="/mnt/nas_home/mrgj4/nlvr2_dataset"
H5="${DATA}/nlvr2_boxes36.h5"
LMDB="${DATA}/test_extraction.lmdb"

#source /home/projects/ku_00062/envs/iglue/bin/activate

cd ../..
python h5_to_lmdb.py --h5 $H5 --lmdb $LMDB

deactivate

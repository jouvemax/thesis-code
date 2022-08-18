#!/bin/bash

H5="/mnt/nas_home/mrgj4/wit_dataset/features/zh_features.h5"
LMDB="/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_2/zh/seed3/fullcov/training_feat_all.lmdb"
INDEXES="/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_2/zh/seed3/fullcov/training_indices_seed3.pickle"

python h5_to_lmdb_pretraining.py --h5 $H5 --lmdb $LMDB --indexes $INDEXES

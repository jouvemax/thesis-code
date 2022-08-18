#!/bin/bash

#LANG="id"
#H5="/mnt/tamedia/marvl/marvl-${LANG}_boxes36.h5"
#LMDB="/mnt/tamedia/marvl/marvl-${LANG}_boxes36.lmdb"

H5="/mnt/nas_home/mrgj4/wit_dataset/features/tr_features.h5"
LMDB="/mnt/nas_home/mrgj4/wit_dataset/utils/concepts_coverage_exp/tr/halfcov_3/training_feat_all.lmdb"
INDEXES="/mnt/nas_home/mrgj4/wit_dataset/utils/concepts_coverage_exp/tr/halfcov_3/training_ind_halfcov_3.pickle"

python h5_to_lmdb_pretraining.py --h5 $H5 --lmdb $LMDB --indexes $INDEXES
#python h5_to_lmdb_pretraining.py --h5 $H5 --lmdb $LMDB

#!/bin/bash


INDIR=/mnt/nas_home/mrgj4/wit_dataset/images/zh
OUTDIR=/mnt/nas_home/mrgj4/wit_dataset/features
CAPTION_PATH=/mnt/nas_home/mrgj4/wit_dataset/captions/zh_captions.json

#mkdir -p $OUTDIR

#source ${basedir}/envs/py-bottomup/bin/activate

#conda activate /mnt/nas_home/mrgj4/miniconda3/envs/py-bottomup/


# TODO:do not forget to change the caption path in detectron2_proposal_maxnms_pretraining.py
# BE CAREFUL
# BE CAREFUL

python wit_pretraining_proposal.py \
  --root $INDIR \
  --outdir $OUTDIR \
  --caption_path $CAPTION_PATH

#conda deactivate
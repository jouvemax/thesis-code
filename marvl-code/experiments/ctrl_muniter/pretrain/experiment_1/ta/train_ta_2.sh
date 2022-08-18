#!/bin/bash

FAMILY=joint
MODEL=ctrl_muniter
MODEL_CONFIG=ctrl_muniter_base


ANNOS=/mnt/nas_home/mrgj4/final_repo/experiment_1/ta/seed2
WIKIS=/mnt/nas_home/mrgj4/wit_dataset/wikipedia
FEATS=/mnt/nas_home/mrgj4/final_repo/experiment_1/ta/seed2

OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/experiment_1/ta/seed2/pretrain
LOGGING_DIR=/mnt/nas_home/mrgj4/final_repo/experiment_1/ta/seed2/pretrain/logging

#source activate /science/image/nlp-datasets/emanuele/envs/mc-bert

# don't forget to change the language --lgs


## CHANGE SHUFFLE AND SEED IF NOT NEEDED
# change shuffle in wit_dataset.py if not needed

cd ../../../../../../marvl-code/volta
python train_wit_wiki.py \
  --bert_model bert-base-multilingual-cased --config_file config/${MODEL_CONFIG}.json \
  --x_pretrained /mnt/nas_home/mrgj4/models/ctrl_muniter/cc_wikipedia_pretrain/pytorch_model_9.bin \
  --train_x_batch_size 256 --train_m_batch_size 256 --gradient_accumulation_steps 4 \
  --max_x_seq_length 66 --max_m_seq_length 66 --m_pretrained bert-base-multilingual-cased \
  --learning_rate 1e-4 --adam_epsilon 1e-6 --adam_betas 0.9 0.999 --weight_decay 0.01 --warmup_proportion 0.1 --clip_grad_norm 5.0 \
  --objective 1 \
  --annotations_path $ANNOS --features_path $FEATS \
  --dataroot $WIKIS --lgs ta --lg_sampling_factor 0.7 \
  --output_dir ${OUTPUT_DIR} \
  --logdir ${LOGGING_DIR} \
  --num_train_epochs 25 \
#  --seed 13 \
#  --resume_file /mnt/localdata/jouve/wit/pretrain/ctrl_muniter_base/pytorch_ckpt_latest.tar

#conda deactivate

#!/bin/bash

TASK=12
MODEL=ctrl_muniter
MODEL_CONFIG=ctrl_muniter_base
TASKS_CONFIG=iglue_trainval_tasks_boxes36.dtu


PRETRAINED=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_1/ta/seed1/pretrain/ctrl_muniter_base/pytorch_model_24.bin

OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_1/varying_finetune_data/ta/25k/seed3
LOGGING_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_1/varying_finetune_data/ta/25k/seed3/logging

NUMBER_OF_ENTRIES=25000

#source /home/projects/ku_00062/envs/iglue/bin/activate

cd ../../../../../../../volta
python train_task.py \
    --bert_model bert-base-multilingual-cased --config_file config/${MODEL_CONFIG}.json \
    --from_pretrained ${PRETRAINED} --cache 500 \
    --tasks_config_file config_tasks/${TASKS_CONFIG}.yml --task $TASK --gradient_accumulation_steps 2 --num_workers 10 --num_val_workers 10\
    --adam_epsilon 1e-6 --adam_betas 0.9 0.999 --adam_correct_bias --weight_decay 0.0001 --warmup_proportion 0.1 --clip_grad_norm 1.0 \
    --output_dir ${OUTPUT_DIR} \
    --logdir ${LOGGING_DIR} \
    --seed 3 \
    --number_of_entries ${NUMBER_OF_ENTRIES} \
#    --resume_file /mnt/nas_home/mrgj4/nlvr2_dataset/concept_cov_exp/sw/fullcov_1/NLVR2_ctrl_muniter_base/pytorch_ckpt_latest.tar

#deactivate
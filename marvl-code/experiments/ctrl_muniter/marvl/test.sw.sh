#!/bin/bash

TASK=12
MODEL=ctrl_muniter
MODEL_CONFIG=ctrl_muniter_base
TRTASK=NLVR2
TETASK=MaRVLsw
TASKS_CONFIG=xling_test_marvl

TEXT_PATH=/mnt/nas_home/mrgj4/marvl-code/data/sw/annotations/marvl-sw.jsonl
FEAT_PATH=/mnt/nas_home/mrgj4/marvl_experiments/marvl-sw_boxes36.lmdb


PRETRAINED=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_2/sw/seed3/zerocov/finetune/NLVR2_ctrl_muniter_base/pytorch_model_best.bin
OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_2/sw/seed3/zerocov/test

# PRETRAINED=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_1/varying_finetune_data/sw/full/seed3/NLVR2_ctrl_muniter_base/pytorch_model_9.bin
# OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_1/varying_finetune_data/sw/full/seed3/test

# PRETRAINED=/mnt/nas_home/mrgj4/nlvr2_dataset/cc_pretrain/pytorch_model_best.bin
# OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/experiment_1/sw/baseline/test

#source /home/projects/ku_00062/envs/marvl/bin/activate

cd ../../../volta
python eval_task.py \
        --bert_model bert-base-multilingual-cased \
        --config_file config/${MODEL_CONFIG}.json \
        --from_pretrained ${PRETRAINED} \
        --val_annotations_jsonpath ${TEXT_PATH} --val_features_lmdbpath ${FEAT_PATH} \
        --tasks_config_file config_tasks/${TASKS_CONFIG}.yml --task $TASK --split test \
        --output_dir ${OUTPUT_DIR}

#deactivate

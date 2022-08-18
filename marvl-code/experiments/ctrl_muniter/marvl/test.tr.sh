#!/bin/bash

TASK=12
MODEL=ctrl_muniter
MODEL_CONFIG=ctrl_muniter_base
TRTASK=NLVR2
TETASK=MaRVLtr
TASKS_CONFIG=xling_test_marvl

# TO CHANGE
TEXT_PATH=/mnt/nas_home/mrgj4/marvl-code/data/tr/annotations/marvl-tr.jsonl
FEAT_PATH=/mnt/nas_home/mrgj4/marvl_experiments/marvl-tr_boxes36.lmdb

PRETRAINED=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_3/grammatical_properties/tr/seed3/noun_verb/finetune/NLVR2_ctrl_muniter_base/pytorch_model_best.bin
OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_3/grammatical_properties/tr/seed3/noun_verb/test


# PRETRAINED=/mnt/nas_home/mrgj4/final_repo/experiment_1/varying_finetune_data/full/seed3/NLVR2_ctrl_muniter_base/pytorch_model_best.bin
# OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/experiment_1/varying_finetune_data/full/seed3/test

# PRETRAINED=/mnt/nas_home/mrgj4/nlvr2_dataset/cc_pretrain/pytorch_model_best.bin
# OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/experiment_1/tr/baseline/test

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

#!/bin/bash

TASK=12
MODEL=ctrl_muniter
MODEL_CONFIG=ctrl_muniter_base
TRTASK=NLVR2
TETASK=MaRVLtr
TASKS_CONFIG=xling_test_marvl

#TEXT_PATH=/mnt/nas_home/mrgj4/marvl-code/data/tr/annotations_machine-translate/marvl-tr_gmt.jsonl
TEXT_PATH=/mnt/nas_home/mrgj4/marvl-tr-en-infused_075total.jsonl
FEAT_PATH=/mnt/nas_home/mrgj4/marvl_experiments/marvl-tr_boxes36.lmdb

PRETRAINED=/mnt/nas_home/mrgj4/nlvr2_dataset/cc_pretrain/pytorch_model_14.bin
#PRETRAINED=/mnt/nas_home/mrgj4/nlvr2_dataset/tr_v2_pretrain/NLVR2_ctrl_muniter_base/pytorch_model_9.bin
OUTPUT_DIR=/mnt/nas_home/mrgj4/test

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

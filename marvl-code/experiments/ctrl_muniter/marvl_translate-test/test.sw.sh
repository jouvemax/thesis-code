#!/bin/bash

TASK=12
MODEL=ctrl_muniter
MODEL_CONFIG=ctrl_muniter_base
TRTASK=NLVR2
TETASK=MaRVLsw
TASKS_CONFIG=xling_test_marvl


#TEXT_PATH=/mnt/nas_home/mrgj4/marvl-code/data/sw/annotations_machine-translate/marvl-sw_gmt.jsonl
TEXT_PATH=/mnt/nas_home/mrgj4/marvl-sw-en-infused_1.jsonl
FEAT_PATH=/mnt/nas_home/mrgj4/marvl_experiments/marvl-sw_boxes36.lmdb

PRETRAINED=/mnt/nas_home/mrgj4/nlvr2_dataset/concept_cov_exp/sw/fullcov_1/NLVR2_ctrl_muniter_base/pytorch_model_9.bin
OUTPUT_DIR=/mnt/nas_home/mrgj4/marvl_experiments/test

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

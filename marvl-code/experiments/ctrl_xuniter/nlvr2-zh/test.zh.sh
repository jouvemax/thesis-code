#!/bin/bash

TASK=12
MODEL=ctrl_xuniter
MODEL_CONFIG=ctrl_xuniter_base
TRTASK=NLVR2zh
TETASK=MaRVLzh
TASKS_CONFIG=xling_test_marvl
TEXT_PATH=/home/projects/ku_00062/data/marvl/annotations/marvl-zh.jsonl
FEAT_PATH=/home/projects/ku_00062/data/marvl/features/marvl-zh_boxes36.lmdb
PRETRAINED=/home/projects/ku_00062/checkpoints/marvl/${MODEL}/${TRTASK}_${MODEL_CONFIG}/pytorch_model_best.bin
OUTPUT_DIR=/home/projects/ku_00062/results/marvl/${MODEL}/${TRTASK}_${MODEL_CONFIG}/$TETASK/test

source /home/projects/ku_00062/envs/marvl/bin/activate

cd ../../../volta
python eval_task.py \
        --bert_model /home/projects/ku_00062/huggingface/xlm-roberta-base \
        --config_file config/${MODEL_CONFIG}.json \
        --from_pretrained ${PRETRAINED} \
        --val_annotations_jsonpath ${TEXT_PATH} --val_features_lmdbpath ${FEAT_PATH} \
        --tasks_config_file config_tasks/${TASKS_CONFIG}.yml --task $TASK --split test \
        --output_dir ${OUTPUT_DIR}

deactivate
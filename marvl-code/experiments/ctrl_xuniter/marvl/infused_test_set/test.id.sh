#!/bin/bash

TASK=12
MODEL=ctrl_xuniter
MODEL_CONFIG=ctrl_xuniter_base
TRTASK=NLVR2
TETASK=MaRVLid
TASKS_CONFIG=xling_test_marvl

TEXT_PATH=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_3/infused_test_set/id/marvl-id-en-infused_concept.jsonl
FEAT_PATH=/mnt/nas_home/mrgj4/marvl_experiments/marvl-id_boxes36.lmdb

PRETRAINED=/mnt/nas_home/mrgj4/nlvr2_dataset/ctrl_xuniter/cc_pretrain/NLVR2_ctrl_xuniter_base/pytorch_model_best.bin
OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_3/infused_test_set/id/xuniter/concept_only

#source /home/projects/ku_00062/envs/marvl/bin/activate

cd ../../../../volta
python eval_task.py \
        --bert_model xlm-roberta-base \
        --config_file config/${MODEL_CONFIG}.json \
        --from_pretrained ${PRETRAINED} \
        --val_annotations_jsonpath ${TEXT_PATH} --val_features_lmdbpath ${FEAT_PATH} \
        --tasks_config_file config_tasks/${TASKS_CONFIG}.yml --task $TASK --split test \
        --output_dir ${OUTPUT_DIR}
#deactivate

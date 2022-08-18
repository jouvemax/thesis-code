#!/bin/bash

TASK=8
SHOT=50
LANG=de
MODEL=m3p
MODEL_CONFIG=m3p_base
TASKS_CONFIG=iglue_fewshot_tasks_X101.dtu
TRTASK=RetrievalxFlickrCO${LANG}_${SHOT}
TEXT_TR=/home/projects/ku_00062/data/xFlickrCO/annotations/${LANG}/train_${SHOT}.jsonl
FEAT_TR=/home/projects/ku_00062/data/xFlickrCO/features/xflickrco-few_X101.lmdb
TEXT_TE=/home/projects/ku_00062/data/flickr30k/annotations/valid_ann.jsonl
PRETRAINED=/home/projects/ku_00062/checkpoints/iglue/zero_shot/xflickrco/${MODEL}/RetrievalFlickr30k_${MODEL_CONFIG}/pytorch_model_best.bin

here=$(pwd)

source /home/projects/ku_00062/envs/iglue/bin/activate

cd ../../../../../../volta

for lr in 1e-4 5e-5 1e-5; do
  OUTPUT_DIR=/home/projects/ku_00062/checkpoints/iglue/few_shot/xflickrco/${TRTASK}/${MODEL}/${lr}
  LOGGING_DIR=/home/projects/ku_00062/logs/iglue/few_shot/xflickrco/${TRTASK}/${lr}/${MODEL_CONFIG}
  python train_task.py \
    --bert_model /home/projects/ku_00062/huggingface/xlm-roberta-base --config_file config/${MODEL_CONFIG}.json \
    --from_pretrained ${PRETRAINED} --is_m3p \
    --tasks_config_file config_tasks/${TASKS_CONFIG}.yml --task $TASK --num_epoch 20 \
    --train_split train_${LANG}_${SHOT} --train_annotations_jsonpath $TEXT_TR --train_features_lmdbpath $FEAT_TR \
    --val_split dev --val_annotations_jsonpath $TEXT_TE \
    --lr $lr --batch_size 16 --gradient_accumulation_steps 2 --num_workers 0 --save_every_num_epochs 5 --eval_batch_size 8 --max_val_batches 260 \
    --adam_epsilon 1e-6 --adam_betas 0.9 0.999 --adam_correct_bias --weight_decay 0.0001 --warmup_proportion 0.1 --clip_grad_norm 1.0 \
    --output_dir ${OUTPUT_DIR} \
    --logdir ${LOGGING_DIR} \
    &> ${here}/train.${lr}.log
done
deactivate

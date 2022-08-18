LIST_INDICES_PATH=/mnt/nas_home/mrgj4/final_repo/experiment_1/zh/zh_valid_ids.pickle
OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/experiment_1/zh/seed3
SEED=3


python build_random_train_val_sets.py \
  --list_indices_path $LIST_INDICES_PATH \
  --output_dir $OUTPUT_DIR \
  --seed $SEED
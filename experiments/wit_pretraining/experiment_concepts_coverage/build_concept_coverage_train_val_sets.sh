#LIST_INDICES_PATH=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_1/tr/tr_valid_ids.pickle
LIST_INDICES_PATH=/mnt/nas_home/mrgj4/wit_dataset/utils/concepts_coverage_exp/id/id_extracted_entries_list.pickle
MARVL_ENTRIES_PATH=/mnt/nas_home/mrgj4/marvl-code/data/id/annotations/marvl-id.jsonl
LANG_ENTRIES_PATH=/mnt/nas_home/mrgj4/wit_dataset/utils/id_entries.pkl

LANG=id

OUTPUT_DIR=/mnt/nas_home/mrgj4/final_repo/thesis-code/experiment_2/id/seed3/zerocov
SEED=3
# full or zero
COVERAGE=zero


python build_concept_coverage_train_val_sets.py \
  --list_indices_path $LIST_INDICES_PATH \
  --marvl_entries_path $MARVL_ENTRIES_PATH \
  --lang_entries_path $LANG_ENTRIES_PATH \
  --lang $LANG \
  --output_dir $OUTPUT_DIR \
  --seed $SEED \
  --coverage $COVERAGE
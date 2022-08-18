LIST_INDICES_PATH=/Users/maxence/Documents/EPFL/Master/Thesis_Code/extracted_entries_list/sw_extracted_entries_list.pickle
OUTPUT_DIR=/Users/maxence/Documents/EPFL/Master/Thesis_Code
PATH_TO_FASTTEXT_MODEL=/Users/maxence/Documents/EPFL/Master/Thesis_Code/models/cc.sw.300.bin
PATH_TO_LANG_ENTRIES=/Users/maxence/Documents/EPFL/Master/Thesis_Code/sw_entries.pkl

LANG=sw


python build_selected_train_val_sets.py \
  --list_indices_path $LIST_INDICES_PATH \
  --output_dir $OUTPUT_DIR \
  --path_to_fasttext_model $PATH_TO_FASTTEXT_MODEL \
  --path_to_lang_entries $PATH_TO_LANG_ENTRIES \
  --lang $LANG
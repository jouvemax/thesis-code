OUTPUT_DIR=.
LANG=id
# Only for TR and TA.
PATH_TO_CAPTIONS=/mnt/nas_home/mrgj4/wit_dataset/captions/ta_captions.json


python build_lang_dictionary.py \
  --output_dir $OUTPUT_DIR \
  --lang $LANG \
  --path_to_captions $PATH_TO_CAPTIONS
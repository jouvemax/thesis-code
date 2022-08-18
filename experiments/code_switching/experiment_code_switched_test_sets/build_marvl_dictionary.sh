OUTPUT_DIR=.
LANG=zh
PATH_TO_MARVL_ANNOTATIONS=/mnt/nas_home/mrgj4/marvl-code/data/zh/annotations/marvl-zh.jsonl


python build_marvl_dictionary.py \
  --output_dir $OUTPUT_DIR \
  --lang $LANG \
  --path_to_marvl_annotations $PATH_TO_MARVL_ANNOTATIONS
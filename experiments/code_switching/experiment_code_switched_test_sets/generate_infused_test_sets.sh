OUTPUT_DIR=./zh
LANG=zh
PATH_TO_MARVL_ANNOTATIONS=/mnt/nas_home/mrgj4/marvl-code/data/zh/annotations/marvl-zh.jsonl
PATH_TO_MARVL_DICT=./zh_to_en_marvl_dict.pickle


python generate_infused_test_sets.py \
  --output_dir $OUTPUT_DIR \
  --lang $LANG \
  --path_to_marvl_annotations $PATH_TO_MARVL_ANNOTATIONS \
  --path_to_marvl_dict $PATH_TO_MARVL_DICT
# input marvl entries
PATH_TO_TEXT=/mnt/nas_home/mrgj4/marvl-code/data/zh/annotations/marvl-zh.jsonl
OUTPUT_DIR=/mnt/nas_home/mrgj4/wit_dataset/infusion_exp

LANG=zh


python extract_lang_pos_marvl.py \
  --path_to_text $PATH_TO_TEXT \
  --output_dir $OUTPUT_DIR \
  --lang $LANG